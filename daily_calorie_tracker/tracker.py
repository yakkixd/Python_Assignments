# Name: Yaksh Kundu 
# Date: 7 November, 2025
# Project: Daily Calorie Tracker CLI

from datetime import datetime

def get_meals():
    meals = []
    cals = []
    while True:
        try:
            n = int(input("How many meals do you want to enter? "))
            if n <= 0:
                print("Enter a positive number.")
                continue
            break
        except:
            print("Please enter a valid number.")
    for i in range(n):
        m = input("Meal name: ").strip()
        while not m:
            m = input("Meal name cannot be empty, re-enter: ").strip()
        while True:
            x = input("Calories: ").strip()
            try:
                x = float(x)
                break
            except:
                print("Enter valid calorie value.")
        meals.append(m)
        cals.append(x)
    return meals, cals

def show_report(meals, cals, limit):
    total = sum(cals)
    avg = total / len(cals)
    print("\nMeal Name\tCalories")
    print("--------------------------------")
    for i in range(len(meals)):
        print(f"{meals[i]}\t{cals[i]}")
    print(f"\nTotal:\t{total}")
    print(f"Average:\t{avg:.2f}")
    if total > limit:
        print("\nWarning: You exceeded your daily limit.")
    else:
        print("\nGood job: You are within your daily limit.")
    return total, avg

def save_log(meals, cals, total, avg, limit):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("calorie_log.txt","w") as f:
        f.write("Daily Calorie Tracker Log\n")
        f.write(f"Timestamp: {now}\n\n")
        for i in range(len(meals)):
            f.write(f"{meals[i]} - {cals[i]} cal\n")
        f.write(f"\nTotal: {total}\n")
        f.write(f"Average: {avg:.2f}\n")
        if total > limit:
            f.write("Status: Exceeded limit\n")
        else:
            f.write("Status: Within limit\n")
    print("Session saved as calorie_log.txt")

def main():
    print("Welcome to the Daily Calorie Tracker")
    print("This tool helps you record meals and track calorie intake.\n")
    meals, cals = get_meals()
    while True:
        try:
            limit = float(input("Enter your daily calorie limit: "))
            break
        except:
            print("Enter a valid number.")
    total, avg = show_report(meals, cals, limit)
    s = input("\nDo you want to save this session? (yes/no): ").strip().lower()
    if s == "yes":
        save_log(meals, cals, total, avg, limit)
    print("Done")

if __name__ == "__main__":
    main()
  
