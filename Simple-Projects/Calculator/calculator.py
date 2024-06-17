import sys
from PyQt5.QtWidgets import *

class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Set window title and initial geometry
        self.setWindowTitle("Calculator Program")
        self.setGeometry(100, 200, 280, 370)

        # Vertical layout for the calculator
        self.vbox = QVBoxLayout()

        # Result field where calculations are displayed
        self.result_field = QLineEdit()
        self.result_field.setMinimumHeight(50)
        self.result_field.returnPressed.connect(self.calculateResult)  # Connect return key press to calculateResult method
        self.vbox.addWidget(self.result_field)

        # Grid layout for buttons
        self.grid = QGridLayout()
        buttons = [
            "7", "8", "9", "/",
            "4", "5", "6", "*",
            "1", "2", "3", "-",
            "0", ".", "=", "+"
        ]

        # Positions for buttons in the grid
        position = [(i, j) for i in range(4) for j in range(4)]

        # Create buttons and connect onClick method
        for position, button in zip(position, buttons):
            self.createButton(button, position)

        # Add grid layout to the vertical layout
        self.vbox.addLayout(self.grid)
        self.setLayout(self.vbox)

    def createButton(self, text, position):
        # Create a button with given text and fixed size
        button = QPushButton(text)
        button.setFixedSize(50, 50)
        button.clicked.connect(self.onClick)  # Connect button click to onClick method
        self.grid.addWidget(button, *position)

    def onClick(self):
        # Handle button click events
        sender = self.sender()
        text = sender.text()
        if text == '=':
            self.calculateResult()  # If '=' button is clicked, calculate result
        else:
            self.result_field.setText(self.result_field.text() + text)  # Append button text to result field

    def calculateResult(self):
        # Evaluate the expression entered in the result field
        try:
            expression = self.result_field.text().replace(",", ".")
            expression = expression.replace("^", "**")  # Replace '^' with '**' for exponentiation
            result = str(eval(expression))  # Evaluate the expression and convert result to string
            self.result_field.setText(result)  # Display the result in the result field
        except Exception as e:
            print(e)
            self.result_field.setText('Error')  # Display 'Error' if calculation fails

# Main application loop
app = QApplication(sys.argv)
calculator = Calculator()
calculator.show()
sys.exit(app.exec_())
