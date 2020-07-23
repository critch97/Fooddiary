from tkinter import *

#Initializing the database

root = Tk()
root.title("Food Diary")
e = Entry(root, width = 25, borderwidth = 5)
e.grid(row=0, column=0, padx=10, pady=10)
e.insert(index = 0 ,  string="What would you like to do?")

class FoodDiary:
    def __init__(self):
        import os
        import csv
        #This is to see if the file already exists, if it does but doesn't contain headings, it writes the headings
        try:
            with open("fooddata.csv", "a") as file:
                writer = csv.writer(file)
                if os.stat("fooddata.csv").st_size == 0:
                    print("Creating file...")
                    writer.writerow(["Food", "Protein(g)", "Carbohydrates(g)", "Fats(g)", "Calories(kcal)"])
                else:
                #This means that the file already exists with headings
                    print("File Open")

        except FileNotFoundError:
        #If the file does not exist, it writes a new file called "fooddata.csv"
            print("File doesn't exist, creating new file")
            with open("fooddata.csv", "w") as file:
                writer = csv.writer(file)
                writer.writerow(["Food", "Protein(g)", "Carbohydrates(g)", "Fats(g)", "Calories(kcal)"])

        import pandas as pd
        #Changing the csv file to a pandas database
        self.food_db = pd.read_csv("fooddata.csv",index_col=[0])

    def add_food(self):
        def submit():
            try:
                #calculating the total calories
                calories = ((4.2 * float(protein.get())) +(4.2 * float(carbs.get())) + (9.1 * float(fat.get())))

                #adding the answers from the text boxes, converting the macronutrients to floats
                self.food_db = self.food_db.append(
                {"Food": food.get(),
                "Protein(g)": float(protein.get()),
                "Carbohydrates(g)": float(carbs.get()),
                "Fats(g)": float(fat.get()),
                "Calories(kcal)": calories},
                ignore_index=True)

                # Clearing the text boxes to prompt it has been added
                food.destroy()
                protein.destroy()
                carbs.destroy()
                fat.destroy()
                food_label.destroy()
                protein_label.destroy()
                carbs_label.destroy()
                fat_label.destroy()
                submit_button.destroy()
                print("Added to diary")
                return self.food_db
            except:
                print("Please enter values correctly")




        #creating the text boxes
        food = Entry(root, width=30)
        food.grid(row=2, column = 1)

        protein = Entry(root, width=30)
        protein.grid(row=3, column=1)

        carbs = Entry(root, width=30)
        carbs.grid(row=4, column=1, padx=20)

        fat = Entry(root, width=30)
        fat.grid(row=5, column=1, padx=20)

        #creating the text box labels
        food_label = Label(root, text="Name of food")
        food_label.grid(row=2, column=0)

        protein_label = Label(root, text="Protein content(g)")
        protein_label.grid(row=3, column=0)

        carbs_label = Label(root, text="Carbohydrate content(g)")
        carbs_label.grid(row=4, column=0)

        fat_label = Label(root, text="Fat content(g)")
        fat_label.grid(row=5, column=0)

        submit_button = Button(root, text="Submit entry", command=submit)
        submit_button.grid(row=6, column=1)

    def remove_food(self):
        def delete():
            #Function to delete the food selected
            try:
                print(f"{fooddel.get()} removed!")
                self.food_db = self.food_db[self.food_db.Food != fooddel.get()]
                fooddel.destroy()
                food_label.destroy()
                delete_button.destroy()
                return self.food_db
            except:
                print("Enter values correctly")
        #Removes one food of the users choice
        for item in self.food_db.loc[:, 'Food']:
            print(item)

        #Creating the textbox
        fooddel = Entry(root, width=30)
        fooddel.grid(row=2, column=1)

        #Creating the labels
        food_label = Label(root, text="Name of food to delete")
        food_label.grid(row=2, column=0)

        #Linking to the delete function delete()
        delete_button = Button(root, text="Delete", command=delete)
        delete_button.grid(row=3, column=1)

    def show_diary(self):
        #Shows the user the database
        return self.__str__()

    def __str__(self):
        print(self.food_db)
        return str()

    def graph(self):
        #Displays the protein,carbs and fat (%) in a pie chart
        import matplotlib.pyplot as plt

        #Macronutrient grams per calorie taken from Mcardle, Katch & Katch (2016).
        #Calculating the calories from protein, carbs and fats
        protein = sum(self.food_db["Protein(g)"])
        carbs = sum(self.food_db["Carbohydrates(g)"])
        fat = sum(self.food_db["Fats(g)"])
        colours = ["#7CB9E8","#50C878", "#DC143C"]
        #Creating a graph with the macronutrients as headings
        total_cals = [protein,carbs,fat]
        labels = f"Protein ({protein}g)",f"Carbohydrates ({carbs}g)",f"Fat ({fat}g)"
        plt.pie(total_cals, autopct='%1.1f%%', wedgeprops={"edgecolor":"black"},
                colors= colours , startangle = 90, textprops = {"color":"w"})
        plt.title("Macronutrients")
        plt.legend(labels, loc="center" ,bbox_to_anchor= (0,0))
        plt.show()

    def close(self):
        #Closing the database and updating the original csv file
        self.food_db = self.food_db.to_csv("fooddata.csv")
        exit()



diary = FoodDiary()
#Creating the buttons appearance and adding the food_diarycsv classes functions as commands
addfood_button = Button(root, text="Add food", padx = 20, pady = 20, command = diary.add_food)
addfood_button.grid(row=2, column = 2)

removefood_button = Button(root, text="Remove food", padx = 10, pady = 20, command =  diary.remove_food)
removefood_button.grid(row=3, column = 2)

graph_button = Button(root, text="Display Graph", padx = 10, pady = 20, command = diary.graph)
graph_button.grid(row=4, column = 2)

showdiary_button = Button(root, text="Show my diary", padx=7, pady=20, command= diary.show_diary)
showdiary_button.grid(row=1, column=2)

closedown_button = Button(root, text="Save & Close", padx = 10, pady = 20, command= diary.close)
closedown_button.grid(row=5, column = 2)

root.mainloop()
