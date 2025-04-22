import sys
import asyncio
import websockets
import json
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                            QScrollArea, QFrame, QTextEdit)
from PyQt5.QtCore import Qt, QSize, QTimer
from PyQt5.QtGui import QFont, QIcon, QPixmap, QImage, QPainter, QRegion
from database1 import Database

class Messages(QWidget):
    def __init__(self, user_id, user_name, parent=None):
        super().__init__(parent)
        self.user_id = user_id
        self.user_name = user_name
        self.current_chat = None
        self.websocket = None
        self.message_timer = QTimer()
        self.message_timer.timeout.connect(self.check_new_messages)
        self.message_timer.start(500)  # Check every half second
        
        # Initialize database connection
        self.db = Database(host='localhost', user='root', password='naitik@mysql', database='saathi')
        
        # Create main layout
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Create left panel (friends list)
        left_panel = QFrame()
        left_panel.setFixedWidth(250)  # Reduced width
        left_panel.setStyleSheet("""
            QFrame {
                background-color: #f0f8ff;
                border-right: 1px solid #b0c4de;
            }
        """)
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(0)
        
        # Friends list header
        header = QLabel("Friends")
        header.setStyleSheet("""
            QLabel {
                background-color: #e6f3ff;
                padding: 15px;
                font-size: 16px;
                font-weight: bold;
                color: #2c3e50;
                border-bottom: 1px solid #b0c4de;
            }
        """)
        left_layout.addWidget(header)
        
        # Friends list scroll area
        self.friends_scroll = QScrollArea()
        self.friends_scroll.setWidgetResizable(True)
        self.friends_scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background: transparent;
            }
            QScrollBar:vertical {
                border: none;
                background: #f0f0f0;
                width: 8px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical {
                background: #b0c4de;
                border-radius: 4px;
            }
        """)
        
        self.friends_widget = QWidget()
        self.friends_layout = QVBoxLayout(self.friends_widget)
        self.friends_layout.setContentsMargins(5, 5, 5, 5)
        self.friends_layout.setSpacing(2)
        self.friends_layout.setAlignment(Qt.AlignTop)
        self.friends_scroll.setWidget(self.friends_widget)
        left_layout.addWidget(self.friends_scroll)
        
        # Create right panel (chat area)
        right_panel = QFrame()
        right_panel.setStyleSheet("""
            QFrame {
                background-color: #ffffff;
            }
        """)
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(0)
        
        # Chat header
        self.chat_header = QFrame()
        self.chat_header.setStyleSheet("""
            QFrame {
                background-color: white;
                border-bottom: 1px solid #e0e0e0;
                padding: 10px;
            }
        """)
        header_layout = QHBoxLayout(self.chat_header)
        header_layout.setContentsMargins(15, 5, 15, 5)
        
        self.header_label = QLabel("Select a friend to start chatting")
        self.header_label.setStyleSheet("""
            font-size: 16px;
            font-weight: bold;
            color: #2c3e50;
        """)
        
        self.refresh_button = QPushButton("⟳")
        self.refresh_button.setFixedSize(30, 30)
        self.refresh_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                border-radius: 15px;
                color: #4682b4;
                font-size: 18px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #f0f0f0;
            }
        """)
        self.refresh_button.clicked.connect(self.refresh_messages)
        self.refresh_button.hide()  # Hide initially until chat is started
        
        header_layout.addWidget(self.header_label)
        header_layout.addStretch()
        header_layout.addWidget(self.refresh_button)
        right_layout.addWidget(self.chat_header)
        
        # Chat messages area
        self.messages_scroll = QScrollArea()
        self.messages_scroll.setWidgetResizable(True)
        self.messages_scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background: white;
            }
            QScrollBar:vertical {
                border: none;
                background: #f0f0f0;
                width: 8px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical {
                background: #b0c4de;
                border-radius: 4px;
            }
        """)
        self.messages_widget = QWidget()
        self.messages_layout = QVBoxLayout(self.messages_widget)
        self.messages_layout.setContentsMargins(0, 10, 0, 10)
        self.messages_layout.setAlignment(Qt.AlignTop)
        self.messages_scroll.setWidget(self.messages_widget)
        
        # Message input area
        input_layout = QHBoxLayout()
        input_layout.setContentsMargins(10, 5, 10, 5)
        input_layout.setSpacing(8)
        
        self.message_input = QTextEdit()
        self.message_input.setPlaceholderText("Type a message...")
        self.message_input.setMaximumHeight(55)
        self.message_input.setStyleSheet("""
            QTextEdit {
                border: 1px solid #e0e0e0;
                border-radius: 18px;
                padding: 8px 15px;
                background-color: white;
                font-size: 13px;
                color: #2c3e50;
            }
            QTextEdit[placeholder="Type a message..."] {
                color: #95a5a6;
            }
        """)
        
        self.send_button = QPushButton("➤")
        self.send_button.setFixedSize(33, 33)
        self.send_button.setStyleSheet("""
            QPushButton {
                background-color: #4682b4;
                border: none;
                border-radius: 16px;
                color: white;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #357abd;
            }
            QPushButton:pressed {
                background-color: #2c5f8d;
            }
        """)
        self.send_button.clicked.connect(self.send_message)
        
        input_layout.addWidget(self.message_input)
        input_layout.addWidget(self.send_button)
        
        # Create a widget for the input layout
        input_widget = QWidget()
        input_widget.setLayout(input_layout)
        
        # Add the messages scroll area and input widget to the right panel
        right_layout.addWidget(self.messages_scroll)
        right_layout.addWidget(input_widget)
        
        # Set stretch factors to give more space to messages
        right_layout.setStretch(1, 1)  # Messages scroll area gets more space
        right_layout.setStretch(2, 0)  # Input area stays at minimum size
        
        # Add panels to main layout
        layout.addWidget(left_panel)
        layout.addWidget(right_panel)
        
        # Load friends list initially
        self.load_friends()
        
        # Connect to WebSocket server
        asyncio.get_event_loop().run_until_complete(self.connect_websocket())

    def load_friends(self):
        """Load friends list from database"""
        cursor = self.db.connection.cursor(dictionary=True)
        try:
            cursor.execute("""
                SELECT u.id, u.name, p.profile_picture,
                       (SELECT message_text FROM messages 
                        WHERE (sender_id = %s AND receiver_id = u.id)
                        OR (sender_id = u.id AND receiver_id = %s)
                        ORDER BY timestamp DESC LIMIT 1) as last_message,
                       (SELECT timestamp FROM messages 
                        WHERE (sender_id = %s AND receiver_id = u.id)
                        OR (sender_id = u.id AND receiver_id = %s)
                        ORDER BY timestamp DESC LIMIT 1) as last_message_time
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
                ORDER BY last_message_time DESC
            """, (self.user_id,) * 8)
            
            friends = cursor.fetchall()
            self.update_friends_list(friends)
            
        except Exception as e:
            print(f"Error loading friends: {e}")
        finally:
            cursor.close()

    def update_friends_list(self, friends):
        # Clear existing friends
        for i in reversed(range(self.friends_layout.count())): 
            self.friends_layout.itemAt(i).widget().setParent(None)
            
        # Add friends
        for friend in friends:
            friend_card = self.create_friend_card(friend)
            self.friends_layout.addWidget(friend_card)
            
        # Add stretch at the end
        self.friends_layout.addStretch()
            
    def create_friend_card(self, friend):
        card = QFrame()
        card.setFixedHeight(70)  # Slightly increased height for better visibility
        card.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 5px;
                padding: 5px;
            }
            QFrame:hover {
                background-color: #e6f3ff;
            }
        """)
        
        layout = QHBoxLayout(card)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(12)
        
        # Profile picture container with fixed size
        profile_pic_container = QLabel()
        profile_pic_container.setFixedSize(50, 50)
        profile_pic_container.setStyleSheet("""
            QLabel {
                background-color: #e6f3ff;
                border-radius: 25px;
                border: none;
            }
        """)
        
        if friend['profile_picture']:
            image = QImage()
            image.loadFromData(friend['profile_picture'])
            if not image.isNull():
                # Scale the image to slightly larger size for better cropping
                pixmap = QPixmap.fromImage(image)
                scaled_size = 60  # Slightly larger than container
                scaled_pixmap = pixmap.scaled(scaled_size, scaled_size, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
                
                # Create a perfectly square crop from the center
                if scaled_pixmap.width() > scaled_size or scaled_pixmap.height() > scaled_size:
                    center_x = (scaled_pixmap.width() - scaled_size) // 2
                    center_y = (scaled_pixmap.height() - scaled_size) // 2
                    scaled_pixmap = scaled_pixmap.copy(center_x, center_y, scaled_size, scaled_size)
                
                # Create circular mask
                mask = QPixmap(50, 50)
                mask.fill(Qt.transparent)
                painter = QPainter(mask)
                painter.setRenderHint(QPainter.Antialiasing)
                painter.setBrush(Qt.black)
                painter.setPen(Qt.NoPen)
                painter.drawEllipse(0, 0, 50, 50)
                painter.end()
                
                # Create final circular image
                result = QPixmap(50, 50)
                result.fill(Qt.transparent)
                painter = QPainter(result)
                painter.setRenderHint(QPainter.Antialiasing)
                painter.setClipRegion(QRegion(mask.mask()))
                painter.drawPixmap(0, 0, scaled_pixmap.scaled(50, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                painter.end()
                
                profile_pic_container.setPixmap(result)
        
        if not friend['profile_picture'] or image.isNull():
            profile_pic_container.setText(friend['name'][0].upper())
            profile_pic_container.setAlignment(Qt.AlignCenter)
            profile_pic_container.setStyleSheet("""
                QLabel {
                    background-color: #e6f3ff;
                    color: #4682b4;
                    font-size: 20px;
                    font-weight: bold;
                    border-radius: 25px;
                }
            """)
        
        # Friend name with improved styling
        name_label = QLabel(friend['name'])
        name_label.setStyleSheet("""
            QLabel {
                font-size: 15px;
                color: #2c3e50;
                font-weight: bold;
            }
        """)
        
        layout.addWidget(profile_pic_container)
        layout.addWidget(name_label, 1)
        
        # Make card clickable
        card.mousePressEvent = lambda e, f=friend: self.start_chat(f)
        
        return card
        
    async def connect_websocket(self):
        try:
            self.websocket = await websockets.connect('ws://localhost:8765')
            # Register user
            await self.websocket.send(json.dumps({
                'type': 'register',
                'user_id': self.user_id
            }))
            # Start listening for messages
            asyncio.create_task(self.listen_messages())
        except Exception as e:
            print(f"WebSocket connection error: {e}")
            
    async def listen_messages(self):
        try:
            while True:
                message = await self.websocket.recv()
                data = json.loads(message)
                
                if data['type'] == 'friends_list':
                    self.update_friends_list(data['friends'])
                elif data['type'] == 'chat_history':
                    self.display_chat_history(data['history'])
                elif data['type'] == 'message':
                    self.display_message(data)
        except Exception as e:
            print(f"Error listening for messages: {e}")
            
    def start_chat(self, friend):
        self.current_chat = friend
        self.header_label.setText(f"{friend['name']}")
        self.refresh_button.show()  # Show refresh button when chat starts

            # Clear existing messages
        for i in reversed(range(self.messages_layout.count())): 
            widget = self.messages_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()
        
        # Load chat history
        cursor = self.db.connection.cursor(dictionary=True)
        try:
            cursor.execute("""
                SELECT m.*, u.name as sender_name
                FROM messages m
                JOIN users u ON m.sender_id = u.id
                WHERE (m.sender_id = %s AND m.receiver_id = %s)
                OR (m.sender_id = %s AND m.receiver_id = %s)
                ORDER BY m.timestamp ASC
            """, (self.user_id, friend['id'], friend['id'], self.user_id))
            
            messages = cursor.fetchall()
            for message in messages:
                self.display_message(message)
                
            # Initialize chat session if it doesn't exist
            cursor.execute("""
                INSERT IGNORE INTO chat_sessions (user1_id, user2_id, last_activity)
                VALUES (%s, %s, NOW())
            """, (min(self.user_id, friend['id']), max(self.user_id, friend['id'])))
            self.db.connection.commit()
                
        except Exception as e:
            print(f"Error loading chat history: {e}")
        finally:
            cursor.close()

    def display_chat_history(self, history):
        self.messages_layout.clear()
        for message in history:
            self.display_message(message)
            
    def display_message(self, message_data):
        message = QFrame()
        is_sender = message_data['sender_id'] == self.user_id
        
        message.setStyleSheet(f"""
            QFrame {{
                background-color: {'#4682b4' if is_sender else '#e6f3ff'};
                border-radius: 15px;
                padding: 8px 15px;
                margin: 2px 5px;
                min-width: 80px;
                max-width: 500px;
            }}
        """)
        
        layout = QVBoxLayout(message)
        layout.setSpacing(2)
        layout.setContentsMargins(2, 2, 2, 2)
        
        # Message text
        text_label = QLabel(message_data['message_text'])
        text_label.setStyleSheet(f"""
            color: {'white' if is_sender else '#2c3e50'};
            font-size: 13px;
            padding: 0px;
            margin: 0px;
            qproperty-wordWrap: true;
        """)
        text_label.setWordWrap(True)
        text_label.setMinimumWidth(60)
        
        # Timestamp
        time_label = QLabel(message_data['timestamp'].strftime('%I:%M %p') if isinstance(message_data['timestamp'], datetime) else message_data['timestamp'])
        time_label.setStyleSheet(f"""
            color: {'#e6f3ff' if is_sender else '#666'};
            font-size: 9px;
            padding: 0px;
            margin: 0px;
        """)
        time_label.setAlignment(Qt.AlignRight)
        
        layout.addWidget(text_label)
        layout.addWidget(time_label)
        
        # Add message to layout with proper spacing
        message_container = QHBoxLayout()
        message_container.setContentsMargins(15, 0, 20, 0)
        message_container.addStretch() if is_sender else None
        message_container.addWidget(message)
        message_container.addStretch() if not is_sender else None
        
        widget = QWidget()
        widget.setLayout(message_container)
        self.messages_layout.addWidget(widget)
        
        # Scroll to bottom
        self.messages_scroll.verticalScrollBar().setValue(
            self.messages_scroll.verticalScrollBar().maximum()
        )

    def send_message(self):
        if not self.current_chat or not self.message_input.toPlainText().strip():
            return

        message = self.message_input.toPlainText().strip()
        self.message_input.clear()

        cursor = self.db.connection.cursor()
        try:
            # Store message in database
            cursor.execute("""
                INSERT INTO messages (sender_id, receiver_id, message_text, timestamp)
                VALUES (%s, %s, %s, %s)
            """, (self.user_id, self.current_chat['id'], message, datetime.now()))
            
            # Update chat session
            cursor.execute("""
                INSERT INTO chat_sessions (user1_id, user2_id, last_message_id, last_activity)
                VALUES (%s, %s, LAST_INSERT_ID(), NOW())
                ON DUPLICATE KEY UPDATE
                last_message_id = LAST_INSERT_ID(),
                last_activity = NOW()
            """, (min(self.user_id, self.current_chat['id']), max(self.user_id, self.current_chat['id'])))
            
            self.db.connection.commit()
            
            # Display message
            self.display_message({
                'sender_id': self.user_id,
                'message_text': message,
                'timestamp': datetime.now(),
                'sender_name': self.user_name
            })
            
        except Exception as e:
            print(f"Error sending message: {e}")
        finally:
            cursor.close()

    def check_new_messages(self):
        if self.current_chat:
            cursor = self.db.connection.cursor(dictionary=True)
            try:
                # Check for new messages
                cursor.execute("""
                    SELECT m.*, u.name as sender_name
                    FROM messages m
                    JOIN users u ON m.sender_id = u.id
                    WHERE ((m.sender_id = %s AND m.receiver_id = %s)
                    OR (m.sender_id = %s AND m.receiver_id = %s))
                    AND m.timestamp > (
                        SELECT COALESCE(MAX(last_activity), '1970-01-01')
                        FROM chat_sessions 
                        WHERE (user1_id = %s AND user2_id = %s)
                        OR (user1_id = %s AND user2_id = %s)
                    )
                    ORDER BY m.timestamp ASC
                """, (self.user_id, self.current_chat['id'], 
                     self.current_chat['id'], self.user_id,
                     min(self.user_id, self.current_chat['id']),
                     max(self.user_id, self.current_chat['id']),
                     min(self.user_id, self.current_chat['id']),
                     max(self.user_id, self.current_chat['id'])))
                
                new_messages = cursor.fetchall()
                if new_messages:
                    for message in new_messages:
                        self.display_message(message)
                    
                    # Update chat session
                    cursor.execute("""
                        INSERT INTO chat_sessions (user1_id, user2_id, last_message_id, last_activity)
                        SELECT %s, %s, %s, NOW()
                        FROM DUAL
                        WHERE NOT EXISTS (
                            SELECT 1 FROM chat_sessions 
                            WHERE (user1_id = %s AND user2_id = %s)
                            OR (user1_id = %s AND user2_id = %s)
                        )
                    """, (min(self.user_id, self.current_chat['id']),
                         max(self.user_id, self.current_chat['id']),
                         new_messages[-1]['message_id'],
                         min(self.user_id, self.current_chat['id']),
                         max(self.user_id, self.current_chat['id']),
                         min(self.user_id, self.current_chat['id']),
                         max(self.user_id, self.current_chat['id'])))
                    
                    cursor.execute("""
                        UPDATE chat_sessions 
                        SET last_message_id = %s,
                            last_activity = NOW()
                        WHERE (user1_id = %s AND user2_id = %s)
                        OR (user1_id = %s AND user2_id = %s)
                    """, (new_messages[-1]['message_id'],
                         min(self.user_id, self.current_chat['id']),
                         max(self.user_id, self.current_chat['id']),
                         min(self.user_id, self.current_chat['id']),
                         max(self.user_id, self.current_chat['id'])))
                    
                    self.db.connection.commit()
                    
            except Exception as e:
                print(f"Error checking new messages: {e}")
            finally:
                cursor.close()
                
    def refresh_messages(self):
        """Manually refresh messages"""
        if self.current_chat:
            cursor = self.db.connection.cursor(dictionary=True)
        try:
            cursor.execute("""
                    SELECT m.*, u.name as sender_name
                    FROM messages m
                    JOIN users u ON m.sender_id = u.id
                    WHERE (m.sender_id = %s AND m.receiver_id = %s)
                    OR (m.sender_id = %s AND m.receiver_id = %s)
                    ORDER BY m.timestamp ASC
                """, (self.user_id, self.current_chat['id'], 
                     self.current_chat['id'], self.user_id))
                
            messages = cursor.fetchall()
                
                # Clear existing messages
            for i in reversed(range(self.messages_layout.count())): 
                widget = self.messages_layout.itemAt(i).widget()
                if widget:
                    widget.deleteLater()
            
            # Display all messages
            for message in messages:
                self.display_message(message)
                    
        except Exception as e:
            print(f"Error refreshing messages: {e}")
        finally:
            cursor.close()
                
    def closeEvent(self, event):
        self.message_timer.stop()
        if self.websocket:
            asyncio.get_event_loop().run_until_complete(self.websocket.close())
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Messages(1, "Alice Johnson")
    window.show()
    sys.exit(app.exec_())
