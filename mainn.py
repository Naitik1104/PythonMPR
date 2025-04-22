import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget, QDialog, QMessageBox, QVBoxLayout, QWidget
from WelcomePage2 import Ui_MainWindow as WelcomePage
from loginform import Ui_Dialog as LoginPage
from Register import RegisterApp as RegisterPage
from UserDiscretion import Ui_Dialog as UserDiscretionPage
from ProfileBuilder import Ui_Dialog as ProfileBuilderPage
from PhotoPicker import ImagePickerApp
from database1 import Database  # Ensure this is imported
from loginform import LoginApp
from HomePage import SaathiDashboard
from PyQt5.QtGui import QPixmap, QPainter, QRegion
from PyQt5.QtCore import Qt
from SelfieVerification import SelfieVerificationApp

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Saathi - Connect.Share.Thrive")
        self.setGeometry(400, 200, 851, 500)
        
        # Store current user
        self.current_user = None

        # Initialize database connection
        self.db = Database(host='localhost', user='root', password='naitik@mysql', database='saathi')

        # Stack to manage multiple pages
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        # Welcome Page
        self.welcome = WelcomePage()
        self.welcome_window = QMainWindow()
        self.welcome.setupUi(self.welcome_window)
        self.stack.addWidget(self.welcome_window)

        # Login Page
        self.login = LoginApp(self)  # Pass self as parent
        self.login_window = self.login
        self.stack.addWidget(self.login_window)

        # Register Page
        self.register = RegisterPage(self)  # Pass self as parent
        self.register_window = self.register
        self.register.ui.register_button.clicked.connect(self.register_user)
        self.stack.addWidget(self.register_window)

        # User Discretion Page
        self.user_discretion = UserDiscretionPage()
        self.user_discretion_window = QDialog()
        self.user_discretion.setupUi(self.user_discretion_window)
        self.user_discretion.pushButton.clicked.connect(self.show_selfie_verification)
        self.stack.addWidget(self.user_discretion_window)

        # Selfie Verification Page
        self.selfie_verification = None  # Will be created when needed
        
        # Profile Builder Page
        self.profile_builder = ProfileBuilderPage()
        self.profile_builder_window = QDialog()
        self.profile_builder.setupUi(self.profile_builder_window)
        self.profile_builder_window.setMinimumSize(851, 500)
        self.profile_builder.proceed_button.clicked.connect(self.check_age_and_proceed)
        self.stack.addWidget(self.profile_builder_window)

        # PhotoPicker placeholder (will be created when needed)
        self.photo_picker = None
        self.photo_picker_index = -1

        # Home Page
        self.home_page = None  # Will be created when needed

        # Button Click Connections
        self.welcome.pushButton.clicked.connect(self.show_login)   
        self.welcome.pushButton_2.clicked.connect(self.show_register)  
        self.login.ui.pushButton.clicked.connect(self.show_register)  
        self.register.ui.pushButton.clicked.connect(self.show_login)  
        self.user_discretion.pushButton_2.clicked.connect(self.show_profile_builder)

        # Show Welcome Page Initially
        self.show_welcome()
    
    def show_welcome(self):
        self.stack.setCurrentWidget(self.welcome_window)
    
    def show_login(self):
        self.stack.setCurrentWidget(self.login_window)
    
    def show_register(self):
        self.stack.setCurrentWidget(self.register_window)

    def show_user_discretion(self, username=None):
        if username:
            self.current_user = username
        self.stack.setCurrentWidget(self.user_discretion_window)

    def show_profile_builder(self):
        if self.current_user:
            # Get user data from users table
            cursor = self.db.connection.cursor()
            try:
                # Get user data
                cursor.execute("""
                    SELECT age, gender, location 
                    FROM users 
                    WHERE name = %s
                """, (self.current_user,))
                user_data = cursor.fetchone()
                
                if user_data:
                    age, gender, location = user_data
                    # Set user data in profile builder
                    self.profile_builder.age_input.setValue(age if age else 25)
                    gender_index = self.profile_builder.gender_input.findText(gender) if gender else 0
                    self.profile_builder.gender_input.setCurrentIndex(gender_index)
                    self.profile_builder.location_input.setText(location if location else "")
                
                # Get user_id
                cursor.execute("SELECT id FROM users WHERE name = %s", (self.current_user,))
                user_id = cursor.fetchone()[0]
                
                # Get profile data including profile picture
                cursor.execute("""
                    SELECT Interests, bio, profile_picture 
                    FROM profiles 
                    WHERE user_id = %s
                """, (user_id,))
                profile_data = cursor.fetchone()
                
                if profile_data:
                    interests, bio, profile_picture = profile_data
                    # Set profile data
                    if interests:
                        self.profile_builder.interests_input.setText(interests)
                    
                    if bio:
                        # Store the bio to be displayed in the prompts dialog
                        self.profile_builder_window.bio = bio
                        # Update progress since we have a bio
                        self.profile_builder.update_progress()
                    
                    # Handle profile picture
                    if profile_picture:
                        # Convert binary data to QPixmap
                        pixmap = QPixmap()
                        pixmap.loadFromData(profile_picture)
                        if not pixmap.isNull():
                            # Store the binary data
                            self.profile_builder.profile_picture.current_picture = profile_picture
                            
                            # Create circular mask
                            mask = QPixmap(150, 150)
                            mask.fill(Qt.transparent)
                            painter = QPainter(mask)
                            painter.setRenderHint(QPainter.Antialiasing)
                            painter.setBrush(Qt.black)
                            painter.setPen(Qt.NoPen)
                            painter.drawEllipse(0, 0, 150, 150)
                            painter.end()
                            
                            # Scale and crop the image
                            pixmap = pixmap.scaled(150, 150, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
                            if pixmap.width() > 150 or pixmap.height() > 150:
                                pixmap = pixmap.copy(
                                    (pixmap.width() - 150) // 2,
                                    (pixmap.height() - 150) // 2,
                                    150, 150
                                )
                            
                            # Apply mask
                            result = QPixmap(150, 150)
                            result.fill(Qt.transparent)
                            painter = QPainter(result)
                            painter.setRenderHint(QPainter.Antialiasing)
                            painter.setClipRegion(QRegion(mask.mask()))
                            painter.drawPixmap(0, 0, pixmap)
                            painter.end()
                            
                            # Set the final image
                            self.profile_builder.profile_picture.picture_label.setPixmap(result)
                            self.profile_builder.profile_picture.picture_label.setStyleSheet("""
                                QLabel {
                                    background-color: transparent;
                                    border-radius: 75px;
                                    border: 2px solid #4A90E2;
                                }
                            """)
                            
                            # Update progress
                            self.profile_builder.update_progress()
                
            finally:
                cursor.close()
        
        self.stack.setCurrentWidget(self.profile_builder_window)

    def show_photo_picker(self):
        # Create new PhotoPicker instance with current user
        if self.current_user:
            self.photo_picker = ImagePickerApp(self, self.db, self.current_user)
            if self.photo_picker_index == -1:
                # First time adding to stack
                self.photo_picker_index = self.stack.addWidget(self.photo_picker)
            else:
                # Replace existing widget
                self.stack.removeWidget(self.stack.widget(self.photo_picker_index))
                self.stack.insertWidget(self.photo_picker_index, self.photo_picker)
            
            # Switch to photo picker
            self.stack.setCurrentWidget(self.photo_picker)
        else:
            QMessageBox.warning(self, "Error", "No user logged in. Please log in first.")

    def show_home_page(self):
        if self.home_page is None:
            self.home_page = SaathiDashboard(self.current_user)
            self.stack.addWidget(self.home_page)
        self.stack.setCurrentWidget(self.home_page)

    def check_age_and_proceed(self):
        try:
            if not self.current_user:
                QMessageBox.critical(self, "Error", "No user logged in. Please log in first.")
                return

            age = int(self.profile_builder.age_input.value())
            if age < 15:
                QMessageBox.critical(self, "Access Denied", "You must be at least 15 years old to use this application.")
                return
            
            # Get profile data using current_user instead of name_input
            gender = self.profile_builder.gender_input.currentText()
            location = self.profile_builder.location_input.text()
            interests = self.profile_builder.interests_input.text()
            profile_picture = self.profile_builder.profile_picture.current_picture
            
            # Get the bio from the profile builder
            bio = ""
            if hasattr(self.profile_builder_window, 'bio'):
                bio = self.profile_builder_window.bio
            
            # Update database with current_user
            self.db.update_user_profile(self.current_user, age, gender, location)
            self.db.update_user_interests(self.current_user, interests)
            
            # Only update bio if it exists
            if bio:
                self.db.update_user_bio(self.current_user, bio)
            
            if profile_picture:
                self.db.update_profile_picture(self.current_user, profile_picture)

            self.show_photo_picker()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save profile: {str(e)}")

    def register_user(self):
        # Collect data from input fields
        mobile = self.register.ui.mobile_input.text()
        username = self.register.ui.username_input.text()
        password = self.register.ui.password_input.text()
        confirm_password = self.register.ui.confirm_password_input.text()

        # Validate input fields
        if not (mobile and username and password and confirm_password):
            QMessageBox.warning(self, "Input Error", "Please fill in all fields.")
            return
            
        if password != confirm_password:
            QMessageBox.warning(self, "Input Error", "Passwords do not match!")
            return

        try:
            # Connect to the database and insert user data
            self.db.insert_user(username, password, mobile, 25, 'Others')
            
            QMessageBox.information(self, "Success", "Registration successful! Let's set up your profile.")
            
            # Set current user and proceed to user discretion
            self.current_user = username
            self.show_user_discretion()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Registration failed: {str(e)}")

    def show_selfie_verification(self):
        if self.current_user:
            self.selfie_verification = SelfieVerificationApp(self, self.current_user)
            if self.selfie_verification.exec_() == QDialog.Accepted:
                self.show_profile_builder()
        else:
            QMessageBox.warning(self, "Error", "No user logged in. Please log in first.")

    def closeEvent(self, event):
        if hasattr(self, 'db'):
            self.db.close_connection()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)  
    window = MainApp()  
    window.show()
    sys.exit(app.exec_())