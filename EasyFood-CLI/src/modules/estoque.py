from src.modules.utils import *
from tabulate import tabulate

def manage_stock():
    while True:
        clear_screen()
        print("\nControle de Estoque")
        print("1. Registrar Entrada")
        print("2. Registrar Saída")
        print("3. Histórico")
        print("4. Voltar")
        
        choice = input("Escolha: ")
        
        if choice == '1':
            add_stock_entry()
        elif choice == '2':
            add_stock_exit()
        elif choice == '3':
            list_stock_movements()
        elif choice == '4':
            break
        else:
            print("Opção inválida.")

def add_stock_entry():
    foods = load_data('foods', Food)
    suppliers = load_data('suppliers', Supplier)
    
    if not foods or not suppliers:
        print("Cadastre alimentos e fornecedores primeiro!")
        return
    
    # Tabela de seleção com unidades incorporadas
    print("\nSelecione o alimento:")
    table_data = [
        [idx+1, food.name, f"{food.quantity_in_stock:.2f} {food.unit}"]
        for idx, food in enumerate(foods)
    ]
    print(tabulate(
        table_data, 
        headers=["#", "Alimento", "Estoque Atual"], 
        tablefmt="grid"
    ))
    
    food = select_from_list(foods, "Selecione o alimento: ")
    if not food:
        return
    
    supplier = select_from_list(suppliers, "Fornecedor: ")
    if not supplier:
        return
    
    # Quantidade e custo
    quantity = get_input(f"Quantidade ({food.unit}): ", validate_positive_number)
    cost = get_input("Custo total R$: ", validate_positive_number)
    date = get_input("Data (dd/mm/aaaa): ", validate_date, datetime.now().strftime('%d/%m/%Y'))
    
    # Converte para float
    quantity = format_decimal(quantity)
    cost = format_decimal(cost)
    
    # Registra a entrada
    entries = load_data('stock_entries', StockEntry)
    entries.append(StockEntry(
        food.name,
        quantity,
        food.unit,
        cost,
        date,
        supplier.name
    ))
    
    save_data(entries, 'stock_entries')
    print("\n✅ Entrada registrada!")

def add_stock_exit():
    foods = load_data('foods', Food)
    if not foods:
        print("Nenhum alimento cadastrado!")
        return
    
    # Tabela de seleção com unidades incorporadas
    print("\nSelecione o alimento:")
    table_data = [
        [idx+1, food.name, f"{food.quantity_in_stock:.2f} {food.unit}"]
        for idx, food in enumerate(foods)
    ]
    print(tabulate(
        table_data, 
        headers=["#", "Alimento", "Estoque Atual"], 
        tablefmt="grid"
    ))
    
    food = select_from_list(foods, "Selecione o alimento: ")
    if not food:
        return
    
    quantity = float(get_input(
        f"Quantidade utilizada ({food.unit}): ", 
        validate_positive_number
    ))
    reason = get_input("Motivo: ", lambda x: len(x) > 0)
    date = get_input("Data (dd/mm/aaaa): ", validate_date, datetime.now().strftime('%d/%m/%Y'))
    
    # Convert to base units
    converted_qty = quantity * BASE_UNITS[food.unit]
    if food.quantity_in_stock < converted_qty:
        print("❌ Estoque insuficiente!")
        return
    
    food.quantity_in_stock -= converted_qty
    exits = load_data('stock_exits', StockExit)
    exits.append(StockExit(
    food.name,
    quantity,
    food.unit,  # Movido para 3ª posição
    date,
    reason
    ))
    
    save_data(foods, 'foods')
    save_data(exits, 'stock_exits')
    print("\n✅ Saída registrada!")

def list_stock_movements():
    entries = load_data('stock_entries', StockEntry)
    exits = load_data('stock_exits', StockExit)
    
    print("\n=== ENTRADAS ===")
    entry_data = [
        [e.date, e.food_name, f"+{e.quantity} {e.unit}", f"R$ {e.cost}", e.supplier]
        for e in entries
    ]
    print(tabulate(
        entry_data,
        headers=["Data", "Alimento", "Quantidade", "Preço", "Fornecedor"],
        tablefmt="grid"
    ))
    
    print("\n=== SAÍDAS ===")
    exit_data = [
        [s.date, s.food_name, f"-{s.quantity} {s.unit}", s.reason]
        for s in exits
    ]
    print(tabulate(
        exit_data,
        headers=["Data", "Alimento", "Quantidade", "Motivo"],
        tablefmt="grid"
    ))
    
    input("\nPressione Enter para voltar...")