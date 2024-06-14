import sys
import os
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.initUI()
        
    def initUI(self):
        
        self.resize(480,440)
        self.move(650, 100)

        v_layout = QVBoxLayout(self)

        self.image_layout = QLabel(self)

        current_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(current_dir, 'images', 'login_image.png')

        self.image_layout.setPixmap(QPixmap(image_path))
        self.image_layout.setAlignment(Qt.AlignHCenter)

        v_layout.addWidget(self.image_layout)
        v_layout.addStretch()

        self.username = QLabel("Username:",self)
        v_layout.addWidget(self.username)

        self.input_username = QLineEdit()
        self.input_username.setPlaceholderText("username is 'admin'")
        v_layout.addWidget(self.input_username)

        self.password = QLabel("Password:", self)
        v_layout.addWidget(self.password)

        self.input_password = QLineEdit()
        self.input_password.setPlaceholderText("password is '1234'")
        self.input_password.setEchoMode(QLineEdit.Password)
        v_layout.addWidget(self.input_password)

        self.login_button = QPushButton("Login --You can also press enter--")
        self.login_button.setShortcut(Qt.Key_Return)
        self.login_button.clicked.connect(self.login)
        v_layout.addWidget(self.login_button)
        
        self.quit_button = QPushButton("Quit")
        self.quit_button.setShortcut("Alt+F4")
        self.quit_button.clicked.connect(self.quit)
        v_layout.addWidget(self.quit_button)

        self.setLayout(v_layout)

    def login(self):
        username = self.input_username.text()
        password = self.input_password.text()

        if (username == "admin" and password == "1234"):
            QMessageBox.information(self, "Information", "Login successful")
            self.start_program()
            self.close()
        else:
            QMessageBox.warning(self,"Login failed" ,"username and password are incorrect")

    def start_program(self):
        self.start = ATM()
        self.start.show()

    def quit(self):
        self.close()
        
class ATM(QWidget):
    def __init__(self):
        super().__init__()
        self.balanceUSD = 5000   
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle("ATM Machine Program")
        self.setGeometry(600, 200, 700, 700)        
        
        self.main_layout = QVBoxLayout(self)
        self.grid = QGridLayout()

        self.balance = QLabel(f"Your Balance: {self.balanceUSD} $",self)
        self.main_layout.addWidget(self.balance)

        self.Qline = QLineEdit()
        self.Qline.setPlaceholderText("Enter value for any transaction")
        self.main_layout.addWidget(self.Qline)
        
        buttons = [
            ("Deposit", self.deposit),
            ("Withdrawal", self.withdrawal),
            ("Money Transfer", self.money_transfer),
            ("Pay Debt", self.pay_debt),
        ]

        positions = [(i, j) for i in range(2) for j in range(2)]
        for position, (label, func) in zip(positions, buttons):
            button = QPushButton(label)
            button.clicked.connect(func)
            self.grid.addWidget(button, *position)

        self.main_layout.addLayout(self.grid)

        self.setLayout(self.main_layout)

    def deposit(self):
        QMessageBox.information(self, 'Information', 'Deposit clicked')

    def withdrawal(self):
        self.open_window = WithdrawalWindow(self.balanceUSD)
        self.open_window.balance_changed.connect(self.update_balance)
        self.open_window.show()

    def money_transfer(self):
        QMessageBox.information(self, 'Information', 'Money Transfer clicked')
        
    def pay_debt(self):
        QMessageBox.information(self, 'Information', 'Pay Debt clicked')

    def update_balance(self, new_balance):
        self.balanceUSD = new_balance
        self.balance.setText(f"Your Balance: {self.balanceUSD} $")

class WithdrawalWindow(QWidget):
    balance_changed = pyqtSignal(int)  # Signal to communicate balance changes

    def __init__(self, balanceUSD):
        super().__init__()
        self.balanceUSD = balanceUSD
        self.setWindowTitle("Withdrawal")
        self.setGeometry(750, 250, 300, 300)

        self.vbox_layout = QVBoxLayout()       
        
        self.hbox_layout = QHBoxLayout()
        self.minor_hbox_layout = QHBoxLayout()
        self.minor_hbox_layout2 = QHBoxLayout() 

        self.balance = QLabel(f"Your Balance: {self.balanceUSD} $",self)
        self.vbox_layout.addWidget(self.balance)        

        self.money = QLabel("Enter the amount to be sent")
        self.input_money = QLineEdit()
        self.currency = QLabel("$")

        self.label = QLabel("Enter an IBAN",self)

        self.label2 = QLabel("TR",self)
        self.iban = QLineEdit()
        self.iban.setText("TR")
        self.iban.textChanged.connect(self.ensure_tr_prefix)
        
        self.cancel_button = QPushButton("Cancel")
        self.approve_button = QPushButton("Approve")        

        self.vbox_layout.addWidget(self.money)
        self.minor_hbox_layout2.addWidget(self.input_money)
        self.minor_hbox_layout2.addWidget(self.currency)
        self.vbox_layout.addWidget(self.label)
        
        self.hbox_layout.addWidget(self.label2)
        self.hbox_layout.addWidget(self.iban)
        
        self.minor_hbox_layout.addWidget(self.cancel_button)
        self.minor_hbox_layout.addWidget(self.approve_button)
        
        self.vbox_layout.addLayout(self.hbox_layout)
        self.vbox_layout.addLayout(self.minor_hbox_layout2)
        self.vbox_layout.addLayout(self.minor_hbox_layout)

        self.setLayout(self.vbox_layout)

        self.cancel_button.clicked.connect(self.close)
        self.approve_button.clicked.connect(self.process)

    def ensure_tr_prefix(self):
        if not self.iban.text().startswith("TR"):
            self.iban.setText("TR" + self.iban.text()[2:])

    def process(self):
        money_text = self.input_money.text()
        try:
            money = int(money_text)
            if self.balanceUSD >= money:
                self.balanceUSD -= money
                self.balance_changed.emit(self.balanceUSD)
                QMessageBox.information(self, "Success", "Transaction completed")
                self.close()
            else:
                QMessageBox.warning(self, "Error", "Insufficient balance")
        except ValueError:
            QMessageBox.warning(self, "Error", "Invalid amount")


app = QApplication(sys.argv)
login_window = LoginWindow()
login_window.show()
sys.exit(app.exec_())
