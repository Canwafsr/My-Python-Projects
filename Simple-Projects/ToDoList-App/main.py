import sys
from PyQt5.QtWidgets import *

class ToDoList(QWidget):
    def __init__(self):
        super().__init__()
        self.todo_list = []  # This list will store the tasks.
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle("To Do List Program")
        self.setGeometry(100, 200, 500, 500)

        main_layout = QHBoxLayout()  # Main layout as a horizontal layout.
        left_layout = QVBoxLayout()  # Vertical layout for task list on the left.
        right_layout = QVBoxLayout()  # Vertical layout for input field and buttons on the right.

        # Task list (Left side)
        self.task_list_widget = QListWidget()  # Widget to list tasks using QListWidget.
        left_layout.addWidget(self.task_list_widget)  # Add widget to the left layout.

        # Input field and buttons (Right side)
        self.task_input = QLineEdit()  # QLineEdit for entering new tasks.
        self.task_input.setPlaceholderText("Input a task.")  # Placeholder text for input field.
        right_layout.addWidget(self.task_input)  # Add input field to the right layout.

        add_button = QPushButton("Add Task")  # Button to add a task.
        add_button.clicked.connect(self.add_task)  # Connect the button click to add_task method.
        right_layout.addWidget(add_button)  # Add button to the right layout.

        remove_button = QPushButton("Remove Task")  # Button to remove a task.
        remove_button.clicked.connect(self.remove_task)  # Connect the button click to remove_task method.
        right_layout.addWidget(remove_button)  # Add button to the right layout.

        main_layout.addLayout(left_layout)  # Add left layout to the main layout.
        main_layout.addLayout(right_layout)  # Add right layout to the main layout.

        self.setLayout(main_layout)  # Set the main layout for the window.

    def add_task(self):
        task = self.task_input.text()  # Get the task entered by the user.

        if task:  # If the input is not empty, proceed.
            self.todo_list.append(task)  # Add the task to our list.
            self.task_list_widget.addItem(task)  # Add the task to QListWidget.
            self.task_input.clear()  # Clear the input field.

    def remove_task(self):
        selected_items = self.task_list_widget.selectedItems()  # Get the selected items.
        if not selected_items:  # If no item is selected, do nothing.
            return
        for item in selected_items:  # Iterate over selected items.
            task = item.text()  # Get the text of the item.
            self.todo_list.remove(task)  # Remove the task from our list.
            self.task_list_widget.takeItem(self.task_list_widget.row(item))  # Remove the item from QListWidget.


if __name__ == "__main__":
    app = QApplication(sys.argv)  # Start the PyQt application.
    window = ToDoList()  # Create a window instance of ToDoList class.
    window.show()  # Show the window.
    sys.exit(app.exec_())  # Execute the application and wait for the exit.
