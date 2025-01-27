from .base import print_table
from src.modules.utils import load_data, Food, Meal, BASE_UNITS

def generate_stock_report():
    foods = load_data('foods', Food)
    meals = load_data('meals', Meal)
    
    headers = ["Item", "Estoque Atual", "Consumo Diário", "Duração (dias)", "Status"]
    table_data = []
    
    for food in foods:
        # Pular alimentos com estoque zero
        if food.quantity_in_stock <= 0:
            continue
            
        daily_use = 0.0
        for meal in meals:
            for item in meal.foods:
                if item['food_name'] == food.name:
                    qty = item['quantity'] * BASE_UNITS[item['unit']] / BASE_UNITS[food.unit]
                    daily_use += qty
        
        status = "✅ Adequado"
        if food.min_stock > 0 and food.quantity_in_stock < food.min_stock:
            status = "🔴 Crítico"
        elif food.quantity_in_stock < food.ideal_stock:
            status = "🟡 Atenção"
            
        duration = food.quantity_in_stock / daily_use if daily_use > 0 else float('inf')
        
        table_data.append([
            food.name,
            f"{food.quantity_in_stock:.1f}{food.unit}",  # Formatado para 1 decimal
            f"{daily_use:.1f}{food.unit}/dia",
            f"{duration:.1f}" if duration != float('inf') else "∞",
            status
        ])
    
    print_table("📦 Análise de Estoque (Itens com Estoque)", headers, table_data)
    input("\nPressione Enter para voltar...")