# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
from database1 import Database  # Import your Database class
import re  # For password validation

class RegisterApp(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setFixedSize(1024, 768)  # Set fixed size to 1024x768
        self.parent_window = parent
        # Connect buttons to their respective functions
        self.ui.register_button.clicked.connect(self.on_register_clicked)
        self.ui.sign_in_button.clicked.connect(self.navigate_to_login)
        # Connect password input to validation
        self.ui.password_input.textChanged.connect(self.validate_password_strength)
        # Connect password requirements button
        self.ui.password_requirements_button.clicked.connect(self.show_password_requirements)
        # Initialize password strength label
        self.ui.password_strength_label.setText("")
        self.ui.password_strength_label.setVisible(False)
        # Initialize password strength bar
        self.ui.password_strength_bar.setValue(0)
        self.ui.password_strength_bar.setVisible(False)
        # Set password requirements tooltip
        self.set_password_requirements_tooltip()

    def set_password_requirements_tooltip(self):
        """Set tooltip for password requirements"""
        requirements = (
            "Password Requirements:\n"
            "• At least 8 characters long\n"
            "• At least one uppercase letter (A-Z)\n"
            "• At least one lowercase letter (a-z)\n"
            "• At least one number (0-9)\n"
            "• At least one special character (!@#$%^&*(),.?\":{}|<>)"
        )
        self.ui.password_input.setToolTip(requirements)
        self.ui.password_requirements_button.setToolTip(requirements)
    
    def show_password_requirements(self):
        """Show password requirements in a popup dialog"""
        requirements = (
            "<h3>Password Requirements</h3>"
            "<p>Your password must include:</p>"
            "<ul>"
            "<li>At least 8 characters long</li>"
            "<li>At least one uppercase letter (A-Z)</li>"
            "<li>At least one lowercase letter (a-z)</li>"
            "<li>At least one number (0-9)</li>"
            "<li>At least one special character (!@#$%^&*(),.?\":{}|<>)</li>"
            "</ul>"
            "<p>Example of a strong password: <b>P@ssw0rd123</b></p>"
        )
        
        msg = QtWidgets.QMessageBox(self)
        msg.setWindowTitle("Password Requirements")
        msg.setTextFormat(QtCore.Qt.RichText)
        msg.setText(requirements)
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msg.exec_()

    def navigate_to_login(self):
        if self.parent_window:
            self.parent_window.show_login()

    def on_register_clicked(self):
        if self.register_user():
            # Only proceed if registration was successful
            if self.parent_window:
                self.parent_window.current_user = self.ui.username_input.text()
                self.parent_window.show_user_discretion()

    def validate_password_strength(self):
        """Check password strength and update UI accordingly"""
        password = self.ui.password_input.text()
        
        # Password strength criteria
        has_uppercase = bool(re.search(r'[A-Z]', password))
        has_lowercase = bool(re.search(r'[a-z]', password))
        has_digit = bool(re.search(r'\d', password))
        has_special = bool(re.search(r'[!@#$%^&*(),.?":{}|<>]', password))
        is_long_enough = len(password) >= 8
        
        # Create a list of missing criteria
        missing_criteria = []
        if not has_uppercase:
            missing_criteria.append("uppercase letter")
        if not has_lowercase:
            missing_criteria.append("lowercase letter")
        if not has_digit:
            missing_criteria.append("number")
        if not has_special:
            missing_criteria.append("special character")
        if not is_long_enough:
            missing_criteria.append("at least 8 characters")
        
        # Calculate strength percentage (0-100)
        criteria_met = 5 - len(missing_criteria)
        strength_percentage = (criteria_met / 5) * 100
        
        # Update password field styling based on strength
        if len(missing_criteria) > 0:
            self.ui.password_input.setStyleSheet("""
                QLineEdit {
                    background: white;
                    border: 2px solid #FF5252;
                    padding: 8px;
                    font-size: 12px;
                    border-radius: 5px;
                }
                QLineEdit:focus {
                    border: 2px solid #FF5252;
                    background: #FFF5F5;
                }
            """)
            # Show password strength label with missing criteria
            self.ui.password_strength_label.setText(f"Password must include: {', '.join(missing_criteria)}")
            self.ui.password_strength_label.setStyleSheet("color: #FF5252; font-size: 11px;")
            self.ui.password_strength_label.setVisible(True)
            
            # Update strength bar
            self.ui.password_strength_bar.setValue(int(strength_percentage))
            self.ui.password_strength_bar.setStyleSheet("""
                QProgressBar {
                    border: 1px solid #FF5252;
                    border-radius: 5px;
                    text-align: center;
                    background-color: #FFF5F5;
                }
                QProgressBar::chunk {
                    background-color: #FF5252;
                    width: 10px;
                }
            """)
            self.ui.password_strength_bar.setVisible(True)
        else:
            self.ui.password_input.setStyleSheet("""
                QLineEdit {
                    background: white;
                    border: 2px solid #4CAF50;
                    padding: 8px;
                    font-size: 12px;
                    border-radius: 5px;
                }
                QLineEdit:focus {
                    border: 2px solid #4CAF50;
                    background: #F5FFF5;
                }
            """)
            # Show password strength label with success message
            self.ui.password_strength_label.setText("Password strength: Strong")
            self.ui.password_strength_label.setStyleSheet("color: #4CAF50; font-size: 11px;")
            self.ui.password_strength_label.setVisible(True)
            
            # Update strength bar
            self.ui.password_strength_bar.setValue(100)
            self.ui.password_strength_bar.setStyleSheet("""
                QProgressBar {
                    border: 1px solid #4CAF50;
                    border-radius: 5px;
                    text-align: center;
                    background-color: #F5FFF5;
                }
                QProgressBar::chunk {
                    background-color: #4CAF50;
                    width: 10px;
                }
            """)
            self.ui.password_strength_bar.setVisible(True)
        
        return len(missing_criteria) == 0, missing_criteria

    def register_user(self):
        # Collect data from input fields
        mobile = self.ui.mobile_input.text().strip()  # Remove any whitespace
        username = self.ui.username_input.text()
        password = self.ui.password_input.text()
        confirm_password = self.ui.confirm_password_input.text()

        # Validate input fields
        if not (mobile and username and password and confirm_password):
            QtWidgets.QMessageBox.warning(self, "Input Error", "Please fill in all fields.")
            return False
            
        if password != confirm_password:
            QtWidgets.QMessageBox.warning(self, "Input Error", "Passwords do not match!")
            return False
        
        # Check password strength
        is_strong, missing_criteria = self.validate_password_strength()
        if not is_strong:
            missing_criteria_str = ", ".join(missing_criteria)
            QtWidgets.QMessageBox.warning(
                self, 
                "Weak Password", 
                f"Your password is not strong enough. Please include: {missing_criteria_str}."
            )
            return False

        try:
            # Connect to the database and insert user data
            db = Database(host='localhost', user='root', password='naitik@mysql', database='saathi')
            
            # Try to insert user
            if db.insert_user(username, password, mobile, 25, 'Others'):
                QtWidgets.QMessageBox.information(self, "Success", "Registration successful! Let's set up your profile.")
                return True
            else:
                QtWidgets.QMessageBox.critical(self, "Error", "This mobile number or username is already registered.")
                return False
            
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"Registration failed. Please try again.")
            return False

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1024, 768)  # Set window size
        
        # Left Frame for Inputs
        self.left_frame = QtWidgets.QFrame(Dialog)
        self.left_frame.setGeometry(QtCore.QRect(0, 0, 512, 768))  # Half width
        self.left_frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #FFFFFF, stop:1 #F5F9FF);
                border-radius: 15px;
            }
        """)
        
        # Right Frame for Logo
        self.right_frame = QtWidgets.QFrame(Dialog)
        self.right_frame.setGeometry(QtCore.QRect(512, 0, 512, 768))  # Right half
        self.right_frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #1E88E5, stop:1 #64B5F6);
                border-radius: 15px;
            }
        """)
        
        # Title Label
        self.label = QtWidgets.QLabel(self.left_frame)
        self.label.setGeometry(QtCore.QRect(50, 50, 412, 40))
        font = QtGui.QFont()
        font.setFamily("Miriam Libre")
        font.setPointSize(24)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #1E88E5;")
        
        # Mobile Number Label and Input
        self.label_2 = QtWidgets.QLabel(self.left_frame)
        self.label_2.setGeometry(QtCore.QRect(50, 120, 412, 30))
        font = QtGui.QFont()
        font.setFamily("Miriam Libre")
        font.setPointSize(14)
        font.setBold(True)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("color: #1E88E5;")
        
        self.mobile_input = QtWidgets.QLineEdit(self.left_frame)
        self.mobile_input.setGeometry(QtCore.QRect(50, 160, 412, 50))
        self.mobile_input.setPlaceholderText("Enter your mobile number")
        self.mobile_input.setStyleSheet("""
            QLineEdit {
                background: white;
                border: 2px solid #E3E9FF;
                padding: 12px;
                font-size: 16px;
                border-radius: 8px;
            }
            QLineEdit:focus {
                border: 2px solid #1E88E5;
                background: #F8FAFF;
            }
        """)
        
        # Username Label and Input
        self.label_4 = QtWidgets.QLabel(self.left_frame)
        self.label_4.setGeometry(QtCore.QRect(50, 230, 412, 30))
        font = QtGui.QFont()
        font.setFamily("Miriam Libre")
        font.setPointSize(14)
        font.setBold(True)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color: #1E88E5;")
        
        self.username_input = QtWidgets.QLineEdit(self.left_frame)
        self.username_input.setGeometry(QtCore.QRect(50, 270, 412, 50))
        self.username_input.setPlaceholderText("Choose a username")
        self.username_input.setStyleSheet("""
            QLineEdit {
                background: white;
                border: 2px solid #E3E9FF;
                padding: 12px;
                font-size: 16px;
                border-radius: 8px;
            }
            QLineEdit:focus {
                border: 2px solid #1E88E5;
                background: #F8FAFF;
            }
        """)
        
        # Password Label and Input
        self.label_6 = QtWidgets.QLabel(self.left_frame)
        self.label_6.setGeometry(QtCore.QRect(50, 340, 412, 30))
        font = QtGui.QFont()
        font.setFamily("Miriam Libre")
        font.setPointSize(14)
        font.setBold(True)
        self.label_6.setFont(font)
        self.label_6.setStyleSheet("color: #1E88E5;")
        
        self.password_input = QtWidgets.QLineEdit(self.left_frame)
        self.password_input.setGeometry(QtCore.QRect(50, 380, 412, 50))
        self.password_input.setPlaceholderText("Create a password")
        self.password_input.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password_input.setStyleSheet("""
            QLineEdit {
                background: white;
                border: 2px solid #E3E9FF;
                padding: 12px;
                font-size: 16px;
                border-radius: 8px;
            }
            QLineEdit:focus {
                border: 2px solid #1E88E5;
                background: #F8FAFF;
            }
        """)
        
        # Password Requirements Button
        self.password_requirements_button = QtWidgets.QPushButton(self.left_frame)
        self.password_requirements_button.setGeometry(QtCore.QRect(420, 340, 40, 30))
        self.password_requirements_button.setText("?")
        self.password_requirements_button.setStyleSheet("""
            QPushButton {
                background-color: #1E88E5;
                color: white;
                border-radius: 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #64B5F6;
            }
        """)
        
        # Password Strength Label and Bar
        self.password_strength_label = QtWidgets.QLabel(self.left_frame)
        self.password_strength_label.setGeometry(QtCore.QRect(50, 440, 412, 20))
        self.password_strength_label.setStyleSheet("color: #666; font-size: 12px;")
        
        self.password_strength_bar = QtWidgets.QProgressBar(self.left_frame)
        self.password_strength_bar.setGeometry(QtCore.QRect(50, 470, 412, 8))
        self.password_strength_bar.setStyleSheet("""
            QProgressBar {
                border: none;
                border-radius: 4px;
                text-align: center;
                background-color: #F5F5F5;
            }
            QProgressBar::chunk {
                border-radius: 4px;
                background-color: #4CAF50;
            }
        """)
        
        # Confirm Password Label and Input
        self.confirm_password_label = QtWidgets.QLabel(self.left_frame)
        self.confirm_password_label.setGeometry(QtCore.QRect(50, 500, 412, 30))
        font = QtGui.QFont()
        font.setFamily("Miriam Libre")
        font.setPointSize(14)
        font.setBold(True)
        self.confirm_password_label.setFont(font)
        self.confirm_password_label.setStyleSheet("color: #1E88E5;")
        
        self.confirm_password_input = QtWidgets.QLineEdit(self.left_frame)
        self.confirm_password_input.setGeometry(QtCore.QRect(50, 540, 412, 50))
        self.confirm_password_input.setPlaceholderText("Confirm your password")
        self.confirm_password_input.setEchoMode(QtWidgets.QLineEdit.Password)
        self.confirm_password_input.setStyleSheet("""
            QLineEdit {
                background: white;
                border: 2px solid #E3E9FF;
                padding: 12px;
                font-size: 16px;
                border-radius: 8px;
            }
            QLineEdit:focus {
                border: 2px solid #1E88E5;
                background: #F8FAFF;
            }
        """)
        
        # Register Button
        self.register_button = QtWidgets.QPushButton(self.left_frame)
        self.register_button.setGeometry(QtCore.QRect(50, 620, 412, 55))
        font = QtGui.QFont()
        font.setFamily("Miriam Libre")
        font.setPointSize(16)
        font.setBold(True)
        self.register_button.setFont(font)
        self.register_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #1E88E5, stop:1 #64B5F6);
                color: white;
                border-radius: 27px;
                font-weight: bold;
                padding: 12px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #64B5F6, stop:1 #1E88E5);
            }
        """)
        
        # Logo in right frame
        self.pushButton = QtWidgets.QPushButton(self.right_frame)
        self.pushButton.setGeometry(QtCore.QRect(131, 234, 250, 250))
        self.pushButton.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("assets/Saathilogo2.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton.setIcon(icon)
        self.pushButton.setIconSize(QtCore.QSize(250, 250))
        self.pushButton.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: none;
            }
        """)
        
        # Sign In Button in right frame
        self.sign_in_button = QtWidgets.QPushButton(self.right_frame)
        self.sign_in_button.setGeometry(QtCore.QRect(131, 600, 250, 50))
        font = QtGui.QFont()
        font.setFamily("Miriam Libre")
        font.setPointSize(14)
        font.setBold(True)
        self.sign_in_button.setFont(font)
        self.sign_in_button.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: white;
                border: 2px solid white;
                border-radius: 25px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: rgba(255, 255, 255, 0.1);
            }
        """)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Register"))
        self.label.setText(_translate("Dialog", "Create Account"))
        self.label_2.setText(_translate("Dialog", "Mobile Number"))
        self.label_4.setText(_translate("Dialog", "Username"))
        self.label_6.setText(_translate("Dialog", "Password"))
        self.confirm_password_label.setText(_translate("Dialog", "Confirm Password"))
        self.register_button.setText(_translate("Dialog", "Register Account"))
        self.sign_in_button.setText(_translate("Dialog", "Sign In"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = RegisterApp()
    Dialog.show()
    sys.exit(app.exec_())