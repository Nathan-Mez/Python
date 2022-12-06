from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column
from sqlalchemy.types import Integer, String
from sqlalchemy.orm import sessionmaker

engine = create_engine("mysql://cf-python:password@localhost/task_database")
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class Recipe(Base):
    __tablename__ = "final_recipes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    ingredients = Column(String(255))
    cooking_time = Column(Integer)
    difficulty = Column(String(20))

    def __repr__(self):
        return "<Recipe ID: " + str(self.id) + "\nName: " + self.name + "\nDifficulty: " + self.difficulty + ">"

    # string representaion for the Recipe class
    def __str__(self):
        output = '\nRecipe for ' + str(self.name) + '\n' + 20*'-' + '\nCooking Time (min) - ' + str(self.cooking_time) + '\nDifficulty - ' + str(self.difficulty) + '\nIngredients - \n'
        self.return_ingredients_as_list()
        for ingredient in self.ingredients:
            output += "    " + ingredient + "\n"
        return output 

    # calculate difficulty of recipe using cooking time and number of ingredients
    def calculate_difficulty(self):
        difficulty = None
        if self.cooking_time < 10 and len(self.ingredients)< 4:
            difficulty = 'Easy'
        elif self.cooking_time < 10 and len(self.ingredients) >= 4: 
            difficulty = 'Medium'
        elif self.cooking_time >= 10 and len(self.ingredients) < 4:    
            difficulty = 'Intermediate'
        elif self.cooking_time >= 10 and len(self.ingredients) >= 4:
            difficulty = 'Hard'   
       
        print("Difficulty of recipe calculated to: " + difficulty)
        self.difficulty = difficulty

    # change user input ingredients string to list
    def return_ingredients_as_list(self):   
        if self.ingredients == "":
            self.ingredients = []
        else:
            self.ingredients = self.ingredients.split(", ") 

# create table on database
Base.metadata.create_all(engine)



# function to create new recipe
def create_recipe():
    name, cooking_time = None, None                       # set name and cooking_time variables
    
    name_input = str(input('Enter the name of the recipe (LETTERS ONLY, max of 50 char.):   '))
    if len(name_input) < 51 and name_input.isalpha():
        name = name_input                                 # get user defined name and set to name
    else:
        print("\nYou have entered words either greater than 50 in length or included numbers or symbols in your name! Try again or Ctrl+C to exit")    
        return None                                       # return to main menu if user entered name is not valid

    cooking_time_input = input('Enter the total cooking time (INTEGER NUMBERS ONLY):   ')
    if cooking_time_input.isnumeric():
        cooking_time = int(cooking_time_input)            # get user defined cooking time to cooking_time
    else:
        print("\nYou have not entered cooking time correctly, please enter cooking time in whole integer numbers or Ctrl+C to exit")
        return None                                       # return to main menu if user entered cooking time is not valid

    ingredients = []
    n = int(input('Enter the number ingredients for this recipe (max ingredient no. 255):   '))   
    if n > 255:
        print("\n Maximum number of ingredients is 255, please try again!!")
        return None
    else:
        print("\n Enter The ingredients for the recipe: " + "\n" + 40*"-" )        
        for i in range(0, n):                                                        # use for loop to fill ingredients list to avoid string representation
            ingredient = input(' - ')                                                # format on ingredients
            ingredients.append(ingredient) 
    ingredients = ", ".join(ingredients)
    

    # create a new object using the user enter info above
    recipe_entry = Recipe(
        name = name,
        cooking_time = cooking_time,
        ingredients = ingredients,
        difficulty = None
    )  
    # calculate difficulty of the new recipe
    recipe_entry.calculate_difficulty() 
    session.add(recipe_entry)
    session.commit()
    print("\n Recipe Added Succesfully!")



# View all recipes
def view_all_recipes():                                            
    recipes_list = session.query(Recipe).all()                                # get all recipe object from database
    if recipes_list == []:
        print("\n There are currently no recipes in the database!")
        return None                                                           # if there're no recipes on database, notify user and return to main menu
    else:
        for recipe in recipes_list:
            print(recipe)                                                     # display string representation of each recipe object in database



# search for recipes using ingredients as key
def search_by_ingredients():
    # Check if any recipes exist on our database, and continue only if there are any
    recipes_count = session.query(Recipe).count()
    if recipes_count == 0:
        print("\n There are currently no recipes in the database!!")
        return None                                                            # Notify and return to main menu if no recipes exist in database
    else:
        # get ingredients list from all recipe objects 
        recipes_list = session.query(Recipe).all()
        recipes_ingredients = [recipe.ingredients for recipe in recipes_list]
         
        # separate and add (non repetitively) to all_ingredients each ingredient from ingrediets list on each recipe object
        all_ingredients = []
        for recipe_ingredient in recipes_ingredients:
            recipe_ingredients = recipe_ingredient.split(", ")
            for ingredient in recipe_ingredients:
                if ingredient not in all_ingredients:
                    all_ingredients.append(ingredient)

        # Print a list of all ingredients in all_ingredients list
        print("\n List of ingredients on the current recipes present on database: " + "\n" + 45*"-")
        count = 1
        for ingredient in all_ingredients:
            print(count, "- ", ingredient)
            count = count + 1     

        # store user input of searched ingredient on search_ingredient variable
        search_num = input('\nEnter the corresponding numbers of the ingredients you want to search (Separate each numbers by space inbetween):   ')
        search_num = search_num.split(" ")   

        search_ingredients = []
        for n in search_num:
            index = int(n) - 1 
            if int(n) <= count:
                ingredient = all_ingredients[index]
                search_ingredients.append(ingredient)

        # set conditions list for conditions for each ingredient to be searched for
        conditions = []
        for ingredient in search_ingredients:
            like_term = "%" + ingredient + "%"
            conditions.append(Recipe.ingredients.like(like_term))

        # Display list of recipes with searched ingredients in ingredients list
        searched_recipes = session.query(Recipe).filter(*conditions).all() 
        print("Recipes with ingredients you searched are:" + "\n" + 45*"-")
        for recipe in searched_recipes:
            print("- " + recipe.name)  



# Edit recipe from recipes list
def edit_recipe():
    # Check if any recipes exist on our database, and continue only if there are any
    recipes_count = session.query(Recipe).count()
    if recipes_count == 0:
        print("\n There are currently no recipes to edit in the database!!")
        return None
    else:
        recipes_list = session.query(Recipe).all()
        print("\n Choose from the following recipes available to edit:" + "\n" + 50*"-")
        recipe_ID_available = []
        for recipe in recipes_list:
            print("ID", recipe.id, "-", recipe.name)
            recipe_ID_available.append(recipe.id)
        id_picked = int(input("\nEnter the corresponding id number of the recipe you want to edit:  ")) 

        if id_picked in recipe_ID_available:
            recipe_to_edit = session.query(Recipe).filter(Recipe.id == id_picked).one()
            print("Choose the corresponding number of the recipe attribute you want to edit: ")
            print("\n1 - Recipe Name: " + recipe_to_edit.name + "\n2 - Recipe Cooking time: " + str(recipe_to_edit.cooking_time) + "\n3 - Ingredients: " + str(recipe_to_edit.ingredients) )
            chosen_attribute = int(input('\nEnter your number here:   '))

            if chosen_attribute == 1 or chosen_attribute == 2 or chosen_attribute == 3:
                if chosen_attribute == 1:
                    name_input = str(input('Enter a new name for the recipe (LETTERS ONLY, max of 50 char.):   '))
                    if len(name_input) < 51 and name_input.isalpha():
                        recipe_to_edit.name = name_input
                        print("\n You have changed recipe name to", recipe_to_edit.name)
                    else:
                        print("\nYou have entered words either greater than 50 in length or included numbers or symbols in your name! Try again or Ctrl+C to exit") 
                        edit_recipe()

                elif chosen_attribute == 2:
                    cooking_time_input = input('Enter the total cooking time (INTEGER NUMBERS ONLY):   ')
                    if cooking_time_input.isnumeric():
                        cooking_time = int(cooking_time_input)
                        recipe_to_edit.cooking_time = cooking_time
                        print("\n You have changed recipe cooking time to", recipe_to_edit.cooking_time)
                    else:
                        print("\nYou have not entered cooking time correctly, please enter cooking time in whole integer numbers or Ctrl+C to exit")
                        edit_recipe()

                elif chosen_attribute == 3:
                    ingredients = []
                    n = int(input('Enter the number ingredients for this recipe (max ingredient no. 255):   '))   
                    if n > 255:
                        print("\n Maximum number of ingredients is 255, please try again!!")
                        edit_recipe()
                    else:
                        print("\n Enter The ingredients for the recipe: " + "\n" + 40*"-" )        
                        for i in range(0, n):                                                        # use for loop to fill ingredients list to avoid string representation
                            ingredient = input(' - ')                                                # format on ingredients
                            ingredients.append(ingredient) 
                    ingredients = ", ".join(ingredients)
                    recipe_to_edit.ingredients = ingredients
                    print("\n You have changed recipe ingredients to ", ingredients)

                # Recalculate the difficulty using the object 'recipe_to_edit' calculate_difficulty() method
                recipe_to_edit.calculate_difficulty()
               
                # commit the change edited to the database
                session.commit()   

            else:
                print("\n The number you have chosen is not in the attributes list, try again!")
                edit_recipe()    

        else:
            print("The id you picked is not available on the list for edit!")
            edit_recipe()



# Delete recipes from recipes list
def delete_recipe():
    # Check if any recipes exist on our database, and continue only if there are any
    recipes_count = session.query(Recipe).count()
    if recipes_count == 0:
        print("\n There are currently no recipes to edit in the database!!")
        return None
    else:
        # Get all recipes from database and display recipes name and their correcponding ID to user to choose
        recipes_list = session.query(Recipe).all()
        print("\n Choose from the following recipes available to Delete:" + "\n" + 50*"-")
        recipe_ID_available = []
        for recipe in recipes_list:
            print("ID", recipe.id, "-", recipe.name)
            recipe_ID_available.append(recipe.id)

        # Get ID of recipe user want to delete and confirm if user want to delete, if not sure return to main menu else continue 
        id_picked = input("\nEnter the corresponding id number of the recipe you want to delete:  ") 
        if id_picked.isnumeric(): 
            id_picked = int(id_picked)
            if id_picked in recipe_ID_available:
                recipe_to_delete = session.query(Recipe).filter(Recipe.id == id_picked).one()
                print("\n Are you sure you want to delete " + recipe_to_delete.name + " recipe. This action cannot be undone!")
                sure_or_not = input("Enter 'Yes' if you're sure otherwise 'No':   ")
                sure_or_not = sure_or_not.lower()
                if sure_or_not == 'no':
                    return None
                else:
                    #get recipe to be delelted using user defined ID filetered from all recipes
                    recipe_to_be_deleted = session.query(Recipe).filter(Recipe.name == recipe_to_delete.name).one()
                    session.delete(recipe_to_be_deleted)
                    # commit the deleted recipe to database
                    session.commit()
                    print("\n Recipe deleted Succesfully!!")
            else:
                print("\nYou have not entered a numeric number, try again!")      

        else:
            print("The id you picked is not available on the list for edit!")
            edit_recipe()




 #------------- The main menu function ---------------------------
def main_menu():
    choice = None
    while not choice == 'quit':
        print("\n     Main Menu" + "\n" + 30*"=")
        print("What would you like to do? Pick a choice!")
        print("1. Create a new recipe")
        print("2. View all recipes")
        print("3. Search for a recipe by ingredient")
        print("4. Edit a recipe")
        print("5. Delete recipe")
        print("Type 'quit' to exit the program")
        choice  = input("\nYour choice:   ")

        if choice == '1':
            create_recipe()
        elif choice =='2':
            view_all_recipes()
        elif choice == '3':
            search_by_ingredients()
        elif choice == '4':
            edit_recipe()
        elif choice == '5':
            delete_recipe()
        elif choice.lower() == 'quit':          # user can exit program by typing 'quit' on main menu
            session.close()
            engine.dispose() 
            print('\nGoodbye!!')   
        else:
            print("Incorrect input, Please enter one of the numbers listed or 'quit' to exit the program")         

# START RUNNING PROGRAM
main_menu()                       

            





            






          

                         



 






