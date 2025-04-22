# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve, Qt
from PyQt5.QtGui import QColor, QPainter, QBrush, QPen, QFont, QPixmap, QRegion

class RoundedButton(QtWidgets.QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setMouseTracking(True)
        self.hovered = False
        self.animation = QPropertyAnimation(self, b"minimumHeight")
        self.animation.setDuration(150)
        self.animation.setEasingCurve(QEasingCurve.OutCubic)
        
        self.normal_style = """
            QPushButton {
                font-family: 'Arial';
                font-weight: bold;
                background-color: #4A90E2;
                color: white;
                font-size: 14px;
                padding: 10px;
                border-radius: 15px;
                border: none;
                text-align: left;
                padding-left: 15px;
            }
        """
        
        self.hover_style = """
            QPushButton {
                font-family: 'Arial';
                font-weight: bold;
                background-color: #6BB9F0;
                color: white;
                font-size: 14px;
                padding: 10px;
                border-radius: 15px;
                border: none;
                text-align: left;
                padding-left: 15px;
            }
        """
        
        self.selected_style = """
            QPushButton {
                font-family: 'Arial';
                font-weight: bold;
                background-color: #2E6DA4;
                color: white;
                font-size: 14px;
                padding: 10px;
                border-radius: 15px;
                border: none;
                text-align: left;
                padding-left: 15px;
            }
        """
        
        self.setStyleSheet(self.normal_style)
        self.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.is_answered = False
        
    def enterEvent(self, event):
        if not self.is_answered:
            self.setStyleSheet(self.hover_style)
            self.animation.setStartValue(self.height())
            self.animation.setEndValue(self.height() + 5)
            self.animation.start()
        super().enterEvent(event)
        
    def leaveEvent(self, event):
        if not self.is_answered:
            self.setStyleSheet(self.normal_style)
            self.animation.setStartValue(self.height())
            self.animation.setEndValue(self.height() - 5)
            self.animation.start()
        super().leaveEvent(event)
        
    def mark_answered(self, answered=True):
        self.is_answered = answered
        if answered:
            self.setStyleSheet(self.selected_style)
        else:
            self.setStyleSheet(self.normal_style)


class CircularProgressBar(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(50, 50)
        self.value = 0
        self.max_value = 100
        self.setStyleSheet("background-color: transparent;")
        
    def set_value(self, value):
        self.value = value
        self.update()
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(QColor("#F0F0F0")))
        painter.drawEllipse(5, 5, self.width() - 10, self.height() - 10)
        pen = QPen(QColor("#4A90E2"), 5)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)
        span_angle = int(360 * (self.value / self.max_value))
        painter.drawArc(10, 10, self.width() - 20, self.height() - 20, 90 * 16, -span_angle * 16)
        painter.setPen(QColor("#333333"))
        painter.setFont(QFont("Arial", 10, QFont.Bold))
        painter.drawText(self.rect(), Qt.AlignCenter, f"{self.value}%")


class ProfilePictureWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(150, 150)
        self.setMaximumSize(150, 150)
        
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        
        self.picture_label = QtWidgets.QLabel()
        self.picture_label.setAlignment(Qt.AlignCenter)
        self.picture_label.setStyleSheet("""
            QLabel {
                background-color: #F0F0F0;
                border-radius: 75px;
                border: 2px dashed #CCCCCC;
            }
        """)
        
        self.set_default_picture()
        
        self.upload_button = QtWidgets.QPushButton("Upload Photo")
        self.upload_button.setStyleSheet("""
            QPushButton {
                background-color: #4A90E2;
                color: white;
                border-radius: 10px;
                padding: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #6BB9F0;
            }
        """)
        
        self.layout.addWidget(self.picture_label)
        self.layout.addWidget(self.upload_button)
        
        self.upload_button.clicked.connect(self.upload_picture)
        
        self.current_picture = None
        
    def set_default_picture(self):
        pixmap = QPixmap(150, 150)
        pixmap.fill(Qt.transparent)
        
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QBrush(QColor("#F0F0F0")))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(0, 0, 150, 150)
        
        painter.setPen(QPen(QColor("#CCCCCC"), 2))
        painter.drawEllipse(60, 40, 30, 30)
        painter.drawLine(75, 70, 75, 100)
        painter.drawLine(75, 80, 60, 95)
        painter.drawLine(75, 80, 90, 95)
        painter.drawLine(75, 100, 60, 120)
        painter.drawLine(75, 100, 90, 120)
        
        painter.end()
        
        mask = pixmap.createMaskFromColor(Qt.transparent)
        pixmap.setMask(mask)
        
        self.picture_label.setPixmap(pixmap)
        
    def upload_picture(self):
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "Select Profile Picture", "", "Image Files (*.png *.jpg *.jpeg)"
        )
        
        if file_name:
            # Read the image file as binary data
            with open(file_name, 'rb') as file:
                self.current_picture = file.read()
            
            # Create QPixmap from binary data
            pixmap = QPixmap()
            pixmap.loadFromData(self.current_picture)
            
            if not pixmap.isNull():
                mask = QPixmap(150, 150)
                mask.fill(Qt.transparent)
                painter = QPainter(mask)
                painter.setRenderHint(QPainter.Antialiasing)
                painter.setBrush(Qt.black)
                painter.setPen(Qt.NoPen)
                painter.drawEllipse(0, 0, 150, 150)
                painter.end()
            
            pixmap = pixmap.scaled(150, 150, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
            
            if pixmap.width() > 150 or pixmap.height() > 150:
                pixmap = pixmap.copy(
                    (pixmap.width() - 150) // 2,
                    (pixmap.height() - 150) // 2,
                    150, 150
                )
            
            result = QPixmap(150, 150)
            result.fill(Qt.transparent)
            painter = QPainter(result)
            painter.setRenderHint(QPainter.Antialiasing)
            painter.setClipRegion(QRegion(mask.mask()))
            painter.drawPixmap(0, 0, pixmap)
            painter.end()
            
            self.picture_label.setPixmap(result)
            self.picture_label.setStyleSheet("""
                QLabel {
                    background-color: transparent;
                    border-radius: 75px;
                    border: 2px solid #4A90E2;
                }
            """)


class PromptDialog(QtWidgets.QDialog):
    def __init__(self, prompt, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Answer Prompt")
        self.setMinimumSize(500, 300)
        self.setStyleSheet("""
            QDialog {
                background-color: white;
                border-radius: 15px;
            }
        """)
        
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(15)
        
        self.prompt_label = QtWidgets.QLabel(prompt)
        self.prompt_label.setStyleSheet("""
            QLabel {
                font-family: 'Arial';
                font-size: 16px;
                font-weight: bold;
                color: #333333;
            }
        """)
        self.layout.addWidget(self.prompt_label)
        
        self.answer_edit = QtWidgets.QTextEdit()
        self.answer_edit.setPlaceholderText("Your answer here... (Be creative and authentic!)")
        self.answer_edit.setStyleSheet("""
            QTextEdit {
                border: 2px solid #DDDDDD;
                border-radius: 10px;
                padding: 10px;
                font-size: 14px;
                background-color: #FAFAFA;
            }
            QTextEdit:focus {
                border: 2px solid #4A90E2;
            }
        """)
        self.layout.addWidget(self.answer_edit)
        
        self.char_count = QtWidgets.QLabel("0/250 characters")
        self.char_count.setStyleSheet("color: #777777; font-size: 12px;")
        self.layout.addWidget(self.char_count)
        
        self.answer_edit.textChanged.connect(self.update_char_count)
        
        self.buttons_layout = QtWidgets.QHBoxLayout()
        self.buttons_layout.setSpacing(10)
        
        self.cancel_button = QtWidgets.QPushButton("Cancel")
        self.cancel_button.setStyleSheet("""
            QPushButton {
                background-color: #F0F0F0;
                border: none;
                border-radius: 10px;
                padding: 10px 20px;
                font-weight: bold;
                color: #333333;
            }
            QPushButton:hover {
                background-color: #E0E0E0;
            }
        """)
        
        self.save_button = QtWidgets.QPushButton("Save Answer")
        self.save_button.setStyleSheet("""
            QPushButton {
                background-color: #4A90E2;
                border: none;
                border-radius: 10px;
                padding: 10px 20px;
                font-weight: bold;
                color: white;
            }
            QPushButton:hover {
                background-color: #6BB9F0;
            }
            QPushButton:disabled {
                background-color: #CCE0F0;
                color: white;
            }
        """)
        self.save_button.setEnabled(False)
        
        self.buttons_layout.addWidget(self.cancel_button)
        self.buttons_layout.addWidget(self.save_button)
        self.buttons_layout.setAlignment(Qt.AlignRight)
        
        self.layout.addLayout(self.buttons_layout)
        
        self.cancel_button.clicked.connect(self.reject)
        self.save_button.clicked.connect(self.check_and_save_answer)
        
    def update_char_count(self):
        count = len(self.answer_edit.toPlainText())
        self.char_count.setText(f"{count}/250 characters")
        self.save_button.setEnabled(count > 0 and count <= 250)
        
        if count > 250:
            self.char_count.setStyleSheet("color: #FF0000; font-size: 12px;")
        else:
            self.char_count.setStyleSheet("color: #777777; font-size: 12px;")
    
    def check_and_save_answer(self):
        # Check if the answer is empty
        if not self.answer_edit.toPlainText().strip():
            response = QMessageBox.question(
                self,
                "No Answer Provided",
                "Selecting prompts for bio would help you get better matches. Do you want to proceed anyway?",
                QMessageBox.Ok | QMessageBox.Yes | QMessageBox.Cancel,
                QMessageBox.Cancel
            )
            if response == QMessageBox.Ok:
                return  # Stay on the fill bio window
            elif response == QMessageBox.Yes:
                self.accept()  # Proceed anyway
                return
        
        # Save the answer if valid
        self.accept()
            
    def get_answer(self):
        return self.answer_edit.toPlainText()


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(851, 500)
        Dialog.setMinimumSize(851, 500)
        Dialog.setMaximumSize(851, 500)
        Dialog.setStyleSheet("""
            QDialog {
                background-color: white;
            }
            QLabel {
                font-weight: bold;
                font-size: 14px;
                color: #333333;
            }
        """)
        Dialog.setWindowTitle("Profile Builder")
        
        self.dialog = Dialog
        
        # Main Layout
        self.main_layout = QtWidgets.QVBoxLayout(Dialog)
        self.main_layout.setContentsMargins(30, 20, 30, 20)
        self.main_layout.setSpacing(20)
        
        # Header Layout
        self.header_layout = QtWidgets.QHBoxLayout()
        self.logo_label = QtWidgets.QLabel("💙 Profile Builder")
        self.logo_label.setStyleSheet("""
            QLabel {
                font-family: 'Arial';
                font-size: 24px;
                font-weight: bold;
                color: #4A90E2;
            }
        """)
        
        self.progress_bar = CircularProgressBar()
        self.progress_bar.set_value(0)
        
        self.header_layout.addWidget(self.logo_label)
        self.header_layout.addStretch()
        self.header_layout.addWidget(self.progress_bar)
        
        self.main_layout.addLayout(self.header_layout)
        
        # Content Container
        self.content_container = QtWidgets.QWidget()
        self.content_container.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 15px;
                border: 1px solid #EEEEEE;
            }
        """)
        
        # Content Layout
        self.content_layout = QtWidgets.QHBoxLayout(self.content_container)
        self.content_layout.setContentsMargins(20, 20, 20, 20)
        self.content_layout.setSpacing(20)
        
        # Left Side - Profile Picture
        self.left_side = QtWidgets.QWidget()
        left_layout = QtWidgets.QVBoxLayout(self.left_side)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(15)
        
        # Profile Picture
        self.profile_picture = ProfilePictureWidget()
        left_layout.addWidget(self.profile_picture, 0, Qt.AlignTop)
        left_layout.addStretch()
        
        self.content_layout.addWidget(self.left_side)
        
        # Right Side - Form Fields
        self.right_side = QtWidgets.QWidget()
        right_layout = QtWidgets.QVBoxLayout(self.right_side)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(20)
        
        # Form Grid
        self.form_grid = QtWidgets.QGridLayout()
        self.form_grid.setSpacing(15)
        
        # Age Input
        self.age_container = QtWidgets.QWidget()
        self.age_container.setStyleSheet("""
            QWidget {
                background-color: #F8F9FA;
                border-radius: 10px;
                padding: 10px;
            }
        """)
        age_layout = QtWidgets.QVBoxLayout(self.age_container)
        age_layout.setSpacing(8)
        
        self.age_label = QtWidgets.QLabel("Age")
        self.age_input = QtWidgets.QSpinBox()
        self.age_input.setMinimum(18)
        self.age_input.setMaximum(99)
        self.age_input.setValue(25)
        self.age_input.setStyleSheet("""
            QSpinBox {
                border: 2px solid #DDDDDD;
                border-radius: 8px;
                padding: 8px;
                font-size: 14px;
                background-color: white;
            }
            QSpinBox:focus {
                border: 2px solid #4A90E2;
            }
        """)
        age_layout.addWidget(self.age_label)
        age_layout.addWidget(self.age_input)
        
        # Gender Input
        self.gender_container = QtWidgets.QWidget()
        self.gender_container.setStyleSheet("""
            QWidget {
                background-color: #F8F9FA;
                border-radius: 10px;
                padding: 10px;
            }
        """)
        gender_layout = QtWidgets.QVBoxLayout(self.gender_container)
        gender_layout.setSpacing(8)
        
        self.gender_label = QtWidgets.QLabel("Gender")
        self.gender_input = QtWidgets.QComboBox()
        self.gender_input.addItems(["Select Gender", "Male", "Female", "Others"])
        self.gender_input.setStyleSheet("""
            QComboBox {
                border: 2px solid #DDDDDD;
                border-radius: 8px;
                padding: 8px;
                font-size: 14px;
                background-color: white;
            }
            QComboBox:focus {
                border: 2px solid #4A90E2;
            }
        """)
        gender_layout.addWidget(self.gender_label)
        gender_layout.addWidget(self.gender_input)
        
        # Location Input
        self.location_container = QtWidgets.QWidget()
        self.location_container.setStyleSheet("""
            QWidget {
                background-color: #F8F9FA;
                border-radius: 10px;
                padding: 10px;
            }
        """)
        location_layout = QtWidgets.QVBoxLayout(self.location_container)
        location_layout.setSpacing(8)
        
        self.location_label = QtWidgets.QLabel("Location")
        self.location_input = QtWidgets.QLineEdit()
        self.location_input.setStyleSheet("""
            QLineEdit {
                border: 2px solid #DDDDDD;
                border-radius: 8px;
                padding: 8px;
                font-size: 14px;
                background-color: white;
            }
            QLineEdit:focus {
                border: 2px solid #4A90E2;
            }
        """)
        location_layout.addWidget(self.location_label)
        location_layout.addWidget(self.location_input)
        
        # Interests Input
        self.interests_container = QtWidgets.QWidget()
        self.interests_container.setStyleSheet("""
            QWidget {
                background-color: #F8F9FA;
                border-radius: 10px;
                padding: 10px;
            }
        """)
        interests_layout = QtWidgets.QVBoxLayout(self.interests_container)
        interests_layout.setSpacing(8)
        
        self.interests_label = QtWidgets.QLabel("Interests")
        self.interests_input = QtWidgets.QLineEdit()
        self.interests_input.setPlaceholderText("Use keywords e.g., Photography, Traveling")
        self.interests_input.setStyleSheet("""
            QLineEdit {
                border: 2px solid #DDDDDD;
                border-radius: 8px;
                padding: 8px;
                font-size: 14px;
                background-color: white;
            }
            QLineEdit:focus {
                border: 2px solid #4A90E2;
            }
        """)
        interests_layout.addWidget(self.interests_label)
        interests_layout.addWidget(self.interests_input)
        
        # Add fields to grid
        self.form_grid.addWidget(self.age_container, 0, 0)
        self.form_grid.addWidget(self.gender_container, 0, 1)
        self.form_grid.addWidget(self.location_container, 1, 0)
        self.form_grid.addWidget(self.interests_container, 1, 1)
        
        right_layout.addLayout(self.form_grid)
        
        # Select Prompts Button
        self.select_prompts_button = QtWidgets.QPushButton("Fill Bio")
        self.select_prompts_button.setFixedWidth(200)
        self.select_prompts_button.setStyleSheet("""
            QPushButton {
                background-color: #4A90E2;
                color: white;
                border-radius: 10px;
                padding: 12px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #357ABD;
            }
        """)
        self.select_prompts_button.clicked.connect(self.show_prompts_dialog)
        right_layout.addWidget(self.select_prompts_button, 0, Qt.AlignCenter)
        
        right_layout.addStretch()
        
        self.content_layout.addWidget(self.right_side)
        
        # Add content container to main layout
        self.main_layout.addWidget(self.content_container)
        
        # Proceed Button
        self.proceed_button = QtWidgets.QPushButton("Proceed")
        self.proceed_button.setFixedWidth(200)
        self.proceed_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border-radius: 10px;
                padding: 12px;
                font-weight: bold;
                font-size: 16px;
            }
            QPushButton:disabled {
                background-color: #A5D6A7;
            }
        """)
        self.proceed_button.setEnabled(False)
        self.main_layout.addWidget(self.proceed_button, 0, Qt.AlignCenter)

        # Connect signals
        self.proceed_button.clicked.connect(self.check_progress)
        self.gender_input.currentIndexChanged.connect(self.update_progress)
        self.location_input.textChanged.connect(self.update_progress)
        self.interests_input.textChanged.connect(self.update_progress)
        
        # Initialize prompts
        self.prompt_answers = {}
        self.dating_prompts = [
            
            "My ambition in life is...",
            "Two truths and a lie...",
            "I'm looking for someone who...",
            "The way to my heart is...",
            "My most controversial opinion is...",
            "My simple pleasures are...",
            "I'm most passionate about...",
            "We'll get along if...",
            "I want someone who...",
            "My love language is..."
        ]
        
        self.update_progress()

    def show_prompts_dialog(self):
        dialog = QtWidgets.QDialog(self.dialog)
        dialog.setWindowTitle("Fill Bio")
        dialog.setMinimumWidth(600)
        dialog.setMinimumHeight(700)
        dialog.setStyleSheet("background-color: white;")
        
        layout = QtWidgets.QVBoxLayout(dialog)
        layout.setSpacing(20)
        
        # Bio Preview/Edit Section
        bio_container = QtWidgets.QWidget()
        bio_container.setStyleSheet("""
            QWidget {
                background-color: #F8F9FA;
                border-radius: 15px;
                padding: 15px;
            }
        """)
        bio_layout = QtWidgets.QVBoxLayout(bio_container)
        
        bio_label = QtWidgets.QLabel("Your Bio")
        bio_label.setStyleSheet("""
            QLabel {
                font-family: 'Arial';
                font-size: 16px;
                font-weight: bold;
                color: #333333;
            }
        """)
        
        self.bio_edit = QtWidgets.QTextEdit()
        self.bio_edit.setMinimumHeight(150)
        self.bio_edit.setStyleSheet("""
            QTextEdit {
                border: 2px solid #DDDDDD;
                border-radius: 10px;
                padding: 10px;
                font-size: 14px;
                background-color: white;
            }
            QTextEdit:focus {
                border: 2px solid #4A90E2;
            }
        """)
        
        # Set current bio if exists
        if hasattr(self.dialog, 'bio') and self.dialog.bio:
            self.bio_edit.setText(self.dialog.bio)
        
        bio_layout.addWidget(bio_label)
        bio_layout.addWidget(self.bio_edit)
        
        layout.addWidget(bio_container)
        
        # Prompts Section Label
        prompts_label = QtWidgets.QLabel("Add to your bio with prompts")
        prompts_label.setStyleSheet("""
            QLabel {
                font-family: 'Arial';
                font-size: 16px;
                font-weight: bold;
                color: #333333;
            }
        """)
        layout.addWidget(prompts_label)
        
        scroll = QtWidgets.QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("border: none;")
        
        scroll_content = QtWidgets.QWidget()
        scroll_layout = QtWidgets.QVBoxLayout(scroll_content)
        
        # Add prompts
        for prompt in self.dating_prompts:
            button = RoundedButton(prompt)
            if prompt in self.prompt_answers:
                button.setText(f"{prompt}\n{self.prompt_answers[prompt]}")
                button.mark_answered(True)
            button.clicked.connect(lambda checked, p=prompt, b=button: self.show_prompt_dialog(p, b, dialog))
            scroll_layout.addWidget(button)
        
        scroll.setWidget(scroll_content)
        layout.addWidget(scroll)
        
        # Done button
        done_button = QtWidgets.QPushButton("Done")
        done_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border-radius: 10px;
                padding: 10px;
                font-size: 14px;
                font-weight: bold;
            }
        """)
        done_button.clicked.connect(lambda: self.save_bio_and_close(dialog))
        layout.addWidget(done_button)
        
        dialog.exec_()
        self.update_progress()

    def save_bio_and_close(self, dialog):
        # Get the current bio text
        current_bio = self.bio_edit.toPlainText()
        
        # If there's no bio text and no prompts are answered, show warning
        if not current_bio and not self.prompt_answers:
            QtWidgets.QMessageBox.warning(
                dialog,
                "Prompts Required",
                "Please answer at least one prompt or write something in your bio before proceeding."
            )
            return
        
        # Save the bio text
        self.dialog.bio = current_bio
        dialog.accept()

    def show_prompt_dialog(self, prompt, button, parent_dialog):
        dialog = PromptDialog(prompt, parent_dialog)
        
        if prompt in self.prompt_answers:
            dialog.answer_edit.setText(self.prompt_answers[prompt])
            dialog.update_char_count()
        
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            answer = dialog.get_answer()
            if answer:
                self.prompt_answers[prompt] = answer
                button.mark_answered(True)
                button.setText(f"{prompt}\n{answer}")
                
                # Append the new prompt answer to the bio
                current_bio = self.bio_edit.toPlainText()
                new_prompt_text = f"\n\n{prompt} {answer}"
                self.bio_edit.setText(current_bio + new_prompt_text)
                
                # Update the dialog's bio attribute
                self.dialog.bio = self.bio_edit.toPlainText()
                
                self.update_progress()
    
    def update_progress(self):
        progress = 0
        
        if self.gender_input.currentIndex() > 0:
            progress += 15
        
        if self.location_input.text():
            progress += 15
        
        if self.profile_picture.current_picture:
            progress += 15
        
        if self.interests_input.text():
            progress += 15
        
        # Calculate bio progress (20% if bio exists)
        if hasattr(self.dialog, 'bio') and self.dialog.bio:
            progress += 20
        
        # Calculate prompts progress (40% total, but at least one prompt required)
        answered_prompts = len(self.prompt_answers)
        if answered_prompts > 0:  # Only add prompt progress if at least one is answered
            progress += min(40, answered_prompts * 8)  # 8 points per prompt, max 40
        
        self.progress_bar.set_value(int(progress))
        # Enable proceed button only if total progress >= 50
        self.proceed_button.setEnabled(progress >= 50)

    def format_bio(self):
        """Format all answered prompts into a bio paragraph"""
        bio_parts = []
        for prompt, answer in self.prompt_answers.items():
            if answer:  # Only check if there's an answer
                # Remove any newlines from answer and format nicely
                clean_answer = answer.replace('\n', ' ').strip()
                if prompt:  # If there's a prompt, include it
                    bio_parts.append(f"{prompt} {clean_answer}")
                else:  # For empty prompt, just include the answer
                    bio_parts.append(clean_answer)
        
        # Join all parts with double newline for paragraph spacing
        return "\n\n".join(bio_parts)

    def check_progress(self):
        if self.progress_bar.value < 50:
            QtWidgets.QMessageBox.warning(self.dialog, "Incomplete Profile", 
                "Please complete at least 50% of your profile.")
            return False
        
        # Get the current bio text
        bio = self.bio_edit.toPlainText() if hasattr(self, 'bio_edit') else ""
        
        # Store the bio for the parent window to access
        self.dialog.bio = bio
        
        QtWidgets.QMessageBox.information(self.dialog, "Success", 
            "Profile is complete! Proceeding to the next step.")
        self.dialog.accept()
        return True

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())