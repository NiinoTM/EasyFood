from .base import print_table, get_food_cost_data
from src.modules.utils import load_data, Meal, BASE_UNITS, StockEntry, Food
from collections import defaultdict


def generate_financial_report():
    foods = {f.name: f for f in load_data('foods', Food)}
    meals = load_data('meals', Meal)
    stock_entries = load_data('stock_entries', StockEntry)

    # Calcular custos médios por alimento
    food_cost_data = defaultdict(list)
    for entry in stock_entries:
        quantity = entry.quantity * BASE_UNITS[entry.unit]
        if quantity > 0:
            food_cost_data[entry.food_name].append({
                'cost_per_unit': entry.cost / quantity,
                'quantity': quantity
            })

    # Calcular custos detalhados por refeição
    meal_costs = {}
    print("\n💵 Relatório Financeiro Detalhado")

    for meal in meals:
        total_cost = 0.0
        meal_details = []
        
        for item in meal.foods:
            food = foods.get(item['food_name'])
            if not food or not food_cost_data.get(food.name):
                continue

            # Calcular média ponderada
            total_cost_spent = sum(e['cost_per_unit'] * e['quantity'] for e in food_cost_data[food.name])
            total_quantity = sum(e['quantity'] for e in food_cost_data[food.name])
            avg_cost = total_cost_spent / total_quantity if total_quantity > 0 else 0

            # Converter quantidade para unidade base
            required = item['quantity'] * BASE_UNITS[item['unit']]
            item_cost = avg_cost * required

            # Armazenar detalhes
            meal_details.append({
                'name': food.name,
                'quantity': f"{required/BASE_UNITS[food.unit]:.2f}{food.unit}",
                'cost': item_cost
            })
            total_cost += item_cost

        # Armazenar custo da refeição
        meal_costs[meal.name] = total_cost

        # Mostrar detalhes da refeição
        print(f"\n🍽 {meal.name}")
        for detail in meal_details:
            print(f"  - {detail['name']}: {detail['quantity']} (R$ {detail['cost']:.2f})")
        print(f"  TOTAL: R$ {total_cost:.2f}")

    # Calcular totais
    daily_total = sum(meal_costs.values())

    # Projeções
    print("\n\n📅 Projeção Diária:")
    for meal_name, cost in meal_costs.items():
        print(f"{meal_name}: R$ {cost:.2f}")
    print("========================")
    print(f"TOTAL DIÁRIO: R$ {daily_total:.2f}")

    print("\n🔄 Projeção Semanal (7 dias):")
    for meal_name, cost in meal_costs.items():
        print(f"{meal_name}: R$ {cost * 7:.2f}")
    print("========================")
    print(f"TOTAL SEMANAL: R$ {daily_total * 7:.2f}")

    print("\n📅 Projeção Mensal (30 dias):")
    for meal_name, cost in meal_costs.items():
        print(f"{meal_name}: R$ {cost * 30:.2f}")
    print("========================")
    print(f"TOTAL MENSAL: R$ {daily_total * 30:.2f}")

    input("\nPressione Enter para voltar...")