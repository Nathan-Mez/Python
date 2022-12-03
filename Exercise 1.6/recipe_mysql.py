import mysql.connector

conn = mysql.connector.connect(
    host = 'localhost',
    user = 'cf-python',
    passwd = 'password')
cursor = conn.cursor() 

cursor.execute("CREATE DATABASE IF NOT EXISTS task_database")
cursor.execute("USE task_database")
cursor.execute('''CREATE TABLE IF NOT EXISTS Recipes(
    id              INT PRIMARY KEY AUTO_INCREMENT,
    name            VARCHAR(50),
    ingredients     VARCHAR(255),
    cooking_time    INT,
    difficulty      VARCHAR(20))
    ''')


def calculate_difficulty(cooking_time, ingredients):
    difficulty = None
    if cooking_time < 10 and len(ingredients)< 4:
            difficulty = 'Easy'
    elif cooking_time < 10 and len(ingredients) >= 4: 
            difficulty = 'Medium'
    elif cooking_time >= 10 and len(ingredients) < 4:    
            difficulty = 'Intermediate'
    elif cooking_time >= 10 and len(ingredients) >= 4:
            difficulty = 'Hard' 

    return difficulty   


def main_menu(conn, cursor):

    # Create a new recipe
    def create_recipe(conn, cursor):
        name = str(input('Enter the name of the recipe:   '))
        cooking_time = int(input('Enter the total cooking time:   '))
        ingredients = []
        n = int(input('Enter the number ingredients for this recipe:   '))           # use for loop to fill ingredients list to avoid string representation
        for i in range(0, n):                                                        # format on ingredients
            ingredient = input(' - ')
            ingredients.append(ingredient)                                           # adding the ingredient to ingredients list
        difficulty = calculate_difficulty(cooking_time, ingredients)

        ingredients = ", ".join(ingredients)
        print(ingredients)

        sql = "INSERT INTO Recipes (name, cooking_time, ingredients, difficulty) VALUES (%s, %s, %s, %s)"
        val = (name, cooking_time, ingredients, difficulty)
        cursor.execute(sql, val)
        conn.commit()



    # search recipe from list of recipes with includes searched ingredient
    def search_recipe(conn, cursor):
        cursor.execute("SELECT ingredients FROM Recipes")
        results = cursor.fetchall() 

        all_ingredients = []
        
        print("List of all ingredients" + '\n' + 40*'=')
        # add all ingredients fetched to all_ingredients list
        for row in results:
            row = row[0]
            row = row.split(", ")
            
            for ingredient in row:
                if ingredient not in all_ingredients:
                    all_ingredients.append(ingredient)

        # Print a list of all ingredients in all_ingredients list
        count = 1
        for ingredient in all_ingredients:
            print(count, "- ", ingredient)
            count = count + 1
        
        # store user input of searched ingredient on search_ingredient variable
        search_ingredient = int(input('Enter the corresponding number of the ingredient you want to search:   '))
        index = search_ingredient - 1
        search_ingredient = all_ingredients[index]

        # print list of recipe name that have searched_ingredient on ingredients list
        sql = "SELECT ingredients FROM Recipes WHERE ingredients LIKE '%" + search_ingredient + "%'"
        cursor.execute(sql)
        results_3 = cursor.fetchall()
        cursor.execute("SELECT name FROM Recipes WHERE ingredients LIKE '%" + search_ingredient + "%'")
        results_2 = cursor.fetchall()
        print("List of recipes with ingredient " + search_ingredient)
        print(45*"=")
        for row in results_2:
            print(row[0])



    # update recipe from a list of recipes
    def update_recipe(conn, cursor):
        cursor.execute("SELECT * FROM Recipes")
        results = cursor.fetchall()

        print("\nChoose the recipe you wish to update:")
        print(40*"=")
        for row in results:
            print(row[0], row[1])

        searched_recipe_id = str(input('Enter the corresponding number of the recipes you want to update:   '))
   
        if not searched_recipe_id == None:
            searched_recipe_column = str(input("What column do you want to update? Type 'name', 'cooking_time' or 'ingredients':   "))

            if searched_recipe_column == 'name':
                new_name = str(input('Enter a new name for this recipe:  '))
                sql = "UPDATE Recipes SET name = '" + new_name + "' WHERE id = " + searched_recipe_id
                cursor.execute(sql)
                print("\nUpdated name to: " + new_name )

            elif searched_recipe_column == 'cooking_time':
                new_cookingtime = str(input('Enter a new cooking time for this recipe:   '))
                new_difficulty = calculate_difficulty (int(new_cookingtime), row[4])
                sql = "UPDATE Recipes SET cooking_time = " + new_cookingtime + " WHERE id = " + searched_recipe_id 
                sql_2 = "UPDATE Recipes SET difficulty = '" + new_difficulty + "' WHERE id = " + searched_recipe_id
                cursor.execute(sql)
                cursor.execute(sql_2)
                print("\nUpdated cooking time to: " + new_cookingtime + ", and difficulty to: " + new_difficulty)

            elif searched_recipe_column == 'ingredients':
                new_ingredients = []
                n = int(input('Enter the number ingredients for this recipe:   '))        
                for i in range(0, n):                                                        
                    ingredient = input(' - ')
                    new_ingredients.append(ingredient)
                new_ingredients_joined = ", ".join(new_ingredients)    
                new_difficulty = calculate_difficulty (row[3], new_ingredients)
                sql = "UPDATE Recipes SET ingredients = '" + new_ingredients_joined + "' WHERE id = " + searched_recipe_id
                sql_2 = "UPDATE Recipes SET difficulty = '" + new_difficulty + "' WHERE id = " + searched_recipe_id
                cursor.execute(sql)
                cursor.execute(sql_2)
                print("\nUpdated Ingredients to: " + new_ingredients_joined + ", and difficulty to: " + new_difficulty)

            else: 
                print("\nYOU DIDN'T TYPE EITHER 'name', 'cooking_time' or 'ingredients'. PLEASE TYPE ONE OF THESE OR Ctrl+c TO EXIT...") 
                update_recipe(conn, cursor)   
 
            conn.commit()
               


    # Delete recipe from database
    def delete_recipe(conn, cursor): 
        cursor.execute("SELECT * FROM Recipes")
        results = cursor.fetchall()

        print("\nChoose the recipe you wish to delete:")
        print(40*"=")
        for row in results:
            print(row[0], row[1])   

        searched_recipe_id = str(input('Enter the corresponding number of the recipes you want to delete:   ')) 
        try:
            sql = "DELETE FROM Recipes WHERE id = " + searched_recipe_id
            cursor.execute(sql)
            conn.commit()
        except:
            print("You didn't enter a number from the list. Please enter numbers only from the list ones or Ctrl+C to exit...")  
            delete_recipe(conn, cursor)        
        else:
            print('\n Deleted Succesfuly!!')                    

    
    choice = None
    while not choice == 'quit':
        print("\n     Main Menu" + "\n" + 30*"=")
        print("What would you like to do? Pick a choice!")
        print("1. Create a new recipe")
        print("2. Search for a recipe by ingredient")
        print("3. Update a recipe")
        print("4. Delete recipe")
        print("Type 'quit' to exit the program")
        choice  = input("\nYour choice:   ")

        if choice == '1':
            create_recipe(conn, cursor)
        elif choice =='2':
            search_recipe(conn, cursor)
        elif choice == '3':
            update_recipe(conn, cursor)
        elif choice == '4':
            delete_recipe(conn, cursor)
        else: 
            conn.commit()
            conn.close()
            print('\nGoodbye!!')     


# START RUNNING PROGRAM
main_menu(conn, cursor)             


# python recipe_mysql.py  

                    
