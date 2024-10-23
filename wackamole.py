import sys
import random
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QWidget, QGridLayout, QVBoxLayout, QInputDialog, QMessageBox, QHBoxLayout
from PyQt5.QtGui import QFont    
from PyQt5.QtCore import QTimer, Qt

class WackAMoleGame(QMainWindow):
    def __init__(self):
        super().__init__()
        # Create window
        self.setWindowTitle("Whack-a-Mole") # set window title
        self.setGeometry(100, 100, 400, 500)# set window dimensions
        #create board
        self.board = [['' for _ in range(5)] for _ in range(5)]# Initialize board 
        self.mole_position = (-1, -1)  # No mole at the start
        self.game_duration = 0  # Initialize game duration
        self.score = 0  # Initialize score
        self.initUI()

    def initUI(self):
        # Define layouts as instance variables
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget) # definecentral widgets 
        self.main_layout = QVBoxLayout(self.central_widget) # define main layout
        self.top_layout = QHBoxLayout() # Define toplayout

        # Timer position
        self.timer_label = QLabel(f"Time left: {self.game_duration} s", self) # set name
        self.timer_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)# set position
        self.timer_label.setFont(QFont('Arial', 14)) # set font
        self.top_layout.addWidget(self.timer_label)

        # Scoreboard position
        self.score_label = QLabel(f"Score: {self.score}", self)# set name
        self.score_label.setAlignment(Qt.AlignRight | Qt.AlignTop)#set position
        self.score_label.setFont(QFont('Arial', 14))#set font
        self.top_layout.addWidget(self.score_label)

        self.main_layout.addLayout(self.top_layout)
        self.top_layout.addStretch()

        # Title
        self.label = QLabel("Whack-a-Mole", self)#set name
        self.label.setAlignment(Qt.AlignCenter)#set position
        self.label.setFont(QFont('Arial', 20))#set font
        self.main_layout.addWidget(self.label)
        
        # Grid layout for buttons
        grid_layout = QGridLayout()
        self.main_layout.addLayout(grid_layout)

        # Clickable buttons
        self.push_buttons = []
        for i in range(5): #set dimentions of grid to 5x5
            for j in range(5):
                button = QPushButton(self) # give button a function
                button.setFont(QFont('Arial', 40)) # set font
                button.clicked.connect(lambda _, row=i, col=j: self.on_click(row, col)) 
                grid_layout.addWidget(button, i, j)# create widget buttons
                self.push_buttons.append(button)

        # Timer setup
        self.timer_limit = QTimer()
        self.timer_limit.timeout.connect(self.end_game)# set functon to end game when timer ends
        self.time_limit, ok = QInputDialog.getInt(self, 'Time Limit', 'Enter a time limit for this Whack-a-Mole game between 15 and 60 seconds:', 15, 15, 60) #display and ask for input
        # Display timer
        if ok:
            self.game_duration = self.time_limit
            self.timer_label.setText(f"Time left: {self.game_duration} s") #set display name
            self.timer_limit.start(self.time_limit * 1000)#set timer to run in seconds

        # Timer countdown update
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_timer_display)# allow displayed timer to update at the same rate the count down timer happens
        self.update_timer.start(1000)

        # Mole creation timer
        self.mole_timer = QTimer()
        self.mole_timer.timeout.connect(self.spawn_mole) # create mole
        self.mole_timer.start(1000)  # Mole appears every second

    def update_timer_display(self):
        self.game_duration -= 1 #containue game as long as timer is grater than 0
        self.timer_label.setText(f"Time left: {self.game_duration} s") #desplay time left
        if self.game_duration <= 0: #set game to end when timer reacher 0
            self.end_game()

    # Button click handler
    def on_click(self, row, col):
        button = self.sender()
        if button.text() == 'Mole':# mole name # if mole is clicked purpose
            self.score += 1 # if mole clicked increase score by 1
            button.setText('')  # Clear the mole
            self.score_label.setText(f"Score: {self.score}")  # Update score display
            self.mole_position = (-1, -1)  # Reset mole position

    # Mole creation
    def spawn_mole(self):
        # Clear the previous mole
        if self.mole_position != (-1, -1):
            prev_row, prev_col = self.mole_position
            self.push_buttons[prev_row * 5 + prev_col].setText('')#  clear mole every time its clicked

        # Pick a random position
        row = random.randint(0, 4) # pick row
        col = random.randint(0, 4) # pick colum
        self.push_buttons[row * 5 + col].setText('Mole')  # Place the mole 
        self.mole_position = (row, col)

    def end_game(self):
        self.update_timer.stop()
        self.mole_timer.stop()
        QMessageBox.information(self, 'Game Over', f'Game over! Final score: {self.score}') # display whn game over
        # Append score to score.txt
        with open('score.txt', 'a') as file:
            file.write(f'{self.score}\n')  # Store only the score
        self.close()

# run game
if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = WackAMoleGame()
    game.show()
    sys.exit(app.exec_()) # close game
