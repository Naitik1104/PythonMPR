import sys
import cv2
import os
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QLabel, 
                           QVBoxLayout, QFrame, QDialog, QHBoxLayout)
from PyQt5.QtGui import QPixmap, QFont, QImage
from PyQt5.QtCore import Qt
from database1 import Database

class SelfieVerificationApp(QDialog):
    def __init__(self, parent=None, current_user=None):
        super().__init__(parent)
        self.current_user = current_user
        self.db = Database(host='localhost', user='root', password='naitik@mysql', database='saathi')
        self.temp_selfie_path = None
        # Load the face detection classifier
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Selfie Verification")
        self.setFixedSize(851, 500)  
        
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 20, 30, 20)
        main_layout.setSpacing(15)
        
        
        header_container = QWidget()
        header_layout = QHBoxLayout(header_container)
        header_layout.setContentsMargins(0, 0, 0, 0)
        
        # Title
        title = QLabel("Selfie Verification")
        title.setStyleSheet("""
            QLabel {
                color: #2196F3;
                font-family: 'Segoe UI';
                font-size: 28px;
                font-weight: bold;
            }
        """)
        
        # Description
        description = QLabel(
            "For authentication and security purposes, we need to verify your identity.\n"
            "Please take a clear selfie in good lighting for verification."
        )
        description.setStyleSheet("""
            QLabel {
                color: #666;
                font-family: 'Segoe UI';
                font-size: 14px;
            }
        """)
        description.setWordWrap(True)
        
        header_layout.addWidget(title)
        header_layout.addWidget(description, 1)
        header_layout.setStretch(0, 0)  # Title doesn't stretch
        header_layout.setStretch(1, 1)  # Description stretches
        
        # Camera frame
        camera_frame = QFrame()
        camera_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 15px;
                padding: 20px;
                border: 2px solid #E3E9FF;
            }
        """)
        camera_layout = QHBoxLayout(camera_frame)  # Changed to horizontal layout
        camera_layout.setSpacing(20)
        
        # Left side - Camera feed
        camera_left = QWidget()
        camera_left_layout = QVBoxLayout(camera_left)
        camera_left_layout.setSpacing(10)
        
        
        camera_instruction = QLabel("Look into the camera")
        camera_instruction.setStyleSheet("""
            QLabel {
                color: #2196F3;
                font-family: 'Segoe UI';
                font-size: 16px;
                font-weight: bold;
            }
        """)
        camera_instruction.setAlignment(Qt.AlignCenter)
        
        
        self.image_label = QLabel()
        self.image_label.setFixedSize(400, 300)  
        self.image_label.setStyleSheet("""
            QLabel {
                background-color: #F5F9FF;
                border-radius: 10px;
                border: 2px dashed #4CA6FF;
            }
        """)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setText("Camera feed will appear here")
        
        camera_left_layout.addWidget(camera_instruction)
        camera_left_layout.addWidget(self.image_label, alignment=Qt.AlignCenter)
        
        
        camera_right = QWidget()
        camera_right_layout = QVBoxLayout(camera_right)
        camera_right_layout.setSpacing(15)
        
        
        instructions = QLabel(
            "Instructions:\n\n"
            "1. Position your face in the center\n"
            "2. Ensure good lighting\n"
            "3. Look directly at the camera\n"
            "4. Keep a neutral expression\n"
            "5. Remove any face coverings"
        )
        instructions.setStyleSheet("""
            QLabel {
                color: #666;
                font-family: 'Segoe UI';
                font-size: 14px;
                line-height: 1.5;
            }
        """)
        
        
        self.status_label = QLabel("")
        self.status_label.setStyleSheet("""
            QLabel {
                color: #666;
                font-family: 'Segoe UI';
                font-size: 14px;
                padding: 10px;
                background-color: #F5F9FF;
                border-radius: 8px;
                border: 1px solid #E3E9FF;
            }
        """)
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setWordWrap(True)
        
        # Buttons container
        buttons_container = QWidget()
        buttons_layout = QVBoxLayout(buttons_container)
        buttons_layout.setSpacing(12)
        
        # Capture button
        self.capture_button = QPushButton("Take Selfie")
        self.capture_button.setFixedSize(200, 40)
        self.capture_button.setStyleSheet("""
            QPushButton {
                background-color: #4CA6FF;
                color: white;
                border: none;
                border-radius: 20px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2196F3;
            }
        """)
        self.capture_button.clicked.connect(self.capture_selfie)
        
        # Proceed button
        self.proceed_button = QPushButton("Proceed")
        self.proceed_button.setFixedSize(200, 40)
        self.proceed_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 20px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.proceed_button.clicked.connect(self.save_and_proceed)
        self.proceed_button.hide()
        
        # Retake button
        self.retake_button = QPushButton("Retake")
        self.retake_button.setFixedSize(200, 40)
        self.retake_button.setStyleSheet("""
            QPushButton {
                background-color: #ff5252;
                color: white;
                border: none;
                border-radius: 20px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #ff1744;
            }
        """)
        self.retake_button.clicked.connect(self.reset_capture)
        self.retake_button.hide()
        
        buttons_layout.addWidget(self.capture_button, alignment=Qt.AlignCenter)
        buttons_layout.addWidget(self.proceed_button, alignment=Qt.AlignCenter)
        buttons_layout.addWidget(self.retake_button, alignment=Qt.AlignCenter)
        
        camera_right_layout.addWidget(instructions)
        camera_right_layout.addWidget(self.status_label)
        camera_right_layout.addStretch()
        camera_right_layout.addWidget(buttons_container)
        
        # Add left and right sections to camera frame
        camera_layout.addWidget(camera_left)
        camera_layout.addWidget(camera_right)
        
        
        main_layout.addWidget(header_container)
        main_layout.addWidget(camera_frame, 1)  # Give camera frame more stretch
        
    def detect_face(self, frame):
        # Convert to grayscale for face detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Detect faces
        faces = self.face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )
        return len(faces) > 0, faces

    def capture_selfie(self):
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            self.status_label.setText("Error: Could not access the camera")
            return
        
        ret, frame = cap.read()
        if ret:
            # Check for face in the image
            has_face, faces = self.detect_face(frame)
            
            if not has_face:
                self.status_label.setText("No face detected. Please try again.")
                cap.release()
                return
            
            # Draw rectangles around detected faces
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            
            # Save image temporarily
            self.temp_selfie_path = "temp_selfie.jpg"
            cv2.imwrite(self.temp_selfie_path, frame)
            
            # Convert frame to QPixmap and display
            height, width = frame.shape[:2]
            bytes_per_line = 3 * width
            image = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888).rgbSwapped()
            pixmap = QPixmap.fromImage(image)
            scaled_pixmap = pixmap.scaled(400, 400, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.image_label.setPixmap(scaled_pixmap)
            
            # Update status and show buttons
            self.status_label.setText("Face detected successfully!")
            self.status_label.setStyleSheet("color: #4CAF50; font-weight: bold;")
            self.capture_button.hide()
            self.proceed_button.show()
            self.retake_button.show()
        else:
            self.status_label.setText("Failed to capture image")
        cap.release()

    def reset_capture(self):
        self.image_label.clear()
        self.image_label.setText("Camera feed will appear here")
        self.status_label.setText("")
        
        if self.temp_selfie_path and os.path.exists(self.temp_selfie_path):
            os.remove(self.temp_selfie_path)
            self.temp_selfie_path = None
        
        self.capture_button.show()
        self.proceed_button.hide()
        self.retake_button.hide()

    def save_and_proceed(self):
        if self.temp_selfie_path and os.path.exists(self.temp_selfie_path):
            try:
                with open(self.temp_selfie_path, 'rb') as file:
                    selfie_data = file.read()
                    cursor = self.db.connection.cursor()
                    cursor.execute("""
                        UPDATE users 
                        SET selfie = %s 
                        WHERE name = %s
                    """, (selfie_data, self.current_user))
                    self.db.connection.commit()
                    cursor.close()
                
                os.remove(self.temp_selfie_path)
                self.temp_selfie_path = None
                self.accept()
                
            except Exception as e:
                self.status_label.setText(f"Error saving selfie: {str(e)}")
                self.status_label.setStyleSheet("color: #ff5252; font-weight: bold;")
        else:
            self.status_label.setText("No selfie captured yet")
            self.status_label.setStyleSheet("color: #ff5252; font-weight: bold;")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SelfieVerificationApp()
    window.show()
    sys.exit(app.exec_())