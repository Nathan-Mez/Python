
recipes_list = []
ingredients_list = []

def take_recipe():
    name = str(input('Enter Name of Recipe?   '))
    cooking_time = int(input('Enter cooking time?   '))
    ingredients = input('Enter the ingredients for this recipe?   ')
    ingredients = ingredients.split()
    recipe = {'name': name, 'cooking_time': cooking_time, 'ingredients': ingredients}
    return recipe


n = int(input('How many recipe would you like to enter?   '))

for i in range(n):
    recipe = take_recipe()
    print(recipe)

    for ingredient in recipe['ingredients']:
        if ingredient not in ingredients_list:
            ingredients_list.append(ingredient)

    recipes_list.append(recipe)


for recipe in recipes_list:
    if recipe['cooking_time'] < 10 and len(recipe['ingredients']) < 4:
        recipe['difficluty'] = 'Easy'

    elif recipe['cooking_time'] < 10 and len(recipe['ingredients']) >= 4: 
        recipe['difficluty'] = 'Medium'

    elif recipe['cooking_time'] >= 10 and len(recipe['ingredients']) < 4:    
        recipe['difficluty'] = 'Intermediate'

    elif recipe['cooking_time'] >= 10 and len(recipe['ingredients']) >= 4:
        recipe['difficluty'] = 'Hard'   
   
    print('==================================================')
    print('Recipe: ', recipe['name'])
    print('Cooking Time (min): ', recipe['cooking_time'])
    print('Ingredients: ' )
    for ingredient in recipe['ingredients']:
        print(ingredient)
    print('Difficulty level: ', recipe['difficluty'])    


print('''Ingredients available across all recipes
-------------------------------------------- ''')     
ingredients_list = []
for recipe in recipes_list:
    for ingredient in recipe['ingredients']:
        ingredients_list.append(ingredient)
for i in ingredients_list:
    print(i)



