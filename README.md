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
quantity_type VARCHAR(255),
primary key (recipe_id, ingredient_id));

CREATE TABLE IF NOT EXISTS grocery_list
(list_id int,
ingredient_id INTEGER references ingredients(ingredient_id),
recipe_id INTEGER references recipes(recipe_id),
quantity REAL,
quantity_type VARCHAR(255),
grabbed BOOLEAN);
```

## REST Endpoints:
Name | HTTP Method | Path | Expected Body (x-www-form-urlencoded)
------------ | ------------- | ------------- | -------------
List | GET | /ingredients |
List | GET | /recipes |
List | GET | /groceries |
Retrieve | GET | /ingredients/ingredientID |
Retrieve | GET | /recipes/recipeID |
Retrieve | GET | /groceries/listID |
Create | POST | /recipes | label, directions
Create | POST | /ingredients | label, category
Create | POST | /groceries |
Create | POST | /recipes/ingredients | recipe_id, ingredient_id, quantity, quantity_type
Replace | PUT | /ingredients/ingredientID
Replace | PUT | /recipes/recipeID
Replace | PUT | /recipes/ingredients
Replace | PUT | /groceries/listID
Delete | DELETE | /recipes/ingredients
Delete | DELETE | /ingredients/ingredientID
Delete | DELETE | /recipes/recipeID
Delete | DELETE | /groceries/listID

## Heroku URL
#### https://stormy-everglades-69504.herokuapp.com/ 
