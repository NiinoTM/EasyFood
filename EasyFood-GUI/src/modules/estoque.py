from PyQt6.QtWidgets import QInputDialog, QMessageBox, QDialog
from src.modules.utils import Food, StockEntry, StockExit, load_data, save_data
from src.modules.search_dialog import SearchDialog

class EstoqueManager:
    def __init__(self, alimentos_manager):  # Receber o AlimentosManager como parâmetro
        self.alimentos_manager = alimentos_manager
        self.alimentos_manager.food_added.connect(self.reload_foods)  # Conectar o sinal
        self.reload_foods()  # Carrega os dados na inicialização
        self.stock_entries = load_data('stock_entries', StockEntry)  # Carrega as entradas de estoque
        self.stock_exits = load_data('stock_exits', StockExit)       # Carrega as saídas de estoque

    def reload_foods(self):
        """Recarrega a lista de alimentos do arquivo JSON."""
        self.foods = load_data('foods', Food)  # Recarrega os alimentos

    def add_stock_entry(self):
        """Registra uma nova entrada no estoque usando o SearchDialog."""
        if not self.foods:
            QMessageBox.warning(None, "Aviso", "Nenhum alimento cadastrado!")
            return

        # Abre o SearchDialog para selecionar o alimento
        dialog = SearchDialog(self.foods, "Selecione o alimento para entrada")
        if dialog.exec() == QDialog.DialogCode.Accepted:
            selected_food = dialog.get_selected_item()
            if selected_food:
                self._add_stock_entry_details(selected_food)
            else:
                QMessageBox.warning(None, "Erro", "Nenhum alimento selecionado!")

    def _add_stock_entry_details(self, food):
        """Adiciona os detalhes da entrada de estoque."""
        from PyQt6.QtWidgets import QInputDialog, QMessageBox

        # Solicita os dados da entrada
        quantity, ok = QInputDialog.getDouble(
            None, "Quantidade", f"Quantidade ({food.unit}):",
            min=0.1, max=100000.0, decimals=2
        )
        if not ok:
            return

        cost, ok = QInputDialog.getDouble(
            None, "Custo", "Custo total (R$):",
            min=0.01, max=100000.0, decimals=2
        )
        if not ok:
            return

        date, ok = QInputDialog.getText(
            None, "Data", "Data da entrada (dd/mm/aaaa):"
        )
        if not ok or not date:
            return

        supplier, ok = QInputDialog.getText(
            None, "Fornecedor", "Nome do fornecedor:"
        )
        if not ok or not supplier:
            return

        # Cria a nova entrada de estoque
        new_entry = StockEntry(
            food_name=food.name,
            quantity=quantity,
            unit=food.unit,
            cost=cost,
            date=date,
            supplier=supplier
        )

        # Adiciona a entrada à lista
        self.stock_entries.append(new_entry)
        save_data(self.stock_entries, 'stock_entries')  # Salva no arquivo JSON

        # Atualiza o estoque do alimento
        food.quantity_in_stock += quantity
        save_data(self.foods, 'foods')

        QMessageBox.information(None, "Sucesso", "Entrada de estoque registrada com sucesso!")

    def add_stock_exit(self):
        """Registra uma nova saída no estoque usando o SearchDialog."""
        if not self.foods:
            QMessageBox.warning(None, "Aviso", "Nenhum alimento cadastrado!")
            return

        # Abre o SearchDialog para selecionar o alimento
        dialog = SearchDialog(self.foods, "Selecione o alimento para saída")
        if dialog.exec() == QDialog.DialogCode.Accepted:
            selected_food = dialog.get_selected_item()
            if selected_food:
                self._add_stock_exit_details(selected_food)
            else:
                QMessageBox.warning(None, "Erro", "Nenhum alimento selecionado!")

    def _add_stock_exit_details(self, food):
        """Adiciona os detalhes da saída de estoque."""
        from PyQt6.QtWidgets import QInputDialog, QMessageBox

        # Solicita os dados da saída
        dialog_text = f"Quantidade ({food.unit}):\n(Estoque total: {food.quantity_in_stock} {food.unit})"

        quantity, ok = QInputDialog.getDouble(
            None, "Quantidade", dialog_text,
            min=0.1, max=food.quantity_in_stock, decimals=2
        )
        if not ok:
            return

        reason, ok = QInputDialog.getText(
            None, "Motivo", "Motivo da saída:"
        )
        if not ok or not reason:
            return

        date, ok = QInputDialog.getText(
            None, "Data", "Data da saída (dd/mm/aaaa):"
        )
        if not ok or not date:
            return

        # Cria a nova saída de estoque
        new_exit = StockExit(
            food_name=food.name,
            quantity=quantity,
            unit=food.unit,
            date=date,
            reason=reason
        )

        # Adiciona a saída à lista
        self.stock_exits.append(new_exit)
        save_data(self.stock_exits, 'stock_exits')  # Salva no arquivo JSON

        # Atualiza o estoque do alimento
        food.quantity_in_stock -= quantity
        save_data(self.foods, 'foods')

        QMessageBox.information(None, "Sucesso", "Saída de estoque registrada com sucesso!")

    def remove_stock(self):
        """Remove uma entrada ou saída de estoque."""
        if not self.stock_entries and not self.stock_exits:
            QMessageBox.warning(None, "Aviso", "Nenhuma entrada ou saída de estoque cadastrada!")
            return

        # Pergunta ao usuário se deseja remover uma entrada ou saída
        option, ok = QInputDialog.getItem(
            None, "Remover Estoque", "Selecione o tipo de estoque para remover:",
            ["Entrada", "Saída"], 0, False
        )
        if not ok:
            return

        if option == "Entrada":
            self._remove_stock_entry()
        else:
            self._remove_stock_exit()

    def _remove_stock_entry(self):
        """Remove uma entrada de estoque."""
        if not self.stock_entries:
            QMessageBox.warning(None, "Aviso", "Nenhuma entrada de estoque cadastrada!")
            return

        # Lista as entradas de estoque para seleção
        entry_names = [f"{entry.food_name} - {entry.quantity}{entry.unit} em {entry.date}" for entry in self.stock_entries]
        entry_name, ok = QInputDialog.getItem(
            None, "Remover Entrada", "Selecione a entrada para remover:",
            entry_names, 0, False
        )
        if not ok:
            return

        # Encontra a entrada selecionada
        selected_entry = next((entry for entry in self.stock_entries if f"{entry.food_name} - {entry.quantity}{entry.unit} em {entry.date}" == entry_name), None)
        if not selected_entry:
            QMessageBox.warning(None, "Erro", "Entrada não encontrada!")
            return

        # Confirma a remoção
        confirm = QMessageBox.question(
            None, "Confirmar Remoção",
            f"Tem certeza que deseja remover a entrada de {selected_entry.food_name}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if confirm == QMessageBox.StandardButton.Yes:
            self.stock_entries = [entry for entry in self.stock_entries if entry != selected_entry]
            save_data(self.stock_entries, 'stock_entries')
            QMessageBox.information(None, "Sucesso", "Entrada de estoque removida com sucesso!")

    def _remove_stock_exit(self):
        """Remove uma saída de estoque."""
        if not self.stock_exits:
            QMessageBox.warning(None, "Aviso", "Nenhuma saída de estoque cadastrada!")
            return

        # Lista as saídas de estoque para seleção
        exit_names = [f"{exit.food_name} - {exit.quantity}{exit.unit} em {exit.date}" for exit in self.stock_exits]
        exit_name, ok = QInputDialog.getItem(
            None, "Remover Saída", "Selecione a saída para remover:",
            exit_names, 0, False
        )
        if not ok:
            return

        # Encontra a saída selecionada
        selected_exit = next((exit for exit in self.stock_exits if f"{exit.food_name} - {exit.quantity}{exit.unit} em {exit.date}" == exit_name), None)
        if not selected_exit:
            QMessageBox.warning(None, "Erro", "Saída não encontrada!")
            return

        # Confirma a remoção
        confirm = QMessageBox.question(
            None, "Confirmar Remoção",
            f"Tem certeza que deseja remover a saída de {selected_exit.food_name}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if confirm == QMessageBox.StandardButton.Yes:
            self.stock_exits = [exit for exit in self.stock_exits if exit != selected_exit]
            save_data(self.stock_exits, 'stock_exits')
            QMessageBox.information(None, "Sucesso", "Saída de estoque removida com sucesso!")