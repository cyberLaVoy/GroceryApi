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
        (recipe_id INTEGER references recipes(recipe_id),
        ingredient_id INTEGER references ingredients(ingredient_id),
        quantity REAL,
        quantity_type VARCHAR(255),
        primary key (recipe_id, ingredient_id));

        CREATE TABLE IF NOT EXISTS grocery_lists
        (list_id serial primary key,
        label VARCHAR(255));

        CREATE TABLE IF NOT EXISTS grocery_list_items
        (list_id INTEGER references grocery_list(list_id),
        ingredient_id INTEGER references ingredients(ingredient_id),
        quantity REAL,
        quantity_type VARCHAR(255),
        num_recipes_referenced INTEGER DEFAULT 0,
        grabbed BOOLEAN DEFAULT FALSE);
        """
        self.cursor.execute(queryString.replace('\n', ' '))
        self.connection.commit()
    def deleteGroceryListTable(self):
        queryString = "DROP TABLE IF EXISTS grocery_lists;"
        self.cursor.execute(queryString)
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
        queryString = "SELECT * FROM ingredients WHERE ingredient_id = %s"
        self.cursor.execute(queryString, (ingredientID,))
        ingredient = self.cursor.fetchall()
        return ingredient[0]
    def updateIngredient(self, label, category, ingredientID):
        queryString = "UPDATE ingredients SET label = %s, category = %s WHERE ingredient_id = %s"
        self.cursor.execute(queryString,(label, category, ingredientID))
        self.connection.commit()
    def deleteIngredient(self, ingredientID):
        queryString = "DELETE FROM ingredients WHERE ingredient_id = %s"
        self.cursor.execute(queryString, (ingredientID,))
        self.connection.commit()
    def ingredientExists(self, ingredientID):
        queryString = "SELECT * FROM ingredients WHERE ingredient_id = %s"
        self.cursor.execute(queryString,(ingredientID,))
        rows = self.cursor.fetchall()
        if len(rows) == 0:
            return False
        return True
# recipe_indgredients operations
    def recipeIngredientExists(self, recipeID, ingredientID):
        queryString = "SELECT * FROM recipe_ingredients WHERE recipe_id = %s AND ingredient_id = %s"
        self.cursor.execute(queryString,(recipeID, ingredientID))
        rows = self.cursor.fetchall()
        if len(rows) == 0:
            return False
        return True
    def addIngredientToRecipe(self, recipeID, ingredientID, quantity, quantityType):
        queryString = "INSERT INTO recipe_ingredients (recipe_id, ingredient_id, quantity, quantity_type) VALUES (%s, %s, %s, %s)"
        self.cursor.execute(queryString, (recipeID, ingredientID, quantity, quantityType))
        self.connection.commit()
    def getRecipeIngredient(self, recipeID, ingredientID):
        queryString = "SELECT * FROM recipe_ingredients WHERE recipe_id = %s AND ingredient_id = %s"
        self.cursor.execute(queryString,(recipeID,ingredientID))
        ingredient = self.cursor.fetchall()
        return ingredient[0]
    def getRecipeIngredients(self, recipeID):
        queryString = "SELECT * FROM recipe_ingredients WHERE recipe_id = %s"
        self.cursor.execute(queryString,(recipeID,))
        rows = self.cursor.fetchall()
        return rows
    def updateRecipeIngredient(self, recipeID, ingredientID, quantity, quantityType):
        queryString = "UPDATE recipe_ingredients SET quantity = %s, quantity_type = %s WHERE recipe_id = %s AND ingredient_id = %s"
        self.cursor.execute(queryString,(quantity, quantityType, recipeID, ingredientID))
        self.connection.commit()
    def deleteRecipeIngredient(self, recipeID, ingredientID):
        queryString = "DELETE FROM recipe_ingredients WHERE recipe_id = %s AND ingredient_id = %s"
        self.cursor.execute(queryString, (recipeID, ingredientID))
        self.connection.commit()
    def deleteRecipeIngredients(self, recipeID):
        queryString = "DELETE FROM recipe_ingredients WHERE recipe_id = %s"
        self.cursor.execute(queryString, (recipeID,))
        self.connection.commit()
# recipes operations
    def appendIngredientsToRecipesList(self, recipies):
        for recipe in recipies:
            ingredients = self.getRecipeIngredients(recipe["recipe_id"])
            for ingredient in ingredients:
                ingredient.pop("recipe_id", None)
                ingredientDetails = self.getIngredient(ingredient["ingredient_id"])
                ingredient["label"] = ingredientDetails["label"]
                ingredient["category"] = ingredientDetails["category"]
            recipe["ingredients"]  = ingredients
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
        recipes = self.cursor.fetchall()
        self.appendIngredientsToRecipesList(recipes)
        return recipes
    def getRecipe(self, recipeID):
        queryString = "SELECT * FROM recipes WHERE recipe_id = %s"
        self.cursor.execute(queryString, (recipeID,))
        recipe = self.cursor.fetchall()
        self.appendIngredientsToRecipesList(recipe)
        return recipe[0]
    def updateRecipe(self, recipeID, label, instructions):
        queryString = "UPDATE recipes SET label = %s, instructions = %s WHERE recipe_id = %s"
        self.cursor.execute(queryString, (label, instructions, recipeID))
        self.connection.commit()
    def deleteRecipe(self, recipeID):
        queryString = "DELETE FROM recipes WHERE recipe_id = %s"
        self.cursor.execute(queryString, (recipeID,))
        self.connection.commit()
        self.deleteRecipeIngredients(recipeID)
# groceries operations
    def appendItemsToGroceryLists(self, groceryLists):
        for groceryList in groceryLists:
            items = self.getGroceryListItems(groceryList["list_id"])
            for item in items:
                item.pop("list_id", None)
                itemDetails = self.getIngredient(item["ingredient_id"])
                item["label"] = itemDetails["label"]
                item["category"] = itemDetails["category"]
            groceryList["items"]  = items
    def groceryListExists(self, listID):
        queryString = "SELECT * FROM grocery_lists WHERE list_id = %s"
        self.cursor.execute(queryString, (listID,))
        rows = self.cursor.fetchall()
        if len(rows) == 0:
            return False
        return True
    def createGroceryList(self, label):
        queryString = "INSERT INTO grocery_lists (label) VALUES (%s)"
        self.cursor.execute(queryString, (label,))
        self.connection.commit()
    def getGroceryLists(self):
        queryString = "SELECT * FROM grocery_lists"
        self.cursor.execute(queryString)
        groceryLists = self.cursor.fetchall()
        self.appendItemsToGroceryLists(groceryLists)
        return groceryLists
    def getGroceryList(self, listID):
        queryString = "SELECT * FROM grocery_lists WHERE list_id = %s"
        self.cursor.execute(queryString, (listID,))
        groceryList = self.cursor.fetchall()
        self.appendItemsToGroceryLists(groceryList)
        return groceryList[0]
    def updateGroceryList(self, listID, label):
        queryString = "UPDATE grocery_lists SET label = %s WHERE list_id = %s"
        self.cursor.execute(queryString, (label, listID))
        self.connection.commit()
    def deleteGroceryList(self, listID):
        queryString = "DELETE FROM grocery_lists WHERE list_id = %s"
        self.cursor.execute(queryString, (listID,))
        self.connection.commit()
        self.deleteGroceryListItems(listID)
# grocery_list_items operations
    def groceryListItemExists(self, listID, ingredientID):
        queryString = "SELECT * FROM grocery_list_items WHERE list_id = %s AND ingredient_id = %s"
        self.cursor.execute(queryString,(listID, ingredientID))
        rows = self.cursor.fetchall()
        if len(rows) == 0:
            return False
        return True
    def addItemToGroceryList(self, listID, ingredientID, quantity, quantityType):
        queryString = "INSERT INTO grocery_list_items (list_id, ingredient_id, quantity, quantity_type) VALUES (%s, %s, %s, %s)"
        self.cursor.execute(queryString, (listID, ingredientID, quantity, quantityType))
        self.connection.commit()
    def addRecipeItemsToGroceryList(self, listID, items): # items is a list of ingredient objects
        for item in items:
            ingredientID = item["ingredient_id"]
            quantity = item["quantity"]
            quantityType = item["quantity_type"]
            self.addItemToGroceryList(listID, ingredientID, quantity, quantityType)
    def getGroceryListItem(self, listID, ingredientID):
        queryString = "SELECT * FROM grocery_list_items WHERE list_id = %s AND ingredient_id = %s"
        self.cursor.execute(queryString,(listID,ingredientID))
        item = self.cursor.fetchall()
        return item[0]
    def getGroceryListItems(self, listID):
        queryString = "SELECT * FROM grocery_list_items WHERE list_id = %s"
        self.cursor.execute(queryString,(listID,))
        rows = self.cursor.fetchall()
        return rows
    def updateGroceryListItem(self, listID, ingredientID, quantity, quantityType):
        queryString = "UPDATE grocery_list_items SET quantity = %s, quantity_type = %s WHERE list_id = %s AND ingredient_id = %s"
        self.cursor.execute(queryString,(quantity, quantityType, listID, ingredientID))
        self.connection.commit()
    def incrementGroceryListItemRecipesReferenced(self, listID, ingredientID):
        item = self.getGroceryListItem(listID, ingredientID)
        recipesReferenced = item["num_recipes_referenced"]
        recipesReferenced += 1
        queryString = "UPDATE grocery_list_items SET num_recipes_referenced = %s WHERE list_id = %s AND ingredient_id = %s"
        self.cursor.execute(queryString,(recipesReferenced, listID, ingredientID))
        self.connection.commit()
    def setGroceryListItemGrabbed(self, grabbed, listID, ingredientID):
        queryString = "UPDATE grocery_list_items SET grabbed = %s WHERE list_id = %s AND ingredient_id = %s"
        self.cursor.execute(queryString,(grabbed, listID, ingredientID))
        self.connection.commit()
    def deleteGroceryListItem(self, listID, ingredientID):
        queryString = "DELETE FROM grocery_list_items WHERE list_id = %s AND ingredient_id = %s"
        self.cursor.execute(queryString, (listID, ingredientID))
        self.connection.commit()
    def deleteGroceryListItems(self, listID):
        queryString = "DELETE FROM grocery_list_items WHERE list_id = %s"
        self.cursor.execute(queryString, (listID,))
        self.connection.commit()