import pickle


#Calculate the difficulty of recipe
def calc_difficulty(recipe):
    if recipe['cooking_time'] < 10 and len(recipe['ingredients']) < 4:
        recipe['difficluty'] = 'Easy'

    elif recipe['cooking_time'] < 10 and len(recipe['ingredients']) >= 4: 
        recipe['difficluty'] = 'Medium'

    elif recipe['cooking_time'] >= 10 and len(recipe['ingredients']) < 4:    
        recipe['difficluty'] = 'Intermediate'

    elif recipe['cooking_time'] >= 10 and len(recipe['ingredients']) >= 4:
        recipe['difficluty'] = 'Hard'   



#Gather information of recipes from user into dictionary
def take_recipe():
    name = str(input('Enter Name of Recipe?   '))
    cooking_time = int(input('Enter cooking time?   '))
    ingredients = input('Enter the ingredients for this recipe?   ')
    ingredients = ingredients.split()
    ingredients = [ingredient.lower() for ingredient in ingredients]

    recipe = {'name': name, 'cooking_time': cooking_time, 'ingredients': ingredients }
    difficluty = calc_difficulty(recipe)

    return recipe    


# get file from user and add details of recipes list and ingredient list to respective files
recipes_list = []
all_ingredients = []

filename = str(input("Enter the filename where you've stored your recipes: (type N if there's not) ")) 
try:
    recipes_file = open(filename, 'rb')
    data = pickle.load(recipes_file)

except FileNotFoundError:
    print("File doesn't exist - creating new file")
    data = {'recipes_list':[], 'all_ingredients': []}

except:
    print("An unexpected error occurred - creating new file")
    data = {'recipes_list':[], 'all_ingredients': []}

else:
    recipes_file.close()    

finally:
    recipes_list = data['recipes_list']
    all_ingredients = data['all_ingredients']  


#Enter recipes details from user
n = int(input('How many recipe would you like to enter?   '))

for i in range(n):
    recipe = take_recipe()
    print(recipe)

    for ingredient in recipe['ingredients']:
        if ingredient not in all_ingredients:
            all_ingredients.append(ingredient)

    recipes_list.append(recipe)       

data = {'recipes_list': recipes_list, 'all_ingredients': all_ingredients}

new_file_name = str(input('Enter a name for your new file??   '))
new_file_name = open(new_file_name, 'wb')
pickle.dump(data, new_file_name)