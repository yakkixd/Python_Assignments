# Name:  Yaksh Kundu
# Date: 7 November, 2025
# Project: Daily Calorie Tracker CLI

from datetime import datetime

print("Welcome to the Daily Calorie Tracker")
print("This program lets you add your meals and check how many calories you ate.\n")

n = int(input("How many meals do you want to enter? "))

meals = []
cals = []

for i in range(n):
    m = input("Meal name: ")
    c = float(input("Calories: "))
    meals.append(m)
    cals.append(c)

total = sum(cals)
avg = total / len(cals)

limit = float(input("Enter your daily calorie limit: "))

print("\nMeal Name\tCalories")
print("--------------------------------")

for i in range(len(meals)):
    print(f"{meals[i]}\t{cals[i]}")

print(f"\nTotal:\t{total}")
print(f"Average:\t{avg:.2f}")

if total > limit:
    print("\nWarning: You exceeded your daily limit.")
else:
    print("\nYou are within your daily limit.")

save = input("\nDo you want to save this report? (yes/no): ")

if save.lower() == "yes":
    t = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    f = open("calorie_log.txt", "w")
    f.write("Calorie Tracker Log\n")
    f.write(f"Time: {t}\n\n")
    for i in range(len(meals)):
        f.write(f"{meals[i]} - {cals[i]} cal\n")
    f.write(f"\nTotal: {total}\n")
    f.write(f"Average: {avg:.2f}\n")
    if total > limit:
        f.write("Status: Exceeded limit\n")
    else:
        f.write("Status: Within limit\n")
    f.close()
    print("Report saved.")
  
