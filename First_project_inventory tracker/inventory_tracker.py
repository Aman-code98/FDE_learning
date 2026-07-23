# Restaurant Inventory Tracker
# Project 1 - Phase 1 - FDE Bootcamp

import json
import os
import sqlite3

# =====================
# DATABASE FUNCTIONS
# =====================

def setup_database():
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS inventory (
            name TEXT PRIMARY KEY,
            quantity INTEGER,
            unit TEXT,
            reorder_lvl INTEGER
        )
    """)
    conn.commit()
    conn.close()

def save_to_database(inventory):
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    for name, details in inventory.items():
        cursor.execute("""
            INSERT OR REPLACE INTO inventory 
            (name, quantity, unit, reorder_lvl)
            VALUES (?, ?, ?, ?)
        """, (name, details['quantity'], details['unit'], details['reorder_lvl']))
    conn.commit()
    conn.close()
    print("✅ Inventory saved to database.")

def load_from_database():
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM inventory')
    rows = cursor.fetchall()
    conn.close()
    if rows:
        inventory = {}
        for row in rows:
            name, quantity, unit, reorder_lvl = row
            inventory[name] = {
                'quantity': quantity,
                'unit': unit,
                'reorder_lvl': reorder_lvl
            }
        return inventory
    return None

# =====================
# FILE BACKUP FUNCTIONS
# =====================

def save_inventory(inventory):
    with open('inventory.json', 'w') as file:
        json.dump(inventory, file)

def load_inventory():
    if os.path.exists('inventory.json'):
        with open('inventory.json', 'r') as file:
            return json.load(file)
    return None

# =====================
# INVENTORY FUNCTIONS
# =====================

def add_ingredient(inventory, name, quantity, unit, reorder_lvl):
    if name in inventory:
        print(f"⚠️ {name} already exists in inventory.")
    else:
        inventory[name] = {
            'quantity': quantity,
            'unit': unit,
            'reorder_lvl': reorder_lvl
        }
        print(f"✅ {name} added successfully.")
    return inventory

def remove_ingredient(inventory, name):
    if name in inventory:
        del inventory[name]
        print(f"✅ {name} removed successfully.")
    else:
        print(f"⚠️ {name} not found in inventory.")
    return inventory

# =====================
# MENU DATA
# =====================

menu = [
    {'name': 'Burger', 'price': 8.99, 'category': 'Mains'},
    {'name': 'Fries', 'price': 3.49, 'category': 'Sides'},
    {'name': 'Coke', 'price': 2.49, 'category': 'Drinks'},
    {'name': 'Pizza', 'price': 11.99, 'category': 'Mains'},
    {'name': 'Salad', 'price': 6.99, 'category': 'Sides'}
]

# =====================
# DEFAULT INVENTORY
# =====================

default_inventory = {
    "tomatoes": {'quantity': 5, 'unit': 'kg', 'reorder_lvl': 10},
    "buns": {'quantity': 200, 'unit': 'pcs', 'reorder_lvl': 50},
    "lettuce": {'quantity': 0, 'unit': 'kg', 'reorder_lvl': 8},
    "cheese": {'quantity': 5, 'unit': 'kg', 'reorder_lvl': 10},
    "cola syrup": {'quantity': 2, 'unit': 'liters', 'reorder_lvl': 5}
}

# =====================
# COMMAND LINE INTERFACE
# =====================

def run_tracker(inventory):
    while True:
        print("\n=== RESTAURANT INVENTORY TRACKER ===")
        print("1. View inventory report")
        print("2. Add ingredient")
        print("3. Remove ingredient")
        print("4. Save and quit")

        choice = input("\nEnter your choice (1-4): ")

        if choice == "1":
            print("\n=== STOCK STATUS REPORT ===")
            for ingredient, details in inventory.items():
                quantity = details['quantity']
                reorder_lvl = details['reorder_lvl']
                unit = details['unit']
                if quantity == 0:
                    status = "🔴 CRITICAL - OUT OF STOCK"
                elif quantity < reorder_lvl:
                    status = "🟡 LOW - REORDER NEEDED"
                else:
                    status = "🟢 OK"
                print(f"{ingredient}: {quantity} {unit} — {status}")

        elif choice == "2":
            name = input("Enter ingredient name: ")
            quantity = int(input("Enter quantity: "))
            unit = input("Enter unit (kg, pcs, liters): ")
            reorder_lvl = int(input("Enter reorder level: "))
            inventory = add_ingredient(inventory, name, quantity, unit, reorder_lvl)

        elif choice == "3":
            name = input("Enter ingredient name to remove: ")
            inventory = remove_ingredient(inventory, name)

        elif choice == "4":
            save_to_database(inventory)
            save_inventory(inventory)
            print("Goodbye!")
            break

        else:
            print("❌ Invalid choice. Please enter 1, 2, 3 or 4.")

# =====================
# MAIN - START HERE
# =====================

setup_database()

inventory = load_from_database()
if inventory:
    print("✅ Loaded inventory from database.")
else:
    print("No saved data found. Using default inventory.")
    inventory = default_inventory

run_tracker(inventory)