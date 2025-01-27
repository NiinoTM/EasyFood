from src.modules.utils import load_data, Food, Meal, StockEntry, BASE_UNITS
from collections import defaultdict

class RelatoriosManager:
    def __init__(self):
        self.foods = load_data('foods', Food)
        self.meals = load_data('meals', Meal)
        self.stock_entries = load_data('stock_entries', StockEntry)

    def _generate_html_table(self, headers, data):
        table = """
    <table style='
        border-collapse: collapse;
        width: 100%;
        font-family: Arial, sans-serif;
        font-size: 14px;
        color: #000;
    '>
    """
    
        # Add table headers
        table += "<thead><tr>"
        for header in headers:
            table += f"""
            <th style='
                border: 1px solid #000;  /* Black border */
                padding: 12px;
                background-color: #4CAF50;
                color: white;
                text-align: left;
            '>{header}</th>
            """
        table += "</tr></thead>"
        
        # Add table rows
        table += "<tbody>"
        for i, row in enumerate(data):
            # Add a bold separator above the total row
            if i == len(data) - 1:  # Check if it's the last row (total row)
                table += "<tr style='border-top: 2px solid #000;'>"  # Bold black separator
            else:
                table += "<tr>"
            
            for cell in row:
                table += f"""
                <td style='
                    border: 1px solid #000;  /* Black border */
                    padding: 8px;
                    text-align: left;
                    background-color: #ede6e8;
                '>{cell}</td>
                """
            table += "</tr>"
        table += "</tbody></table>"
        
        return table

    def generate_nutrition_report(self):
        """Generate a professional nutrition report with HTML tables"""
        report = []
        meals = load_data('meals', Meal)
        foods = {f.name: f for f in load_data('foods', Food)}
        
        # Nutrition headers
        nutri_headers = ["Item", "Porção", "Calorias", "Proteínas", "Carboidratos", "Gorduras"]
        
        for meal in meals:
            table_data = []
            total = {'cal': 0.0, 'prot': 0.0, 'carb': 0.0, 'fat': 0.0}
            
            for item in meal.foods:
                food = foods.get(item['food_name'])
                if not food:
                    continue
                
                base_qty = item['quantity'] * BASE_UNITS[item['unit']]
                portions = base_qty / (food.quantity_per_portion * BASE_UNITS[food.unit])
                
                calories = portions * food.calories
                proteins = portions * food.proteins
                carbs = portions * food.carbs
                fats = portions * food.fats
                
                table_data.append([
                    food.name,
                    f"{base_qty/BASE_UNITS[food.unit]:.1f}{food.unit}",
                    f"{calories:.1f}",
                    f"{proteins:.1f}",
                    f"{carbs:.1f}",
                    f"{fats:.1f}"
                ])
                
                total['cal'] += calories
                total['prot'] += proteins
                total['carb'] += carbs
                total['fat'] += fats
            
            # Add total row
            table_data.append([
                "<b>TOTAL</b>",
                "",
                f"<b>{total['cal']:.1f}</b>",
                f"<b>{total['prot']:.1f}</b>",
                f"<b>{total['carb']:.1f}</b>",
                f"<b>{total['fat']:.1f}</b>"
            ])
            
            # Generate HTML table
            report.append(f"<h2 style='color: #4CAF50;'>🍽 {meal.name}</h2>")
            report.append(self._generate_html_table(nutri_headers, table_data))
        
        # Add projections
        report.append("<h2 style='color: #4CAF50;'>📅 Projeções</h2>")
        proj_headers = ["Refeição", "Frequência", "Calorias", "Proteínas", "Carboidratos", "Gorduras"]
        
        for days, period in [(1, "Diária"), (7, "Semanal"), (30, "Mensal")]:
            proj_data = []
            grand_total = {'cal': 0.0, 'prot': 0.0, 'carb': 0.0, 'fat': 0.0}
            
            for meal in meals:
                total = {'cal': 0.0, 'prot': 0.0, 'carb': 0.0, 'fat': 0.0}
                
                for item in meal.foods:
                    food = foods.get(item['food_name'])
                    if not food:
                        continue
                    
                    base_qty = item['quantity'] * BASE_UNITS[item['unit']]
                    portions = base_qty / (food.quantity_per_portion * BASE_UNITS[food.unit])
                    
                    total['cal'] += portions * food.calories
                    total['prot'] += portions * food.proteins
                    total['carb'] += portions * food.carbs
                    total['fat'] += portions * food.fats
                
                proj_data.append([
                    meal.name,
                    f"{days}x",
                    f"{total['cal'] * days:.1f}",
                    f"{total['prot'] * days:.1f}",
                    f"{total['carb'] * days:.1f}",
                    f"{total['fat'] * days:.1f}"
                ])
                
                grand_total['cal'] += total['cal'] * days
                grand_total['prot'] += total['prot'] * days
                grand_total['carb'] += total['carb'] * days
                grand_total['fat'] += total['fat'] * days
            
            # Add grand total row
            proj_data.append([
                "<b>TOTAL PROJETADO</b>",
                "",
                f"<b>{grand_total['cal']:.1f}</b>",
                f"<b>{grand_total['prot']:.1f}</b>",
                f"<b>{grand_total['carb']:.1f}</b>",
                f"<b>{grand_total['fat']:.1f}</b>"
            ])
            
            report.append(f"<h3>📅 Projeção {period} ({days} dias)</h3>")
            report.append(self._generate_html_table(proj_headers, proj_data))
        
        return "<br>".join(report)

    def generate_financial_report(self):
        """Generate a professional financial report with HTML tables"""
        report = ["<h2 style='color: #4CAF50;'>💵 RELATÓRIO FINANCEIRO 💵</h2>"]
        foods = {f.name: f for f in load_data('foods', Food)}
        meals = load_data('meals', Meal)
        stock_entries = load_data('stock_entries', StockEntry)
        
        # Calculate average costs
        food_cost_data = defaultdict(list)
        for entry in stock_entries:
            quantity = entry.quantity * BASE_UNITS[entry.unit]
            if quantity > 0:
                food_cost_data[entry.food_name].append(entry.cost / quantity)
        
        # Meal cost breakdown
        meal_costs = {}
        for meal in meals:
            total_cost = 0.0
            table_data = []
            
            for item in meal.foods:
                food = foods.get(item['food_name'])
                if not food or not food_cost_data.get(food.name):
                    continue
                
                avg_cost = sum(food_cost_data[food.name]) / len(food_cost_data[food.name])
                quantity = item['quantity'] * BASE_UNITS[item['unit']] / BASE_UNITS[food.unit]
                item_cost = avg_cost * quantity
                
                table_data.append([
                    food.name,
                    f"{quantity:.2f}{food.unit}",
                    f"R$ {avg_cost:.4f}",
                    f"R$ {item_cost:.2f}"
                ])
                total_cost += item_cost
            
            # Store meal cost for projections
            meal_costs[meal.name] = total_cost
            
            # Add total row
            table_data.append([
                "<b>TOTAL</b>",
                "",
                "",
                f"<b>R$ {total_cost:.2f}</b>"
            ])
            
            report.append(f"<h3>🍽 {meal.name}</h3>")
            report.append(self._generate_html_table(
                ["Item", "Quantidade", "Custo Unitário", "Custo Total"],
                table_data
            ))
        
        # Add projections
        report.append("<h2 style='color: #4CAF50;'>📅 Projeções Financeiras</h2>")
        proj_headers = ["Refeição", "Frequência", "Custo Total"]
        
        for days, period in [(1, "Diária"), (7, "Semanal"), (30, "Mensal")]:
            proj_data = []
            grand_total = 0.0
            
            for meal_name, cost in meal_costs.items():
                proj_data.append([
                    meal_name,
                    f"{days}x",
                    f"R$ {cost * days:.2f}"
                ])
                grand_total += cost * days
            
            # Add grand total row
            proj_data.append([
                "<b>TOTAL PROJETADO</b>",
                "",
                f"<b>R$ {grand_total:.2f}</b>"
            ])
            
            report.append(f"<h3>📅 Projeção {period} ({days} dias)</h3>")
            report.append(self._generate_html_table(proj_headers, proj_data))
        
        return "<br>".join(report)

    def generate_stock_report(self):
        """Generate a professional stock report with HTML tables"""
        report = ["<h2 style='color: #4CAF50;'>📦 RELATÓRIO DE ESTOQUE 📦</h2>"]
        foods = load_data('foods', Food)
        
        table_data = []
        for food in foods:
            if food.quantity_in_stock <= 0:
                continue  # Skip items with zero stock
            
            status = "✅ Adequado"
            if food.min_stock > 0 and food.quantity_in_stock < food.min_stock:
                status = "🔴 Crítico"
            elif food.quantity_in_stock < food.ideal_stock:
                status = "🟡 Atenção"
            
            table_data.append([
                food.name,
                f"{food.quantity_in_stock:.1f}{food.unit}",
                f"{food.min_stock:.1f}{food.unit}" if food.min_stock > 0 else "N/A",
                f"{food.ideal_stock:.1f}{food.unit}" if food.ideal_stock > 0 else "N/A",
                status
            ])
        
        report.append(self._generate_html_table(
            ["Item", "Estoque Atual", "Estoque Mínimo", "Estoque Ideal", "Status"],
            table_data
        ))
        report.append("<p><b>Legenda:</b> ✅ Adequado  🔴 Crítico  🟡 Atenção</p>")
        
        return "<br>".join(report)