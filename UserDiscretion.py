from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1024, 768)
        Dialog.setStyleSheet("background-color: rgb(255, 255, 255);")
        
        # Main Layout
        self.main_layout = QtWidgets.QVBoxLayout(Dialog)
        self.main_layout.setContentsMargins(40, 40, 40, 40)
        self.main_layout.setSpacing(30)
        
        # Title Group Box
        self.groupBox = QtWidgets.QGroupBox(Dialog)
        self.groupBox.setGeometry(QtCore.QRect(100, 60, 824, 80))
        font = QtGui.QFont()
        font.setFamily("Dutch801 XBd BT")
        font.setPointSize(36)
        font.setBold(False)
        font.setWeight(50)
        self.groupBox.setFont(font)
        self.groupBox.setObjectName("groupBox")
        
        # Privacy Text Label
        self.privacy_label = QtWidgets.QLabel(Dialog)
        self.privacy_label.setGeometry(QtCore.QRect(100, 180, 824, 250))
        font = QtGui.QFont()
        font.setFamily("Dutch801 XBd BT")
        font.setPointSize(18)
        self.privacy_label.setFont(font)
        self.privacy_label.setWordWrap(True)
        self.privacy_label.setObjectName("privacy_label")
        
        # Button Layout
        self.button_layout = QtWidgets.QVBoxLayout()
        self.button_layout.setSpacing(20)
        
        # Accept Button
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(100, 500, 824, 60))
        font = QtGui.QFont()
        font.setFamily("Dutch801 Rm BT")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton.setFont(font)
        self.pushButton.setStyleSheet("""
            QPushButton {
                color: rgb(255, 255, 255);
                background-color: blue;
                border-radius: 30px;
                padding: 15px;
            }
            QPushButton:hover {
                background-color: rgb(142, 0, 2);
            }
        """)
        self.pushButton.setObjectName("pushButton")
        
        # Personalize Button
        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(100, 580, 824, 60))
        font = QtGui.QFont()
        font.setFamily("Dutch801 Rm BT")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setStyleSheet("""
            QPushButton {
                color: rgb(122, 0, 2);
                background: transparent;
                border: none;
            }
            QPushButton:hover {
                color: rgb(142, 0, 2);
            }
        """)
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.hide()  # Hide instead of removing to maintain layout structure

        # Add the selfie notice
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(100, 420, 824, 60))
        font = QtGui.QFont()
        font.setFamily("Miriam Libre")
        font.setPointSize(14)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color: #1E88E5;")
        self.label_4.setText("Note: We will record your selfie for verification and security purposes.")
        self.label_4.setWordWrap(True)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "User Discretion"))
        self.groupBox.setTitle(_translate("Dialog", "We Value Your Privacy!"))
        self.privacy_label.setText(_translate("Dialog", 
            "We make sure all your data is secure and isn't shared to any third-party apps. "
            "We believe in the utmost discretion and confidentiality that the user has entrusted upon us.\n\n"
            "Hope you have a wonderful time using our app!"))
        self.pushButton.setText(_translate("Dialog", "I Accept"))
        self.pushButton_2.setText(_translate("Dialog", "Personalize my choices"))
