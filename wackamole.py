import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QWidget, QGridLayout, QVBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

#open window
class wakeamoleWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("wack-a-mole")
        self.setGeometry(100, 100, 400, 500)
        self.board = [['' for _ in range(5)] for _ in range(5)]
        self.initUI()

    def initUI(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        #title
        self.label = QLabel("wack-a-mole", self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setFont(QFont('Arial', 20))
        layout.addWidget(self.label)
        
        grid_layout = QGridLayout()
        layout.addLayout(grid_layout)
        #clickable buttons
        self.push_buttons = []
        for i in range(5):
            for j in range(5):
                button = QPushButton(self)
                button.setFont(QFont('Arial', 40))
                button.clicked.connect(lambda _, row=i, col=j: self.on_click(row, col))
                grid_layout.addWidget(button, i, j)
                self.push_buttons.append(button)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = wakeamoleWindow()
    window.show()
    sys.exit(app.exec_())