from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QPushButton, QGridLayout, QCheckBox, QSizePolicy, QDialog, QRadioButton, QButtonGroup, QLineEdit, QInputDialog, QMessageBox, QFileDialog
)
from PySide6.QtCore import Qt
import sys
import os
import json

class LCDconfigDialog(QDialog):
    def __init__(self, media_data=None):
        super().__init__()

        self.setWindowTitle(f"Configure LCD Screen")
        self.setMinimumSize(400, 300)

        self.result = {}  # Store config result

        layout=QVBoxLayout()

        self.add_button = QPushButton("+\nAdd Media")
        self.add_button.setFixedSize(150,100)
        self.add_button.clicked.connect(self.open_file_dialog)
        layout.addWidget(self.add_button, alignment=Qt.AlignHCenter)

        self.path_field = QLineEdit()
        self.path_field.setReadOnly(True)

        layout.addWidget(QLabel("File Path:"))
        layout.addWidget(self.path_field)

        # buttons
        button_layout = QHBoxLayout()
        save_btn = QPushButton("Save")
        cancel_btn = QPushButton("Cancel")
        save_btn.clicked.connect(self.save)
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(save_btn)
        button_layout.addWidget(cancel_btn)

        layout.addLayout(button_layout)
        self.setLayout(layout)

        if media_data:
            self.path_field.setText(media_data.get("VALUE", ""))
    
    def save(self):
        path = self.path_field.text()
        ext = os.path.splitext(path)[1].lower()

        if ext in [".gif"]:
            media_type = "gif"
        elif ext in [".mp4", ".mov", ".avi", ".webm"]:
            media_type = "video"
        elif ext in [".png", ".jpg", ".jpeg",".svg"]:
            media_type = "image"
        else:
            media_type = "unknown"

        self.result = {
            "TYPE":media_type,
            "VALUE":path
        }
        self.accept()

    def open_file_dialog(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Media File", "", "Media Files (*.png *.jpg *.jpeg *.gif *.mp4 *.mov *.avi *.webm)"
        )
        if file_path:
            self.path_field.setText(file_path)

class KeyConfigDialog(QDialog):
    def __init__(self, key_label, key_data=None):
        super().__init__()
        self.setWindowTitle(f"Configure Key: {key_label}")
        self.setMinimumSize(400, 300)

        self.result = {}  # Store config result

        layout = QVBoxLayout()

        # Header label
        layout.addWidget(QLabel("Key Name:"))
        self.key_name_input = QLineEdit()
        self.key_name_input.setText(str(key_label))
        layout.addWidget(self.key_name_input)


        # Radio buttons for type selection
        self.type_group = QButtonGroup(self)
        radio_layout = QHBoxLayout()
        for i, option in enumerate(["Character/Sentence", "Application", "Website", "Command"]):
            btn = QRadioButton(option)
            if i == 0:
                btn.setChecked(True)
            self.type_group.addButton(btn, i)
            radio_layout.addWidget(btn)
        layout.addLayout(radio_layout)

        # Input fields
        self.char_input = QLineEdit()
        self.app_input = QLineEdit()
        self.web_input = QLineEdit()
        self.command_input = QLineEdit()

        """ load values into text field """

        # If existing key data was passed, fill it
        if key_data:
            # Set key name
            self.key_name_input.setText(key_data.get("LABEL", str(key_label)))

            # Set correct radio button
            type_map = {
                "character": 0,
                "application": 1,
                "website": 2,
                "command": 3
            }
            type_index = type_map.get(key_data.get("TYPE", "").lower(), 0)
            button = self.type_group.button(type_index)
            if button:
                button.setChecked(True)

            # Fill input fields
            self.char_input.setText(key_data.get("VALUE", "") if key_data.get("TYPE") == "character" else "")
            self.app_input.setText(key_data.get("VALUE", "") if key_data.get("TYPE") == "application" else "")
            self.web_input.setText(key_data.get("VALUE", "") if key_data.get("TYPE") == "website" else "")
            self.command_input.setText(key_data.get("VALUE", "") if key_data.get("TYPE") == "command" else "")

        """  """

        layout.addWidget(QLabel("Character or Expression:"))
        layout.addWidget(self.char_input)
        layout.addWidget(QLabel("Application:"))
        layout.addWidget(self.app_input)
        layout.addWidget(QLabel("Website:"))
        layout.addWidget(self.web_input)
        layout.addWidget(QLabel("Command:"))
        layout.addWidget(self.command_input)

        # Buttons
        button_layout = QHBoxLayout()
        save_btn = QPushButton("Save Key")
        cancel_btn = QPushButton("Cancel")
        save_btn.clicked.connect(self.save)
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(save_btn)
        button_layout.addWidget(cancel_btn)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def save(self):
        selected_type = self.type_group.checkedButton().text().lower()
        self.result = {
            "label": self.key_name_input.text(),
            "type": selected_type,
            "character": self.char_input.text(),
            "application": self.app_input.text(),
            "website": self.web_input.text()
        }
        self.accept()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Calling profile manager class
        from ProfileManager import ProfileManager
        # initializing profile_manager. will contain
        self.profile_manager = ProfileManager()

        # initializing key_buttons. will contain
        self.key_buttons = {}

        # define dropdown menu early so it's available to all methods
        self.dropdown = QComboBox()  

        # Call function in the event of dropdown menu name change
        # if name == "+ New Profile" open pop up to create new profile
        # if name != "+ New Profile" call profile_manager.switch_profile()
        self.dropdown.currentTextChanged.connect(self.change_profile)

        # Set main window title and GUI dimensions
        self.setWindowTitle("Keypad Mapper")
        self.setGeometry(500, 300, 400, 600)

        # Creating Main layout
        main_layout = QVBoxLayout()

        # Calling different functions which contain the different parts of the main GUI
        self.header(main_layout)
        self.mainBody(main_layout)
        self.footer(main_layout)
        self.setLayout(main_layout)

        # After header is built, fill the dropdown
        self.refresh_profile_dropdown()
        self.update_key_labels()

    # In the event that the user selects an item from the dropdown menu this function is called. if the name of the item is "+ New Profile" then a dialog box is opened to prompt the user to create a new entity. if the name is not "+ New Profile" then the profile will simply be switched 
    def change_profile(self, name):
        # checking if name is specified name to create new profile
        if name == "+ New Profile":
            # event yes
            # opening dialog box with tab title "New Profile" and body text "Enter profile name: ". 
            # new_name (type str) and ok (type bool) contain the user input name and answer to confirmation button "OK" or "Cancel"
            new_name, ok = QInputDialog.getText(self, "New Profile", 
            "Enter profile name:")
            # if ok is True and new_name is ! empty
            if ok and new_name:
                # calling add_profiles(self, profile_name) function from the class ProfileManager. sending new_name as profile_name. if condition is evaluating returned value.
                # Called function returns True if profile does not already exist
                # Called function returns False if profile already exists
                if self.profile_manager.add_profiles(new_name):
                    # refresh_profile_dropdown(self) function is called, appending the newley created profile
                    self.refresh_profile_dropdown()
                    # setting current display value to the created profile
                    self.dropdown.setCurrentText(new_name)
                
                # If false returned then display an error message of Duplicate profile
                else:
                    QMessageBox.warning(self, "Duplicate", "Profile already exists.")

    def set_active_profile(self):
        selected_profile = self.dropdown.currentText()

        if selected_profile == "+ New Profile":
            return

        if selected_profile == self.profile_manager.current_profile_name:
            # Already current in memory but check if it is primary
            if self.profile_manager.profiles[selected_profile].get("primary", False):
                QMessageBox.information(self, "Already Active", f"'{selected_profile}' is already the active profile.")
                return

        confirm = QMessageBox.question(
            self,
            "Set Active Profile",
            f"Set '{selected_profile}' as the active profile?",
            QMessageBox.Yes | QMessageBox.No
        )

        if confirm == QMessageBox.Yes:
            self.profile_manager.switch_profile(selected_profile)
            self.refresh_profile_dropdown()
            self.update_key_labels()
            QMessageBox.information(self, "Active Profile Changed", f"Profile '{selected_profile}' is now active.")

    def update_key_labels(self):
        # calls the method get_current_profile(self) from the class ProfileManager. returns the current profile name
        profile = self.profile_manager.get_current_profile()
        # if profile doesnt exist, return nothing
        if not profile:
            return
        # iterates through key:value pairs of key label: button
        for pos_key, button in self.key_buttons.items():
            label = profile["keys"].get(pos_key, {}).get("LABEL", pos_key)
            button.setText(label)
    
    # changes the list of keys available in the dropdown menu
    def refresh_profile_dropdown(self):
        # blocking 
        self.dropdown.blockSignals(True)
        # clearing dropdown menu
        self.dropdown.clear()
        # calling get_profile_names(self) from Class ProfileManager. this method simply returns the profile keys in the dictonary, these keys are the names of the profiles
        profiles = self.profile_manager.get_profile_names()
        # appending the key names and the action name of "+ New Profile"
        self.dropdown.addItems(profiles + ["+ New Profile"])
        # setting the displayed profile name by accessing the variable defined in the class ProfileManager. this variable stores the current selected profile
        self.dropdown.setCurrentText(self.profile_manager.current_profile_name)
        # Allowing input again
        self.dropdown.blockSignals(False)

    # =================== Header ===================
    # taking in the main_layout Vertical box layout and creating sub layout
    def header(self, main_layout):
        # creating header container for the contents of the container 
        header_container = QWidget()
        # Assigning ID tag for styling in qss file
        header_container.setObjectName("header")  
        # Assigning the container a grid layout
        header_layout = QGridLayout()
        # Label containing the current profile 
        label_profile = QLabel("Profile:")
        # Creating label containing current version of the app
        #label_version = QLabel("Ver. x.x.x")

        self.set_active_button = QPushButton("Set As Active")
        self.set_active_button.clicked.connect(self.set_active_profile)

        # Creating the checkbox for light or dark mode
        toggle = QCheckBox("light")
        # assigning checkbox an ID for styling in qss file 
        toggle.setObjectName("themeToggle")
        # Set True by defualt
        toggle.setChecked(True)

        # Appending items to the dropdown menu from the profileManager class and get_profile_names method and the event name "+ New Profile"
        self.dropdown = QComboBox()
        self.dropdown.addItems(self.profile_manager.get_profile_names() + ["+ New Profile"])
        # currentTextChanged is a Qt signal that is emmitted every time the selected text in the dropdown menu changes
        # the connect() links the signal to the change_profile() method which runs when the dropdown is changed by the user
        self.dropdown.currentTextChanged.connect(self.change_profile)

        # adding widgets to different areas of the header
        header_layout.addWidget(label_profile, 0, 0)
        header_layout.addWidget(toggle, 1, 0)
        header_layout.addWidget(self.dropdown, 0, 1)
        header_layout.addWidget(self.set_active_button, 1, 1)

        # calling the setLayout(self, main_layout) and sending header_layout as main_layout
        header_container.setLayout(header_layout)
        # assigning header container to main layout
        main_layout.addWidget(header_container)

    # =================== Main Body ===================
    def mainBody(self, main_layout):
        keypad_container = QWidget()
        keypad_container.setObjectName("body")

        """ LCD and Dial Section """
        # ---- LCD Screen and Dial Section ----
        top_section = QWidget()
        top_layout = QHBoxLayout()
        top_section.setLayout(top_layout)

        # LCD Screen Button
        self.lcd_button = QPushButton("LCD Screen")
        self.lcd_button.setFixedSize(200, 100)  # Width x Height
        self.lcd_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.lcd_button.setObjectName("lcdScreen")  # For QSS styling if needed
        top_layout.addWidget(self.lcd_button)

        self.lcd_button.clicked.connect(self.lcd_clicked)

        # Spacer between LCD and Dial
        top_layout.addStretch()

        # Dial Button (Circle)
        self.dial_button = QPushButton("")
        self.dial_button.setFixedSize(80, 80)
        self.dial_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.dial_button.setObjectName("dialButton")  # For QSS styling if needed
        top_layout.addWidget(self.dial_button)

        main_layout.addWidget(top_section)
        """  """

        grid_layout = QGridLayout()
        self.key_buttons = {}

        profile = self.profile_manager.get_current_profile()
        if not profile:
            return

        # Correct fixed positions
        expected_positions = [
            "0-0", "0-1", "0-2", "0-3", "0-4",
            "1-0", "1-1", "1-2", "1-3", "1-4",
            "2-0", "2-1", "2-2", "2-4",
            "3-0", "3-1", "3-2", "3-3", "3-4",
            "4-0", "4-2", "4-4"
        ]

        span_keys_id_vertical = {"1-3", "3-3"}
        span_keys_id_horizontal = {"4-0"}

        for pos_key in expected_positions:
            if pos_key in profile["keys"]:
                data = profile["keys"][pos_key]
                label = data.get("LABEL", pos_key)

                row, col = map(int, pos_key.split("-"))
                btn = QPushButton(label)
                btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                btn.clicked.connect(lambda _, k=pos_key: self.keys_clicked(k))

                rowspan, colspan = 1, 1
                if pos_key in span_keys_id_vertical:
                    rowspan = 2
                if pos_key in span_keys_id_horizontal:
                    colspan = 2

                grid_layout.addWidget(btn, row, col, rowspan, colspan)
                self.key_buttons[pos_key] = btn

        # Ensure rows and columns expand equally
        for i in range(5):
            grid_layout.setColumnStretch(i, 1)
            grid_layout.setRowStretch(i, 1)

        keypad_container.setLayout(grid_layout)
        main_layout.addWidget(keypad_container)

    def lcd_clicked(self):
        profile = self.profile_manager.get_current_profile()
        dialog = LCDconfigDialog(profile.get("media", None))

        if dialog.exec():
            profile["media"] = dialog.result


    # argument: grid position of button (e.g 3-3, 1-2, etc)
    def keys_clicked(self, key):
        # Calls the get_current+profile() methid from ProfileManager class to retrieve current active profile. profile contains a dictionary with name, keys, and value
        profile = self.profile_manager.get_current_profile()

        # storing keys and values for the key 'keys' and the level 2 key of the specified grid position
        key_data = profile["keys"].get(key, None)

        # calls KeyConfigDialog() class and passes btn grid position and profile values for key 'keys'
        dialog = KeyConfigDialog(key, key_data)

        # if user clicks 'save' continue with if elif else dont. 
        if dialog.exec():
            # Stores the dictionary saved in the method save()
            """ 
                "label": "Word",
                "type": "application",
                "character": "",
                "application": "C:\\Program Files\\Word\\winword.exe",
                "website": "",
                "command": "" 
            """
            result = dialog.result

            # Update profile key data with the key label (what is displayed on the buttons in the GUI) and the type of service it is (command, application, character, website). 
            profile["keys"][key]["LABEL"] = result["label"]
            profile["keys"][key]["TYPE"] = result["type"]
            
            # then depending on the type, the value is stored
            # profile[keys - level 1 key][grid position - level 2 value to 'keys' but a dictionary itself, acts as key][service - level 3 value to lvl 2 but a dictionary itself acts as key]
            # profile[1][2][3] = input text from pop up gui
            if result["type"] == "character/sentence":
                profile["keys"][key]["VALUE"] = result["character"]
            elif result["type"] == "application":
                profile["keys"][key]["VALUE"] = result["application"]
            elif result["type"] == "website":
                profile["keys"][key]["VALUE"] = result["website"]
            elif result["type"] == "command":
                profile["keys"][key]["VALUE"] = result["command"]

            # Updates the visible label on the gui to be the 'label' as set in the pop up
            self.key_buttons[key].setText(result["label"])

    # =================== Footer ===================
    def footer(self, main_layout):
        footer_container = QWidget()
        footer_container.setObjectName("footer")

        footer_layout = QHBoxLayout()
        save_button = QPushButton("Save Profile")
        delete_button = QPushButton("Delete Profile")

        save_button.clicked.connect(self.save_profile)
        delete_button.clicked.connect(self.delete_profile)

        footer_layout.addWidget(save_button)
        footer_layout.addWidget(delete_button)
        footer_container.setLayout(footer_layout)

        main_layout.addWidget(footer_container)

    def save_profile(self):
        self.profile_manager._write_to_file()
        QMessageBox.information(self, "Profile Saved", f"Profile '{self.profile_manager.current_profile_name}' has been saved.")

    def delete_profile(self):
        current_name = self.profile_manager.current_profile_name

        # Prevent deleting the last profile
        if len(self.profile_manager.get_profile_names()) <= 1:
            QMessageBox.warning(self, "Action Denied", "Cannot delete the last remaining profile.")
            return

        # Confirm deletion
        confirm = QMessageBox.question(
            self,
            "Delete Profile",
            f"Are you sure you want to delete profile '{current_name}'?",
            QMessageBox.Yes | QMessageBox.No
        )

        if confirm == QMessageBox.Yes:
            if self.profile_manager.delete_profile(current_name):
                self.refresh_profile_dropdown()
                self.update_key_labels()
                QMessageBox.information(self, "Deleted", f"Profile '{current_name}' has been deleted.")
            else:
                QMessageBox.warning(self, "Error", "Failed to delete profile.")

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
