
class Recipe(object):

    def __init__(self, name):
        self.name = name
        self.ingredients = []
        self.cooking_time = 0
        self.difficulty = self.calculate_difficulty() 

    def get_name(self):
        return self.name

    def get_cooking_time(self):
        return self.cooking_time

    def set_name(self, name):
        self.name = name

    def set_cooking_time(self, cooking_time):
        self.cooking_time = cooking_time

    def add_ingredients(self, *args):
        for ingredient in args:
            self.ingredients.append(ingredient)
        self.update_all_ingredients()    
        print('ingredients list: ', self.ingredients)  

    def ingredients(self):
        return self.ingredients  

    def calculate_difficulty(self):
        print('difficult ingredient: ', self.ingredients) 
        if self.cooking_time < 10 and len(self.ingredients)< 4:
            self.difficulty = 'Easy'
        elif self.cooking_time < 10 and len(self.ingredients) >= 4: 
            self.difficulty = 'Medium'
        elif self.cooking_time >= 10 and len(self.ingredients) < 4:    
            self.difficulty = 'Intermediate'
        elif self.cooking_time >= 10 and len(self.ingredients) >= 4:
            self.difficulty = 'Hard'       
        return self.difficulty    

    def get_difficulty(self):
        self.calc_difficulty()
        return self.difficulty

    def search_ingredient(recipe, ingredient):
        if ingredient in recipe.ingredients:
            return True
        else:
            return False

    all_ingredients = []

    def update_all_ingredients(self):
        if not self.ingredients == None:
            for ingredient in self.ingredients:
                if ingredient not in self.all_ingredients:
                    self.all_ingredients.append(ingredient)

    def __str__(self):
        output = '\nRecipe for ' + str(self.name) + '\n' + 20*'-' + '\nCooking Time (min) - ' + str(self.cooking_time) + '\nDifficulty - ' + str(self.difficulty) + '\nIngredients - \n'
        for ingredient in self.ingredients:
            output += "    " + ingredient + "\n"
        return output        

    def recipe_search(self, data, search_term):
        for recipe in data:
            print(recipe)
            if self.search_ingredient(recipe, search_term):
                print(recipe)  

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
Recipe.recipe_search(recipes_list, 'Water')



    

                
                

