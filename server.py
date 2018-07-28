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
    def do_POST(self):
        if self.path == "/ingredients":
            self.handleCreateIngredient()
    def do_PUT(self):
        pass
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
        ingredients = { "ingredient" : db.getIngredients() }

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

    def handle404(self):
        self.send_response(404)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(bytes("Not Found.", "utf-8"))

    def handle422(self):
        self.send_response(422)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(bytes("Invalid data entry.", "utf-8"))

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
