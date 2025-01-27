import sys
from PyQt6.QtWidgets import QApplication
from main_window import MainWindow
import os
import json

def check_data_files():
    """Ensure the data directory and required JSON files exist."""
    data_dir = "data"
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)  # Create the data directory if it doesn't exist

    # List of required JSON files
    required_files = [
        'foods.json',
        'suppliers.json',
        'stock_entries.json',
        'stock_exits.json',
        'meals.json'
    ]

    # Create empty JSON files if they don't exist
    for file in required_files:
        file_path = os.path.join(data_dir, file)
        if not os.path.exists(file_path):
            with open(file_path, 'w') as f:
                f.write('[]')  # Initialize with an empty list

def main():
    # Ensure data files exist
    check_data_files()

    # Cria a aplicação
    app = QApplication(sys.argv)

    # Cria e exibe a janela principal
    window = MainWindow()
    window.show()

    # Executa a aplicação
    sys.exit(app.exec())

if __name__ == "__main__":
    main()