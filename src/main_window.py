import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QLabel, QSpinBox, QPushButton,
    QTableWidget, QTableWidgetItem, QMessageBox, QFileDialog
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from game_controller import GameController
from price_graph import PriceGraph


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.controller = GameController(end_probability=0.2)
        self.setWindowTitle("Game Theory Simulation - Duopoly")
        self.setMinimumSize(750, 550)
        self._build_ui()

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QHBoxLayout(central)

        #left side controls
        left = QVBoxLayout()

        title = QLabel("Duopoly Game")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        left.addWidget(title)

        left.addWidget(QLabel("Your production quantity:"))
        self.quantity_input = QSpinBox()
        self.quantity_input.setRange(0, 100)
        self.quantity_input.setValue(20)
        left.addWidget(self.quantity_input)

        self.submit_btn = QPushButton("Submit")
        self.submit_btn.clicked.connect(self.play_round)
        left.addWidget(self.submit_btn)

        # info labels
        self.round_label = QLabel("Round: 0")
        self.price_label = QLabel("Current Price: -")
        self.profit_label = QLabel("Your Profit this round: -")
        self.total_profit_label = QLabel("Total Profit: -")
        self.ai_qty_label = QLabel("AI Quantity: -")

        for lbl in [self.round_label, self.price_label, self.ai_qty_label,
                    self.profit_label, self.total_profit_label]:
            left.addWidget(lbl)

        left.addSpacing(10)

        eq = self.controller.get_equilibrium()
        hint = QLabel(
            f"Nash Eq. quantity: {eq['quantity_each']}\n"
            f"Nash Eq. price: {eq['price']}"
        )
        hint.setStyleSheet("color: gray; font-size: 11px;")
        left.addWidget(hint)

        left.addSpacing(10)

        reset_btn = QPushButton("New Game")
        reset_btn.clicked.connect(self.reset_game)
        left.addWidget(reset_btn)

        self.save_btn = QPushButton("Save Results")
        self.save_btn.clicked.connect(self.save_results)
        self.save_btn.setEnabled(False)  # only enabled after game ends
        left.addWidget(self.save_btn)

        left.addStretch()
        main_layout.addLayout(left)

        #right side graph+table
        right = QVBoxLayout()

        right.addWidget(QLabel("Price History:"))
        self.graph = PriceGraph()
        self.graph.setMinimumHeight(180)
        right.addWidget(self.graph)

        right.addWidget(QLabel("Round History:"))
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(
            ["Round", "Your Qty", "AI Qty", "Price", "Your Profit"]
        )
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.horizontalHeader().setStretchLastSection(True)
        right.addWidget(self.table)

        main_layout.addLayout(right)

    def play_round(self):
        if self.controller.game_over:
            return

        quantity = self.quantity_input.value()
        result = self.controller.play_round(quantity)

        self.round_label.setText(f"Round: {result['round']}")
        self.price_label.setText(f"Current Price: {result['price']}")
        self.ai_qty_label.setText(f"AI Quantity: {result['ai_quantity']}")
        self.profit_label.setText(f"Your Profit this round: {result['player_profit']}")
        self.total_profit_label.setText(
            f"Total Profit: {round(self.controller.player.total_profit, 2)}"
        )

        # add row to history table
        row = self.table.rowCount()
        self.table.insertRow(row)
        self.table.setItem(row, 0, QTableWidgetItem(str(result["round"])))
        self.table.setItem(row, 1, QTableWidgetItem(str(result["player_quantity"])))
        self.table.setItem(row, 2, QTableWidgetItem(str(result["ai_quantity"])))
        self.table.setItem(row, 3, QTableWidgetItem(str(result["price"])))
        self.table.setItem(row, 4, QTableWidgetItem(str(result["player_profit"])))

        # update price graph
        prices = [r["price"] for r in self.controller.history]
        self.graph.update_prices(prices)

        if self.controller.game_over:
            self._show_end_screen()

    def _show_end_screen(self):
        s = self.controller.get_summary()
        msg = QMessageBox(self)
        msg.setWindowTitle("Game Over")
        msg.setText(
            f"Game ended after {s['rounds']} round(s)!\n\n"
            f"Your total profit:  {s['player_total_profit']}\n"
            f"AI total profit:    {s['ai_total_profit']}\n\n"
            f"Your avg quantity:  {s['avg_player_quantity']}\n"
            f"AI avg quantity:    {s['avg_ai_quantity']}\n\n"
            f"--- Nash Equilibrium (optimal play) ---\n"
            f"Optimal quantity per firm: {s['eq_quantity']}\n"
            f"Optimal price:             {s['eq_price']}\n"
        )
        msg.exec_()
        self.submit_btn.setEnabled(False)
        self.save_btn.setEnabled(True)

    def save_results(self):
        # open a file dialog so the user can choose where to save
        path, _ = QFileDialog.getSaveFileName(
            self, "Save Results", "results.txt", "Text Files (*.txt)"
        )
        if path:
            self.controller.save_results(path)
            QMessageBox.information(self, "Saved", f"Results saved to:\n{path}")

    def reset_game(self):
        self.controller.reset()
        self.table.setRowCount(0)
        self.round_label.setText("Round: 0")
        self.price_label.setText("Current Price: -")
        self.ai_qty_label.setText("AI Quantity: -")
        self.profit_label.setText("Your Profit this round: -")
        self.total_profit_label.setText("Total Profit: -")
        self.graph.update_prices([])
        self.submit_btn.setEnabled(True)
        self.save_btn.setEnabled(False)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())