from src.modules.utils import (
    Food, Meal, load_data, save_data,
    get_input, select_from_list, clear_screen,
    validate_positive_number, UNIDADES
)

def manage_meals():
    while True:
        clear_screen()
        print("\n🍽️ Gerenciamento de Refeições Padrão")
        print("1. Nova Refeição")
        print("2. Editar Refeição")
        print("3. Remover Refeição")
        print("4. Listar Refeições")
        print("5. Voltar")
        
        choice = input("Escolha uma opção: ")
        
        if choice == '1':
            add_meal()
        elif choice == '2':
            edit_meal()
        elif choice == '3':
            remove_meal()
        elif choice == '4':
            list_meals()
        elif choice == '5':
            break
        else:
            print("Opção inválida!")
        input("\nPressione Enter para continuar...")

def add_meal():
    foods = load_data('foods', Food)
    if not foods:
        print("Cadastre alimentos primeiro!")
        input("Pressione Enter para voltar...")
        return
    
    print("\n📥 Nova Refeição Padrão")
    name = get_input("Nome da refeição: ", lambda x: len(x) > 0)
    meal_foods = []
    
    while True:
        clear_screen()
        print(f"Composição de {name}:")
        for item in meal_foods:
            print(f"- {item['food_name']}: {item['quantity']}{item['unit']}")
        
        print("\n1. Adicionar alimento")
        print("2. Finalizar")
        op = input("Opção: ")
        
        if op == '1':
            food = select_from_list(foods, "Selecione o alimento: ")
            if not food:
                continue
            
            # Get the food's registered unit
            food_unit = food.unit
            
            # Ask for quantity using the food's native unit
            quantity = float(get_input(
                f"Quantidade ({food_unit}): ", 
                validate_positive_number
            ))
            
            meal_foods.append({
                'food_name': food.name,
                'quantity': quantity,
                'unit': food_unit  # Use the food's registered unit
            })
            
        elif op == '2':
            break
        else:
            print("Opção inválida!")
    
    meals = load_data('meals', Meal)
    meals.append(Meal(name, meal_foods))
    save_data(meals, 'meals')
    print("\n✅ Refeição padrão cadastrada!")
    input("Pressione Enter para continuar...")

def edit_meal():
    meals = load_data('meals', Meal)
    foods = load_data('foods', Food)
    
    if not meals:
        print("Nenhuma refeição cadastrada!")
        input("Pressione Enter para voltar...")
        return
    
    meal = select_from_list(meals, "Selecione a refeição para editar: ")
    if not meal:
        return
    
    print("\nDeixe em branco para manter o valor atual")
    new_name = get_input(f"Nome atual ({meal.name}): ", default=meal.name)
    
    # Editar alimentos
    while True:
        clear_screen()
        print(f"\n📝 Editando: {new_name}")
        print("Composição atual:")
        for i, item in enumerate(meal.foods, 1):
            print(f"{i}. {item['food_name']} - {item['quantity']}{item['unit']}")
            
        print("\n1. Adicionar alimento")
        print("2. Editar alimento")
        print("3. Remover alimento")
        print("4. Finalizar")
        op = input("Opção: ")
        
        if op == '1':
            food = select_from_list(foods, "Selecione o alimento: ")
            if food:
                quantity = float(get_input("Quantidade: ", validate_positive_number))
                unit = get_input(f"Unidade ({', '.join(UNIDADES)}): ", lambda x: x in UNIDADES)
                meal.foods.append({
                    'food_name': food.name,
                    'quantity': quantity,
                    'unit': unit
                })
                
        elif op == '2':
            if not meal.foods:
                print("Nenhum alimento para editar!")
                continue
                
            idx = int(get_input("Número do alimento para editar: ", 
                              lambda x: x.isdigit() and 0 < int(x) <= len(meal.foods))) - 1
            item = meal.foods[idx]
            
            new_quantity = float(get_input(f"Quantidade atual ({item['quantity']}): ",
                                         validate_positive_number,
                                         default=str(item['quantity'])))
            new_unit = get_input(f"Unidade atual ({item['unit']}): ",
                                lambda x: x in UNIDADES,
                                default=item['unit'])
            
            meal.foods[idx] = {
                'food_name': item['food_name'],
                'quantity': new_quantity,
                'unit': new_unit
            }
            
        elif op == '3':
            if not meal.foods:
                print("Nenhum alimento para remover!")
                continue
                
            idx = int(get_input("Número do alimento para remover: ",
                              lambda x: x.isdigit() and 0 < int(x) <= len(meal.foods))) - 1
            del meal.foods[idx]
            
        elif op == '4':
            break
            
        else:
            print("Opção inválida!")
    
    meal.name = new_name
    save_data(meals, 'meals')
    print("\n✅ Refeição atualizada!")
    input("Pressione Enter para continuar...")

def remove_meal():
    meals = load_data('meals', Meal)
    if not meals:
        print("Nenhuma refeição cadastrada!")
        input("Pressione Enter para voltar...")
        return
    
    meal = select_from_list(meals, "Selecione a refeição para remover: ")
    if not meal:
        return
    
    confirm = input(f"Tem certeza que deseja remover {meal.name}? (s/n): ").lower()
    if confirm == 's':
        meals.remove(meal)
        save_data(meals, 'meals')
        print("✅ Refeição removida!")
    input("Pressione Enter para voltar...")

def list_meals():
    meals = load_data('meals', Meal)
    if not meals:
        print("Nenhuma refeição cadastrada!")
        input("Pressione Enter para voltar...")
        return
    
    print("\n📋 Refeições Padrão:")
    for meal in meals:
        print(f"\n🔸 {meal.name}")
        for item in meal.foods:
            print(f"  - {item['food_name']}: {item['quantity']}{item['unit']}")
    input("\nPressione Enter para voltar...")