# Grocery List App Documentation

## Resources:

#### ingredients
##### Attributes:
* label (a name for ingredient)
* category (the category of ingredient)

#### recipes
##### Attributes:
* label (a name for recipe)
* ingredients (a list of ingredients)
* instructions (directions to make recipe)

#### grocery_list
##### Attributes:
* items

## Database Schema:
```SQL
CREATE TABLE ingredients
(ingredient_id INTEGER primary key
 label VARCHAR(255) not null,
 catagory VARCHAR(255));

CREATE TABLE recipes
(recipe_id INTEGER primary key,
 label VARCHAR(255),
 ingredients INTEGER references recipe_ingredients(recipe_id, ingedient_id),
 instructions VARCHAR(255));

CREATE TABLE recipe_ingredients
(recipe_id INTEGER not null,
 ingredient_id INTEGER not null,
 quantity REAL,
 quantity_type INTEGER,
 primary key (recipe_id, ingredient_id));

CREATE TABLE grocery_list
(list_id int,
 ingredient_id INTEGER references ingredients(ingredient_id),
 recipe_id INTEGER references recipes(recipe_id)
 quantity REAL,
 quantity_type VARCHAR(255)
 grabbed BOOLEAN);
```

## REST Endpoints:
Name | HTTP Method | Path
------------ | ------------- | -------------
List | GET | /ingredients
List | GET | /recipes
List | GET | /groceries
Retrieve | GET | /ingredients/ingredientID
Retrieve | GET | /recipes/recipeID
Retrieve | GET | /groceries/listID
Create | POST | /recipes
Create | POST | /ingredients
Create | POST | /groceries
Replace | PUT | /ingredients/ingredientID
Replace | PUT | /recipes/recipeID
Replace | PUT | /groceries/listID
Delete | DELETE | /ingredients/ingredientID
Delete | DELETE | /recipes/recipeID
Delete | DELETE | /groceries/listID

## Heroku URL
#### https://afternoon-wave-54596.herokuapp.com/
