from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QLabel, QGridLayout, 
                           QFileDialog, QScrollArea, QHBoxLayout, QMessageBox, QDialog)
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt
import sys
from PyQt5.QtCore import pyqtSignal
from HomePage import SaathiDashboard

class ImagePickerApp(QWidget):
    # Define custom signals
    photos_saved = pyqtSignal()
    photos_skipped = pyqtSignal()

    def __init__(self, parent=None, db=None, current_user=None):
        super().__init__(parent)
        self.db = db
        self.current_user = current_user
        self.parent_dialog = parent
        self.photo_paths = [None] * 6
        self.photo_data = [None] * 6
        print(f"Initializing PhotoPicker for user: {current_user}")  # Debug print
        self.initUI()
        self.load_existing_photos()

    def initUI(self):
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #E8F0FE, stop:1 #FFFFFF);
            }
            QLabel {
                background-color: transparent;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        # Add back button
        back_button = QPushButton("Back", self)
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
        back_button.clicked.connect(self.close)
        layout.addWidget(back_button, alignment=Qt.AlignLeft)

        # Title
        title = QLabel("Add Photos")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #333;")
        layout.addWidget(title, alignment=Qt.AlignCenter)

        # Create scroll area for photos
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
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

        scroll_content = QWidget()
        scroll_content.setStyleSheet("background: transparent;")
        grid_layout = QGridLayout(scroll_content)
        grid_layout.setContentsMargins(0, 0, 0, 0)
        grid_layout.setSpacing(15)

        self.image_labels = []
        self.image_containers = []

        for i in range(2):  # 2 rows
            for j in range(3):  # 3 columns
                container = QWidget()
                container.setStyleSheet("""
                    QWidget {
                        background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                            stop:0 #F8FAFF, stop:1 #FFFFFF);
                        border-radius: 10px;
                        padding: 10px;
                        border: 2px solid #E3E9FF;
                    }
                """)
                container_layout = QVBoxLayout(container)
                container_layout.setContentsMargins(5, 5, 5, 5)
                container_layout.setSpacing(5)

                img_label = QLabel()
                img_label.setFixedSize(200, 200)
                img_label.setStyleSheet("""
                    QLabel {
                        border: 2px dashed #2196F3;
                        border-radius: 10px;
                        background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                            stop:0 #E3F2FD, stop:1 #F5F9FF);
                        color: #2196F3;
                    }
                """)
                img_label.setAlignment(Qt.AlignCenter)
                img_label.setText("+")
                img_label.setFont(QFont("Arial", 20, QFont.Bold))

                # Store the index in the label for use in mousePressEvent
                img_label.index = len(self.image_labels)
                img_label.mousePressEvent = self.create_click_handler(img_label.index)

                self.image_labels.append(img_label)
                container_layout.addWidget(img_label)

                # Add remove button
                remove_btn = QPushButton("Remove")
                remove_btn.setStyleSheet("""
                    QPushButton {
                        background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                            stop:0 #FF5252, stop:1 #FF1744);
                        color: white;
                        border-radius: 5px;
                        padding: 5px;
                        font-size: 12px;
                        font-weight: bold;
                    }
                    QPushButton:hover {
                        background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                            stop:0 #FF1744, stop:1 #FF5252);
                    }
                """)
                remove_btn.clicked.connect(self.create_remove_handler(img_label.index))
                container_layout.addWidget(remove_btn)

                self.image_containers.append(container)
                grid_layout.addWidget(container, i, j)

        scroll.setWidget(scroll_content)
        layout.addWidget(scroll)

        # Buttons layout
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(10)

        self.save_button = QPushButton("Save Photos")
        self.save_button.setFont(QFont("Arial", 12, QFont.Bold))
        self.save_button.setFixedWidth(200)  # Set fixed width for consistent sizing
        self.save_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white; 
                border-radius: 20px; 
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.save_button.clicked.connect(self.save_photos)  # Connect to save_photos method
        buttons_layout.addWidget(self.save_button, alignment=Qt.AlignCenter)

        self.skip_button = QPushButton("Skip for now")
        self.skip_button.setFont(QFont("Arial", 12, QFont.Bold))
        self.skip_button.setFixedWidth(200)  # Set fixed width for consistent sizing
        self.skip_button.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white; 
                border-radius: 20px; 
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        self.skip_button.clicked.connect(self.skipAction)  # Connect to skipAction method
        buttons_layout.addWidget(self.skip_button, alignment=Qt.AlignCenter)

        layout.addLayout(buttons_layout)
        self.setLayout(layout)

    def create_click_handler(self, index):
        return lambda event: self.openFileDialog(index)

    def create_remove_handler(self, index):
        return lambda: self.remove_photo(index)

    def load_existing_photos(self):
        if self.db and self.current_user:
            print(f"Loading photos for user: {self.current_user}")  # Debug print
            try:
                photos = self.db.get_user_photos(self.current_user)
                print(f"Retrieved {len(photos)} photos from database")  # Debug print
                
                for i, photo_data in enumerate(photos):
                    if i < len(self.image_labels):
                        self.photo_data[i] = photo_data
                        pixmap = QPixmap()
                        pixmap.loadFromData(photo_data)
                        if not pixmap.isNull():
                            self.image_labels[i].setPixmap(pixmap.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                            self.image_labels[i].setText("")
                            print(f"Loaded photo {i+1} successfully")  # Debug print
                        else:
                            print(f"Failed to load photo {i+1} - pixmap is null")  # Debug print
            except Exception as e:
                print(f"Error loading photos: {str(e)}")  # Debug print
        else:
            print("Cannot load photos: db or current_user is None")  # Debug print

    def openFileDialog(self, index):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Select an Image", "", "Images (*.png *.jpg *.jpeg)", options=options)
        if file_name:
            self.photo_paths[index] = file_name
            # Read the image file as binary data
            with open(file_name, 'rb') as file:
                self.photo_data[index] = file.read()
            
            pixmap = QPixmap(file_name)
            if not pixmap.isNull():
                self.image_labels[index].setPixmap(pixmap.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                self.image_labels[index].setText("")

    def remove_photo(self, index):
        self.photo_paths[index] = None
        self.photo_data[index] = None
        self.image_labels[index].setPixmap(QPixmap())
        self.image_labels[index].setText("+")

    def save_photos(self):
        """Save selected photos to the database."""
        if not any(self.photo_data):
            QMessageBox.warning(self, "No Photos", "Please select at least one photo to save.")
            return

        try:
            # Save photos to database
            self.db.save_user_photos(self.current_user, self.photo_data)
            QMessageBox.information(self, "Success", "Photos saved successfully!")
            self.photos_saved.emit()
            
            # Close the dialog if opened from ProfilePage
            if isinstance(self.parent_dialog, QDialog):
                self.parent_dialog.accept()
            # If opened during registration, navigate to HomePage
            else:
                main_window = self.window()
                if hasattr(main_window, 'stack'):
                    dashboard = SaathiDashboard(self.current_user)
                    main_window.stack.addWidget(dashboard)
                    main_window.stack.setCurrentWidget(dashboard)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save photos: {str(e)}")

    def skipAction(self):
        """Handles the skip action."""
        self.photos_skipped.emit()
        
        # Close the dialog if opened from ProfilePage
        if isinstance(self.parent_dialog, QDialog):
            self.parent_dialog.accept()
        # If opened during registration, navigate to HomePage
        else:
            main_window = self.window()
            if hasattr(main_window, 'stack'):
                dashboard = SaathiDashboard(self.current_user)
                main_window.stack.addWidget(dashboard)
                main_window.stack.setCurrentWidget(dashboard)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ImagePickerApp()
    sys.exit(app.exec_())