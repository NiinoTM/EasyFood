from tabulate import tabulate
from collections import defaultdict
from src.modules.utils import load_data, BASE_UNITS, Food, Meal, StockEntry

def get_food_cost_data():
    stock_entries = load_data('stock_entries', StockEntry)
    food_cost_data = defaultdict(list)
    
    for entry in stock_entries:
        quantity = entry.quantity * BASE_UNITS[entry.unit]
        if quantity > 0:
            food_cost_data[entry.food_name].append({
                'cost_per_unit': entry.cost / quantity,
                'quantity': quantity
            })
    return food_cost_data

def print_table(title, headers, data, table_style="grid"):
    print(f"\n{title}")
    print(tabulate(data, headers=headers, tablefmt=table_style))
    print()