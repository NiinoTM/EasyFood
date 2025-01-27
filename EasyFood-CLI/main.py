# -*- coding: utf-8 -*-
from src.modules.backup_manager import backup_manager
from src.modules import alimentos, fornecedores, estoque, refeicoes, relatorios
from src.modules.utils import clear_screen, load_data, Food, Supplier, StockEntry, Meal
import os

def check_data_files():
    data_dir = "data"
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    
    required_files = [
        'foods.json',
        'suppliers.json',
        'stock_entries.json',
        'stock_exits.json',
        'meals.json'
    ]
    
    for file in required_files:
        path = os.path.join(data_dir, file)
        if not os.path.exists(path):
            with open(path, 'w') as f:
                f.write('[]')


def main():
    check_data_files()
    backup_manager.create_backup()  # Backup inicial ao iniciar
    
    while True:
        clear_screen()
        foods = load_data('foods', Food)
        suppliers = load_data('suppliers', Supplier)
        stock_entries = load_data('stock_entries', StockEntry)
        meals = load_data('meals', Meal)
        
        menu_options = []
        
        # Sempre mostra Alimentos
        menu_options.append("1. Alimentos")
        
        # Fornecedores só aparece se tiver alimentos
        if len(foods) > 0:
            menu_options.append("2. Fornecedores")
        
        # Estoque e Refeições só aparecem se tiver fornecedores
        if len(suppliers) > 0:
            menu_options.append("3. Estoque")
            menu_options.append("4. Refeições")
        
        # Relatórios só aparece se tiver todos os requisitos
        if len(foods) > 0 and len(suppliers) > 0 and len(stock_entries) > 0 and len(meals) > 0:
            menu_options.append("5. Relatórios")
        
        # Opções fixas no final
        menu_options.append("6. Sair")
        menu_options.append("7. Restaurar Backup")  # Nova opção sempre visível

        print("""
        🍽️  EasyFood - SGA
              
            Sistema de Gestão Alimentícia
        --------------------------------------""")
        print("\n".join(menu_options))
        
        op = input("\n Opção: ").strip()
        
        try:
            if op == '1':
                alimentos.manage_foods()
            elif op == '2':
                fornecedores.manage_suppliers()
            elif op == '3':
                estoque.manage_stock()
            elif op == '4':
                refeicoes.manage_meals()
            elif op == '5':
                relatorios.generate_reports()
            elif op == '6':
                print("\nAté logo! 👋")
                break
            elif op == '7':  # Novo caso para restauração
                backup_manager.restore_backup()
            else:
                print("Opção inválida!")
        except Exception as e:
            print(f"Erro: {str(e)}")
        input("\nPressione Enter para continuar...")

if __name__ == "__main__":
    main()