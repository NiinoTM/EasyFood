from src.modules.utils import clear_screen
from .reports import (
    generate_nutrition_report,
    generate_financial_report,
    generate_stock_report
)

def generate_reports():
    while True:
        clear_screen()
        print("\n📊 Relatórios")
        print("1. Nutricional Diário")
        print("2. Consumo de Estoque")
        print("3. Financeiro")
        print("4. Voltar")
        
        choice = input("Escolha uma opção: ").strip()
        
        if choice == '1':
            generate_nutrition_report()
        elif choice == '2':
            generate_stock_report()
        elif choice == '3':
            generate_financial_report()
        elif choice == '4':
            break
        else:
            print("Opção inválida!")
            input("Pressione Enter para continuar...")