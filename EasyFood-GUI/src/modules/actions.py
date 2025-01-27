from PyQt6.QtWidgets import QMessageBox, QInputDialog
from src.modules.alimentos import AlimentosManager
from src.modules.fornecedores import FornecedoresManager
from src.modules.estoque import EstoqueManager
from src.modules.refeicoes import RefeicoesManager
from src.modules.relatorios import RelatoriosManager
from src.modules.backup_manager import backup_manager

class ActionsManager:
    def __init__(self, main_window):
        self.main_window = main_window
        self.alimentos_manager = AlimentosManager()  # Criar o AlimentosManager
        self.fornecedores_manager = FornecedoresManager()
        self.estoque_manager = EstoqueManager(self.alimentos_manager)  # Passar o AlimentosManager
        self.refeicoes_manager = RefeicoesManager()
        self.relatorios_manager = RelatoriosManager()

    # Existing food management methods
    def add_food(self):
        self.alimentos_manager.add_food()

    def edit_food(self):
        self.alimentos_manager.edit_food()

    def remove_food(self):
        self.alimentos_manager.remove_food()

    # Existing supplier management methods
    def add_supplier(self):
        self.fornecedores_manager.add_supplier()

    def edit_supplier(self):
        self.fornecedores_manager.edit_supplier()

    def remove_supplier(self):
        self.fornecedores_manager.remove_supplier()

    # Existing stock management methods
    def add_stock_entry(self):
        self.estoque_manager.add_stock_entry()

    def add_stock_exit(self):
        self.estoque_manager.add_stock_exit()

    def edit_stock(self):
        self.estoque_manager.edit_stock()

    def remove_stock(self):
        self.estoque_manager.remove_stock()

    # Existing meal management methods
    def add_meal(self):
        self.refeicoes_manager.add_meal()

    def edit_meal(self):
        self.refeicoes_manager.edit_meal()

    def remove_meal(self):
        self.refeicoes_manager.remove_meal()

    # Backup management methods
    def create_backup(self):
        success = backup_manager.create_backup()
        if success:
            QMessageBox.information(self.main_window, "Backup", "Backup criado com sucesso!")
        else:
            QMessageBox.warning(self.main_window, "Erro", "Falha ao criar backup!")

    def list_backups(self):
        backups = backup_manager.list_backups()
        if backups:
            QMessageBox.information(self.main_window, "Backups Disponíveis", "\n".join(backups))
        else:
            QMessageBox.warning(self.main_window, "Backups", "Nenhum backup disponível!")

    def restore_backup(self):
        backups = backup_manager.list_backups()
        if not backups:
            QMessageBox.warning(self.main_window, "Backups", "Nenhum backup disponível!")
            return

        backup_name, ok = QInputDialog.getItem(
            self.main_window, "Restaurar Backup", "Selecione o backup:",
            backups, 0, False
        )
        if ok and backup_name:
            success, message = backup_manager.restore_backup(backup_name)
            if success:
                QMessageBox.information(self.main_window, "Sucesso", message)
            else:
                QMessageBox.warning(self.main_window, "Erro", message)

    # Report generation methods
    def generate_nutrition_report(self):
        return self.relatorios_manager.generate_nutrition_report()

    def generate_financial_report(self):
        return self.relatorios_manager.generate_financial_report()

    def generate_stock_report(self):
        return self.relatorios_manager.generate_stock_report()
    
    def remove_stock(self):
        """Remove uma entrada ou saída de estoque."""
        self.estoque_manager.remove_stock()