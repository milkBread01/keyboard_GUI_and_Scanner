from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QComboBox, QPushButton, QGridLayout, QCheckBox, QSizePolicy
)
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Keypad Mapper")
        self.setGeometry(500, 300, 800, 600)

        # Main layout
        main_layout = QVBoxLayout()

        self.header(main_layout)
        self.mainBody(main_layout)
        self.footer(main_layout)
        self.setLayout(main_layout)

    # =================== Header ===================
    def header(self, main_layout):
        header_container = QWidget()
        header_container.setObjectName("header")  # Assign ID for styling

        header_layout = QGridLayout()
        
        label_profile = QLabel("Profile:")
        label_version = QLabel("Ver. x.x.x")
        toggle = QCheckBox("light")
        toggle.setObjectName("themeToggle")
        toggle.setChecked(True)
        dropdown = QComboBox()
        dropdown.addItems(["Default", "Gaming", "Coding"])

        header_layout.addWidget(label_profile, 0, 0)
        header_layout.addWidget(toggle, 1, 0)
        header_layout.addWidget(dropdown, 0, 1)
        header_layout.addWidget(label_version, 1, 1)


        header_container.setLayout(header_layout)
        main_layout.addWidget(header_container)


    # =================== Main Body ===================
    def mainBody(self, main_layout):
        keypad_container = QWidget()
        keypad_container.setObjectName("body")

        grid_layout = QGridLayout()

        # Key placement map: key_number → (row, col, rowspan, colspan)
        key_map = {
            "TEST": (0, 0, 1, 1), 2: (0, 1, 1, 1), 3: (0, 2, 1, 1), 4: (0, 3, 1, 1), 5: (0, 4, 1, 1),
            6: (1, 0, 1, 1), 7: (1, 1, 1, 1), 8: (1, 2, 1, 1), 9: (1, 3, 2, 1), 10: (1, 4, 1, 1),
            11: (2, 0, 1, 1), 12: (2, 1, 1, 1), 13: (2, 2, 1, 1), 14: (2, 4, 1, 1),
            15: (3, 0, 1, 1), 16: (3, 1, 1, 1), 17: (3, 2, 1, 1), 18: (3, 3, 2, 1), 19: (3, 4, 1, 1),
            20: (4, 0, 1, 2), 21: (4, 2, 1, 1), 22: (4, 4, 1, 1)
        }

        for key, (r, c, rs, cs) in key_map.items():
            btn = QPushButton(str(key))
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            grid_layout.addWidget(btn, r, c, rs, cs)

        # Ensure each row and column expands equally
        for i in range(5):  # You have 5 columns
            grid_layout.setColumnStretch(i, 1)

        for i in range(5):  # You have 5 rows
            grid_layout.setRowStretch(i, 1)

        keypad_container.setLayout(grid_layout)
        main_layout.addWidget(keypad_container)

    # =================== Footer ===================
    def footer(self, main_layout):
        footer_container = QWidget()
        footer_container.setObjectName("footer")

        footer_layout = QHBoxLayout()
        save_button = QPushButton("Save Profile")
        delete_button = QPushButton("Delete Profile")

        footer_layout.addWidget(save_button)
        footer_layout.addWidget(delete_button)
        footer_container.setLayout(footer_layout)

        main_layout.addWidget(footer_container)

    def setLayout(self, main_layout):
        # Set layout to main widget
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

def load_stylesheet(path):
    with open(path, "r") as f:
        return f.read()

def main():
    app = QApplication(sys.argv)
    # Load the external stylesheet
    app.setStyleSheet(load_stylesheet("styles.qss"))
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
