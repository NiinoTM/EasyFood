import json
import os
from datetime import datetime

# Caminhos dos arquivos JSON
DATA_FILES = {
    'foods': 'data/foods.json',
    'suppliers': 'data/suppliers.json',
    'stock_entries': 'data/stock_entries.json',
    'stock_exits': 'data/stock_exits.json',
    'meals': 'data/meals.json'
}

# ==================== CLASS DEFINITIONS ====================
class Food:
    def __init__(self, name, unit, quantity_in_stock, quantity_per_portion, calories, proteins, carbs, fats, min_stock=0, ideal_stock=0):
        self.name = name
        self.unit = unit
        self.quantity_in_stock = quantity_in_stock
        self.quantity_per_portion = quantity_per_portion
        self.calories = calories
        self.proteins = proteins
        self.carbs = carbs
        self.fats = fats
        self.min_stock = min_stock
        self.ideal_stock = ideal_stock

    def to_dict(self):
        return self.__dict__

class Supplier:
    def __init__(self, name, type, location):
        self.name = name
        self.type = type
        self.location = location

    def to_dict(self):
        return {
            'name': self.name,
            'type': self.type,
            'location': self.location
        }

class StockEntry:
    def __init__(self, food_name, quantity, unit, cost, date, supplier):
        self.food_name = food_name
        self.quantity = quantity
        self.unit = unit
        self.cost = cost
        self.date = date
        self.supplier = supplier

    def to_dict(self):
        return self.__dict__

class StockExit:
    def __init__(self, food_name, quantity, unit, date, reason):
        self.food_name = food_name
        self.quantity = quantity
        self.unit = unit
        self.date = date
        self.reason = reason

    def to_dict(self):
        return self.__dict__

class Meal:
    def __init__(self, name, foods):
        self.name = name
        self.foods = foods  # Lista de dicionários: {'food_name': str, 'quantity': float, 'unit': str}

    def to_dict(self):
        return {
            'name': self.name,
            'foods': self.foods
        }

# ==================== UTILITY FUNCTIONS ====================
def load_data(file_key, class_type):
    """
    Carrega dados de um arquivo JSON e retorna uma lista de objetos da classe especificada.
    """
    try:
        with open(DATA_FILES[file_key], 'r') as f:
            return [class_type(**item) for item in json.load(f)]
    except (FileNotFoundError, json.JSONDecodeError):
        return []  # Retorna uma lista vazia se o arquivo não existir ou estiver corrompido

def save_data(data, file_key):
    """
    Salva uma lista de objetos em um arquivo JSON.
    """
    with open(DATA_FILES[file_key], 'w') as f:
        json.dump([item.to_dict() for item in data], f, indent=2)