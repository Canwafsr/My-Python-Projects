import sys, random, time
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *




class MainScreen(QWidget):
    def __init__(self, name, energy = 50, health = 5, computer_energy = 50, computer_health = 5):
        super().__init__()

        self.computer_name = "Computer"
        self.computer_health = computer_health
        self.computer_energy = computer_energy

        self.name = name

        self.energy = energy
        self.health = health
        self.damage = 0

        self.setWindowTitle("Hit and Run")
        self.resize(640,480)

        self.top_h_box = QHBoxLayout()
        self.middle_h_box = QHBoxLayout()

        self.major_v_box = QGridLayout()
        self.middle_v_box = QVBoxLayout()

        player_label = QLabel("\t\tYour Situation")
        computer_label = QLabel("\t\tComputer Situation")

        self.top_h_box.addWidget(player_label)
        self.top_h_box.addWidget(computer_label)

        self.your_health_label = QLabel(f"Health: {self.health}")
        self.your_energy_label = QLabel(f"Energy: {self.energy}")

        self.middle_v_box.addWidget(self.your_health_label)
        self.middle_v_box.addWidget(self.your_energy_label)

        self.major_v_box.addLayout(self.top_h_box,0,1)
        self.major_v_box.addLayout(self.middle_v_box,0,2)


        self.setLayout(self.major_v_box)

    def attack(self, computer):
        
        result = random.randint(0, 2)

        if result == 0:
            QMessageBox.information(self, "Draw", "The attack failed, but he couldn't attack either.\nDraw !")

        elif result == 1:
            self.calculate_attack(computer)
            QMessageBox.information(self, "Won", "The attack is successful, you damage the opponent.")
            
        elif result == 2:
            QMessageBox.warning(self, "Failure", "The attack failed and the opponent attacked you.\nYou took damage!")
    
    def run(self):
        result = random.randint(0,100)

        if result <= 25:
            self.calculate_attack(self)
            QMessageBox.warning(self, "Failure", "You tripped while running and the opponent caught you off guard.\nYou took damage!")
        else:
            QMessageBox.information(self, "Partial Success","You managed to escape from the pursuer but he found you again.\nGet ready!")
    
    def current_status(self):
        pass

    def calculate_attack(self, took_hit):
        took_hit.damage += 1
        took_hit.energy -= 1

        if took_hit.damage % 5 == 0:
            took_hit.health -= 1

        if took_hit.health < 1:
            took_hit.energy = 0
            QMessageBox.information(self, f"{self.name} won this game...")
            self.close()



        



app = QApplication(sys.argv)

window = MainScreen("You")
window.show()

app.exec()

