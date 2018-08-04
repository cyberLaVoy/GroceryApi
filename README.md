# Grocery List App Documentation

## Resources:

### Ingredients
##### Attributes:
* label (a name for ingredient)
* category (the category of ingredient)

### Recipes
##### Attributes:
* label (a name for recipe)
* ingredients (a list of ingredients, with quantity and quantity type)
* instructions (directions to make recipe)

### Grocery List
##### Attributes:
* label (a name for the grocery list)
* items (a list of items, with quantity and quantity type)


## Database Schema:
```SQL
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
quantity VARCHAR(255),
quantity_type VARCHAR(255),
primary key (recipe_id, ingredient_id));

CREATE TABLE IF NOT EXISTS grocery_lists
(list_id serial primary key,
label VARCHAR(255));

CREATE TABLE IF NOT EXISTS grocery_list_items
(list_id INTEGER references grocery_lists(list_id),
ingredient_id INTEGER references ingredients(ingredient_id),
quantity VARCHAR(255),
quantity_type VARCHAR(255),
num_recipes_referenced INTEGER DEFAULT 0,
grabbed BOOLEAN DEFAULT FALSE,
primary key (list_id, ingredient_id, quantity_type));
```

## REST Endpoints:
Name | HTTP Method | Path | Request Body (x-www-form-urlencoded) *denotes required
------------ | ------------- | ------------- | -------------
List | GET | /ingredients |
List | GET | /recipes |
List | GET | /groceries |
Retrieve | GET | /ingredients/ingredientID |
Retrieve | GET | /recipes/recipeID |
Retrieve | GET | /groceries/listID |
Create | POST | /recipes | label, directions
Create | POST | /ingredients | label, category
Create | POST | /recipes/ingredients | *recipe_id, *ingredient_id, quantity, quantity_type
Create | POST | /groceries | label
Create | POST | /groceries/items | *list_id, *ingredient_id, *quantity_type, quantity
Create | POST | /groceries/recipes | *list_id, *recipe_id
Replace | PUT | /ingredients/ingredientID | label, category
Replace | PUT | /recipes/recipeID | label, instructions
Replace | PUT | /recipes/ingredients | *recipe_id, *ingredient_id, quantity, quantity_type
Replace | PUT | /groceries/listID | label
Replace | PUT | /groceries/items | *list_id, *ingredient_id, *original_quantity_type, new_quantity_type, quantity, grabbed
Delete | DELETE | /recipes/ingredients | *recipe_id, *ingredient_id
Delete | DELETE | /ingredients/ingredientID | 
Delete | DELETE | /recipes/recipeID |
Delete | DELETE | /groceries/listID |
Delete | DELETE | /groceries/items | *list_id, *ingredient_id, *quantity_type

## Heroku URL
#### https://stormy-everglades-69504.herokuapp.com/ 
