from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView, QVBoxLayout, QTextEdit, QPushButton, QDialog
from src.modules.utils import load_data, Food, Supplier, StockEntry, StockExit, Meal

class ReportDialog(QDialog):
    def __init__(self, content, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Relatório")
        self.setGeometry(200, 200, 800, 600)
        
        layout = QVBoxLayout()
        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        self.text_edit.setPlainText(content)
        
        close_btn = QPushButton("Fechar")
        close_btn.clicked.connect(self.accept)
        
        layout.addWidget(self.text_edit)
        layout.addWidget(close_btn)
        self.setLayout(layout)

class VisualizacaoManager:
    def __init__(self, main_window):
        self.main_window = main_window

    def view_foods(self):
        """Populates the foods page with a table of foods."""
        # Load the foods data
        foods = load_data('foods', Food)
        
        # Define the table headers
        headers = ["Name", "Unit", "Quantity in Stock", "Calories", "Proteins", "Carbs", "Fats"]
        
        # Prepare the data for the table
        data = []
        for food in foods:
            data.append([
                food.name,
                food.unit,
                str(food.quantity_in_stock),
                str(food.calories),
                str(food.proteins),
                str(food.carbs),
                str(food.fats)
            ])
        
        # Get the table widget from the foods page
        table = self.main_window.foods_page.layout().itemAt(0).widget()
        
        # Update the table with the headers and data
        self.update_table(table, headers, data)
        
        # Show the foods page
        self.main_window.show_page(1)  # Assuming foods_page is at index 1

    def view_suppliers(self):
        """Populates the suppliers page with a table of suppliers."""
        # Load the suppliers data
        suppliers = load_data('suppliers', Supplier)
        
        # Define the table headers
        headers = ["Name", "Type", "Location"]
        
        # Prepare the data for the table
        data = []
        for supplier in suppliers:
            data.append([
                supplier.name,
                supplier.type,
                supplier.location
            ])
        
        # Get the table widget from the suppliers page
        table = self.main_window.suppliers_page.layout().itemAt(0).widget()
        
        # Update the table with the headers and data
        self.update_table(table, headers, data)
        
        # Show the suppliers page
        self.main_window.show_page(2)  # Assuming suppliers_page is at index 2

    def view_stock_entries(self):
        """Populates the stock entries page with a table of stock entries."""
        # Load the stock entries data
        stock_entries = load_data('stock_entries', StockEntry)
        
        # Define the table headers
        headers = ["Food Name", "Quantity", "Unit", "Cost", "Date", "Supplier"]
        
        # Prepare the data for the table
        data = []
        for entry in stock_entries:
            data.append([
                entry.food_name,
                str(entry.quantity),
                entry.unit,
                str(entry.cost),
                entry.date,
                entry.supplier
            ])
        
        # Get the table widget from the stock entries page
        table = self.main_window.stock_entries_page.layout().itemAt(0).widget()
        
        # Update the table with the headers and data
        self.update_table(table, headers, data)
        
        # Show the stock entries page
        self.main_window.show_page(3)  # Assuming stock_entries_page is at index 3

    def view_stock_exits(self):
        """Populates the stock exits page with a table of stock exits."""
        # Load the stock exits data
        stock_exits = load_data('stock_exits', StockExit)
        
        # Define the table headers
        headers = ["Food Name", "Quantity", "Unit", "Date", "Reason"]
        
        # Prepare the data for the table
        data = []
        for exit in stock_exits:
            data.append([
                exit.food_name,
                str(exit.quantity),
                exit.unit,
                exit.date,
                exit.reason
            ])
        
        # Get the table widget from the stock exits page
        table = self.main_window.stock_exits_page.layout().itemAt(0).widget()
        
        # Update the table with the headers and data
        self.update_table(table, headers, data)
        
        # Show the stock exits page
        self.main_window.show_page(4)  # Assuming stock_exits_page is at index 4

    def view_meals(self):
        """Populates the meals page with a table of meals."""
        # Load the meals data
        meals = load_data('meals', Meal)
        
        # Define the table headers
        headers = ["Meal Name", "Foods"]
        
        # Prepare the data for the table
        data = []
        for meal in meals:
            foods_str = ", ".join([f"{food['food_name']} ({food['quantity']}{food['unit']})" for food in meal.foods])
            data.append([
                meal.name,
                foods_str
            ])
        
        # Get the table widget from the meals page
        table = self.main_window.meals_page.layout().itemAt(0).widget()
        
        # Update the table with the headers and data
        self.update_table(table, headers, data)
        
        # Show the meals page
        self.main_window.show_page(5)  # Assuming meals_page is at index 5

    def update_table(self, table, headers, data):
        """Updates a QTableWidget with the provided headers and data."""
        table.setRowCount(len(data))
        table.setColumnCount(len(headers))
        table.setHorizontalHeaderLabels(headers)
        
        for row_idx, row_data in enumerate(data):
            for col_idx, cell_data in enumerate(row_data):
                table.setItem(row_idx, col_idx, QTableWidgetItem(cell_data))
        
        table.resizeColumnsToContents()