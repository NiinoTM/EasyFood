from .base import print_table
from src.modules.utils import load_data, Food, Meal, BASE_UNITS

def generate_nutrition_report():
    meals = load_data('meals', Meal)
    foods = {f.name: f for f in load_data('foods', Food)}
    
    # Nutrition headers
    nutri_headers = ["Item", "Porção", "Calorias", "Proteínas", "Carboidratos", "Gorduras"]
    meal_totals = {}

    for meal in meals:
        table_data = []
        total = {'cal': 0.0, 'prot': 0.0, 'carb': 0.0, 'fat': 0.0}
        
        for item in meal.foods:
            food = foods.get(item['food_name'])
            if not food:
                continue

            base_qty = item['quantity'] * BASE_UNITS[item['unit']]
            portions = base_qty / (food.quantity_per_portion * BASE_UNITS[food.unit])
            
            # Calcular valores como floats primeiro
            calories = round(portions * food.calories, 1)
            proteins = round(portions * food.proteins, 1)
            carbs = round(portions * food.carbs, 1)
            fats = round(portions * food.fats, 1)
            
            row = [
                food.name,
                f"{base_qty/BASE_UNITS[food.unit]:.1f}{food.unit}",
                calories,  # Manter como float para cálculos
                proteins,
                carbs,
                fats
            ]
            table_data.append(row)
            
            # Acumular totais com floats
            total['cal'] += calories
            total['prot'] += proteins
            total['carb'] += carbs
            total['fat'] += fats

        # Formatar valores apenas para exibição
        formatted_data = [
            [
                row[0], 
                row[1], 
                f"{row[2]:.1f}", 
                f"{row[3]:.1f}", 
                f"{row[4]:.1f}", 
                f"{row[5]:.1f}"
            ] 
            for row in table_data
        ]
        
        # Adicionar linha de total formatada
        formatted_data.append([
            "TOTAL", 
            "", 
            f"{total['cal']:.1f}", 
            f"{total['prot']:.1f}", 
            f"{total['carb']:.1f}", 
            f"{total['fat']:.1f}"
        ])
        
        print_table(f"🍽 {meal.name}", nutri_headers, formatted_data)
        meal_totals[meal.name] = total

    # Projections
    proj_headers = ["Refeição", "Frequência", "Calorias", "Proteínas", "Carboidratos", "Gorduras"]
    
    for days, period in [(1, "Diária"), (7, "Semanal"), (30, "Mensal")]:
        proj_data = []
        grand_total = {'cal': 0.0, 'prot': 0.0, 'carb': 0.0, 'fat': 0.0}
        
        for meal_name, totals in meal_totals.items():
            row = [
                meal_name,
                f"{days}x",
                totals['cal'] * days,
                totals['prot'] * days,
                totals['carb'] * days,
                totals['fat'] * days
            ]
            proj_data.append(row)
            grand_total['cal'] += row[2]
            grand_total['prot'] += row[3]
            grand_total['carb'] += row[4]
            grand_total['fat'] += row[5]
        
        proj_data.append([
            "TOTAL PROJETADO",
            "",
            grand_total['cal'],
            grand_total['prot'],
            grand_total['carb'],
            grand_total['fat']
        ])
        
        print_table(f"📅 Projeção {period} ({days} dias)", proj_headers, proj_data)

    input("\nPressione Enter para voltar...")