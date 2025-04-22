from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDialog, QMessageBox
import sys
import mysql.connector
from database1 import Database  

class LoginApp(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.parent_window = parent  # Store parent window reference
        
        # Initialize database connection
        try:
            self.db = Database(host='localhost', user='root', password='naitik@mysql', database='saathi')
            if not self.db.connection or not self.db.connection.is_connected():
                raise Exception("Failed to connect to database")
        except Exception as e:
            QMessageBox.critical(self, "Database Error", f"Failed to connect to database: {str(e)}")
            self.db = None
        
        # Connect Sign In button to the sign_in method
        self.ui.sign_in_button.clicked.connect(self.sign_in)

    def sign_in(self):
        username = self.ui.plainTextEdit.text()
        password = self.ui.plainTextEdit_2.text()
        
        if not username or not password:
            QMessageBox.warning(self, "Error", "Please enter both username and password.")
            return
        
        if not self.db or not self.db.connection or not self.db.connection.is_connected():
            QMessageBox.critical(self, "Error", "Database connection not available.")
            return
        
        try:
            user = self.db.get_user(username)  # Using username to fetch user data
            
            if user and user[2] == password:  # Check if password matches
                QMessageBox.information(self, "Success", "Login successful! We hope you enjoy your time on the app")
                if self.parent_window:
                    self.parent_window.current_user = username  # Set current user
                    self.close()
                    self.parent_window.show_home_page()  # Redirect to HomePage
            else:
                QMessageBox.warning(self, "Error", "Invalid username or password.")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Login failed: {str(e)}")

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1024, 768)
        font = QtGui.QFont()
        font.setPointSize(12)
        Dialog.setFont(font)
        Dialog.setStyleSheet("""
            QDialog {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #E8F0FE, stop:1 #FFFFFF);
            }
        """)
        
        # Left Frame for Logo
        self.frame_2 = QtWidgets.QFrame(Dialog)
        self.frame_2.setGeometry(QtCore.QRect(0, 0, 512, 768))  # Half width
        self.frame_2.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #1E88E5, stop:1 #64B5F6);
                border-radius: 15px;
            }
        """)
        
        # Logo Button in left frame
        self.logo_button = QtWidgets.QPushButton(self.frame_2)
        self.logo_button.setGeometry(QtCore.QRect(131, 234, 250, 250))  # Centered, larger size
        self.logo_button.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("assets/Saathilogo2.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.logo_button.setIcon(icon)
        self.logo_button.setIconSize(QtCore.QSize(250, 250))
        self.logo_button.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: none;
            }
        """)
        
        # Right Frame for Inputs
        self.frame = QtWidgets.QFrame(Dialog)
        self.frame.setGeometry(QtCore.QRect(512, 0, 512, 768))  # Right half
        self.frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #FFFFFF, stop:1 #F5F9FF);
                border-radius: 15px;
            }
        """)
        
        # Welcome Back Label
        self.label_3 = QtWidgets.QLabel(self.frame)
        self.label_3.setGeometry(QtCore.QRect(60, 100, 392, 50))
        font = QtGui.QFont()
        font.setFamily("Miriam Libre")
        font.setPointSize(32)
        font.setBold(True)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("color: #1E88E5;")
        
        # Username Label
        self.label_4 = QtWidgets.QLabel(self.frame)
        self.label_4.setGeometry(QtCore.QRect(60, 200, 200, 41))
        font = QtGui.QFont()
        font.setFamily("Miriam Libre")
        font.setPointSize(14)
        font.setBold(True)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color: #1E88E5;")
        
        # Username Input
        self.plainTextEdit = QtWidgets.QLineEdit(self.frame)
        self.plainTextEdit.setGeometry(QtCore.QRect(60, 250, 392, 50))
        self.plainTextEdit.setPlaceholderText("Enter your username")
        self.plainTextEdit.setStyleSheet("""
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
        
        # Password Label
        self.label_5 = QtWidgets.QLabel(self.frame)
        self.label_5.setGeometry(QtCore.QRect(60, 320, 200, 41))
        font = QtGui.QFont()
        font.setFamily("Miriam Libre")
        font.setPointSize(14)
        font.setBold(True)
        self.label_5.setFont(font)
        self.label_5.setStyleSheet("color: #1E88E5;")
        
        # Password Input
        self.plainTextEdit_2 = QtWidgets.QLineEdit(self.frame)
        self.plainTextEdit_2.setGeometry(QtCore.QRect(60, 370, 392, 50))
        self.plainTextEdit_2.setPlaceholderText("Enter your password")
        self.plainTextEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.plainTextEdit_2.setStyleSheet("""
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
        
        # Already have an account Label
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setGeometry(QtCore.QRect(60, 440, 392, 41))
        font = QtGui.QFont()
        font.setFamily("Miriam Libre")
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #1E88E5;")
        
        # Sign Up Button
        self.pushButton = QtWidgets.QPushButton(self.frame)
        self.pushButton.setGeometry(QtCore.QRect(60, 490, 392, 50))
        font = QtGui.QFont()
        font.setFamily("Miriam Libre")
        font.setPointSize(14)
        self.pushButton.setFont(font)
        self.pushButton.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: #1E88E5;
                border: none;
                font-weight: bold;
                text-decoration: underline;
            }
            QPushButton:hover {
                color: #64B5F6;
            }
        """)
        
        # Sign In Button
        self.sign_in_button = QtWidgets.QPushButton(self.frame)
        self.sign_in_button.setGeometry(QtCore.QRect(60, 560, 392, 55))
        font = QtGui.QFont()
        font.setFamily("Miriam Libre")
        font.setPointSize(16)
        font.setBold(True)
        self.sign_in_button.setFont(font)
        self.sign_in_button.setStyleSheet("""
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

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Login"))
        self.label.setText(_translate("Dialog", "Already have an account?"))
        self.pushButton.setText(_translate("Dialog", "Sign Up"))
        self.label_3.setText(_translate("Dialog", "Welcome Back"))
        self.label_4.setText(_translate("Dialog", "Username"))
        self.label_5.setText(_translate("Dialog", "Password"))
        self.sign_in_button.setText(_translate("Dialog", "Log In"))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())