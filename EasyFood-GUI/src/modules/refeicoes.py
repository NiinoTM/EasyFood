import json
from PyQt6.QtWidgets import QInputDialog, QMessageBox, QDialog, QVBoxLayout, QLabel, QPushButton, QListWidget
from src.modules.utils import Food, Meal, load_data, save_data
from src.modules.search_dialog import SearchDialog  # Importing the SearchDialog

class RefeicoesManager:
    def __init__(self):
        self.meals = load_data('meals', Meal)  # Load meals from JSON
        self.foods = load_data('foods', Food)  # Load foods for meal composition

    def add_meal(self):
        """Add a new meal using SearchDialog for food selection."""
        if not self.foods:
            QMessageBox.warning(None, "Aviso", "Nenhum alimento cadastrado! Cadastre alimentos primeiro.")
            return

        # Ask for the meal name
        name, ok = QInputDialog.getText(None, "Adicionar Refeição", "Nome da refeição:")
        if not ok or not name:
            return

        # List to store selected foods
        selected_foods = []

        # Dialog to add foods to the meal
        while True:
            # Open SearchDialog to select a food
            dialog = SearchDialog(self.foods, "Selecione um alimento para adicionar à refeição")
            if dialog.exec() == QDialog.DialogCode.Accepted:
                selected_food = dialog.get_selected_item()
                if selected_food:
                    # Ask for the quantity of the selected food
                    quantity, ok = QInputDialog.getDouble(
                        None, "Quantidade", f"Quantidade de {selected_food.name} ({selected_food.unit}):",
                        min=0.1, max=1000.0, decimals=2
                    )
                    if ok:
                        selected_foods.append({
                            'food_name': selected_food.name,
                            'quantity': quantity,
                            'unit': selected_food.unit
                        })
                        QMessageBox.information(None, "Sucesso", f"{selected_food.name} adicionado à refeição!")
                else:
                    QMessageBox.warning(None, "Erro", "Nenhum alimento selecionado!")
            else:
                break  # Exit the loop if the user cancels

        # If foods were selected, create the meal
        if selected_foods:
            new_meal = Meal(
                name=name,
                foods=selected_foods
            )
            self.meals.append(new_meal)
            save_data(self.meals, 'meals')
            QMessageBox.information(None, "Sucesso", "Refeição criada com sucesso!")
        else:
            QMessageBox.warning(None, "Aviso", "Adicione pelo menos um alimento à refeição!")

    def edit_meal(self):
        """Edit an existing meal using SearchDialog for selection."""
        if not self.meals:
            QMessageBox.warning(None, "Aviso", "Nenhuma refeição cadastrada!")
            return

        # Open SearchDialog to select a meal
        dialog = SearchDialog(self.meals, "Selecione a refeição para editar")
        if dialog.exec() == QDialog.DialogCode.Accepted:
            selected_meal = dialog.get_selected_item()
            if selected_meal:
                self._edit_meal_details(selected_meal)
            else:
                QMessageBox.warning(None, "Erro", "Nenhuma refeição selecionada!")

    def _edit_meal_details(self, meal):
        """Edit the details of a selected meal."""
        from PyQt6.QtWidgets import QInputDialog, QMessageBox, QDialog, QVBoxLayout, QLabel, QPushButton, QListWidget

        # Create a dialog to edit the meal
        dialog = QDialog()
        dialog.setWindowTitle(f"Editando {meal.name}")
        layout = QVBoxLayout()

        # List of foods in the meal
        label = QLabel("Alimentos na refeição:")
        layout.addWidget(label)

        list_widget = QListWidget()
        for food in meal.foods:
            list_widget.addItem(f"{food['food_name']} - {food['quantity']}{food['unit']}")
        layout.addWidget(list_widget)

        # Button to edit a food item
        edit_button = QPushButton("Editar Alimento")
        layout.addWidget(edit_button)

        def edit_food_in_meal():
            selected_item = list_widget.currentItem()
            if selected_item:
                food_name = selected_item.text().split(" - ")[0]
                food = next((f for f in meal.foods if f['food_name'] == food_name), None)
                if food:
                    # Ask for the new quantity
                    new_quantity, ok = QInputDialog.getDouble(
                        None, "Editar Quantidade", f"Nova quantidade de {food['food_name']} ({food['unit']}):",
                        value=food['quantity'], min=0.1, max=1000.0, decimals=2
                    )
                    if ok:
                        food['quantity'] = new_quantity
                        QMessageBox.information(None, "Sucesso", f"{food['food_name']} editado!")
                        list_widget.clear()
                        for food in meal.foods:
                            list_widget.addItem(f"{food['food_name']} - {food['quantity']}{food['unit']}")

        edit_button.clicked.connect(edit_food_in_meal)

        # Button to remove a food item
        remove_button = QPushButton("Remover Alimento")
        layout.addWidget(remove_button)

        def remove_food_from_meal():
            selected_item = list_widget.currentItem()
            if selected_item:
                food_name = selected_item.text().split(" - ")[0]
                meal.foods = [f for f in meal.foods if f['food_name'] != food_name]
                QMessageBox.information(None, "Sucesso", f"{food_name} removido da refeição!")
                list_widget.clear()
                for food in meal.foods:
                    list_widget.addItem(f"{food['food_name']} - {food['quantity']}{food['unit']}")

        remove_button.clicked.connect(remove_food_from_meal)

        # Button to add a new food item
        add_button = QPushButton("Adicionar Alimento")
        layout.addWidget(add_button)

        def add_food_to_meal():
            # Open SearchDialog to select a food
            dialog = SearchDialog(self.foods, "Selecione um alimento para adicionar à refeição")
            if dialog.exec() == QDialog.DialogCode.Accepted:
                selected_food = dialog.get_selected_item()
                if selected_food:
                    # Ask for the quantity of the selected food
                    quantity, ok = QInputDialog.getDouble(
                        None, "Quantidade", f"Quantidade de {selected_food.name} ({selected_food.unit}):",
                        min=0.1, max=1000.0, decimals=2
                    )
                    if ok:
                        meal.foods.append({
                            'food_name': selected_food.name,
                            'quantity': quantity,
                            'unit': selected_food.unit
                        })
                        QMessageBox.information(None, "Sucesso", f"{selected_food.name} adicionado à refeição!")
                        list_widget.clear()
                        for food in meal.foods:
                            list_widget.addItem(f"{food['food_name']} - {food['quantity']}{food['unit']}")

        add_button.clicked.connect(add_food_to_meal)

        # Button to finish editing
        finish_button = QPushButton("Finalizar Edição")
        layout.addWidget(finish_button)

        def finish_edit():
            save_data(self.meals, 'meals')
            QMessageBox.information(None, "Sucesso", "Refeição editada com sucesso!")
            dialog.close()

        finish_button.clicked.connect(finish_edit)

        dialog.setLayout(layout)
        dialog.exec()

    def remove_meal(self):
        """Remove a meal using SearchDialog for selection."""
        if not self.meals:
            QMessageBox.warning(None, "Aviso", "Nenhuma refeição cadastrada!")
            return

        # Open SearchDialog to select a meal
        dialog = SearchDialog(self.meals, "Selecione a refeição para remover")
        if dialog.exec() == QDialog.DialogCode.Accepted:
            selected_meal = dialog.get_selected_item()
            if selected_meal:
                # Confirm removal
                confirm = QMessageBox.question(
                    None, "Confirmar Remoção",
                    f"Tem certeza que deseja remover {selected_meal.name}?",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                )
                if confirm == QMessageBox.StandardButton.Yes:
                    self.meals = [m for m in self.meals if m.name != selected_meal.name]
                    save_data(self.meals, 'meals')
                    QMessageBox.information(None, "Sucesso", "Refeição removida com sucesso!")
            else:
                QMessageBox.warning(None, "Erro", "Nenhuma refeição selecionada!")