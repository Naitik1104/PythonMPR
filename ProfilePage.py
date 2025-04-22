from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QMessageBox, QDialog
from PyQt5.QtCore import Qt
from database1 import Database

class ProfilePage(QWidget):
    def __init__(self, current_user=None):
        super().__init__()
        self.current_user = current_user
        self.setFixedSize(774, 768)  # Adjusted for 1024x768 with sidebar
        
        # Initialize database connection
        try:
            self.db = Database(host='localhost', user='root', password='naitik@mysql', database='saathi')
        except Exception as e:
            print(f"Error connecting to database in ProfilePage: {e}")
            QMessageBox.critical(self, "Database Error", "Could not connect to database. Please check your connection and try again.")
            return
            
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # Connect buttons
        self.ui.pushButton.clicked.connect(self.edit_profile)
        self.ui.pushButton_2.clicked.connect(self.add_photos)
        
        self.load_user_data()

    def load_user_data(self):
        if not self.current_user:
            return

        cursor = self.db.connection.cursor()
        try:
            # Get user data
            cursor.execute("""
                SELECT age, gender, location, Interests 
                FROM Users u
                LEFT JOIN Profiles p ON u.id = p.user_id
                WHERE u.name = %s
            """, (self.current_user,))
            user_data = cursor.fetchone()
            
            if user_data:
                age, gender, location, interests = user_data
                # Update user info
                self.ui.username.setText(self.current_user)
                self.ui.label.setText(f"{gender}, {age} years")
                self.ui.label_2.setText(f"Loves: {interests}" if interests else "No interests added")
                self.ui.label_3.setText(location if location else "Location not set")

            # Get friend count
            cursor.execute("""
                SELECT COUNT(*) FROM friends f
                JOIN users u ON (f.user1_id = u.id OR f.user2_id = u.id)
                WHERE u.name = %s
            """, (self.current_user,))
            friend_count = cursor.fetchone()[0]
            self.ui.label_7.setText(f"{friend_count} Mates")

            # Get profile picture
            cursor.execute("""
                SELECT profile_picture 
                FROM Profiles p
                JOIN Users u ON u.id = p.user_id
                WHERE u.name = %s
            """, (self.current_user,))
            profile_pic = cursor.fetchone()
            
            if profile_pic and profile_pic[0]:
                pixmap = QtGui.QPixmap()
                pixmap.loadFromData(profile_pic[0])
                if not pixmap.isNull():
                    self.ui.Profilepic.setPixmap(pixmap.scaled(130, 111, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))

            # Get bio
            cursor.execute("""
                SELECT bio 
                FROM Profiles p
                JOIN Users u ON u.id = p.user_id
                WHERE u.name = %s
            """, (self.current_user,))
            bio = cursor.fetchone()
            
            if bio and bio[0]:
                self.ui.textEdit.setText(bio[0])
                self.ui.textEdit.setReadOnly(True)  # Make bio non-editable

            # Get photos with upload dates
            cursor.execute("""
                SELECT photo, upload_date 
                FROM Photos p
                JOIN Users u ON u.id = p.user_id
                WHERE u.name = %s
                ORDER BY upload_date DESC
            """, (self.current_user,))
            photos = cursor.fetchall()
            
            # Update photo labels and dates
            photo_labels = [self.ui.label_4, self.ui.label_13, self.ui.label_15]
            date_labels = [self.ui.label_9, self.ui.label_10, self.ui.label_14]
            
            for i, (photo_data, upload_date) in enumerate(photos):
                if i < len(photo_labels):
                    pixmap = QtGui.QPixmap()
                    pixmap.loadFromData(photo_data)
                    if not pixmap.isNull():
                        photo_labels[i].setPixmap(pixmap.scaled(131, 121, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
                        # Format and display upload date
                        formatted_date = upload_date.strftime("%B %d, %Y")
                        date_labels[i].setText(f"Uploaded: {formatted_date}")

        finally:
            cursor.close()

    def edit_profile(self):
        if not self.current_user:
            return
            
        # Create and show ProfileBuilder in the same window
        from ProfileBuilder import Ui_Dialog as ProfileBuilderPage
        self.profile_builder = ProfileBuilderPage()
        self.profile_builder_window = QtWidgets.QDialog(self)
        self.profile_builder.setupUi(self.profile_builder_window)
        self.profile_builder_window.setMinimumSize(851, 500)
        
        # Add back button
        back_button = QtWidgets.QPushButton("Back", self.profile_builder_window)
        back_button.setGeometry(20, 20, 80, 30)
        back_button.setStyleSheet("""
            QPushButton {
                background-color: #4CA6FF;
                color: white;
                border: none;
                border-radius: 15px;
                padding: 5px 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2196F3;
            }
        """)
        back_button.clicked.connect(self.profile_builder_window.reject)
        
        # Set window style to prevent fading
        self.profile_builder_window.setStyleSheet("""
            QDialog {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #E8F0FE, stop:1 #FFFFFF);
            }
        """)
        
        # Load existing data into ProfileBuilder
        cursor = self.db.connection.cursor()
        try:
            cursor.execute("""
                SELECT age, gender, location, Interests, bio, profile_picture 
                FROM Users u
                LEFT JOIN Profiles p ON u.id = p.user_id
                WHERE u.name = %s
            """, (self.current_user,))
            user_data = cursor.fetchone()
            
            if user_data:
                age, gender, location, interests, bio, profile_picture = user_data
                self.profile_builder.age_input.setValue(age if age else 25)
                gender_index = self.profile_builder.gender_input.findText(gender) if gender else 0
                self.profile_builder.gender_input.setCurrentIndex(gender_index)
                self.profile_builder.location_input.setText(location if location else "")
                self.profile_builder.interests_input.setText(interests if interests else "")
                
                if bio:
                    self.profile_builder_window.bio = bio
                
                if profile_picture:
                    self.profile_builder.profile_picture.current_picture = profile_picture
                    pixmap = QtGui.QPixmap()
                    pixmap.loadFromData(profile_picture)
                    if not pixmap.isNull():
                        self.profile_builder.profile_picture.picture_label.setPixmap(pixmap.scaled(150, 150, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
        finally:
            cursor.close()
        
        # Connect proceed button to save changes
        self.profile_builder.proceed_button.clicked.connect(self.save_profile_changes)
        self.profile_builder_window.exec_()

    def save_profile_changes(self):
        try:
            age = self.profile_builder.age_input.value()
            gender = self.profile_builder.gender_input.currentText()
            location = self.profile_builder.location_input.text()
            interests = self.profile_builder.interests_input.text()
            profile_picture = self.profile_builder.profile_picture.current_picture
            bio = self.profile_builder_window.bio if hasattr(self.profile_builder_window, 'bio') else ""
            
            # Update database
            self.db.update_user_profile(self.current_user, age, gender, location)
            self.db.update_user_interests(self.current_user, interests)
            if bio:
                self.db.update_user_bio(self.current_user, bio)
            if profile_picture:
                self.db.update_profile_picture(self.current_user, profile_picture)
            
            QtWidgets.QMessageBox.information(self, "Success", "Profile updated successfully!")
            self.profile_builder_window.accept()
            self.load_user_data()  # Reload user data
            
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"Failed to update profile: {str(e)}")

    def add_photos(self):
        """Shows the PhotoPicker dialog for adding photos."""
        if not self.current_user:
            QMessageBox.warning(self, "Error", "Please log in to add photos.")
            return

        try:
            from PhotoPicker import ImagePickerApp
            photo_picker_dialog = QDialog(self)
            photo_picker_dialog.setWindowTitle("Add Photos")
            photo_picker_dialog.setFixedSize(851, 500)
            
            # Create layout for the dialog
            layout = QtWidgets.QVBoxLayout(photo_picker_dialog)
            
            # Create ImagePickerApp instance with the dialog as parent
            photo_picker = ImagePickerApp(photo_picker_dialog, self.db, self.current_user)
            layout.addWidget(photo_picker)
            
            # Connect signals to reload user data
            photo_picker.photos_saved.connect(self.load_user_data)
            photo_picker.photos_skipped.connect(self.load_user_data)
            
            # Show dialog
            photo_picker_dialog.exec_()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to open photo picker: {str(e)}")

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        
        # Create main layout
        self.main_layout = QtWidgets.QVBoxLayout(MainWindow)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(20)
        
        # Create scroll area
        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background: transparent;
            }
            QScrollBar:vertical {
                border: none;
                background: #F0F0F0;
                width: 10px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background: #2196F3;
                border-radius: 5px;
            }
        """)
        
        # Create scroll content widget
        self.scroll_content = QtWidgets.QWidget()
        self.scroll_layout = QtWidgets.QVBoxLayout(self.scroll_content)
        self.scroll_layout.setContentsMargins(0, 0, 0, 0)
        self.scroll_layout.setSpacing(20)
        
        # Top section with profile info
        self.top_section = QtWidgets.QWidget()
        self.top_layout = QtWidgets.QHBoxLayout(self.top_section)
        
        # Profile picture
        self.Profilepic = QtWidgets.QLabel()
        self.Profilepic.setFixedSize(130, 111)
        self.Profilepic.setStyleSheet("""
            QLabel {
                border-radius: 20px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #E3F2FD, stop:1 #F5F9FF);
            }
        """)
        
        # User info section
        self.user_info = QtWidgets.QWidget()
        self.user_info_layout = QtWidgets.QVBoxLayout(self.user_info)
        
        self.username = QtWidgets.QLabel()
        self.username.setStyleSheet("""
            QLabel {
                color: #2196F3;
                font-size: 20px;
                font-weight: bold;
            }
        """)
        
        self.label = QtWidgets.QLabel()
        self.label_2 = QtWidgets.QLabel()
        self.label_3 = QtWidgets.QLabel()
        
        self.user_info_layout.addWidget(self.username)
        self.user_info_layout.addWidget(self.label)
        self.user_info_layout.addWidget(self.label_2)
        self.user_info_layout.addWidget(self.label_3)
        
        # Stats section
        self.stats_section = QtWidgets.QWidget()
        self.stats_layout = QtWidgets.QVBoxLayout(self.stats_section)
        
        self.label_5 = QtWidgets.QLabel("Popularity Score")
        self.label_6 = QtWidgets.QLabel("34")
        self.label_6.setStyleSheet("""
            QLabel {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #4C21FF, stop:1 #6B9FFF);
                color: white;
                border-radius: 30px;
                padding: 10px;
                font-weight: bold;
            }
        """)
        self.label_7 = QtWidgets.QLabel("31 Mates")
        self.label_7.setStyleSheet("color: #FF0000;")
        self.label_8 = QtWidgets.QLabel("7 Communities")
        self.label_8.setStyleSheet("color: #FF0000;")
        self.label_8.hide()  # Hide the communities label instead of removing to maintain layout
        
        self.stats_layout.addWidget(self.label_5)
        self.stats_layout.addWidget(self.label_6)
        self.stats_layout.addWidget(self.label_7)
        self.stats_layout.addWidget(self.label_8)
        
        # Add widgets to top layout
        self.top_layout.addWidget(self.Profilepic)
        self.top_layout.addWidget(self.user_info)
        self.top_layout.addWidget(self.stats_section)
        
        # Action buttons
        self.buttons_layout = QtWidgets.QHBoxLayout()
        
        self.pushButton = QtWidgets.QPushButton("Edit Profile")
        self.pushButton.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #46CEFF, stop:1 #6B9FFF);
                color: white;
                border-radius: 25px;
                padding: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #6B9FFF, stop:1 #46CEFF);
            }
        """)
        
        self.pushButton_2 = QtWidgets.QPushButton("Add Photos")
        self.pushButton_2.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #53D7FF, stop:1 #6B9FFF);
                color: white;
                border-radius: 25px;
                padding: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #6B9FFF, stop:1 #53D7FF);
            }
        """)
        
        self.buttons_layout.addWidget(self.pushButton)
        self.buttons_layout.addWidget(self.pushButton_2)
        
        # Bio section
        self.bio_section = QtWidgets.QWidget()
        self.bio_layout = QtWidgets.QVBoxLayout(self.bio_section)
        
        self.label_11 = QtWidgets.QLabel("About Myself")
        self.textEdit = QtWidgets.QTextEdit()
        self.textEdit.setStyleSheet("""
            QTextEdit {
                border: 2px solid #E3E9FF;
                border-radius: 10px;
                padding: 10px;
                background: white;
            }
            QTextEdit:focus {
                border: 2px solid #4CA6FF;
            }
        """)
        
        self.bio_layout.addWidget(self.label_11)
        self.bio_layout.addWidget(self.textEdit)
        
        # Photos section
        self.photos_section = QtWidgets.QWidget()
        self.photos_layout = QtWidgets.QVBoxLayout(self.photos_section)
        
        self.label_12 = QtWidgets.QLabel("Uploaded Photos")
        self.photos_grid = QtWidgets.QGridLayout()
        
        # Create photo labels
        self.label_4 = QtWidgets.QLabel()
        self.label_13 = QtWidgets.QLabel()
        self.label_15 = QtWidgets.QLabel()
        
        # Add photo labels to grid
        self.photos_grid.addWidget(self.label_4, 0, 0)
        self.photos_grid.addWidget(self.label_13, 0, 1)
        self.photos_grid.addWidget(self.label_15, 0, 2)
        
        # Add photo date labels
        self.label_9 = QtWidgets.QLabel("Uploaded Date")
        self.label_10 = QtWidgets.QLabel("Uploaded Date")
        self.label_14 = QtWidgets.QLabel("Uploaded Date")
        
        self.photos_grid.addWidget(self.label_9, 1, 0)
        self.photos_grid.addWidget(self.label_10, 1, 1)
        self.photos_grid.addWidget(self.label_14, 1, 2)
        
        self.photos_layout.addWidget(self.label_12)
        self.photos_layout.addLayout(self.photos_grid)
        
        # Add all sections to scroll layout
        self.scroll_layout.addWidget(self.top_section)
        self.scroll_layout.addLayout(self.buttons_layout)
        self.scroll_layout.addWidget(self.bio_section)
        self.scroll_layout.addWidget(self.photos_section)
        
        # Set scroll area widget
        self.scroll_area.setWidget(self.scroll_content)
        
        # Add scroll area to main layout
        self.main_layout.addWidget(self.scroll_area)
        
        # Set window style
        MainWindow.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #E8F0FE, stop:1 #FFFFFF);
            }
        """)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = ProfilePage()
    MainWindow.show()
    sys.exit(app.exec_())