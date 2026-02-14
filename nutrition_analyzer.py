
import csv

DATA_FILE = "archive(1)/Food_Nutrition_Dataset.csv" 

with open(DATA_FILE, newline='', encoding="latin1") as file:
    reader = csv.reader(file)
    headers = next(reader)
    print("CSV Headers:", headers)
import os
import difflib
from datetime import datetime


def to_float(value):
    try :
        return float(value)
    except (ValueError , TypeError):
        return 0.0
REPORTS_DIR = "reports"


def load_food_data():
    
    food_db = []

    try:
        with open(DATA_FILE, newline='', encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Convert values to float, handle missing data
                food_db.append({
                    "food": row["food_name"].lower(),
                    "calories":to_float(row.get("calories", 0)),
                    "protein": to_float(row.get("protein", 0)),
                    "fat": to_float(row.get("fat", 0)),
                    "carbs":to_float(row.get("carbs", 0)),
                    "iron": to_float(row.get("iron", 0)),
                    "vitamin_c": to_float(row.get("vitamin_c", 0))
                })
    except FileNotFoundError:
        print(f" Dataset '{DATA_FILE}' not found! Place it in the project folder.")
        exit()

    return food_db


def search_food(food_db, query):
  
    query = query.lower()
    matches = [item for item in food_db if query in item["food"]]
    return matches


def save_report(summary):
    """
    Save daily nutrition summary as CSV in 'reports/' folder.
    """
    if not os.path.exists(REPORTS_DIR):
        os.mkdir(REPORTS_DIR)

    filename = f"daily_report_{datetime.now().date()}.csv"
    path = os.path.join(REPORTS_DIR, filename)

    with open(path, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Nutrient", "Amount"])
        for nutrient, value in summary.items():
            writer.writerow([nutrient, f"{value:.2f}"])

    print(f"\n📁 Report saved at: {path}")


def main():
    print("\n===== NUTRITION ANALYZER =====")
    print("Type 'Done' finished.\n")

    food_db = load_food_data()

   
    totals = {
        "Calories (kcal)": 0,
        "Protein (g)": 0,
        "Fat (g)": 0,
        "Carbs (g)": 0,
        "Iron (mg)": 0,
        "Vitamin C (mg)": 0
    }

    while True:
        food_input = input("Enter food: ").strip()
        if food_input.lower() == "done":
            break

        matches = search_food(food_db, food_input)

        if not matches:
            print(" Food not found. Try again.")
            continue

       
        if len(matches) > 1:
            print("\nMultiple matches found:")
            for i, item in enumerate(matches, 1):
                print(f"{i}. {item['food'].title()}")
            try:
                choice = int(input("Select option number: ")) - 1
                selected = matches[choice]
            except (ValueError, IndexError):
                print("Invalid choice. Try again.")
                continue
        else:
            selected = matches[0]

        try:
            servings = float(input("Enter number of servings: "))
        except ValueError:
            print("Invalid number. Try again.")
            continue

       
        totals["Calories (kcal)"] += selected["calories"] * servings
        totals["Protein (g)"] += selected["protein"] * servings
        totals["Fat (g)"] += selected["fat"] * servings
        totals["Carbs (g)"] += selected["carbs"] * servings
        totals["Iron (mg)"] += selected["iron"] * servings
        totals["Vitamin C (mg)"] += selected["vitamin_c"] * servings

        print(f" Added {servings} serving(s) of {selected['food'].title()}!\n")

    
    print("\n===== DAILY NUTRITION SUMMARY =====")
    for nutrient, value in totals.items():
        print(f"{nutrient}: {value:.2f}")

    """
      health alerts 
       if totals["Vitamin C (mg)"] < 75:
       print("⚠️ Warning: Vitamin C intake is low today.")
       if totals["Iron (mg)"] < 18:
      print("⚠️ Warning: Iron intake is low today.")"""

   
    save_report(totals)

    print("\n Nutrition analysis completed!")


if __name__ == "__main__":
    main()