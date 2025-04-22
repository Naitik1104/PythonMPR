from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                           QPushButton, QFrame, QApplication, QStackedWidget, QScrollArea, QMessageBox, QLineEdit, QDialog)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPixmap, QFont, QColor, QPalette
from database1 import Database
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from geopy.distance import geodesic
from geopy.geocoders import Nominatim

class UserCard(QWidget):
    def __init__(self, explore_page, user_data, db):
        super().__init__()
        self.explore_page = explore_page
        self.db = db
        self.user_id = user_data.get('id')  # Store user_id as instance variable
        self.name = user_data.get('name', '')
        self.age = user_data.get('age', '')
        self.gender = user_data.get('gender', '')
        self.bio = user_data.get('bio', '')
        self.profile_picture = user_data.get('profile_picture', '')
        self.location = user_data.get('location', '')
        self.interests = user_data.get('interests', '')
        self.initUI()

    def initUI(self):
        # Set fixed size for the card
        self.setFixedSize(480, 500)
        
        # Main vertical layout
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(15, 15, 15, 15)
        
        # Photo container (50% of card height)
        photo_container = QWidget()
        photo_container.setFixedHeight(int(self.height() * 0.5))
        photo_layout = QVBoxLayout(photo_container)
        photo_layout.setContentsMargins(0, 0, 0, 0)
        
        # Try to load user photo from photos table first
        cursor = self.db.connection.cursor()
        try:
            cursor.execute("""
                SELECT photo FROM photos 
                WHERE user_id = %s 
                ORDER BY upload_date DESC 
                LIMIT 1
            """, (self.user_id,))
            photo_data = cursor.fetchone()
            
            if photo_data and photo_data[0]:
                pixmap = QPixmap()
                pixmap.loadFromData(photo_data[0])
                scaled_pixmap = pixmap.scaled(450, int(self.height() * 0.5), 
                    Qt.AspectRatioMode.KeepAspectRatio, 
                    Qt.TransformationMode.SmoothTransformation)
                photo_label = QLabel()
                photo_label.setPixmap(scaled_pixmap)
                photo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                photo_layout.addWidget(photo_label)
            # Fallback to profile picture if no photos found
            elif self.profile_picture:
                pixmap = QPixmap()
                pixmap.loadFromData(self.profile_picture)
                scaled_pixmap = pixmap.scaled(450, int(self.height() * 0.5), 
                    Qt.AspectRatioMode.KeepAspectRatio, 
                    Qt.TransformationMode.SmoothTransformation)
                photo_label = QLabel()
                photo_label.setPixmap(scaled_pixmap)
                photo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                photo_layout.addWidget(photo_label)
            else:
                default_photo = QLabel("No Photo Available")
                default_photo.setAlignment(Qt.AlignmentFlag.AlignCenter)
                default_photo.setStyleSheet("background-color: #f0f0f0; border-radius: 10px; padding: 20px; font-size: 16px;")
                photo_layout.addWidget(default_photo)
        finally:
            cursor.close()
        
        main_layout.addWidget(photo_container)
        
        # User info container
        info_container = QWidget()
        info_layout = QVBoxLayout(info_container)
        info_layout.setSpacing(8)
        info_layout.setContentsMargins(0, 0, 0, 0)
        
        # Name, age, gender
        name_label = QLabel(f"{self.name}, {self.age}")
        name_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        info_layout.addWidget(name_label)
        
        gender_label = QLabel(self.gender)
        gender_label.setStyleSheet("font-size: 16px; color: #666;")
        info_layout.addWidget(gender_label)
        
        # Location
        if self.location:
            location_label = QLabel(f"📍 {self.location}")
            location_label.setStyleSheet("font-size: 16px; color: #666;")
            info_layout.addWidget(location_label)
        
        # Interests
        if self.interests:
            interests_label = QLabel(f"Interests: {self.interests}")
            interests_label.setStyleSheet("""
                font-size: 16px; 
                color: #333; 
                background-color: #f0f8ff; 
                padding: 8px; 
                border-radius: 6px;
            """)
            interests_label.setWordWrap(True)
            info_layout.addWidget(interests_label)
        
        # Bio
        if self.bio:
            bio_text = self.bio[:100] + '...' if len(self.bio) > 100 else self.bio
            bio_label = QLabel(bio_text)
            bio_label.setWordWrap(True)
            bio_label.setStyleSheet("font-size: 14px; color: #333; margin-top: 5px;")
            info_layout.addWidget(bio_label)
        
        main_layout.addWidget(info_container)
        
        # Buttons container with white background
        buttons_container = QWidget()
        buttons_container.setStyleSheet("""
            QWidget {
                background-color: white;
                border-top: 1px solid #e0e0e0;
            }
            QPushButton {
                color: white;
                border: none;
                border-radius: 15px;
                min-width: 180px;
                min-height: 40px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton#viewProfileBtn {
                background-color: #2196F3;
            }
            QPushButton#viewProfileBtn:hover {
                background-color: #1976D2;
            }
            QPushButton#sendRequestBtn {
                background-color: #4CAF50;
            }
            QPushButton#sendRequestBtn:hover {
                background-color: #388E3C;
            }
        """)
        buttons_layout = QHBoxLayout(buttons_container)
        buttons_layout.setContentsMargins(10, 10, 10, 10)
        buttons_layout.setSpacing(20)  # Increased spacing between buttons
        
        # View Profile button
        view_profile_btn = QPushButton("View Profile")
        view_profile_btn.setObjectName("viewProfileBtn")
        view_profile_btn.clicked.connect(self.view_profile)
        buttons_layout.addWidget(view_profile_btn)
        
        # Send Request button
        send_request_btn = QPushButton("Send Request")
        send_request_btn.setObjectName("sendRequestBtn")
        send_request_btn.clicked.connect(self.handle_request)
        buttons_layout.addWidget(send_request_btn)
        
        main_layout.addWidget(buttons_container)
        
        # Set white background and border for the card
        self.setStyleSheet("""
            UserCard {
                background-color: white;
                border: 1px solid #e0e0e0;
                border-radius: 10px;
            }
        """)

    def handle_request(self):
        try:
            if not self.explore_page or not self.explore_page.current_user:
                QMessageBox.warning(self, "Error", "Please log in to send friend requests.", 
                    QMessageBox.StandardButton.Ok)
                return

            cursor = self.db.connection.cursor()
            
            # Get current user's ID
            cursor.execute("SELECT id FROM users WHERE name = %s", (self.explore_page.current_user,))
            sender_result = cursor.fetchone()
            
            if not sender_result:
                QMessageBox.warning(self, "Error", "Could not find your user account.",
                    QMessageBox.StandardButton.Ok)
                return
                
            sender_id = sender_result[0]
            
            # Check if request already exists
            cursor.execute("""
                SELECT status FROM friend_requests 
                WHERE (sender_id = %s AND receiver_id = %s)
                OR (sender_id = %s AND receiver_id = %s)
            """, (sender_id, self.user_id, self.user_id, sender_id))
            
            existing_request = cursor.fetchone()
            
            if existing_request:
                msg = QMessageBox()
                msg.setWindowTitle("Friend Request")
                msg.setText("A friend request already exists between you and this user.")
                msg.setIcon(QMessageBox.Information)
                msg.setStyleSheet("""
                    QMessageBox {
                        background-color: white;
                    }
                    QMessageBox QLabel {
                        color: #333;
                        font-size: 14px;
                    }
                    QMessageBox QPushButton {
                        background-color: #2196F3;
                        color: white;
                        border-radius: 15px;
                        min-width: 100px;
                        min-height: 30px;
                        font-size: 14px;
                        font-weight: bold;
                    }
                    QMessageBox QPushButton:hover {
                        background-color: #1976D2;
                    }
                """)
                msg.exec_()
                return
                
            # Check if already friends
            cursor.execute("""
                SELECT * FROM friends 
                WHERE (user1_id = %s AND user2_id = %s)
                OR (user1_id = %s AND user2_id = %s)
            """, (sender_id, self.user_id, self.user_id, sender_id))
            
            if cursor.fetchone():
                msg = QMessageBox()
                msg.setWindowTitle("Already Friends")
                msg.setText(f"You are already friends with {self.name}.")
                msg.setIcon(QMessageBox.Information)
                msg.setStyleSheet("""
                    QMessageBox {
                        background-color: white;
                    }
                    QMessageBox QLabel {
                        color: #333;
                        font-size: 14px;
                    }
                    QMessageBox QPushButton {
                        background-color: #2196F3;
                        color: white;
                        border-radius: 15px;
                        min-width: 100px;
                        min-height: 30px;
                        font-size: 14px;
                        font-weight: bold;
                    }
                    QMessageBox QPushButton:hover {
                        background-color: #1976D2;
                    }
                """)
                msg.exec_()
                return
            
            # Insert new friend request
            cursor.execute("""
                INSERT INTO friend_requests (sender_id, receiver_id, status, request_date)
                VALUES (%s, %s, 'pending', NOW())
            """, (sender_id, self.user_id))
            
            self.db.connection.commit()
            
            msg = QMessageBox()
            msg.setWindowTitle("Success")
            msg.setText(f"Friend request sent to {self.name}!")
            msg.setIcon(QMessageBox.Information)
            msg.setStyleSheet("""
                QMessageBox {
                    background-color: white;
                }
                QMessageBox QLabel {
                    color: #333;
                    font-size: 14px;
                }
                QMessageBox QPushButton {
                    background-color: #4CAF50;
                    color: white;
                    border-radius: 15px;
                    min-width: 100px;
                    min-height: 30px;
                    font-size: 14px;
                    font-weight: bold;
                }
                QMessageBox QPushButton:hover {
                    background-color: #388E3C;
                }
            """)
            msg.exec_()
            
        except Exception as e:
            self.db.connection.rollback()
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            msg.setText(f"Failed to send friend request: {str(e)}")
            msg.setIcon(QMessageBox.Critical)
            msg.setStyleSheet("""
                QMessageBox {
                    background-color: white;
                }
                QMessageBox QLabel {
                    color: #333;
                    font-size: 14px;
                }
                QMessageBox QPushButton {
                    background-color: #FF5252;
                    color: white;
                    border-radius: 15px;
                    min-width: 100px;
                    min-height: 30px;
                    font-size: 14px;
                    font-weight: bold;
                }
                QMessageBox QPushButton:hover {
                    background-color: #FF1744;
                }
            """)
            msg.exec_()
        finally:
            cursor.close()

    def view_profile(self):
        try:
            from HomePage import ViewProfileDialog
            profile_dialog = ViewProfileDialog(self.user_id, self.db)
            profile_dialog.setStyleSheet("""
                QDialog {
                    background-color: white;
                }
                QLabel {
                    color: #333;
                    font-size: 14px;
                }
                QPushButton {
                    background-color: #2196F3;
                    color: white;
                    border-radius: 15px;
                    min-width: 100px;
                    min-height: 30px;
                    font-size: 14px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #1976D2;
                }
            """)
            profile_dialog.exec_()
        except Exception as e:
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            msg.setText(f"Failed to open profile: {str(e)}")
            msg.setIcon(QMessageBox.Critical)
            msg.setStyleSheet("""
                QMessageBox {
                    background-color: white;
                }
                QMessageBox QLabel {
                    color: #333;
                    font-size: 14px;
                }
                QPushButton {
                    background-color: #FF5252;
                    color: white;
                    border-radius: 15px;
                    min-width: 100px;
                    min-height: 30px;
                }
                QPushButton:hover {
                    background-color: #FF1744;
                }
            """)
            msg.exec_()

class ExplorePage(QWidget):
    def __init__(self, current_user=None):
        super().__init__()
        self.current_user = current_user
        self.setFixedSize(774, 768)  # Set size to match 1024-sidebar width
        self.db = Database(host='localhost', user='root', password='naitik@mysql', database='saathi')
        self.current_index = 0
        self.users = []
        self.geolocator = Nominatim(user_agent="saathi_app")
        self.location_cache = {}  # Cache for geocoding results
        self.initUI()
        self.load_users()

    def calculate_profile_completeness(self, age, location, gender, interests, bio, profile_pic):
        """Calculate profile completeness score"""
        score = 0
        if age: score += 20
        if location: score += 20
        if gender: score += 10
        if interests: score += 20
        if bio: score += 20
        if profile_pic: score += 10
        return score / 100.0

    def calculate_interest_similarity(self, interests1, interests2):
        """Calculate Jaccard similarity between interests"""
        if not interests1 or not interests2:
            return 0.0
        set1 = set(interests1.lower().split(','))
        set2 = set(interests2.lower().split(','))
        intersection = len(set1.intersection(set2))
        union = len(set1.union(set2))
        return intersection / union if union > 0 else 0.0

    def calculate_location_proximity(self, loc1, loc2):
        """Calculate normalized distance between locations with caching"""
        try:
            if not loc1 or not loc2:
                return 0.0
            
            # Check cache first
            cache_key = f"{loc1}_{loc2}"
            if cache_key in self.location_cache:
                return self.location_cache[cache_key]
            
            location1 = self.geolocator.geocode(loc1)
            location2 = self.geolocator.geocode(loc2)
            if location1 and location2:
                distance = geodesic(
                    (location1.latitude, location1.longitude),
                    (location2.latitude, location2.longitude)
                ).kilometers
                # Normalize distance (closer = higher score)
                score = 1 / (1 + distance/100)  # 100km as normalization factor
                # Cache the result
                self.location_cache[cache_key] = score
                return score
            return 0.0
        except:
            return 0.0

    def calculate_age_compatibility(self, age1, age2):
        """Calculate age compatibility score"""
        if not age1 or not age2:
            return 0.0
        age_diff = abs(age1 - age2)
        return 1 / (1 + age_diff/5)  # 5 years as normalization factor

    def initUI(self):
        self.setStyleSheet("""
            QWidget {
                background: #F5F9FF;
            }
            QPushButton#navBtn {
                background: #2196F3;
                color: white;
                border-radius: 25px;
                font-size: 20px;
                font-weight: bold;
                min-width: 50px;
                min-height: 50px;
            }
            QPushButton#navBtn:hover {
                background: #1976D2;
            }
            QLineEdit {
                padding: 8px 15px;
                border: 2px solid #E3E9FF;
                border-radius: 20px;
                background: white;
                font-size: 14px;
                min-width: 400px;
            }
            QLineEdit:focus {
                border: 2px solid #2196F3;
            }
        """)

        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # Title and search container
        top_layout = QHBoxLayout()
        title = QLabel("Explore New Friends")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #1E88E5;")
        
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search users by username...")
        self.search_bar.setFixedHeight(40)
        self.search_bar.textChanged.connect(self.search_users)
        
        top_layout.addWidget(title)
        top_layout.addStretch()
        top_layout.addWidget(self.search_bar)
        
        main_layout.addLayout(top_layout)

        # Center container for card and navigation
        center_container = QWidget()
        center_layout = QHBoxLayout(center_container)
        center_layout.setContentsMargins(0, 0, 0, 0)
        center_layout.setSpacing(20)

        # Previous button
        prev_btn = QPushButton("❮")
        prev_btn.setObjectName("navBtn")
        prev_btn.setFixedSize(50, 50)
        prev_btn.clicked.connect(self.show_previous)
        
        # Card container
        self.card_container = QStackedWidget()
        self.card_container.setFixedSize(500, 520)
        
        # Next button
        next_btn = QPushButton("❯")
        next_btn.setObjectName("navBtn")
        next_btn.setFixedSize(50, 50)
        next_btn.clicked.connect(self.show_next)

        # Add widgets to center layout
        center_layout.addStretch()
        center_layout.addWidget(prev_btn)
        center_layout.addWidget(self.card_container)
        center_layout.addWidget(next_btn)
        center_layout.addStretch()

        # Add content container to main layout with vertical centering
        main_layout.addStretch(1)
        main_layout.addWidget(center_container)
        main_layout.addStretch(1)

    def fetch_users(self):
        """Fetch and sort users based on compatibility with optimized queries"""
        users = []
        if not self.current_user:
            return users

        cursor = self.db.connection.cursor()
        try:
            # Get current user's data in a single query with index hints
            cursor.execute("""
                SELECT u.id, u.age, u.gender, u.location, p.Interests, p.Bio, p.profile_picture
                FROM users u USE INDEX (PRIMARY)
                LEFT JOIN profiles p ON u.id = p.user_id 
                WHERE u.name = %s
            """, (self.current_user,))
            current_user_data = cursor.fetchone()
            if not current_user_data:
                return users

            current_id, current_age, current_gender, current_location, current_interests, current_bio, current_pic = current_user_data

            # Get potential matches with optimized query using index hints
            cursor.execute("""
                SELECT DISTINCT u.id, u.name, u.age, u.gender, u.location, 
                    p.profile_picture, p.Interests, p.Bio
                FROM users u
                LEFT JOIN profiles p ON u.id = p.user_id
                WHERE u.id != %s
                AND u.id NOT IN (
                    SELECT user2_id FROM friends WHERE user1_id = %s
                    UNION
                    SELECT user1_id FROM friends WHERE user2_id = %s
                )
                AND u.id NOT IN (
                    SELECT receiver_id FROM friend_requests 
                    WHERE sender_id = %s AND status = 'pending'
                    UNION
                    SELECT sender_id FROM friend_requests 
                    WHERE receiver_id = %s AND status = 'pending'
                )
                AND u.id NOT IN (
                    SELECT not_interested_user_id
                    FROM not_interested
                    WHERE user_id = %s
                )
                LIMIT 50
            """, (current_id, current_id, current_id, current_id, current_id, current_id))

            potential_matches = cursor.fetchall()
            user_scores = []

            # Pre-calculate location scores for all users
            location_scores = {}
            for user in potential_matches:
                if user[4] and current_location:  # if both locations exist
                    cache_key = f"{current_location}_{user[4]}"
                    if cache_key in self.location_cache:
                        location_scores[user[0]] = self.location_cache[cache_key]
                    else:
                        score = self.calculate_location_proximity(current_location, user[4])
                        self.location_cache[cache_key] = score
                        location_scores[user[0]] = score

            for user in potential_matches:
                user_id, name, age, gender, location, profile_pic, interests, bio = user
                
                # Calculate individual scores using cached location scores
                completeness = self.calculate_profile_completeness(age, location, gender, interests, bio, profile_pic)
                interest_sim = self.calculate_interest_similarity(current_interests, interests) if interests and current_interests else 0
                location_prox = location_scores.get(user_id, 0)
                age_compat = self.calculate_age_compatibility(current_age, age) if age and current_age else 0

                # Calculate total score with weights
                total_score = (
                    0.30 * completeness +
                    0.30 * interest_sim +
                    0.20 * location_prox +
                    0.20 * age_compat
                )

                user_info = {
                    'id': user_id,
                    'name': name,
                    'age': age,
                    'gender': gender,
                    'location': location,
                    'profile_picture': profile_pic,
                    'interests': interests if interests else "",
                    'bio': bio if bio else "",
                    'score': total_score
                }
                user_scores.append(user_info)

            # Sort users by total score
            users = sorted(user_scores, key=lambda x: x['score'], reverse=True)

        finally:
            cursor.close()
        return users

    def load_users(self):
        """Load users asynchronously to improve performance"""
        try:
            self.users = self.fetch_users()
            # Clear existing cards
            while self.card_container.count():
                self.card_container.removeWidget(self.card_container.widget(0))
            
            # Create cards for all users
            for user_data in self.users:
                card = UserCard(self, user_data, self.db)
                self.card_container.addWidget(card)
            
            # Show first card if available
            if self.users:
                self.card_container.setCurrentIndex(0)
            else:
                # Show "No more profiles" message
                no_profiles = QLabel("No more profiles to show!")
                no_profiles.setStyleSheet("""
                    font-size: 16px;
                    color: #666;
                    padding: 20px;
                """)
                no_profiles.setAlignment(Qt.AlignCenter)
                self.card_container.addWidget(no_profiles)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load users: {str(e)}")

    def show_previous(self):
        if self.users:
            self.current_index = (self.current_index - 1) % len(self.users)
            self.card_container.setCurrentIndex(self.current_index)

    def show_next(self):
        if self.users:
            self.current_index = (self.current_index + 1) % len(self.users)
            self.card_container.setCurrentIndex(self.current_index)

    def search_users(self):
        """Search users by username"""
        search_text = self.search_bar.text().strip().lower()
        if not search_text:
            self.load_users()
            return

        cursor = self.db.connection.cursor()
        try:
            # Get current user's ID
            cursor.execute("SELECT id FROM users WHERE name = %s", (self.current_user,))
            current_user_id = cursor.fetchone()
            if not current_user_id:
                return
            current_user_id = current_user_id[0]

            # Search for users
            cursor.execute("""
                SELECT 
                    u.id, u.name, u.age, u.gender, u.location, 
                    p.profile_picture, p.Interests, p.Bio
                FROM users u
                LEFT JOIN profiles p ON u.id = p.user_id
                WHERE u.id != %s
                AND LOWER(u.name) LIKE %s
                AND u.id NOT IN (
                    SELECT CASE 
                        WHEN user1_id = %s THEN user2_id
                        WHEN user2_id = %s THEN user1_id
                    END
                    FROM friends
                    WHERE user1_id = %s OR user2_id = %s
                )
                AND u.id NOT IN (
                    SELECT CASE 
                        WHEN sender_id = %s THEN receiver_id
                        WHEN receiver_id = %s THEN sender_id
                    END
                    FROM friend_requests
                    WHERE (sender_id = %s OR receiver_id = %s)
                    AND status = 'pending'
                )
                AND u.id NOT IN (
                    SELECT not_interested_user_id
                    FROM not_interested
                    WHERE user_id = %s
                )
            """, (current_user_id, f"%{search_text}%", current_user_id, current_user_id, current_user_id, current_user_id,
                  current_user_id, current_user_id, current_user_id, current_user_id, current_user_id))

            users = cursor.fetchall()
            
            # Clear existing cards
            while self.card_container.count():
                self.card_container.removeWidget(self.card_container.widget(0))
            
            # Add new cards
            for user in users:
                user_id, name, age, gender, location, profile_pic, interests, bio = user
                card = UserCard(self, {'id': user_id, 'name': name, 'age': age, 'gender': gender, 'bio': bio, 'profile_picture': profile_pic, 'location': location, 'interests': interests}, self.db)
                self.card_container.addWidget(card)
            
            # Show first card if available
            if users:
                self.card_container.setCurrentIndex(0)
            else:
                no_results = QLabel("No users found")
                no_results.setStyleSheet("""
                    font-size: 16px;
                    color: #666;
                    padding: 20px;
                """)
                no_results.setAlignment(Qt.AlignCenter)
                self.card_container.addWidget(no_results)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to search users: {str(e)}")
        finally:
            cursor.close()

if __name__ == '__main__':
    app = QApplication([])
    window = ExplorePage()
    window.show()
    app.exec_() 