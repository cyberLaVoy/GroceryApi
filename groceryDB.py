import os
import psycopg2
import psycopg2.extras
import urllib.parse

class GroceryDB:
    def __init__(self):
        urllib.parse.uses_netloc.append("postgres")
        url = urllib.parse.urlparse(os.environ["DATABASE_URL"])
        self.connection = psycopg2.connect(
            cursor_factory=psycopg2.extras.RealDictCursor,
            database=url.path[1:],
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port
        )
        self.cursor = self.connection.cursor()

    def __del__(self):
        self.connection.close()

    def createTables(self):
        queryString = """
        CREATE TABLE IF NOT EXISTS ingredients
        (ingredient_id serial primary key,
        label VARCHAR(255) not null,
        category VARCHAR(255));

        CREATE TABLE IF NOT EXISTS recipes
        (recipe_id serial primary key,
        label VARCHAR(255),
        instructions VARCHAR(255));

        CREATE TABLE IF NOT EXISTS recipe_ingredients
        (recipe_id INTEGER not null,
        ingredient_id INTEGER not null,
        quantity REAL,
        quantity_type INTEGER,
        primary key (recipe_id, ingredient_id));

        CREATE TABLE IF NOT EXISTS grocery_list
        (list_id int,
        ingredient_id INTEGER references ingredients(ingredient_id),
        recipe_id INTEGER references recipes(recipe_id),
        quantity REAL,
        quantity_type VARCHAR(255),
        grabbed BOOLEAN);
        """
        self.cursor.execute(queryString.replace('\n', ' '))
        self.connection.commit()

# ingredients operations
    def createIngredient(self, label, category):
        queryString = "INSERT INTO ingredients (label, category) VALUES (%s, %s)"
        self.cursor.execute(queryString, (label, category))
        self.connection.commit()
    def getIngredients(self):
        queryString = "SELECT * FROM ingredients"
        self.cursor.execute(queryString)
        rows = self.cursor.fetchall()
        return rows 
    def getIngredient(self, ingredientID):
        Query = "SELECT * FROM ingredients WHERE ingredient_id = %s"
        self.cursor.execute(Query, (ingredientID,))
        item = self.cursor.fetchall()
        return item
    def replaceIngredient(self, label, category, ingredientID):
        Query = "UPDATE ingredients SET label = %s, category = %s WHERE ingredient_id = %s"
        self.cursor.execute(Query,(label, category, ingredientID))
        self.connection.commit()
    def deleteIngredient(self, ingredientID):
        Query = "DELETE FROM ingredients WHERE ingredient_id = %s"
        self.cursor.execute(Query, (ingredientID,))
        self.connection.commit()
    def ingredientExists(self, ingredientID):
        queryString = "SELECT * FROM ingredients WHERE ingredient_id = %s"
        self.cursor.execute(queryString,(ingredientID,))
        rows = self.cursor.fetchall()
        if len(rows) == 0:
            return False
        return True
# recipe_indgredients operations
    def addIngredientToRecipe(self, recipeID, ingredientID, quanity, quantityType):
        queryString = "INSERT INTO recipe_ingredients (recipe_id, ingredient_id, quanity, quantity_type) VALUES (%s, %s, %s, %s)"
        self.cursor.execute(queryString, (recipeID, ingredientID, quanity, quantityType))
        self.connection.commit()
# recipes operations
    def recipeExists(self, recipeID):
        queryString = "SELECT * FROM recipes WHERE recipe_id = %s"
        self.cursor.execute(queryString, (recipeID,))
        rows = self.cursor.fetchall()
        if len(rows) == 0:
            return False
        return True
    def createRecipe(self, label, instructions):
        queryString = "INSERT INTO recipes (label, instructions) VALUES (%s, %s)"
        self.cursor.execute(queryString, (label, instructions))
        self.connection.commit()
    def getRecipes(self):
        queryString = "SELECT * FROM recipes"
        self.cursor.execute(queryString)
        rows = self.cursor.fetchall()
        return rows 
    def getRecipe(self, ingredientID):
        Query = "SELECT * FROM recipes WHERE recipe_id = %s"
        self.cursor.execute(Query, (ingredientID,))
        item = self.cursor.fetchall()
        return item
    def replaceRecipe(self, label, category, ingredientID):
        Query = "UPDATE ingredients SET label = %s, category = %s WHERE ingredient_id = %s"
        self.cursor.execute(Query,(label, category, ingredientID))
        self.connection.commit()
    def deleteRecipe(self, ingredientID):
        Query = "DELETE FROM ingredients WHERE ingredient_id = %s"
        self.cursor.execute(Query, (ingredientID,))
        self.connection.commit()