from PyQt6.QtCore import QObject, pyqtSignal  # Importar QObject e pyqtSignal
from PyQt6.QtWidgets import QInputDialog, QMessageBox, QDialog
from src.modules.utils import Food, load_data, save_data
from src.modules.search_dialog import SearchDialog

class AlimentosManager(QObject):  # Herdar de QObject para usar sinais
    food_added = pyqtSignal()  # Definir o sinal

    def __init__(self):
        super().__init__()  # Inicializar a classe base QObject
        self.foods = load_data('foods', Food)  # Carrega os alimentos do arquivo JSON

    def add_food(self):
        """Adiciona um novo alimento."""
        from PyQt6.QtWidgets import QInputDialog, QMessageBox

        # Solicita os dados do alimento
        name, ok = QInputDialog.getText(None, "Adicionar Alimento", "Nome do alimento:")
        if not ok or not name:
            return

        unit, ok = QInputDialog.getItem(
            None, "Unidade de Medida", "Selecione a unidade:",
            ["g", "kg", "ml", "litros", "unidades"], 0, False
        )
        if not ok:
            return

        quantity_per_portion, ok = QInputDialog.getDouble(
            None, "Quantidade por Porção", "Quantidade por porção:",
            min=0.1, max=1000.0, decimals=2
        )
        if not ok:
            return

        calories, ok = QInputDialog.getDouble(
            None, "Calorias", "Calorias por porção:",
            min=0.1, max=1000.0, decimals=2
        )
        if not ok:
            return

        proteins, ok = QInputDialog.getDouble(
            None, "Proteínas", "Proteínas por porção (g):",
            min=0.0, max=100.0, decimals=2
        )
        if not ok:
            return

        carbs, ok = QInputDialog.getDouble(
            None, "Carboidratos", "Carboidratos por porção (g):",
            min=0.0, max=100.0, decimals=2
        )
        if not ok:
            return

        fats, ok = QInputDialog.getDouble(
            None, "Gorduras", "Gorduras por porção (g):",
            min=0.0, max=100.0, decimals=2
        )
        if not ok:
            return

        # Cria o novo alimento
        new_food = Food(
            name=name,
            unit=unit,
            quantity_per_portion=quantity_per_portion,
            calories=calories,
            proteins=proteins,
            carbs=carbs,
            fats=fats,
            quantity_in_stock=0.0,  # Estoque inicial zero
            min_stock=0.0,          # Estoque mínimo zero
            ideal_stock=0.0         # Estoque ideal zero
        )

        # Adiciona o alimento à lista
        self.foods.append(new_food)
        save_data(self.foods, 'foods')  # Salva no arquivo JSON

        # Emitir o sinal após adicionar o alimento
        self.food_added.emit()

        QMessageBox.information(None, "Sucesso", "Alimento adicionado com sucesso!")

    def edit_food(self):
        """Edita um alimento existente usando o SearchDialog."""
        if not self.foods:
            QMessageBox.warning(None, "Aviso", "Nenhum alimento cadastrado!")
            return

        # Abre o SearchDialog para selecionar o alimento
        dialog = SearchDialog(self.foods, "Selecione o alimento para editar")
        if dialog.exec() == QDialog.DialogCode.Accepted:
            selected_food = dialog.get_selected_item()
            if selected_food:
                self._edit_food_details(selected_food)
            else:
                QMessageBox.warning(None, "Erro", "Nenhum alimento selecionado!")

    def _edit_food_details(self, food):
        """Edita os detalhes de um alimento selecionado."""
        from PyQt6.QtWidgets import QInputDialog, QMessageBox

        # Solicita os novos dados
        new_name, ok = QInputDialog.getText(
            None, "Editar Alimento", "Novo nome:",
            text=food.name
        )
        if ok and new_name:
            food.name = new_name

        new_unit, ok = QInputDialog.getItem(
            None, "Editar Unidade", "Nova unidade:",
            ["g", "kg", "ml", "litros", "unidades"], ["g", "kg", "ml", "litros", "unidades"].index(food.unit), False
        )
        if ok:
            food.unit = new_unit

        new_quantity_per_portion, ok = QInputDialog.getDouble(
            None, "Editar Quantidade por Porção", "Nova quantidade por porção:",
            value=food.quantity_per_portion, min=0.1, max=1000.0, decimals=2
        )
        if ok:
            food.quantity_per_portion = new_quantity_per_portion

        new_calories, ok = QInputDialog.getDouble(
            None, "Editar Calorias", "Novas calorias por porção:",
            value=food.calories, min=0.1, max=1000.0, decimals=2
        )
        if ok:
            food.calories = new_calories

        new_proteins, ok = QInputDialog.getDouble(
            None, "Editar Proteínas", "Novas proteínas por porção (g):",
            value=food.proteins, min=0.0, max=100.0, decimals=2
        )
        if ok:
            food.proteins = new_proteins

        new_carbs, ok = QInputDialog.getDouble(
            None, "Editar Carboidratos", "Novos carboidratos por porção (g):",
            value=food.carbs, min=0.0, max=100.0, decimals=2
        )
        if ok:
            food.carbs = new_carbs

        new_fats, ok = QInputDialog.getDouble(
            None, "Editar Gorduras", "Novas gorduras por porção (g):",
            value=food.fats, min=0.0, max=100.0, decimals=2
        )
        if ok:
            food.fats = new_fats

        # Salva as alterações
        save_data(self.foods, 'foods')
        QMessageBox.information(None, "Sucesso", "Alimento editado com sucesso!")

    def remove_food(self):
        """Remove um alimento usando o SearchDialog."""
        if not self.foods:
            QMessageBox.warning(None, "Aviso", "Nenhum alimento cadastrado!")
            return

        # Abre o SearchDialog para selecionar o alimento
        dialog = SearchDialog(self.foods, "Selecione o alimento para remover")
        if dialog.exec() == QDialog.DialogCode.Accepted:
            selected_food = dialog.get_selected_item()
            if selected_food:
                # Confirma a remoção
                confirm = QMessageBox.question(
                    None, "Confirmar Remoção",
                    f"Tem certeza que deseja remover {selected_food.name}?",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                )
                if confirm == QMessageBox.StandardButton.Yes:
                    self.foods = [f for f in self.foods if f.name != selected_food.name]
                    save_data(self.foods, 'foods')
                    QMessageBox.information(None, "Sucesso", "Alimento removido com sucesso!")
            else:
                QMessageBox.warning(None, "Erro", "Nenhum alimento selecionado!")