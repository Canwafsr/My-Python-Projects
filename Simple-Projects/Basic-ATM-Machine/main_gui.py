import re, sys, os
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QWidget

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
        self.balanceUSD = 5000.32  
        self.debtUSD = 1700.59
        self.initUI()
        

    def initUI(self):
        self.setWindowTitle("ATM Machine Program")
        self.setGeometry(600, 200, 480, 400)        
        
        self.main_layout = QVBoxLayout(self)
        self.grid = QGridLayout()

        self.balance = QLabel(f"Your Balance: {self.balanceUSD:.2f} $",self)
        self.main_layout.addWidget(self.balance)

        self.debtLabel = QLabel(f"Your Debt: {self.debtUSD:.2f} $", self)
        self.main_layout.addWidget(self.debtLabel)
        
        self.money_transfer_button = QPushButton()
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
        self.open_depositWindow = DepositWindow(self.balanceUSD)
        self.open_depositWindow.balance_changed.connect(self.update_balance)
        self.open_depositWindow.show()
    def withdrawal(self):
        self.open_withdrawalWindow = WithdrawalWindow(self.balanceUSD)
        self.open_withdrawalWindow.balance_changed.connect(self.update_balance)
        self.open_withdrawalWindow.show()   
    def money_transfer(self):
        self.open_money_transfer_window = MoneyTransferWindow(self.balanceUSD)
        self.open_money_transfer_window.balance_changed.connect(self.update_balance)
        self.open_money_transfer_window.show()
    def pay_debt(self):
        self.open_pay_debt_window = PayDebt(self.balanceUSD,self.debtUSD)
        self.open_pay_debt_window.balance_changed.connect(self.update_balance)
        self.open_pay_debt_window.debt_changed.connect(self.update_debt)
        self.open_pay_debt_window.show()
    def update_balance(self, new_balance):
        self.balanceUSD = new_balance
        self.balance.setText(f"Your Balance: {self.balanceUSD:.2f} $")

    def update_debt(self, new_debt):
        self.debtUSD = new_debt
        self.debtLabel.setText(f"Your Debt: {self.debtUSD:.2f} $")

class MoneyTransferWindow(QWidget):
    balance_changed = pyqtSignal(float)

    def __init__(self, balanceUSD):
        super().__init__()
        self.balanceUSD = balanceUSD
        self.setWindowTitle("Money Transfer")
        self.setGeometry(750,250,300,300)

        self.vbox_layout = QVBoxLayout()       
        
        self.hbox_layout = QHBoxLayout()
        self.minor_hbox_layout = QHBoxLayout()
        self.minor_hbox_layout2 = QHBoxLayout() 

        self.balance = QLabel(f"Your Balance: {self.balanceUSD:.2f} $",self)
        self.vbox_layout.addWidget(self.balance)        

        self.money = QLabel("Enter the amount to be sent")
        self.input_money = QLineEdit()
        self.currency = QLabel("$")

        self.label = QLabel("Enter an IBAN",self)

        self.iban = QLineEdit()        
        self.iban.setText("TR")
        self.iban.textChanged.connect(self.ensure_tr_prefix)

        self.cancel_button = QPushButton("Cancel")
        self.approve_button = QPushButton("Approve")        

        
        self.minor_hbox_layout2.addWidget(self.input_money)
        self.minor_hbox_layout2.addWidget(self.currency)
        self.vbox_layout.addWidget(self.label)
        
        
        self.vbox_layout.addWidget(self.iban)
        self.vbox_layout.addWidget(self.money)
        
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
        iban_text = self.iban.text()

        if not self.validate_iban(iban_text):
            QMessageBox.warning(self, "Error", "Invalid IBAN. It must be 26 characters long and contain only digits after 'TR'.")
            return
        try:
            money = float(money_text)
            if self.balanceUSD >= money:
                self.balanceUSD -= money
                self.balance_changed.emit(self.balanceUSD)
                QMessageBox.information(self, "Success", "Transaction completed")
                self.close()
            else:
                QMessageBox.warning(self, "Error", "Insufficient balance")
        except ValueError:
            QMessageBox.warning(self, "Error", "Invalid amount")
    def validate_iban(self, iban):
        if len(iban) != 26:
            return False
        if not iban.startswith("TR"):
            return False
        if not re.match(r"^TR\d{24}$", iban):
            return False
        return True
        

class DepositWindow(QWidget):
    balance_changed = pyqtSignal(float)

    def __init__(self, balanceUSD):
        super().__init__()
        self.balanceUSD = balanceUSD
        self.setWindowTitle("Deposit")
        self.setGeometry(750,250,300,300)

        self.v_box = QVBoxLayout()
        self.h_box = QHBoxLayout()

        self.showBalance = QLabel(f"Your balance: {self.balanceUSD:.2f} $")
        

        self.balance = QLabel("How much money do you want to deposit?")
        self.addBalance = QLineEdit()
        self.currency = QLabel("$")

        self.cancelButton = QPushButton("Cancel")
        self.okayButton = QPushButton("Okay")

        self.v_box.addWidget(self.showBalance)
        self.v_box.addWidget(self.balance)
        self.v_box.addWidget(self.addBalance)

        self.h_box.addWidget(self.cancelButton)
        self.h_box.addWidget(self.okayButton)
        
        self.v_box.addLayout(self.h_box)

        self.setLayout(self.v_box)

        self.cancelButton.clicked.connect(self.close)
        self.okayButton.clicked.connect(self.deposit)

    def deposit(self):
        money_text = self.addBalance.text()

        try:
            money = float(money_text)            
            self.balanceUSD += money
            self.balance_changed.emit(self.balanceUSD)
            QMessageBox.information(self, "Success", "Deposit completed")
            self.close()      
        except ValueError:
            QMessageBox.warning(self, "Error", "Invalid Type")


class WithdrawalWindow(QWidget):
    balance_changed = pyqtSignal(float)

    def __init__(self, balanceUSD):
        super().__init__()
        self.balanceUSD = balanceUSD
        self.setWindowTitle("Withdrawal")
        self.setGeometry(750,250,300,300)

        self.v_box = QVBoxLayout()
        self.h_box = QHBoxLayout()
        
        self.showBalance = QLabel(f"Your Balance: {self.balanceUSD:.2f} $")

        self.withdrawalLabel = QLabel("How much do you want to withdraw from your account?")
        self.input_withdrawal = QLineEdit()

        self.cancelButton = QPushButton("Cancel")
        self.okayButton = QPushButton("Okay")

        self.v_box.addWidget(self.showBalance)
        self.v_box.addWidget(self.withdrawalLabel)
        self.v_box.addWidget(self.input_withdrawal)

        self.h_box.addWidget(self.cancelButton)
        self.h_box.addWidget(self.okayButton)

        self.v_box.addLayout(self.h_box)
        self.setLayout(self.v_box)

        self.cancelButton.clicked.connect(self.close)
        self.okayButton.clicked.connect(self.withdrawal)


    def withdrawal(self): 
        money_text = self.input_withdrawal.text()

        try:
            money = float(money_text)

            if money < self.balanceUSD:
                self.balanceUSD -= money
                self.balance_changed.emit(self.balanceUSD)
                QMessageBox.information(self, "Success", "Withdrawal completed")
                self.close()

            else:
                QMessageBox.warning(self, "Error", "Insufficient balance")

        except ValueError:
            QMessageBox.warning(self, "Error", "Invalid Type")



class PayDebt(QWidget):
    balance_changed = pyqtSignal(float)
    debt_changed = pyqtSignal(float)

    def __init__(self, balanceUSD, debtUSD):
        super().__init__()
        self.balanceUSD = balanceUSD
        self.debtUSD = debtUSD
        self.setWindowTitle("Pay Debt")
        self.setGeometry(750,250,300,300)

        self.v_box = QVBoxLayout()
        self.h_box = QHBoxLayout()

        self.balanceLabel = QLabel(f"Your Balance: {self.balanceUSD:.2f} $", self)
        self.debtLabel = QLabel(f"Your Debt: {self.debtUSD:.2f} $", self)

        self.question = QLabel(f"How much do you wanna pay ?",self)
        self.input_quantity = QLineEdit()

        self.cancel_button = QPushButton("Cancel")
        self.okay_button = QPushButton("Okay")

        self.v_box.addWidget(self.balanceLabel)
        self.v_box.addWidget(self.debtLabel)
        self.v_box.addWidget(self.question)
        self.v_box.addWidget(self.input_quantity)

        self.h_box.addWidget(self.cancel_button)
        self.h_box.addWidget(self.okay_button)

        self.v_box.addLayout(self.h_box)

        self.setLayout(self.v_box)


        self.cancel_button.clicked.connect(self.close)
        self.okay_button.clicked.connect(self.pay_debt)


    def pay_debt(self):
        money_text = self.input_quantity.text()

        try:
            money = float(money_text)
            if (money < self.debtUSD) and (money < self.balanceUSD):
                self.debtUSD -= money
                self.balanceUSD -= money
                
                self.balance_changed.emit(self.balanceUSD)
                self.debt_changed.emit(self.debtUSD)

                QMessageBox.information(self, "Success", "Payment completed")
                self.close()

            else:
                QMessageBox.warning(self, "Error", "You cannot pay more than your debt")

        except ValueError:
            QMessageBox.warning(self, "Error", "Invalid Type")

app = QApplication(sys.argv)
login_window = LoginWindow()
login_window.show()
sys.exit(app.exec_())