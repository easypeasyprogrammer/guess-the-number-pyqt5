from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QMessageBox
from PyQt5.QtCore import Qt
import sys
import random

class GuessTheNumberApp(QWidget):
    def __init__(self):
        super().__init__()
        self.wins = 0
        self.losses = 0
        self.best_scores = {"Easy": None, "Medium": None, "Hard": None}
        self.best_times = {"Easy": None, "Medium": None, "Hard": None}
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Guess The Number")
        self.setGeometry(100, 100, 400, 300)
        self.setStyleSheet("background-color: #D6EAF8;")
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignCenter)
        self.show_main_menu()
        self.setLayout(self.layout)

    def clear_layout(self):
        while self.layout.count():
            item = self.layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def show_main_menu(self):
        self.clear_layout()
        self.title = QLabel("Guess The Number!", self)
        self.title.setStyleSheet("font-size: 24px; font-weight: bold; color: #154360;")
        self.layout.addWidget(self.title)

        self.play_button = QPushButton("Play", self)
        self.style_button(self.play_button)
        self.play_button.clicked.connect(self.show_difficulty)
        self.layout.addWidget(self.play_button)

        self.quit_button = QPushButton("Quit", self)
        self.style_button(self.quit_button)
        self.quit_button.clicked.connect(self.close)
        self.layout.addWidget(self.quit_button)

    def style_button(self, button):
        button.setStyleSheet("font-size: 16px; background-color: #3498DB; color: white; border-radius: 10px; padding: 6px;")
        button.setCursor(Qt.PointingHandCursor)

    def show_difficulty(self):
        self.clear_layout()
        self.title = QLabel("Choose Difficulty")
        self.title.setStyleSheet("font-size: 20px; font-weight: bold; color: #154360;")
        self.layout.addWidget(self.title)

        difficulties = {"Easy (1-10, 5 attempts)": ("Easy", 1, 10, 5),
                        "Medium (1-50, 7 attempts)": ("Medium", 1, 50, 7),
                        "Hard (1-100, 10 attempts)": ("Hard", 1, 100, 10)}

        for text, (level, low, high, attempts) in difficulties.items():
            btn = QPushButton(text)
            self.style_button(btn)
            btn.clicked.connect(lambda _, l=level, lo=low, hi=high, a=attempts: self.start_game(l, lo, hi, a))
            self.layout.addWidget(btn)

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
        self.title = QLabel(f"Level: {self.level} ({self.low} - {self.high})")
        self.title.setStyleSheet("font-size: 20px; font-weight: bold; color: #154360;")
        self.layout.addWidget(self.title)

        self.feedback_label = QLabel("Guess the number:")
        self.feedback_label.setStyleSheet("font-size: 16px; color: #154360;")
        self.layout.addWidget(self.feedback_label)

        self.guess_entry = QLineEdit()
        self.guess_entry.setStyleSheet("font-size: 16px; padding: 4px; border: 1px solid #3498DB; border-radius: 5px;")
        self.guess_entry.returnPressed.connect(self.check_guess)
        self.layout.addWidget(self.guess_entry)

        self.attempts_label = QLabel(f"Attempts left: {self.chances}")
        self.attempts_label.setStyleSheet("font-size: 16px; color: #154360;")
        self.layout.addWidget(self.attempts_label)

        self.submit_btn = QPushButton("Submit")
        self.style_button(self.submit_btn)
        self.submit_btn.clicked.connect(self.check_guess)
        self.layout.addWidget(self.submit_btn)

    def check_guess(self):
        try:
            guess = int(self.guess_entry.text())
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Please enter a valid number.")
            self.guess_entry.clear()
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
        self.guess_entry.clear()

        if self.attempts >= self.chances:
            QMessageBox.information(self, "Game Over", f"You're out of attempts! The number was {self.target}.")
            self.show_replay_option()

    def show_replay_option(self):
        self.clear_layout()

        self.title = QLabel("Game Over!")
        self.title.setStyleSheet("font-size: 20px; font-weight: bold; color: #154360;")
        self.layout.addWidget(self.title)

        replay_btn = QPushButton("Play Again")
        self.style_button(replay_btn)
        replay_btn.clicked.connect(self.show_difficulty)
        self.layout.addWidget(replay_btn)

        stats_btn = QPushButton("Statistics")
        self.style_button(stats_btn)
        stats_btn.clicked.connect(self.show_statistics)
        self.layout.addWidget(stats_btn)

        quit_btn = QPushButton("Quit")
        self.style_button(quit_btn)
        quit_btn.clicked.connect(self.close)
        self.layout.addWidget(quit_btn)

    def show_statistics(self):
        QMessageBox.information(self, "Statistics", "Statistics feature coming soon!")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = GuessTheNumberApp()
    window.show()
    sys.exit(app.exec_())
