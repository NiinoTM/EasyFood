# -*- coding: utf-8 -*-
from src.modules.utils import (
    Food, StockEntry, StockExit, Meal,
    load_data, save_data, get_input,
    select_from_list, clear_screen,
    validate_positive_number, 
    validate_non_negative_number, UNIDADES
)
from tabulate import tabulate 

def manage_foods():
    while True:
        clear_screen()
        print("\n🍎 Gerenciamento de Alimentos")
        print("1. Adicionar alimento")
        print("2. Editar alimento")
        print("3. Remover alimento")
        print("4. Listar alimentos")
        print("5. Voltar")
        
        choice = input("Escolha uma opção: ")
        
        if choice == '1':
            add_food()
        elif choice == '2':
            edit_food()
        elif choice == '3':
            remove_food()
        elif choice == '4':
            list_foods()
        elif choice == '5':
            break
        else:
            print("Opção inválida!")
        input("\nPressione Enter para continuar...")

def add_food():
    clear_screen()
    print("📥 Cadastro de Novo Alimento")
    
    # Validações específicas para texto
    name = get_input("Nome do alimento: ", lambda x: bool(x) and len(x.strip()) > 0)
    
    print("\nInforme os valores por porção:")
    
    # Validações para números
    unit = get_input(f"Unidade ({', '.join(UNIDADES)}): ", lambda x: x in UNIDADES)
    quantity_per_portion = float(get_input("Quantidade por porção: ", validate_positive_number, is_number=True))
    calories = float(get_input("Calorias por porção: ", validate_positive_number, is_number=True))
    proteins = float(get_input("Proteínas por porção (g): ", validate_positive_number, is_number=True))
    carbs = float(get_input("Carboidratos por porção (g): ", validate_positive_number, is_number=True))
    fats = float(get_input("Gorduras por porção (g): ", validate_positive_number, is_number=True))
    
    quantity_in_stock = float(get_input("\nQuantidade em estoque: ", lambda x: validate_non_negative_number(x) or x == '0', default='0'))
    min_stock = float(get_input("Estoque mínimo (0 para desativar): ", lambda x: validate_non_negative_number(x), default='0'))
    ideal_stock = float(get_input("Estoque ideal: ", validate_non_negative_number, default='0'))
    
    foods = load_data('foods', Food)
    foods.append(Food(
        name=name,
        unit=unit,
        quantity_in_stock=quantity_in_stock,
        quantity_per_portion=quantity_per_portion,
        calories=calories,
        proteins=proteins,
        carbs=carbs,
        fats=fats,
        min_stock=min_stock,
        ideal_stock=ideal_stock
    ))
    save_data(foods, 'foods')
    print("\n✅ Alimento cadastrado com sucesso!")

def edit_food():
    foods = load_data('foods', Food)
    if not foods:
        print("Nenhum alimento cadastrado!")
        return
    
    # Seleciona o alimento a editar
    food = select_from_list(foods, "Selecione o alimento para editar: ")
    if not food:
        return
    
    old_name = food.name
    print("\nDeixe em branco para manter o valor atual")

    # Nome do alimento
    new_name = get_input(
        f"Nome atual ({old_name}): ", 
        validation_func=lambda x: bool(x.strip()) if x else True,  # Valida apenas se não estiver vazio
        default=old_name
    )

    # Unidade de medida
    new_unit = get_input(
        f"Unidade ({food.unit}): ", 
        validation_func=lambda x: x in UNIDADES if x else True, 
        default=food.unit
    )
    
    # Estoque atual
    new_quantity = get_input(
        f"Estoque atual ({food.quantity_in_stock}): ", 
        validation_func=validate_non_negative_number, 
        default=str(food.quantity_in_stock), 
        is_number=True
    )
    
    # Quantidade por porção
    new_portion = get_input(
        f"Quantidade por porção ({food.quantity_per_portion}): ", 
        validation_func=validate_positive_number, 
        default=str(food.quantity_per_portion), 
        is_number=True
    )
    if new_name != old_name:
        entries = load_data('stock_entries', StockEntry)
        for entry in entries:
            if entry.food_name == old_name:
                entry.food_name = new_name
        save_data(entries, 'stock_entries')
        
        exits = load_data('stock_exits', StockExit)
        for exit in exits:
            if exit.food_name == old_name:
                exit.food_name = new_name
        save_data(exits, 'stock_exits')
        
        meals = load_data('meals', Meal)
        for meal in meals:
            for item in meal.foods:
                if item['food_name'] == old_name:
                    item['food_name'] = new_name
        save_data(meals, 'meals')
    
    food.name = new_name
    food.unit = new_unit
    food.quantity_in_stock = new_quantity
    food.quantity_per_portion = new_portion
    save_data(foods, 'foods')
    print("\n✅ Alimento e histórico atualizados!")

def remove_food():
    foods = load_data('foods', Food)
    if not foods:
        print("Nenhum alimento cadastrado!")
        return
    
    food = select_from_list(foods, "Selecione o alimento para remover: ")
    if not food:
        return
    
    confirm = input(f"Tem certeza que deseja remover {food.name}? (s/n): ").lower()
    if confirm == 's':
        foods.remove(food)
        
        entries = load_data('stock_entries', StockEntry)
        entries = [e for e in entries if e.food_name != food.name]
        save_data(entries, 'stock_entries')
        
        exits = load_data('stock_exits', StockExit)
        exits = [e for e in exits if e.food_name != food.name]
        save_data(exits, 'stock_exits')
        
        meals = load_data('meals', Meal)
        for meal in meals:
            meal.foods = [item for item in meal.foods if item['food_name'] != food.name]
        save_data(meals, 'meals')
        
        save_data(foods, 'foods')
        print("✅ Alimento e histórico removidos!")

def list_foods():
    foods = load_data('foods', Food)
    if not foods:
        print("Nenhum alimento cadastrado!")
        return
    
    table_data = []
    for food in foods:
        status = ""
        if food.min_stock > 0 and food.quantity_in_stock < food.min_stock:
            status = "🔴 BAIXO"
        elif food.quantity_in_stock < food.ideal_stock:
            status = "🟡 Ideal"
            
        table_data.append([
            food.name,  # Remova a conversão de encoding aqui
            f"{food.quantity_in_stock:.2f}{food.unit}",
            f"{food.quantity_per_portion:.2f}{food.unit}",
            f"{food.calories:.2f}kcal",
            f"{food.proteins:.2f}g",
            f"{food.carbs:.2f}g", 
            f"{food.fats:.2f}g",
            status
        ])
    
    headers = ["Nome", "Estoque", "Porção", "Calorias", "Proteínas", "Carboidr.", "Gorduras", "Status"]
    
    print("\n📋 Lista de Alimentos")
    print(tabulate(table_data, headers=headers, tablefmt="grid"))
    input("\nPressione Enter para voltar...")