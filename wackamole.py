import sys
import random
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QWidget, QGridLayout, QVBoxLayout, QInputDialog, QMessageBox, QHBoxLayout
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QTimer, Qt

class WackAMoleGame(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Whack-a-Mole")
        self.setGeometry(100, 100, 400, 500)
        self.board = [['' for _ in range(5)] for _ in range(5)]
        self.score = 0
        self.game_duration = 0  # Initialize game duration
        self.initUI()

    def initUI(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        #  timer position
        top_layout = QHBoxLayout()
        self.timer_label = QLabel(f"Time left: {self.game_duration} s", self)
        self.timer_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.timer_label.setFont(QFont('Arial', 14))
        top_layout.addWidget(self.timer_label)
        top_layout.addStretch()  
        
        main_layout.addLayout(top_layout)

        # Title
        self.label = QLabel("Whack-a-Mole", self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setFont(QFont('Arial', 20))
        main_layout.addWidget(self.label)
        
        # Grid layout for buttons
        grid_layout = QGridLayout()
        main_layout.addLayout(grid_layout)

        # Clickable buttons
        self.push_buttons = []
        for i in range(5):
            for j in range(5):
                button = QPushButton(self)
                button.setFont(QFont('Arial', 40))
                button.clicked.connect(lambda _, row=i, col=j: self.on_click(row, col))
                grid_layout.addWidget(button, i, j)
                self.push_buttons.append(button)

        # Timer setup
        self.timer_limit = QTimer()
        self.timer_limit.timeout.connect(self.end_game)
        self.time_limit, ok = QInputDialog.getInt(self, 'Time Limit', 'Enter a time limit for this Whack-a-Mole game between 15 and 60 seconds:', 15, 15, 60)
        
        if ok:
            self.game_duration = self.time_limit
            self.timer_label.setText(f"Time left: {self.game_duration} s")
            self.timer_limit.start(self.time_limit * 1000)

        # Timer countdown update
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_timer_display)
        self.update_timer.start(1000)  # Update every second

    def update_timer_display(self):
        self.game_duration -= 1
        self.timer_label.setText(f"Time left: {self.game_duration} s")
        if self.game_duration <= 0:
            self.end_game()


    def end_game(self):
        self.update_timer.stop()
        QMessageBox.information(self, 'Game Over', f'Game over! Final score: {self.score}')
        with open('score.txt', 'w') as file:
            file.write(f'Final score: {self.score}')
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = WackAMoleGame()
    game.show()
    sys.exit(app.exec_())