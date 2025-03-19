from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QMessageBox
from PyQt5.QtCore import Qt
import sys
import random

class GuessTheNumberApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Set up window
        self.setWindowTitle("Guess The Number")
        self.setGeometry(100, 100, 400, 300)
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignCenter)

        # Title Label
        self.title = QLabel("Guess The Number!", self)
        self.title.setStyleSheet("font-size: 20px; font-weight: bold;")
        self.layout.addWidget(self.title)

        # Play Button
        self.play_button = QPushButton("Play", self)
        self.play_button.setStyleSheet("font-size: 18px;")
        self.play_button.clicked.connect(self.show_difficulty)
        self.layout.addWidget(self.play_button)

        # Quit Button
        self.quit_button = QPushButton("Quit", self)
        self.quit_button.setStyleSheet("font-size: 18px;")
        self.quit_button.clicked.connect(self.close)
        self.layout.addWidget(self.quit_button)

        self.setLayout(self.layout)

    def clear_layout(self):
        """Clear all widgets from the layout."""
        while self.layout.count():
            item = self.layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def show_difficulty(self):
        self.clear_layout()

        # Difficulty Selection
        self.title = QLabel("Choose Difficulty")
        self.title.setStyleSheet("font-size: 20px; font-weight: bold;")
        self.layout.addWidget(self.title)

        difficulties = {
            "Easy (1-10, 5 attempts)": ("Easy", 1, 10, 5),
            "Medium (1-50, 7 attempts)": ("Medium", 1, 50, 7),
            "Hard (1-100, 10 attempts)": ("Hard", 1, 100, 10),
        }

        for text, (level, low, high, attempts) in difficulties.items():
            btn = QPushButton(text)
            btn.clicked.connect(lambda _, l=level, lo=low, hi=high, a=attempts: self.start_game(l, lo, hi, a))
            self.layout.addWidget(btn)

        # Quit Button in Difficulty Screen
        quit_btn = QPushButton("Quit")
        quit_btn.clicked.connect(self.close)
        self.layout.addWidget(quit_btn)

    def start_game(self, level, low, high, chances):
        self.level = level
        self.target = random.randint(low, high)
        self.chances = chances
        self.attempts = 0
        self.low = low
        self.high = high
        self.show_game_screen()

    def show_game_screen(self):
        self.clear_layout()

        # Level Title
        self.title = QLabel(f"Level: {self.level} ({self.low} - {self.high})")
        self.title.setStyleSheet("font-size: 20px; font-weight: bold;")
        self.layout.addWidget(self.title)

        # Feedback Label
        self.feedback_label = QLabel("Guess the number:")
        self.layout.addWidget(self.feedback_label)

        # Input Field
        self.guess_entry = QLineEdit()
        self.guess_entry.returnPressed.connect(self.check_guess)  # Enter Key Submits
        self.layout.addWidget(self.guess_entry)

        # Attempts Label
        self.attempts_label = QLabel(f"Attempts left: {self.chances}")
        self.layout.addWidget(self.attempts_label)

        # Submit Button
        self.submit_btn = QPushButton("Submit")
        self.submit_btn.clicked.connect(self.check_guess)
        self.layout.addWidget(self.submit_btn)

        # Quit Button in Game Screen
        quit_btn = QPushButton("Quit")
        quit_btn.clicked.connect(self.close)
        self.layout.addWidget(quit_btn)

    def check_guess(self):
        try:
            guess = int(self.guess_entry.text())
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Please enter a valid number.")
            self.guess_entry.clear()  # Clear invalid input
            return
        
        self.attempts += 1
        remaining_attempts = self.chances - self.attempts

        if guess == self.target:
            QMessageBox.information(self, "Congratulations!", f"You guessed the number in {self.attempts} attempts!")
            self.show_replay_option()
        elif guess > self.target:
            self.feedback_label.setText(f"Too high! Attempts left: {remaining_attempts}")
        else:
            self.feedback_label.setText(f"Too low! Attempts left: {remaining_attempts}")

        self.attempts_label.setText(f"Attempts left: {remaining_attempts}")
        self.guess_entry.clear()  # Clear the input field after each guess

        if self.attempts >= self.chances:
            QMessageBox.information(self, "Game Over", f"You're out of attempts! The number was {self.target}.")
            self.show_replay_option()

    def show_replay_option(self):
        self.clear_layout()

        # Replay Title
        self.title = QLabel("Play Again?")
        self.title.setStyleSheet("font-size: 20px; font-weight: bold;")
        self.layout.addWidget(self.title)

        # Replay Button
        replay_btn = QPushButton("Play Again")
        replay_btn.clicked.connect(self.initUI)
        self.layout.addWidget(replay_btn)

        # Quit Button on Replay Screen
        quit_btn = QPushButton("Quit")
        quit_btn.clicked.connect(self.close)
        self.layout.addWidget(quit_btn)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = GuessTheNumberApp()
    window.show()
    sys.exit(app.exec_())
