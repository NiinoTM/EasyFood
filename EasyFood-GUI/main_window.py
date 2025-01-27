from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QStackedWidget,
    QMenuBar, QMenu, QDialog, QTextBrowser, QPushButton
)
from PyQt6.QtGui import QAction, QFont
from src.modules.visualizacao import VisualizacaoManager
from src.modules.actions import ActionsManager
from src.modules.utils import create_table_page

class ReportDialog(QDialog):
    def __init__(self, content, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Relatório")
        self.setGeometry(200, 200, 800, 600)
        
        layout = QVBoxLayout()
        
        # Configure HTML display
        self.text_browser = QTextBrowser()
        self.text_browser.setFont(QFont("Arial", 10))
        self.text_browser.setHtml(content)
        
        # Close button
        close_btn = QPushButton("Fechar")
        close_btn.clicked.connect(self.accept)
        
        # Layout setup
        layout.addWidget(self.text_browser)
        layout.addWidget(close_btn)
        self.setLayout(layout)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("EasyFood - SGA")
        self.setGeometry(100, 100, 800, 600)
        
        # Initialize modules
        self.visualizacao_manager = VisualizacaoManager(self)
        self.actions_manager = ActionsManager(self)
        
        # Setup UI components
        self._setup_ui()

    def _setup_ui(self):
        # Central stacked widget setup
        self.central_stacked = QStackedWidget()
        self.setCentralWidget(self.central_stacked)
        
        # Create pages
        self._create_pages()
        
        # Create menu system
        self.menu_bar = QMenuBar()
        self.setMenuBar(self.menu_bar)
        self._create_menus()

    def _create_pages(self):
        # Create and add all pages
        self.blank_page = QWidget()
        self.foods_page = self._create_table_page("Alimentos")
        self.suppliers_page = self._create_table_page("Fornecedores")
        self.stock_entries_page = self._create_table_page("Entradas Estoque")
        self.stock_exits_page = self._create_table_page("Saídas Estoque")
        self.meals_page = self._create_table_page("Refeições")
        
        # Add pages to the stacked widget
        self.central_stacked.addWidget(self.blank_page)
        self.central_stacked.addWidget(self.foods_page)
        self.central_stacked.addWidget(self.suppliers_page)
        self.central_stacked.addWidget(self.stock_entries_page)
        self.central_stacked.addWidget(self.stock_exits_page)
        self.central_stacked.addWidget(self.meals_page)

    def _create_table_page(self, title):
        """Helper method to create a table page with a title"""
        page = QWidget()
        page.setLayout(QVBoxLayout())
        table = create_table_page()
        page.layout().addWidget(table)
        return page

    def _create_menus(self):
        # Alimentos Menu
        alimentos_menu = QMenu("Alimentos", self)
        alimentos_menu.addAction("Adicionar", self.actions_manager.add_food)
        alimentos_menu.addAction("Editar", self.actions_manager.edit_food)
        alimentos_menu.addAction("Remover", self.actions_manager.remove_food)
        alimentos_menu.addAction("Visualizar", lambda: self.visualizacao_manager.view_foods())
        self.menu_bar.addMenu(alimentos_menu)

        # Fornecedores Menu
        fornecedores_menu = QMenu("Fornecedores", self)
        fornecedores_menu.addAction("Adicionar", self.actions_manager.add_supplier)
        fornecedores_menu.addAction("Editar", self.actions_manager.edit_supplier)
        fornecedores_menu.addAction("Remover", self.actions_manager.remove_supplier)
        fornecedores_menu.addAction("Visualizar", lambda: self.visualizacao_manager.view_suppliers())
        self.menu_bar.addMenu(fornecedores_menu)

        # Estoque Menu
        estoque_menu = QMenu("Estoque", self)
        estoque_menu.addAction("Entrada", self.actions_manager.add_stock_entry)
        estoque_menu.addAction("Saída", self.actions_manager.add_stock_exit)
        estoque_menu.addAction("Editar", self.actions_manager.edit_stock)
        estoque_menu.addAction("Remover", self.actions_manager.remove_stock)
        estoque_menu.addAction("Visualizar Entradas", lambda: self.visualizacao_manager.view_stock_entries())
        estoque_menu.addAction("Visualizar Saídas", lambda: self.visualizacao_manager.view_stock_exits())
        self.menu_bar.addMenu(estoque_menu)

        # Refeições Menu
        refeicoes_menu = QMenu("Refeições", self)
        refeicoes_menu.addAction("Adicionar", self.actions_manager.add_meal)
        refeicoes_menu.addAction("Editar", self.actions_manager.edit_meal)
        refeicoes_menu.addAction("Remover", self.actions_manager.remove_meal)
        refeicoes_menu.addAction("Visualizar", lambda: self.visualizacao_manager.view_meals())
        self.menu_bar.addMenu(refeicoes_menu)

        # Relatórios Menu
        relatorios_menu = QMenu("Relatórios", self)
        relatorios_menu.addAction("Nutricional", self._show_nutrition_report)
        relatorios_menu.addAction("Financeiro", self._show_financial_report)
        relatorios_menu.addAction("Estoque", self._show_stock_report)
        self.menu_bar.addMenu(relatorios_menu)

        # Backups Menu
        backups_menu = QMenu("Backups", self)
        backups_menu.addAction("Criar Backup", self.actions_manager.create_backup)
        backups_menu.addAction("Listar Backups", self.actions_manager.list_backups)
        backups_menu.addAction("Restaurar Backup", self.actions_manager.restore_backup)
        self.menu_bar.addMenu(backups_menu)

    def _show_nutrition_report(self):
        content = self.actions_manager.relatorios_manager.generate_nutrition_report()
        self._show_report("Relatório Nutricional", content)

    def _show_financial_report(self):
        content = self.actions_manager.relatorios_manager.generate_financial_report()
        self._show_report("Relatório Financeiro", content)

    def _show_stock_report(self):
        content = self.actions_manager.relatorios_manager.generate_stock_report()
        self._show_report("Relatório de Estoque", content)

    def _show_report(self, title, content):
        dialog = ReportDialog(content, self)
        dialog.setWindowTitle(title)
        dialog.exec()

    def show_page(self, index: int):
        """Show the requested page in the stacked widget"""
        self.central_stacked.setCurrentIndex(index)