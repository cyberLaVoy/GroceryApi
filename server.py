from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
from groceryDB import GroceryDB
import json, sys

class RequestHandler(BaseHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", self.headers["Origin"])
        self.send_header("Access-Control-Allow-Credentials", "true")
        BaseHTTPRequestHandler.end_headers(self)
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
    def do_GET(self):
        pathParams = self.path.split('/')
        if self.path == "/ingredients":
            self.handleListIngredients()
        elif self.path == "/recipes":
            self.handleListRecipes()
        elif self.path == "/groceries":
            self.handleListGroceryLists()
        elif len(pathParams) >= 3:
            if pathParams[1] == "ingredients":
                ingredientID = pathParams[2]
                self.handleIngredientRetrieve(ingredientID)
            elif pathParams[1] == "recipes":
                recipeID = pathParams[2]
                self.handleRecipeRetrieve(recipeID)
            elif pathParams[1] == "groceries":
                listID = pathParams[2]
                self.handleGroceryListRetrieve(listID)
    def do_POST(self):
        if self.path == "/ingredients":
            self.handleCreateIngredient()
        elif self.path == "/recipes":
            self.handleCreateRecipe()
        elif self.path == "/groceries":
            self.handleCreateGroceryList()
        elif self.path == "/groceries/items":
            self.handleAddGroceryListItem()
        elif self.path == "/groceries/recipes":
            self.handleAddRecipeToGroceryList()
        elif self.path == "/recipes/ingredients":
            self.handleAddRecipeIngredient()
    def do_PUT(self):
        pathParams = self.path.split('/')
        if self.path == "/recipes/ingredients":
            self.handleUpdateRecipeIngredient()
        elif len(pathParams) >= 3:
            if pathParams[1] == "recipes":
                recipeID = pathParams[2]
                self.handleUpdateRecipe(recipeID)
            elif pathParams[1] == "ingredients":
                ingredientID = pathParams[2]
                self.handleUpdateIngredient(ingredientID)
            elif pathParams[1] == "groceries":
                listID = pathParams[2]
                self.handleUpdateGroceryList(listID)
    def do_DELETE(self):
        pathParams = self.path.split('/')
        if self.path == "/recipes/ingredients":
            self.handleDeleteRecipeIngredient()
        if len(pathParams) >= 3:
            if pathParams[1] == "recipes":
                recipeID = pathParams[2]
                self.handleDeleteRecipe(recipeID)
            elif pathParams[1] == "ingredients":
                ingredientID = pathParams[2]
                self.handleDeleteIngredient(ingredientID)
            elif pathParams[1] == "groceries":
                listID = pathParams[2]
                self.handleDeleteGroceryList(listID)


# ingredient operations
    def handleCreateIngredient(self):
        parsedBody = self.getParsedBody()
        db = GroceryDB()
        label = "Ingredient Label"
        category = "Ingredient Category"
        if parsedBody.get("label") != None:
            label = parsedBody["label"][0]
        if parsedBody.get("category") != None:
            category = parsedBody["category"][0]
        db.createIngredient(label, category)
        self.handle201("Ingredient created.")
    def handleListIngredients(self):
        db = GroceryDB()
        ingredients = { "ingredients" : db.getIngredients() }
        self.handle200JSONResponse(ingredients)
    def handleIngredientRetrieve(self, ingredientID):
        db = GroceryDB()
        if not db.ingredientExists(ingredientID):
            self.handle404("Ingredient does not exist.")
        else:
            ingredient = db.getIngredient(ingredientID)
            self.handle200JSONResponse(ingredient)
    def handleUpdateIngredient(self, ingredientID):
        parsedBody = self.getParsedBody()
        db = GroceryDB()
        ingredient = db.getIngredient(ingredientID)
        label = ingredient["label"]
        category = ingredient["category"]
        if parsedBody.get("label") != None:
            label = parsedBody["label"][0]
        if parsedBody.get("category") != None:
            category = parsedBody["category"][0]
        db.updateIngredient(label, category, ingredientID)
        self.handle201("Ingredient updated.")
    def handleDeleteIngredient(self, ingredientID):
        db = GroceryDB()
        if not db.ingredientExists(ingredientID):
            self.handle404("Ingredient does not exist.")
        db.deleteIngredient(ingredientID)
        self.handle200("Ingredient successfully deleted")

# recipes operations
    def handleCreateRecipe(self):
        parsedBody = self.getParsedBody()
        db = GroceryDB()
        label = "Recipe Label"
        instructions = ""
        if parsedBody.get("label") != None:
            label = parsedBody["label"][0]
        if parsedBody.get("instructions") != None:
            instructions = parsedBody["instructions"][0]
        db.createRecipe(label, instructions)
        self.handle201("Recipe created.")
    def handleUpdateRecipe(self, recipeID):
        parsedBody = self.getParsedBody()
        db = GroceryDB()
        if not db.recipeExists(recipeID):
            self.handle404("Recipe does not exist.")
        else:
            recipe = db.getRecipe(recipeID)
            label = recipe["label"]
            instructions = recipe["instructions"]
            if parsedBody.get("label") != None:
                label = parsedBody["label"][0]
            if parsedBody.get("instructions") != None:
                instructions = parsedBody["instructions"][0]
            db.updateRecipe(recipeID, label, instructions)
            self.handle201("Recipe updated.")
    def handleListRecipes(self):
        db = GroceryDB()
        recipes = { "recipes" : db.getRecipes() }
        self.handle200JSONResponse(recipes)
    def handleRecipeRetrieve(self, recipeID):
        db = GroceryDB()
        if not db.recipeExists(recipeID):
            self.handle404("Recipe does not exist.")
        else:
            recipe = db.getRecipe(recipeID)
            self.handle200JSONResponse(recipe)
    def handleDeleteRecipe(self, recipeID):
        db = GroceryDB()
        if not db.recipeExists(recipeID):
            self.handle404("Recipe does not exist.")
        else:
            db.deleteRecipe(recipeID)
            self.handle200("Recipe successfully deleted")

# recipe_ingredients operations
    def handleAddRecipeIngredient(self):
        db = GroceryDB()
        parsedBody = self.getParsedBody()
        ingredientID = -1
        recipeID = -1
        if parsedBody.get("ingredient_id") != None:
            ingredientID = parsedBody["ingredient_id"][0]
        if parsedBody.get("recipe_id") != None:
            recipeID = parsedBody["recipe_id"][0]
        if not db.ingredientExists(ingredientID) or not db.recipeExists(recipeID):
            self.handle404("Ingredient or recipe does not exist.")
        elif db.recipeIngredientExists(recipeID, ingredientID):
            self.handle422("Recipe ingredient already exists.")
        else:
            quantity = ""
            quantityType = ""
            if parsedBody.get("quantity") != None:
                quantity = parsedBody["quantity"][0]
            if parsedBody.get("quantity_type") != None:
                quantityType = parsedBody["quantity_type"][0]
            db.addIngredientToRecipe(recipeID, ingredientID, quantity, quantityType)
            self.handle201("Recipe ingredient added.")
    def handleUpdateRecipeIngredient(self):
        db = GroceryDB()
        parsedBody = self.getParsedBody()
        ingredientID = -1
        recipeID = -1
        if parsedBody.get("ingredient_id") != None:
            ingredientID = parsedBody["ingredient_id"][0]
        if parsedBody.get("recipe_id") != None:
            recipeID = parsedBody["recipe_id"][0]
        if not db.recipeIngredientExists(recipeID, ingredientID):
            self.handle404("Recipe ingredient does not exist.")
        else:
            recipeIngredient = db.getRecipeIngredient(recipeID, ingredientID)
            quantity = recipeIngredient["quantity"]
            quantityType = recipeIngredient["quantity_type"]
            if parsedBody.get("quantity") != None:
                quantity = parsedBody["quantity"][0]
            if parsedBody.get("quantity_type") != None:
                quantityType = parsedBody["quantity_type"][0]
            db.updateRecipeIngredient(recipeID, ingredientID, quantity, quantityType)
            self.handle201("Recipe ingredient updated.")
    def handleDeleteRecipeIngredient(self):
        db = GroceryDB()
        parsedBody = self.getParsedBody()
        ingredientID = -1
        recipeID = -1
        if parsedBody.get("ingredient_id") != None:
            ingredientID = parsedBody["ingredient_id"][0]
        if parsedBody.get("recipe_id") != None:
            recipeID = parsedBody["recipe_id"][0]
        if not db.recipeIngredientExists(recipeID, ingredientID):
            self.handle404("Recipe ingredient does not exist.")
        else:
            db.deleteRecipeIngredient(recipeID, ingredientID)
            self.handle200("Recipe ingredient successfully deleted")

# groceries operations
    def handleListGroceryLists(self):
        db = GroceryDB()
        groceryLists = { "grocery_lists" : db.getGroceryLists() }
        self.handle200JSONResponse(groceryLists)
    def handleCreateGroceryList(self):
        parsedBody = self.getParsedBody()
        db = GroceryDB()
        label = "Grocery List Label"
        if parsedBody.get("label") != None:
            label = parsedBody["label"][0]
        db.createGroceryList(label)
        self.handle201("Grocery List created.")
    def handleGroceryListRetrieve(self, listID):
        db = GroceryDB()
        if not db.groceryListExists(listID):
            self.handle404("Grocery List does not exist.")
        else:
            groceryList = db.getGroceryList(listID)
            self.handle200JSONResponse(groceryList)
    def handleUpdateGroceryList(self, listID):
        parsedBody = self.getParsedBody()
        db = GroceryDB()
        if not db.groceryListExists(listID):
            self.handle404("Grocery list does not exist.")
        else:
            groceryList = db.getGroceryList(listID)
            label = groceryList["label"]
            if parsedBody.get("label") != None:
                label = parsedBody["label"][0]
            db.updateGroceryList(listID, label)
            self.handle201("Grocery list updated.")
    def handleDeleteGroceryList(self, listID):
        db = GroceryDB()
        if not db.groceryListExists(listID):
            self.handle404("Grocery list does not exist.")
        else:
            db.deleteGroceryList(listID)
            self.handle200("Grocery list successfully deleted")

# grocery_list_items operations
    def handleAddGroceryListItem(self):
        db = GroceryDB()
        parsedBody = self.getParsedBody()
        ingredientID = -1
        listID = -1
        if parsedBody.get("ingredient_id") != None:
            ingredientID = parsedBody["ingredient_id"][0]
        if parsedBody.get("list_id") != None:
            listID = parsedBody["list_id"][0]
        if not db.ingredientExists(ingredientID) or not db.groceryListExists(listID):
            self.handle404("Ingredient or grocery list does not exist.")
        else:
            quantity = ""
            quantityType = ""
            if parsedBody.get("quantity") != None:
                quantity = parsedBody["quantity"][0]
            if parsedBody.get("quantity_type") != None:
                quantityType = parsedBody["quantity_type"][0]
            db.addItemToGroceryList(listID, ingredientID, quantity, quantityType)
            self.handle201("Item added to grocery list.")
    def handleAddRecipeToGroceryList(self):
        db = GroceryDB()
        parsedBody = self.getParsedBody()
        recipeID = -1
        listID = -1
        if parsedBody.get("recipe_id") != None:
            recipeID = parsedBody["recipe_id"][0]
        if parsedBody.get("list_id") != None:
            listID = parsedBody["list_id"][0]
        if not db.recipeExists(recipeID) or not db.groceryListExists(listID):
            self.handle404("Recipe or grocery list does not exist.")
        else:
            ingredients = db.getRecipeIngredients(recipeID)
            db.addRecipeItemsToGroceryList(listID, ingredients)
            self.handle201("Recipe added to grocery list")

# General Methods
    def getParsedBody(self):
        length = int(self.headers["Content-length"])
        body = self.rfile.read(length).decode("utf-8")
        parsed_body = parse_qs(body)
        return parsed_body
    def handle200(self, message):
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(bytes(message, "utf-8"))
    def handle200JSONResponse(self, jsonString):
        jsonData = json.dumps(jsonString)
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(bytes(jsonData, "utf-8"))
    def handle201(self, message):
        self.send_response(201)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(bytes(message, "utf-8"))
    def handle404(self, message):
        self.send_response(404)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(bytes(message, "utf-8"))
    def handle422(self, message):
        self.send_response(422)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(bytes(message, "utf-8"))
    def handle401(self):
        self.send_response(401)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(bytes("This request requires user authetication.", "utf-8"))
    def handle403(self):
        self.send_response(403)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(bytes("Not authorized.", "utf-8"))

def main():
    db = GroceryDB()
    db.createTables()
    port = 8080
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    listen = ("0.0.0.0", port)
    server = HTTPServer(listen, RequestHandler)
    print("Listening...")
    server.serve_forever()
main()
