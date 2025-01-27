# src/modules/fornecedores.py
from src.modules.utils import (
    Supplier, StockEntry,
    load_data, save_data, get_input,
    select_from_list, clear_screen, TIPOS_FORNECEDORES
)

def manage_suppliers():
    while True:
        clear_screen()
        print("\n🏭 Gerenciamento de Fornecedores")
        print("1. Adicionar fornecedor")
        print("2. Editar fornecedor")
        print("3. Remover fornecedor")
        print("4. Listar fornecedores")
        print("5. Voltar")
        
        choice = input("Escolha uma opção: ")
        
        if choice == '1':
            add_supplier()
        elif choice == '2':
            edit_supplier()
        elif choice == '3':
            remove_supplier()
        elif choice == '4':
            list_suppliers()
        elif choice == '5':
            break
        else:
            print("Opção inválida!")
        input("\nPressione Enter para continuar...")

def add_supplier():
    clear_screen()
    print("📥 Cadastro de Novo Fornecedor")
    
    name = get_input("Nome do fornecedor: ", lambda x: len(x) > 0)
    type_ = get_input(f"Tipo ({', '.join(TIPOS_FORNECEDORES)}): ", lambda x: x in TIPOS_FORNECEDORES)
    location = get_input("Localização (ex: Av. Principal, 123): ", lambda x: len(x) > 0)

    suppliers = load_data('suppliers', Supplier)
    suppliers.append(Supplier(name, type_, location))
    save_data(suppliers, 'suppliers')
    print("\n✅ Fornecedor cadastrado com sucesso!")

def edit_supplier():
    suppliers = load_data('suppliers', Supplier)
    if not suppliers:
        print("Nenhum fornecedor cadastrado!")
        return
    
    supplier = select_from_list(suppliers, "Selecione o fornecedor para editar: ")
    if not supplier:
        return
    
    old_name = supplier.name
    print("\nDeixe em branco para manter o valor atual")
    new_name = get_input(f"Nome atual ({old_name}): ", default=old_name)
    new_type = get_input(f"Tipo ({supplier.type}): ", lambda x: x in TIPOS_FORNECEDORES, default=supplier.type)
    new_location = get_input(f"Localização atual ({supplier.location}): ", default=supplier.location)
    
    if new_name != old_name:
        # Atualizar histórico de entradas
        entries = load_data('stock_entries', StockEntry)
        for entry in entries:
            if entry.supplier == old_name:
                entry.supplier = new_name
        save_data(entries, 'stock_entries')
    
    supplier.name = new_name
    supplier.type = new_type
    supplier.location = new_location
    save_data(suppliers, 'suppliers')
    print("\n✅ Fornecedor atualizado!")

def remove_supplier():
    suppliers = load_data('suppliers', Supplier)
    if not suppliers:
        print("Nenhum fornecedor cadastrado!")
        return
    
    supplier = select_from_list(suppliers, "Selecione o fornecedor para remover: ")
    if not supplier:
        return
    
    confirm = input(f"Tem certeza que deseja remover {supplier.name}? (s/n): ").lower()
    if confirm == 's':
        suppliers.remove(supplier)
        save_data(suppliers, 'suppliers')
        print("✅ Fornecedor removido!")

def list_suppliers():
    suppliers = load_data('suppliers', Supplier)
    if not suppliers:
        print("Nenhum fornecedor cadastrado!")
        return
    
    print("\n📋 Lista de Fornecedores:")
    for supplier in suppliers:
        print(f"""
Nome: {supplier.name}
Tipo: {supplier.type}
Localização: {supplier.location}
{'-'*40}""")
    input("\nPressione Enter para voltar...")