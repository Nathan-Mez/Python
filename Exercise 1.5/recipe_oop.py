
class Recipe(object):

    def __init__(self, name):
        self.name = name
        self.cooking_time = 0
        self.ingredients = []
        self.difficulty = None

    # get name of recipe
    def get_name(self):
        return self.name

    # get cooking time of recipe
    def get_cooking_time(self):
        return self.cooking_time

    def set_name(self, name):
        self.name = name
   
    # update cooking time of recipe
    def set_cooking_time(self, cooking_time):
        self.cooking_time = cooking_time
        self.difficluty = self.calculate_difficulty()       # update recipe difficulty each time cooking time is altered

    # add recipe ingredients 
    def add_ingredients(self, *args):
        for ingredient in args:
            self.ingredients.append(ingredient)   
        self.difficluty = self.calculate_difficulty()       # update recipe difficulty each time ingredient is added 
        self.update_all_ingredients()                       # update list of all ingredients 

    # get list of ingredients of the recipe in focus
    def ingredients_list(self):
        return self.ingredients  

    # calculate the recipe cooking difficulty
    def calculate_difficulty(self):
        ingredients = self.ingredients_list()
        if self.cooking_time < 10 and len(ingredients)< 4:
            self.difficulty = 'Easy'
        elif self.cooking_time < 10 and len(ingredients) >= 4: 
            self.difficulty = 'Medium'
        elif self.cooking_time >= 10 and len(ingredients) < 4:    
            self.difficulty = 'Intermediate'
        elif self.cooking_time >= 10 and len(ingredients) >= 4:
            self.difficulty = 'Hard'       
        return self.difficulty    

    # get the difficulty of recipe in focus
    def get_difficulty(self):
        self.calculate_difficulty()
        return self.difficulty

    # search ingredient on recipe ingredients in focus
    def search_ingredient(self, ingredient):
        if ingredient in self.ingredients_list():
            return True
        else:
            return False

    # find recipes that contain specific ingredient
    def recipe_search(data, search_term):
        print('\nRecipes that include ingredient', search_term, '\n', 40 *'-') 
        for recipe in data:
            if recipe.search_ingredient(search_term):
                print(recipe.name)
               
                                

    all_ingredients = []          # set class variable to store list of all ingredients across all objects

    # update list of all ingredients in 'all_ingredients' list
    def update_all_ingredients(self):
        if not self.ingredients == None:
            for ingredient in self.ingredients:
                if ingredient not in self.all_ingredients:
                    self.all_ingredients.append(ingredient)

    # string representaion for the Recipe class
    def __str__(self):
        output = '\nRecipe for ' + str(self.name) + '\n' + 20*'-' + '\nCooking Time (min) - ' + str(self.cooking_time) + '\nDifficulty - ' + str(self.difficulty) + '\nIngredients - \n'
        for ingredient in self.ingredients:
            output += "    " + ingredient + "\n"
        return output        

                 

#   python recipe_oop.py

tea = Recipe('Tea')
tea.add_ingredients('Tea Leaves', 'Water', 'Sugar')
tea.set_cooking_time(5)
print(tea)


coffee = Recipe('Coffee')
coffee.add_ingredients('Coffee Powder', 'Sugar', 'Water')
coffee.set_cooking_time(5)
print(coffee)

cake = Recipe('Cake')
cake.add_ingredients('Sugar', 'Butter', 'Eggs', 'Vanilla Essence', 'Flour', 'Baking Powder', 'Milk')
cake.set_cooking_time(50)
print(cake)

banana_smoothie = Recipe('Banana Smoothie')
banana_smoothie.add_ingredients('Bananas', 'Milk', 'Peanut Butter', 'Sugar', 'Ice Cubes')
banana_smoothie.set_cooking_time(5)
print(banana_smoothie)

recipes_list = [tea, coffee, cake, banana_smoothie]
print(Recipe.recipe_search(recipes_list, 'Water'))
print(Recipe.recipe_search(recipes_list, 'Sugar'))
print(Recipe.recipe_search(recipes_list, 'Bananas'))



    

                
                

