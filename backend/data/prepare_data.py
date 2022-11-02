import json


def add_parametrs(ingredient, id):
    return {
        "model": "recipes.ingredient",
        "pk": id,
        "fields": ingredient
    }


def create_fixtures():
    with open('ingredients.json', 'r') as f:
        ingredients = json.loads(f.read())
        for i in range(len(ingredients)):
            ingredients[i] = add_parametrs(ingredients[i], i + 1)
    with open('fixtures.json', 'w') as f:
        f.write(json.dumps(ingredients))


if __name__ == '__main__':
    create_fixtures()