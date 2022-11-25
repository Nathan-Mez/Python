import pickle

# function to display a recipe
def display_recipe(recipe):
    print('''Recipe details
    =====================''')
    print('Name: ', recipe['name'])
    print('Cooking time (min): ', recipe['cooking_time'])
    print('Ingredients: ', recipe['ingredients'])
    print('Difficulty: ', recipe['difficluty'])


#search ingredient and print all recipes that needs the searched ingredient

def search_ingredient(data):
    ingredients_list = data['all_ingredients']
    indexed_ingredients_list = list(enumerate(ingredients_list, 1))      #will retrun in the format [(1, a), (2, b), (3, c)]

    for ingredient in indexed_ingredients_list:
        print('No.', ingredient[0], ' - ', ingredient[1])

    try: 
        chosen_num = int(input('Enter the corresponding number of your chosen ingredient:   '))
        index = chosen_num - 1
        ingredient_searched = ingredients_list[index]
        ingredient_searched = ingredient_searched.lower()
    except IndexError:
        print('The number you entered is not on the list!')
    except:
        print('Some error happened finding the ingredient...')
    else:
        print('Recipes that include', ingredient_searched, 'are: ')
        print('---------------------------------------------------')
        for recipe in data['recipes_list']:
            if ingredient_searched in recipe['ingredients']:
                print(recipe['name']) 


# Enter the file name where the recipe data in hold
filename = str(input("Enter the filename where you've stored your recipes:  ")) 
try:
    recipes_file = open(filename, 'rb')
    data = pickle.load(recipes_file)

except FileNotFoundError:
    print("File doesn't exist in the current directory")
    data = {'recipes_list':[], 'all_ingredients': []}

except:
    print("An unexpected error occurred")
    data = {'recipes_list':[], 'all_ingredients': []}

else:
    search_ingredient(data)



        
        

