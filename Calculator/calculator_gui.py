import sys
from PyQt5.QtWidgets import *

class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Calculator Program")
        self.setGeometry(100, 200, 280, 370)

        self.vbox = QVBoxLayout()

        self.result_field = QLineEdit()
        self.result_field.setMinimumHeight(50)
        self.result_field.returnPressed.connect(self.calculateResult)  # Enter tuşu için sinyal bağlantısı
        self.vbox.addWidget(self.result_field)

        self.grid = QGridLayout()
        buttons = [
            "7", "8", "9", "/",
            "4", "5", "6", "*",
            "1", "2", "3", "-",
            "0", ".", "=", "+"
        ]

        position = [(i, j) for i in range(4) for j in range(4)]

        for position, button in zip(position, buttons):
            self.createButton(button, position)

        self.vbox.addLayout(self.grid)
        self.setLayout(self.vbox)

    def createButton(self, text, position):
        button = QPushButton(text)
        button.setFixedSize(50, 50)
        button.clicked.connect(self.onClick)
        self.grid.addWidget(button, *position)

    def onClick(self):
        sender = self.sender()
        text = sender.text()
        if text == '=':
            self.calculateResult()
        else:
            self.result_field.setText(self.result_field.text() + text)

    def calculateResult(self):
        try:
            expression = self.result_field.text().replace(",", ".")
            expression = expression.replace("^", "**")
            result = str(eval(expression))
            self.result_field.setText(result)
        except Exception as e:
            print(e)
            self.result_field.setText('Error')

app = QApplication(sys.argv)
calculator = Calculator()
calculator.show()
sys.exit(app.exec_())
