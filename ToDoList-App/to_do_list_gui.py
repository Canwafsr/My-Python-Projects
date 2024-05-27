import sys
from PyQt5.QtWidgets import *

class ToDoList(QWidget):
    def __init__(self):
        super().__init__()
        self.todo_list = []
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle("To Do List Program")
        self.setGeometry(100, 200, 500, 500)

        main_layout = QHBoxLayout()
        left_layout = QVBoxLayout()
        right_layout = QVBoxLayout()

        # Task list (Left side)

        self.task_list_widget = QListWidget()
        left_layout.addWidget(self.task_list_widget)


        # Buttons (Right side)
        self.task_input = QLineEdit()
        self.task_input.setPlaceholderText("Input a task.")
        right_layout.addWidget(self.task_input)

        add_button = QPushButton("Add Task")
        add_button.clicked.connect(self.add_task)
        right_layout.addWidget(add_button)


        remove_button = QPushButton("Remove Task")
        remove_button.clicked.connect(self.remove_task)
        right_layout.addWidget(remove_button)

        main_layout.addLayout(left_layout)
        main_layout.addLayout(right_layout)

        self.setLayout(main_layout)

    def add_task(self):
        task = self.task_input.text()

        if task:
            self.todo_list.append(task)
            self.task_list_widget.addItem(task)
            self.task_input.clear()

    def remove_task(self):
        selected_items = self.task_list_widget.selectedItems()
        if not selected_items:
            return
        for item in selected_items:
            task = item.text()
            self.todo_list.remove(task)
            self.task_list_widget.takeItem(self.task_list_widget.row(item))



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ToDoList()
    window.show()
    sys.exit(app.exec_())