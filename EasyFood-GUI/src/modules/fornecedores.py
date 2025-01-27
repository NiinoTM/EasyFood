import json
from src.modules.utils import Food, Supplier, StockEntry, StockExit, Meal, load_data, save_data

class FornecedoresManager:
    def __init__(self):
        self.suppliers = load_data('suppliers', Supplier)  # Carrega os fornecedores do arquivo JSON

    def add_supplier(self):
        """Adiciona um novo fornecedor."""
        from PyQt6.QtWidgets import QInputDialog, QMessageBox

        # Solicita os dados do fornecedor
        name, ok = QInputDialog.getText(None, "Adicionar Fornecedor", "Nome do fornecedor:")
        if not ok or not name:
            return

        type_, ok = QInputDialog.getItem(
            None, "Tipo de Fornecedor", "Selecione o tipo:",
            ["mercado", "padaria", "açougue", "outro"], 0, False
        )
        if not ok:
            return

        location, ok = QInputDialog.getText(None, "Localização", "Localização do fornecedor:")
        if not ok or not location:
            return

        # Cria o novo fornecedor
        new_supplier = Supplier(
            name=name,
            type=type_,
            location=location
        )

        # Adiciona o fornecedor à lista
        self.suppliers.append(new_supplier)
        save_data(self.suppliers, 'suppliers')  # Salva no arquivo JSON

        QMessageBox.information(None, "Sucesso", "Fornecedor adicionado com sucesso!")

    def edit_supplier(self):
        """Edita um fornecedor existente."""
        from PyQt6.QtWidgets import QInputDialog, QMessageBox

        if not self.suppliers:
            QMessageBox.warning(None, "Aviso", "Nenhum fornecedor cadastrado!")
            return

        # Lista os fornecedores para seleção
        supplier_names = [supplier.name for supplier in self.suppliers]
        supplier_name, ok = QInputDialog.getItem(
            None, "Editar Fornecedor", "Selecione o fornecedor:",
            supplier_names, 0, False
        )
        if not ok:
            return

        # Encontra o fornecedor selecionado
        supplier = next((s for s in self.suppliers if s.name == supplier_name), None)
        if not supplier:
            QMessageBox.warning(None, "Erro", "Fornecedor não encontrado!")
            return

        # Solicita os novos dados
        new_name, ok = QInputDialog.getText(
            None, "Editar Fornecedor", "Novo nome:",
            text=supplier.name
        )
        if ok and new_name:
            supplier.name = new_name

        new_type, ok = QInputDialog.getItem(
            None, "Editar Tipo", "Novo tipo:",
            ["mercado", "padaria", "açougue", "outro"], ["mercado", "padaria", "açougue", "outro"].index(supplier.type), False
        )
        if ok:
            supplier.type = new_type

        new_location, ok = QInputDialog.getText(
            None, "Editar Localização", "Nova localização:",
            text=supplier.location
        )
        if ok and new_location:
            supplier.location = new_location

        # Salva as alterações
        save_data(self.suppliers, 'suppliers')
        QMessageBox.information(None, "Sucesso", "Fornecedor editado com sucesso!")

    def remove_supplier(self):
        """Remove um fornecedor."""
        from PyQt6.QtWidgets import QInputDialog, QMessageBox

        if not self.suppliers:
            QMessageBox.warning(None, "Aviso", "Nenhum fornecedor cadastrado!")
            return

        # Lista os fornecedores para seleção
        supplier_names = [supplier.name for supplier in self.suppliers]
        supplier_name, ok = QInputDialog.getItem(
            None, "Remover Fornecedor", "Selecione o fornecedor:",
            supplier_names, 0, False
        )
        if not ok:
            return

        # Confirma a remoção
        confirm = QMessageBox.question(
            None, "Confirmar Remoção",
            f"Tem certeza que deseja remover {supplier_name}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if confirm == QMessageBox.StandardButton.No:
            return

        # Remove o fornecedor
        self.suppliers = [s for s in self.suppliers if s.name != supplier_name]
        save_data(self.suppliers, 'suppliers')
        QMessageBox.information(None, "Sucesso", "Fornecedor removido com sucesso!")