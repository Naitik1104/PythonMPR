import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QPushButton, QFrame, QScrollArea,
                             QLineEdit, QSpacerItem, QSizePolicy, QStackedWidget, QMessageBox, QDialog, QGridLayout, QComboBox)
from PyQt5.QtCore import Qt, QSize, pyqtSignal
from PyQt5.QtGui import QIcon, QFont, QPixmap, QColor, QPalette, QPainter, QPainterPath, QImage
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from geopy.distance import geodesic
import re
from Messages import Messages
from PyQt5 import QtCore

class FriendSuggestionCard(QFrame):
    def __init__(self, name, interests, image_path):
        super().__init__()
        self.setFixedSize(300, 400)  # Increased from 250x350
        self.setStyleSheet("""
            QFrame {
                background: white;
                border-radius: 15px;
                border: 1px solid #E3E9FF;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Profile picture
        profile_pic = QLabel()
        profile_pic.setFixedSize(200, 200)  # Increased from 150x150
        profile_pic.setPixmap(QPixmap(image_path).scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        profile_pic.setAlignment(Qt.AlignCenter)
        
        # Name
        name_label = QLabel(name)
        name_label.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: bold;
                color: #1E88E5;
            }
        """)
        name_label.setAlignment(Qt.AlignCenter)
        
        # Interests
        interests_label = QLabel(interests)
        interests_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #666;
            }
        """)
        interests_label.setWordWrap(True)
        interests_label.setAlignment(Qt.AlignCenter)
        
        # Buttons
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(10)
        
        add_btn = QPushButton("Add Friend")
        add_btn.setFixedSize(120, 40)  # Increased from 100x35
        add_btn.setStyleSheet("""
            QPushButton {
                background: #4CAF50;
                color: white;
                border: none;
                border-radius: 20px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #45a049;
            }
        """)
        
        view_btn = QPushButton("View Profile")
        view_btn.setFixedSize(120, 40)  # Increased from 100x35
        view_btn.setStyleSheet("""
            QPushButton {
                background: #2196F3;
                color: white;
                border: none;
                border-radius: 20px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #1976D2;
            }
        """)
        
        buttons_layout.addWidget(add_btn)
        buttons_layout.addWidget(view_btn)
        
        layout.addWidget(profile_pic)
        layout.addWidget(name_label)
        layout.addWidget(interests_label)
        layout.addLayout(buttons_layout)

class ActivityCard(QFrame):
    def __init__(self, title, description, time, image_path=None):
        super().__init__()
        self.setObjectName("activityCard")
        self.setStyleSheet("""
            #activityCard {
                background-color: white;
                border-radius: 6px;
                padding: 10px;
                margin: 3px;
            }
            QLabel {
                color: #333;
            }
            QLabel#time {
                color: #888;
                font-size: 9px;
            }
        """)
        
        # Create layout
        layout = QHBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(8)
        
        # Left side - image if provided
        if image_path:
            image_label = QLabel()
            image_label.setFixedSize(40, 40)
            image_label.setScaledContents(True)
            
            # Use placeholder if image path is not available
            try:
                pixmap = QPixmap(image_path)
                if pixmap.isNull():
                    pixmap = QPixmap(40, 40)
                    pixmap.fill(QColor("#6c5ce7"))
            except:
                pixmap = QPixmap(40, 40)
                pixmap.fill(QColor("#6c5ce7"))
                
            image_label.setPixmap(pixmap)
            layout.addWidget(image_label)
        
        # Right side - content
        content_layout = QVBoxLayout()
        content_layout.setSpacing(3)
        
        title_label = QLabel(title)
        title_label.setFont(QFont("Segoe UI", 9, QFont.Bold))
        
        desc_label = QLabel(description)
        desc_label.setWordWrap(True)
        desc_label.setFont(QFont("Segoe UI", 8))
        
        time_label = QLabel(time)
        time_label.setObjectName("time")
        
        content_layout.addWidget(title_label)
        content_layout.addWidget(desc_label)
        content_layout.addWidget(time_label)
        
        layout.addLayout(content_layout)
        layout.setStretch(0, 0)
        layout.setStretch(1, 1)

class EventCard(QFrame):
    def __init__(self, title, date, location):
        super().__init__()
        self.setObjectName("eventCard")
        self.setStyleSheet("""
            #eventCard {
                background-color: white;
                border-radius: 6px;
                padding: 10px;
                margin: 3px;
            }
            QLabel {
                color: #333;
            }
            QLabel#eventDate, QLabel#eventLocation {
                color: #666;
                font-size: 9px;
            }
            QPushButton {
                background-color: #6c5ce7;
                color: white;
                border: none;
                border-radius: 3px;
                padding: 4px 8px;
                font-size: 10px;
            }
            QPushButton:hover {
                background-color: #5b4bc4;
            }
        """)
        
        # Create layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(3)
        
        # Event info
        title_label = QLabel(title)
        title_label.setFont(QFont("Segoe UI", 10, QFont.Bold))
        
        date_label = QLabel(date)
        date_label.setObjectName("eventDate")
        
        location_label = QLabel(location)
        location_label.setObjectName("eventLocation")
        
        # Join button
        join_btn = QPushButton("Join Event")
        
        # Add widgets to layout
        layout.addWidget(title_label)
        layout.addWidget(date_label)
        layout.addWidget(location_label)
        layout.addWidget(join_btn, alignment=Qt.AlignRight)

class SideBar(QFrame):
    button_clicked_signal = pyqtSignal(str)  # Define the signal at class level
    
    def __init__(self):
        super().__init__()
        self.setFixedWidth(250)
        self.setStyleSheet("""
            QFrame {
                background: #E3F2FD;  /* Warm light blue background */
                border-right: 2px solid #BBDEFB;
            }
        """)
        
        # Create main layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Logo
        logo_label = QLabel()
        logo_label.setFixedSize(150, 150)
        logo_pixmap = QPixmap("assets/Saathilogo2.png")
        if not logo_pixmap.isNull():
            logo_label.setPixmap(logo_pixmap.scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        logo_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(logo_label)
        
        # Navigation buttons in specified order
        buttons = [
            ("Home", "icons/home.png"),
            ("Explore", "icons/explore.png"),
            ("Messages", "icons/chat.png"),
            ("Events", "icons/event.png"),
            ("Profile", "icons/profile.png"),
            ("", ""),  # Spacer
            ("Help", "icons/help.png")
        ]
        
        for text, icon_path in buttons:
            if text == "":  # Spacer
                layout.addStretch()
                continue
                
            button = QPushButton(text)
            button.setFixedHeight(50)
            button.setStyleSheet("""
            QPushButton {
                    background: transparent;
                border: none;
                    color: #666;
                    font-size: 16px;
                    text-align: left;
                    padding-left: 20px;
                    border-radius: 8px;
            }
            QPushButton:hover {
                    background: #F5F9FF;
                    color: #1E88E5;
                }
                QPushButton:checked {
                    background: #E3F2FD;
                    color: #1E88E5;
                    font-weight: bold;
            }
        """)
            button.setCheckable(True)
            button.clicked.connect(lambda checked, b=button: self.button_clicked(b))
            
            # Add icon if available
            if icon_path:
                icon = QIcon(icon_path)
                button.setIcon(icon)
                button.setIconSize(QtCore.QSize(24, 24))
            
            layout.addWidget(button)
        
        # Set first button (Home) as checked by default
        if layout.count() > 1:  # Check if there are any buttons
            first_button = layout.itemAt(1).widget()  # First button after logo
            if isinstance(first_button, QPushButton):
                first_button.setChecked(True)
    
    def button_clicked(self, button):
        # Uncheck all other buttons
        for btn in self.findChildren(QPushButton):
            if btn != button:
                btn.setChecked(False)
        button.setChecked(True)
        # Emit the signal with the button's text
        self.button_clicked_signal.emit(button.text())

class ViewProfileDialog(QDialog):
    def __init__(self, user_id, db, parent=None):
        super().__init__(parent)
        self.db = db
        self.user_id = user_id
        self.setWindowTitle("View Profile")
        self.setFixedSize(800, 600)
        self.setStyleSheet("""
            QDialog {
                background: #F5F9FF;
            }
        """)
        self.initUI()
        self.load_user_data()

    def initUI(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        # Create scroll area
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

        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(20)

        # Profile section
        profile_widget = QWidget()
        profile_layout = QHBoxLayout(profile_widget)

        # Profile picture
        self.profile_pic = QLabel()
        self.profile_pic.setFixedSize(150, 150)
        self.profile_pic.setStyleSheet("""
            QLabel {
                background: #F5F5F5;
                border-radius: 75px;
                border: 2px solid #E3E9FF;
            }
        """)

        # User info
        info_widget = QWidget()
        info_layout = QVBoxLayout(info_widget)
        self.name_label = QLabel()
        self.name_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #333;")
        self.age_gender_label = QLabel()
        self.location_label = QLabel()
        self.interests_label = QLabel()
        
        info_layout.addWidget(self.name_label)
        info_layout.addWidget(self.age_gender_label)
        info_layout.addWidget(self.location_label)
        info_layout.addWidget(self.interests_label)
        info_layout.addStretch()

        profile_layout.addWidget(self.profile_pic)
        profile_layout.addWidget(info_widget)
        profile_layout.addStretch()

        # Bio section
        bio_widget = QWidget()
        bio_layout = QVBoxLayout(bio_widget)
        bio_title = QLabel("About")
        bio_title.setStyleSheet("font-size: 18px; font-weight: bold; color: #333;")
        self.bio_text = QLabel()
        self.bio_text.setWordWrap(True)
        self.bio_text.setStyleSheet("font-size: 14px; color: #666; line-height: 1.4;")
        
        bio_layout.addWidget(bio_title)
        bio_layout.addWidget(self.bio_text)

        # Photos section
        photos_widget = QWidget()
        photos_layout = QVBoxLayout(photos_widget)
        photos_title = QLabel("Photos")
        photos_title.setStyleSheet("font-size: 18px; font-weight: bold; color: #333;")
        
        photos_grid = QGridLayout()
        self.photo_labels = []
        for i in range(6):
            photo_label = QLabel()
            photo_label.setFixedSize(200, 200)
            photo_label.setStyleSheet("""
                QLabel {
                    background: #F5F5F5;
                    border-radius: 10px;
                    border: 2px solid #E3E9FF;
                }
            """)
            self.photo_labels.append(photo_label)
            photos_grid.addWidget(photo_label, i // 3, i % 3)

        photos_layout.addWidget(photos_title)
        photos_layout.addLayout(photos_grid)

        # Add all sections to main layout
        content_layout.addWidget(profile_widget)
        content_layout.addWidget(bio_widget)
        content_layout.addWidget(photos_widget)
        content_layout.addStretch()

        scroll.setWidget(content_widget)
        layout.addWidget(scroll)

    def load_user_data(self):
        cursor = self.db.connection.cursor()
        try:
            # Get user data
            cursor.execute("""
                SELECT u.name, u.age, u.gender, u.location, 
                       p.Interests, p.Bio, p.profile_picture
                FROM users u
                LEFT JOIN profiles p ON u.id = p.user_id
                WHERE u.id = %s
            """, (self.user_id,))
            user_data = cursor.fetchone()
            
            if user_data:
                name, age, gender, location, interests, bio, profile_pic = user_data
                
                # Update UI elements
                self.name_label.setText(name)
                self.age_gender_label.setText(f"{age} • {gender}")
                self.location_label.setText(location if location else "Location not set")
                self.interests_label.setText(f"Interests: {interests}" if interests else "No interests listed")
                self.bio_text.setText(bio if bio else "No bio available")

                # Set profile picture
                if profile_pic:
                    pixmap = QPixmap()
                    pixmap.loadFromData(profile_pic)
                    if not pixmap.isNull():
                        self.profile_pic.setPixmap(pixmap.scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation))

                # Get and set photos
                cursor.execute("""
                    SELECT photo FROM photos 
                    WHERE user_id = %s 
                    ORDER BY upload_date DESC
                """, (self.user_id,))
                photos = cursor.fetchall()

                for i, photo in enumerate(photos):
                    if i < len(self.photo_labels):
                        pixmap = QPixmap()
                        pixmap.loadFromData(photo[0])
                        if not pixmap.isNull():
                            self.photo_labels[i].setPixmap(
                                pixmap.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                            )

        finally:
            cursor.close()

class ViewAllDialog(QDialog):
    def __init__(self, title, items, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setFixedSize(800, 600)
        self.items = items
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        # Title
        title_label = QLabel(self.windowTitle())
        title_label.setStyleSheet("""
            QLabel {
                color: #2196F3;
                font-size: 24px;
                font-weight: bold;
            }
        """)
        layout.addWidget(title_label)

        # Scroll Area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background: transparent;
            }
            QScrollBar:vertical {
                width: 12px;
                background: #F0F0F0;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background: #2196F3;
                border-radius: 6px;
                min-height: 50px;
            }
        """)

        # Container widget for grid
        container = QWidget()
        grid_layout = QGridLayout(container)
        grid_layout.setSpacing(20)
        grid_layout.setContentsMargins(10, 10, 10, 10)

        # Add items to grid, 3 items per row
        for i, item in enumerate(self.items):
            row = i // 3
            col = i % 3
            grid_layout.addWidget(item, row, col)

        scroll.setWidget(container)
        layout.addWidget(scroll)

        # Close button
        close_btn = QPushButton("Close")
        close_btn.setFixedSize(200, 40)
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border-radius: 20px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn, alignment=Qt.AlignCenter)

class DashboardWidget(QWidget):
    def __init__(self, current_user=None, db=None):
        super().__init__()
        self.current_user = current_user
        self.db = db
        self.setFixedSize(774, 768)  # Set fixed width and height to match the main window
        self.messages_page = None
        self.stacked_widget = None
        
        # Get current user's ID
        cursor = self.db.connection.cursor()
        cursor.execute("SELECT id FROM users WHERE name = %s", (self.current_user,))
        result = cursor.fetchone()
        self.current_user_id = result[0] if result else None
        cursor.close()
        
        self.initUI()
        self.load_friend_requests()
        self.load_friends()

    def initUI(self):
        # Create main scroll area to contain everything
        main_scroll = QScrollArea(self)
        main_scroll.setFixedSize(774, 768)  # Set fixed size to match parent
        main_scroll.setWidgetResizable(True)
        main_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        main_scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background: transparent;
            }
            QScrollBar:vertical {
                width: 12px;
                background: #F0F0F0;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background: #2196F3;
                border-radius: 6px;
                min-height: 50px;
            }
        """)

        # Create container widget for the scroll area
        container = QWidget()
        main_layout = QVBoxLayout(container)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(30)

        # Friend Requests Section
        requests_section = QWidget()
        requests_layout = QVBoxLayout(requests_section)
        requests_layout.setContentsMargins(0, 0, 0, 0)
        requests_layout.setSpacing(15)

        # Header with title and View All button
        requests_header = QHBoxLayout()
        requests_title = QLabel("Friend Requests")
        requests_title.setStyleSheet("font-size: 20px; font-weight: bold; color: #2196F3;")
        view_all_requests = QPushButton("View All")
        view_all_requests.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border-radius: 15px;
                padding: 5px 15px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        view_all_requests.clicked.connect(self.show_all_requests)
        requests_header.addWidget(requests_title)
        requests_header.addStretch()
        requests_header.addWidget(view_all_requests)
        requests_layout.addLayout(requests_header)

        # Create scroll area for requests
        requests_scroll = QScrollArea()
        requests_scroll.setWidgetResizable(True)
        requests_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        requests_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        requests_scroll.setMinimumHeight(300)
        requests_scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background: transparent;
            }
            QScrollBar:horizontal {
                height: 12px;
                background: #F0F0F0;
                border-radius: 6px;
            }
            QScrollBar::handle:horizontal {
                background: #2196F3;
                border-radius: 6px;
                min-width: 50px;
            }
        """)

        # Container for requests grid
        requests_container = QWidget()
        self.requests_grid = QHBoxLayout(requests_container)
        self.requests_grid.setSpacing(20)
        self.requests_grid.setContentsMargins(0, 0, 20, 0)  # Added right margin for scrollbar
        requests_scroll.setWidget(requests_container)
        requests_layout.addWidget(requests_scroll)

        # Your Requests Section (similar structure)
        your_requests_section = QWidget()
        your_requests_layout = QVBoxLayout(your_requests_section)
        your_requests_layout.setContentsMargins(0, 0, 0, 0)
        your_requests_layout.setSpacing(15)

        your_requests_header = QHBoxLayout()
        your_requests_title = QLabel("Track Your Requests")
        your_requests_title.setStyleSheet("font-size: 20px; font-weight: bold; color: #2196F3;")
        view_all_your_requests = QPushButton("View All")
        view_all_your_requests.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border-radius: 15px;
                padding: 5px 15px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        view_all_your_requests.clicked.connect(self.show_all_sent_requests)
        your_requests_header.addWidget(your_requests_title)
        your_requests_header.addStretch()
        your_requests_header.addWidget(view_all_your_requests)
        your_requests_layout.addLayout(your_requests_header)

        your_requests_scroll = QScrollArea()
        your_requests_scroll.setWidgetResizable(True)
        your_requests_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        your_requests_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        your_requests_scroll.setMinimumHeight(300)
        your_requests_scroll.setStyleSheet(requests_scroll.styleSheet())

        your_requests_container = QWidget()
        self.your_requests_grid = QHBoxLayout(your_requests_container)
        self.your_requests_grid.setSpacing(20)
        self.your_requests_grid.setContentsMargins(0, 0, 20, 0)  # Added right margin for scrollbar
        your_requests_scroll.setWidget(your_requests_container)
        your_requests_layout.addWidget(your_requests_scroll)

        # Friends Section (similar structure)
        friends_section = QWidget()
        friends_layout = QVBoxLayout(friends_section)
        friends_layout.setContentsMargins(0, 0, 0, 0)
        friends_layout.setSpacing(15)

        friends_header = QHBoxLayout()
        friends_title = QLabel("Friends")
        friends_title.setStyleSheet("font-size: 20px; font-weight: bold; color: #2196F3;")
        view_all_friends = QPushButton("View All")
        view_all_friends.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border-radius: 15px;
                padding: 5px 15px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        view_all_friends.clicked.connect(self.show_all_friends)
        friends_header.addWidget(friends_title)
        friends_header.addStretch()
        friends_header.addWidget(view_all_friends)
        friends_layout.addLayout(friends_header)

        friends_scroll = QScrollArea()
        friends_scroll.setWidgetResizable(True)
        friends_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        friends_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        friends_scroll.setMinimumHeight(300)
        friends_scroll.setStyleSheet(requests_scroll.styleSheet())

        friends_container = QWidget()
        self.friends_grid = QHBoxLayout(friends_container)
        self.friends_grid.setSpacing(20)
        self.friends_grid.setContentsMargins(0, 0, 20, 0)  # Added right margin for scrollbar
        friends_scroll.setWidget(friends_container)
        friends_layout.addWidget(friends_scroll)

        # Add all sections to main layout
        main_layout.addWidget(requests_section)
        main_layout.addWidget(your_requests_section)
        main_layout.addWidget(friends_section)

        # Set the container as the scroll area widget
        main_scroll.setWidget(container)

        # Load initial data
        self.load_friend_requests()
        self.load_your_requests()
        self.load_friends()

    def load_friend_requests(self):
        """Load friend requests into the horizontal scroll area"""
        # Clear existing items
        while self.requests_grid.count():
            item = self.requests_grid.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        try:
            cursor = self.db.connection.cursor()
            cursor.execute("""
                    SELECT u.id, u.name, p.profile_picture 
                    FROM friend_requests fr
                    JOIN users u ON fr.sender_id = u.id
                    LEFT JOIN profiles p ON u.id = p.user_id
                WHERE fr.receiver_id = (SELECT id FROM users WHERE name = %s)
                AND fr.status = 'pending'
            """, (self.current_user,))
            requests = cursor.fetchall()
                
            if not requests:
                # Add placeholder message
                placeholder = QLabel("No friend requests")
                placeholder.setStyleSheet("""
                    QLabel {
                        color: #666;
                        font-size: 16px;
                        padding: 20px;
                    }
                """)
                self.requests_grid.addWidget(placeholder)
            else:
                # Add request cards horizontally
                for request in requests:
                    sender_id, name, profile_pic = request
                    card = self.create_request_card(name, profile_pic, sender_id)
                    self.requests_grid.addWidget(card)

                # Add stretch at the end to keep cards left-aligned
                self.requests_grid.addStretch()
                
        except Exception as e:
            print(f"Error loading friend requests: {e}")
        finally:
            cursor.close()

    def load_your_requests(self):
        """Load sent friend requests into the horizontal scroll area"""
        # Clear existing items
        while self.your_requests_grid.count():
            item = self.your_requests_grid.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        try:
            cursor = self.db.connection.cursor()
            cursor.execute("""
                SELECT u.id, u.name, p.profile_picture, fr.status, fr.request_date
                FROM friend_requests fr
                JOIN users u ON fr.receiver_id = u.id
                LEFT JOIN profiles p ON u.id = p.user_id
                WHERE fr.sender_id = (SELECT id FROM users WHERE name = %s)
                AND fr.status IN ('pending', 'declined')
                ORDER BY fr.request_date DESC
            """, (self.current_user,))
            requests = cursor.fetchall()

            if not requests:
                # Add placeholder message
                placeholder = QLabel("No sent requests")
                placeholder.setStyleSheet("""
                    QLabel {
                        color: #666;
                        font-size: 16px;
                        padding: 20px;
                    }
                """)
                self.your_requests_grid.addWidget(placeholder)
            else:
                # Add request cards horizontally
                for request in requests:
                    receiver_id, name, profile_pic, status, request_date = request
                    card = self.create_sent_request_card(name, profile_pic, receiver_id, status, request_date)
                    self.your_requests_grid.addWidget(card)

                # Add stretch at the end to keep cards left-aligned
                self.your_requests_grid.addStretch()

        except Exception as e:
            print(f"Error loading your requests: {e}")
        finally:
            cursor.close()

    def load_friends(self):
        """Load friends into the horizontal scroll area"""
        # Clear existing items
        while self.friends_grid.count():
            item = self.friends_grid.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        try:
            cursor = self.db.connection.cursor()
            cursor.execute("""
                    SELECT u.id, u.name, p.profile_picture
                    FROM friends f
                    JOIN users u ON (CASE 
                    WHEN f.user1_id = (SELECT id FROM users WHERE name = %s) 
                    THEN f.user2_id = u.id
                    ELSE f.user1_id = u.id
                    END)
                    LEFT JOIN profiles p ON u.id = p.user_id
                WHERE f.user1_id = (SELECT id FROM users WHERE name = %s)
                OR f.user2_id = (SELECT id FROM users WHERE name = %s)
                ORDER BY u.name
            """, (self.current_user, self.current_user, self.current_user))
            friends = cursor.fetchall()
                
            if not friends:
                # Add placeholder message
                placeholder = QLabel("No friends yet")
                placeholder.setStyleSheet("""
                    QLabel {
                        color: #666;
                        font-size: 16px;
                        padding: 20px;
                    }
                """)
                self.friends_grid.addWidget(placeholder)
            else:
                # Add friend cards horizontally
                for friend in friends:
                    friend_id, name, profile_pic = friend
                    card = self.create_friend_card(name, profile_pic, friend_id)
                    self.friends_grid.addWidget(card)

                # Add stretch at the end to keep cards left-aligned
                self.friends_grid.addStretch()
                
        except Exception as e:
            print(f"Error loading friends: {e}")
        finally:
            cursor.close()

    def create_request_card(self, name, profile_pic, sender_id):
        """Create a card widget for a friend request"""
        card = QFrame()
        card.setFixedSize(200, 280)
        card.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
                padding: 15px;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Profile picture
        pic_label = QLabel()
        pic_label.setFixedSize(120, 120)
        if profile_pic:
            pixmap = QPixmap()
            pixmap.loadFromData(profile_pic)
            pic_label.setPixmap(pixmap.scaled(120, 120, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            pic_label.setText("No Photo")
            pic_label.setStyleSheet("""
            QLabel {
                    background-color: #f0f0f0;
                    border-radius: 60px;
                    color: #666;
                    font-size: 14px;
            }
        """)
        pic_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(pic_label, alignment=Qt.AlignCenter)
        
        # Name label
        name_label = QLabel(name)
        name_label.setStyleSheet("""
            QLabel {
                color: #333;
                font-size: 16px;
                font-weight: bold;
                background-color: rgba(255, 255, 255, 0.9);
                padding: 5px;
                border-radius: 5px;
            }
        """)
        name_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(name_label)
        
        # Buttons container
        buttons_layout = QHBoxLayout()
        
        # Accept button
        accept_btn = QPushButton("Accept")
        accept_btn.setFixedSize(85, 30)
        accept_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border-radius: 5px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        accept_btn.clicked.connect(lambda: self.accept_request(sender_id, card))
        buttons_layout.addWidget(accept_btn)
        
        # Decline button
        decline_btn = QPushButton("Decline")
        decline_btn.setFixedSize(85, 30)
        decline_btn.setStyleSheet("""
            QPushButton {
                background-color: #ff5252;
                color: white;
                border-radius: 5px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #ff1744;
            }
        """)
        decline_btn.clicked.connect(lambda: self.decline_request(sender_id, card))
        buttons_layout.addWidget(decline_btn)
        
        layout.addLayout(buttons_layout)
        
        # View Profile button
        view_btn = QPushButton("View Profile")
        view_btn.setFixedSize(180, 30)
        view_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border-radius: 5px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        view_btn.clicked.connect(lambda: self.view_profile(sender_id))
        layout.addWidget(view_btn)
        
        card.setLayout(layout)
        return card

    def create_sent_request_card(self, name, profile_pic, receiver_id, status, request_date):
        """Create a card widget for a sent friend request"""
        card = QFrame()
        card.setFixedSize(200, 280)
        card.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
                padding: 15px;
            }
        """)

        layout = QVBoxLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Profile picture
        pic_label = QLabel()
        pic_label.setFixedSize(120, 120)
        if profile_pic:
            pixmap = QPixmap()
            pixmap.loadFromData(profile_pic)
            pic_label.setPixmap(pixmap.scaled(120, 120, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            pic_label.setText("No Photo")
            pic_label.setStyleSheet("""
                QLabel {
                    background-color: #f0f0f0;
                    border-radius: 60px;
                        color: #666;
                    font-size: 14px;
                }
            """)
        pic_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(pic_label, alignment=Qt.AlignCenter)
        
        # Name label
        name_label = QLabel(name)
        name_label.setStyleSheet("""
            QLabel {
                color: #333;
                font-size: 16px;
                font-weight: bold;
                background-color: rgba(255, 255, 255, 0.9);
                padding: 5px;
                border-radius: 5px;
            }
        """)
        name_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(name_label)
        
        # Status label
        status_label = QLabel(f"Status: {status.title()}")
        status_color = "#FF9800" if status == "pending" else "#F44336"  # Orange for pending, Red for declined
        status_label.setStyleSheet(f"""
            QLabel {{
                color: {status_color};
                font-size: 14px;
                font-weight: bold;
                background-color: rgba(255, 255, 255, 0.9);
                padding: 5px;
                border-radius: 5px;
            }}
        """)
        status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(status_label)
        
        # Roll back button (only for pending requests)
        if status == "pending":
            rollback_btn = QPushButton("Roll Back")
            rollback_btn.setFixedSize(180, 30)
            rollback_btn.setStyleSheet("""
                QPushButton {
                    background-color: #ff5252;
                    color: white;
                border-radius: 5px;
                    font-size: 12px;
                }
                QPushButton:hover {
                    background-color: #ff1744;
            }
        """)
            rollback_btn.clicked.connect(lambda: self.rollback_request(receiver_id, card))
            layout.addWidget(rollback_btn)
        
        # Date label
        date_str = request_date.strftime("%Y-%m-%d %H:%M")
        date_label = QLabel(f"Sent: {date_str}")
        date_label.setStyleSheet("""
            QLabel {
                        color: #666;
                font-size: 12px;
                background-color: rgba(255, 255, 255, 0.9);
                padding: 5px;
                border-radius: 5px;
            }
        """)
        date_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(date_label)
        
        card.setLayout(layout)
        return card

    def create_friend_card(self, name, profile_pic, friend_id):
        """Create a card widget for a friend"""
        card = QFrame()
        card.setFixedSize(200, 280)
        card.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
                padding: 15px;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Profile picture
        pic_label = QLabel()
        pic_label.setFixedSize(120, 120)
        if profile_pic:
            pixmap = QPixmap()
            pixmap.loadFromData(profile_pic)
            pic_label.setPixmap(pixmap.scaled(120, 120, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            pic_label.setText("No Photo")
            pic_label.setStyleSheet("""
            QLabel {
                    background-color: #f0f0f0;
                    border-radius: 60px;
                    color: #666;
                    font-size: 14px;
            }
        """)
        pic_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(pic_label, alignment=Qt.AlignCenter)
        
        # Name label
        name_label = QLabel(name)
        name_label.setStyleSheet("""
            QLabel {
                color: #333;
                font-size: 16px;
                font-weight: bold;
                background-color: rgba(255, 255, 255, 0.9);
                padding: 5px;
                border-radius: 5px;
            }
        """)
        name_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(name_label)
        
        # Buttons container
        buttons_layout = QHBoxLayout()
        
        # View Profile button
        view_btn = QPushButton("View")
        view_btn.setFixedSize(85, 30)
        view_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border-radius: 5px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        view_btn.clicked.connect(lambda: self.view_profile(friend_id))
        buttons_layout.addWidget(view_btn)
        
        # Remove button
        remove_btn = QPushButton("Remove")
        remove_btn.setFixedSize(85, 30)
        remove_btn.setStyleSheet("""
            QPushButton {
                background-color: #ff5252;
                color: white;
                border-radius: 5px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #ff1744;
            }
        """)
        remove_btn.clicked.connect(lambda: self.remove_friend(friend_id, card))
        buttons_layout.addWidget(remove_btn)
        
        layout.addLayout(buttons_layout)
        card.setLayout(layout)
        return card

    def rollback_request(self, receiver_id, card):
        """Roll back a pending friend request"""
        reply = QMessageBox.question(
            self,
            "Confirm Roll Back",
            "Are you sure you want to roll back this friend request?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                cursor = self.db.connection.cursor()
                cursor.execute("""
                    DELETE FROM friend_requests 
                    WHERE sender_id = (SELECT id FROM users WHERE name = %s)
                    AND receiver_id = %s
                """, (self.current_user, receiver_id))
                self.db.connection.commit()
                
                # Remove the card from UI
                card.setParent(None)
                self.load_your_requests()  # Reload the requests section
                    
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to roll back request: {str(e)}")
            finally:
                cursor.close()

    def remove_friend(self, friend_id, card):
        """Remove a friend and delete the entry from database"""
        reply = QMessageBox.question(
            self,
            "Confirm Remove",
            "Are you sure you want to remove this friend?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            try:
                cursor = self.db.connection.cursor()
                cursor.execute("""
                    DELETE FROM friends 
                    WHERE (user1_id = (SELECT id FROM users WHERE name = %s) AND user2_id = %s)
                    OR (user2_id = (SELECT id FROM users WHERE name = %s) AND user1_id = %s)
                """, (self.current_user, friend_id, self.current_user, friend_id))
                self.db.connection.commit()
                
                # Remove the card from UI
                card.setParent(None)
                self.load_friends()  # Reload the friends section
                
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to remove friend: {str(e)}")
            finally:
                cursor.close()

    def view_profile(self, friend_id):
        dialog = ViewProfileDialog(friend_id, self.db, self)
        dialog.exec_()

    def calculate_profile_completeness(self, age, location, gender, interests, bio, profile_pic):
        """Calculate profile completeness score"""
        score = 0
        if age: score += 0.2
        if location: score += 0.2
        if gender: score += 0.1
        if interests: score += 0.2
        if bio: score += 0.2
        if profile_pic: score += 0.1
        return score

    def calculate_interest_similarity(self, user1_id, user2_id):
        """Calculate interest similarity between two users"""
        cursor = self.db.connection.cursor()
        try:
            # Get interests for both users
            cursor.execute("""
                SELECT user_id, Interests
                FROM profiles
                WHERE user_id IN (%s, %s)
            """, (user1_id, user2_id))
            
            interests_data = cursor.fetchall()
            if len(interests_data) != 2:
                return 0
            
            # Convert interests strings to sets
            interests1 = set(interests_data[0][1].lower().split(',')) if interests_data[0][1] else set()
            interests2 = set(interests_data[1][1].lower().split(',')) if interests_data[1][1] else set()
            
            # Calculate Jaccard similarity
            if not interests1 or not interests2:
                return 0
                
            similarity = len(interests1.intersection(interests2)) / len(interests1.union(interests2))
            return similarity
            
        finally:
            cursor.close()

    def accept_request(self, sender_id, card):
        try:
            cursor = self.db.connection.cursor()
            
            # Add to friends table
            cursor.execute("""
                INSERT INTO friends (user1_id, user2_id)
                VALUES (%s, %s)
            """, (sender_id, self.current_user_id))
            
            # Remove from friend_requests table
            cursor.execute("""
                DELETE FROM friend_requests
                WHERE sender_id = %s AND receiver_id = %s
            """, (sender_id, self.current_user_id))
            
            self.db.connection.commit()
            
            # Remove the request card from the UI
            self.requests_grid.removeWidget(card)
            card.deleteLater()
            
            # Add to friends section
            self.load_friends()
            
            # Show success message
            QMessageBox.information(self, "Success", "Friend request accepted!")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to accept friend request: {str(e)}")
        finally:
            cursor.close()

    def decline_request(self, sender_id, card):
        try:
            cursor = self.db.connection.cursor()
            
            # Remove from friend_requests table
            cursor.execute("""
                DELETE FROM friend_requests
                WHERE sender_id = %s AND receiver_id = %s
            """, (sender_id, self.current_user_id))
            
            self.db.connection.commit()
            
            # Remove the request card from the UI
            self.requests_grid.removeWidget(card)
            card.deleteLater()
            
            # Show success message
            QMessageBox.information(self, "Success", "Friend request declined!")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to decline friend request: {str(e)}")
        finally:
            cursor.close()

    def show_all_requests(self):
        """Show all friend requests in a dialog"""
        try:
            cursor = self.db.connection.cursor()
            cursor.execute("""
                SELECT fr.sender_id, u.name, p.profile_picture, fr.status
                FROM friend_requests fr
                JOIN users u ON fr.sender_id = u.id
                LEFT JOIN profiles p ON fr.sender_id = p.user_id
                WHERE fr.receiver_id = %s AND fr.status = 'pending'
                ORDER BY fr.request_date DESC
            """, (self.current_user_id,))
            
            requests = cursor.fetchall()
            request_cards = []
            
            for request in requests:
                sender_id, name, profile_pic, status = request
                card = self.create_request_card(name, profile_pic, sender_id)
                request_cards.append(card)
            
            dialog = ViewAllDialog("Friend Requests", request_cards, self)
            dialog.exec_()
            
        finally:
            cursor.close()

    def show_all_friends(self):
        """Show all friends in a dialog"""
        try:
            cursor = self.db.connection.cursor()
            cursor.execute("""
                SELECT u.id, u.name, p.profile_picture
                FROM users u
                LEFT JOIN profiles p ON u.id = p.user_id
                WHERE u.id IN (
                    SELECT CASE 
                        WHEN user1_id = %s THEN user2_id
                        WHEN user2_id = %s THEN user1_id
                    END
                    FROM friends
                    WHERE user1_id = %s OR user2_id = %s
                )
            """, (self.current_user_id, self.current_user_id, self.current_user_id, self.current_user_id))
            
            friends = cursor.fetchall()
            friend_cards = []
            
            for friend in friends:
                friend_id, username, profile_pic = friend
                card = self.create_friend_card(username, profile_pic, friend_id)
                friend_cards.append(card)
            
            dialog = ViewAllDialog("Friends", friend_cards, self)
            dialog.exec_()
            
        finally:
            cursor.close()

    def show_all_sent_requests(self):
        """Show all sent requests in a dialog"""
        try:
            cursor = self.db.connection.cursor()
            cursor.execute("""
                SELECT fr.receiver_id, u.name, p.profile_picture, fr.status, fr.request_date
                FROM friend_requests fr
                JOIN users u ON fr.receiver_id = u.id
                LEFT JOIN profiles p ON fr.receiver_id = p.user_id
                WHERE fr.sender_id = %s AND fr.status IN ('pending', 'declined')
                ORDER BY fr.request_date DESC
            """, (self.current_user_id,))
            
            requests = cursor.fetchall()
            request_cards = []
            
            for request in requests:
                receiver_id, name, profile_pic, status, request_date = request
                card = self.create_sent_request_card(name, profile_pic, receiver_id, status, request_date)
                request_cards.append(card)
            
            dialog = ViewAllDialog("Track Your Requests", request_cards, self)
            dialog.exec_()
            
        finally:
            cursor.close()

    def show_all_friends_and_requests(self):
        """Show all friends and requests"""
        self.show_all_friends()
        self.show_all_requests()

class SaathiDashboard(QMainWindow):
    def __init__(self, current_user=None):
        super().__init__()
        self.current_user = current_user
        self.setWindowTitle("Saathi - Dashboard")
        self.setGeometry(100, 100, 1024, 768)
        
        # Initialize pages as None
        self.profile_page = None
        self.events_page = None
        self.safety_page = None
        self.explore_page = None
        self.messages_page = None
        
        # Initialize database connection
        try:
            from database1 import Database
            self.db = Database(host='localhost', user='root', password='naitik@mysql', database='saathi')
        except Exception as e:
            print(f"Error connecting to database: {e}")
            QMessageBox.critical(self, "Database Error", "Could not connect to database. Please check your connection and try again.")
            return
        
        # Set app style
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f7fa;
            }
            QLabel {
                color: #333;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QPushButton {
                background-color: #4CA6FF;
                color: white;
                border: none;
                border-radius: 3px;
                padding: 4px 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2196F3;
            }
            QLineEdit {
                padding: 4px;
                border: 1px solid #ddd;
                border-radius: 3px;
            }
            QScrollBar:vertical {
                border: none;
                background: #f0f0f0;
                width: 8px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #c0c0c0;
                min-height: 20px;
                border-radius: 4px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Create sidebar
        self.sidebar = SideBar()
        main_layout.addWidget(self.sidebar)
        
        # Create stacked widget for different pages
        self.stacked_widget = QStackedWidget()
        main_layout.addWidget(self.stacked_widget)
        
        # Create dashboard widget with database connection
        self.dashboard = DashboardWidget(current_user, self.db)
        self.stacked_widget.addWidget(self.dashboard)
        
        # Set layout ratio (sidebar:content)
        main_layout.setStretch(0, 1)  # Sidebar takes 1 part
        main_layout.setStretch(1, 5)  # Content takes 5 parts
        
        # Connect sidebar button signals to page switching
        self.sidebar.button_clicked_signal.connect(self.handle_sidebar_button)

    def handle_sidebar_button(self, button_text):
        if button_text == "Home":
            self.show_home_page()
        elif button_text == "Profile":
            self.show_profile()
        elif button_text == "Events":
            self.show_events()
        elif button_text == "Help":
            self.show_safety_page()
        elif button_text == "Explore":
            self.show_explore()
        elif button_text == "Messages":
            self.show_messages()

    def update_sidebar_highlight(self, button_text):
        # Find the button in the sidebar and set it as checked
        for i in range(self.sidebar.layout().count()):
            widget = self.sidebar.layout().itemAt(i).widget()
            if isinstance(widget, QPushButton) and widget.text() == button_text:
                widget.setChecked(True)
            elif isinstance(widget, QPushButton):
                widget.setChecked(False)
        
    def show_home_page(self):
        self.stacked_widget.setCurrentWidget(self.dashboard)
        self.update_sidebar_highlight("Home")
        
    def show_profile(self):
        if self.profile_page is None:
            from ProfilePage import ProfilePage
            self.profile_page = ProfilePage(current_user=self.current_user)
            self.stacked_widget.addWidget(self.profile_page)
        self.stacked_widget.setCurrentWidget(self.profile_page)
        self.update_sidebar_highlight("Profile")
        
    def show_events(self):
        if self.events_page is None:
            from EventPage import CalendarApp
            self.events_page = CalendarApp()
            self.stacked_widget.addWidget(self.events_page)
        self.stacked_widget.setCurrentWidget(self.events_page)
        self.update_sidebar_highlight("Events")
        
    def show_safety_page(self):
        if self.safety_page is None:
            from SafetyPage import HelpSafetyPage
            self.safety_page = HelpSafetyPage(current_user=self.current_user)
            self.stacked_widget.addWidget(self.safety_page)
        self.stacked_widget.setCurrentWidget(self.safety_page)
        self.update_sidebar_highlight("Help")
        
    def show_explore(self):
        if self.explore_page is None:
            from ExplorePage import ExplorePage
            self.explore_page = ExplorePage(current_user=self.current_user)
            self.stacked_widget.addWidget(self.explore_page)
        self.stacked_widget.setCurrentWidget(self.explore_page)
        self.update_sidebar_highlight("Explore")
        
    def show_messages(self):
        if self.messages_page is None:
            from Messages import Messages
            cursor = self.db.connection.cursor()
            cursor.execute("SELECT id FROM users WHERE name = %s", (self.current_user,))
            user_id = cursor.fetchone()[0]
            cursor.close()
            
            self.messages_page = Messages(user_id, self.current_user)
            self.stacked_widget.addWidget(self.messages_page)
        self.stacked_widget.setCurrentWidget(self.messages_page)
        self.update_sidebar_highlight("Messages")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SaathiDashboard()
    window.show()
    sys.exit(app.exec_())
