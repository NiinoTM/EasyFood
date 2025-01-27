# src/modules/utils.py
import os
import json
from datetime import datetime
from collections import defaultdict
from difflib import get_close_matches
import unicodedata

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
    
    def normalize_name(self):
        return unicodedata.normalize('NFD', self.name).encode('ascii', 'ignore').decode('ascii').lower()

class Supplier:
    def __init__(self, name, type, location):
        self.name = name
        self.type = type
        self.location = location  # Alterado para localização

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


# ==================== CONSTANTS ====================
UNIDADES = ['g', 'kg', 'unidades', 'litros', 'ml']
TIPOS_FORNECEDORES = ['mercado', 'padaria', 'açougue', 'outro']
BASE_UNITS = {'g': 1, 'kg': 1000, 'ml': 1, 'litros': 1000, 'unidades': 1}
DATA_FILES = {
    'foods': 'data/foods.json',
    'suppliers': 'data/suppliers.json',
    'stock_entries': 'data/stock_entries.json',
    'stock_exits': 'data/stock_exits.json',
    'meals': 'data/meals.json'
}

# ==================== UTILITY FUNCTIONS ====================
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def load_data(file_key, class_type):
    try:
        with open(DATA_FILES[file_key], 'r') as f:
            return [class_type(**item) for item in json.load(f)]
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_data(data, file_key):
    with open(DATA_FILES[file_key], 'w') as f:
        json.dump([item.to_dict() for item in data], f, indent=2)

def validate_positive_number(value):
    """Valida se o valor é um número positivo"""
    value = format_decimal(value)
    return value is not None and value > 0
    
def validate_non_negative_number(value):
    try:
        num = float(value)
        return num >= 0  # Allow zero and positive numbers
    except ValueError:
        return False

def validate_date(date_str):
    try:
        datetime.strptime(date_str, '%d/%m/%Y')
        return True
    except ValueError:
        return False

def get_input(prompt, validation_func=None, default=None, is_number=False):
    while True:
        value = input(prompt).strip()
        
        # Retorna o valor padrão, se fornecido, quando a entrada está vazia
        if not value and default is not None:
            return default
        
        # Processa números somente se for necessário
        if is_number:
            try:
                value = format_decimal(value)  # Tenta converter para número
            except ValueError:
                print("Erro: Insira um valor numérico válido.")
                continue
        
        # Valida o valor (formatado ou não)
        if validation_func:
            if validation_func(value):
                return value
            else:
                print("Entrada inválida. Tente novamente.")
        else:
            # Sem função de validação, retorna o valor diretamente
            return value
        
def format_decimal(value):
    """Converte vírgulas em pontos e valida números decimais"""
    if isinstance(value, str):
        value = value.replace(",", ".")  # Substitui vírgula por ponto
    try:
        return float(value)
    except ValueError:
        return None
    
def select_from_list(items, prompt, min_confidence=0.6):
    """Interactively search for items, handling special characters"""
    current_matches = items.copy()
    
    while True:
        # Show current matches
        if current_matches:
            print("\nItens encontrados:")
            for i, item in enumerate(current_matches, 1):
                print(f"{i}. {item.name}")
            
            # Auto-select if only one match
            if len(current_matches) == 1:
                print(f"\nItem único encontrado: {current_matches[0].name}")
                return current_matches[0]
        else:
            print("\nNenhum item encontrado. Tente novamente.")
            current_matches = items.copy()
        
        # Get user input
        user_input = input(f"\n{prompt} (digite o número, novo termo, ou 'sair'): ").strip().lower()
        
        # Handle number selection
        if user_input.isdigit():
            index = int(user_input) - 1
            if 0 <= index < len(current_matches):
                return current_matches[index]
            print("Número inválido. Tente novamente.")
            continue
        
        # Handle search term
        if user_input and user_input != 'sair':
            # Normalize both input and food names
            normalized_input = unicodedata.normalize('NFD', user_input)\
                .encode('ascii', 'ignore').decode('ascii')
            
            current_matches = [
                item for item in current_matches
                if normalized_input in unicodedata.normalize('NFD', item.name)
                .encode('ascii', 'ignore').decode('ascii').lower()
            ]
        elif user_input == 'sair':
            return None

        # Handle empty input
        else:
            print("Entrada inválida. Tente novamente.")