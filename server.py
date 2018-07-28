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
        if self.path == "/ingredients":
            self.handleListIngredients()
        elif self.path == "/recipes":
            self.handleListRecipes()
    def do_POST(self):
        if self.path == "/ingredients":
            self.handleCreateIngredient()
        if self.path == "/recipes":
            self.handleCreateRecipe()
    def do_PUT(self):
        pathParams = self.path.split('/')
        if len(pathParams) >= 4:
            if pathParams[1] == "recipes" and pathParams[2] == "ingredients":
                recipeID = pathParams[3]
                self.handleAddRecipeIngredient(recipeID)
    def do_DELETE(self):
        pass

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
        self.send_response(201)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(bytes("Ingredient created.", "utf-8"))

    def handleListIngredients(self):
        db = GroceryDB()
        ingredients = { "ingredients" : db.getIngredients() }
        jsonData = json.dumps(ingredients)
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(bytes(jsonData, "utf-8"))

# recipe operations
    def handleCreateRecipe(self):
        parsedBody = self.getParsedBody()
        db = GroceryDB()
        label = "Recipe Label"
        directions = ""
        if parsedBody.get("label") != None:
            label = parsedBody["label"][0]
        if parsedBody.get("directions") != None:
            directions = parsedBody["directions"][0]
        db.createRecipe(label, directions)
        self.send_response(201)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(bytes("Recipe created.", "utf-8"))

    def handleAddRecipeIngredient(self, recipeID):
        db = GroceryDB()
        parsedBody = self.getParsedBody()
        ingredientID = -1
        if parsedBody.get("ingredient_id") != None:
            ingredientID = parsedBody["ingredient_id"][0]
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
            self.send_response(201)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(bytes("Recipe ingredient added.", "utf-8"))

    def handleListRecipes(self):
        db = GroceryDB()
        ingredients = { "recipes" : db.getRecipes() }
        jsonData = json.dumps(ingredients)
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(bytes(jsonData, "utf-8"))

# General Methods
    def getParsedBody(self):
        length = int(self.headers["Content-length"])
        body = self.rfile.read(length).decode("utf-8")
        parsed_body = parse_qs(body)
        return parsed_body

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
