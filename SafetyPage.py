from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, 
    QScrollArea, QFrame, QDialog, QLineEdit, QHBoxLayout, QMessageBox, QInputDialog, QMainWindow, QTextEdit
)
from PyQt5.QtCore import Qt
from database1 import Database

class HelpSafetyPage(QWidget):
    def __init__(self, parent=None, current_user=None):
        super().__init__(parent)
        self.current_user = current_user
        self.db = Database(host='localhost', user='root', password='naitik@mysql', database='saathi')
        self.setWindowTitle("Help & Safety - Saathi")
        self.setGeometry(100, 100, 1024, 768)
        self.setStyleSheet("""
            QWidget {
                background-color: #f5f5f5;
                font-family: 'Arial';
            }
            QLabel {
                color: #2c3e50;
                font-weight: 500;
            }
            QPushButton {
                font-weight: bold;
            }
            QMessageBox {
                background-color: white;
            }
            QMessageBox QPushButton {
                background-color: #2196F3;
                color: white;
                border-radius: 8px;
                padding: 12px 24px;
                min-width: 100px;
                font-size: 16px;
            }
            QMessageBox QPushButton:hover {
                background-color: #1976D2;
            }
            QInputDialog {
                background-color: white;
            }
            QInputDialog QLineEdit {
                padding: 12px;
                border: 2px solid #E3E9FF;
                border-radius: 8px;
                font-size: 16px;
            }
            QInputDialog QPushButton {
                background-color: #2196F3;
                color: white;
                border-radius: 8px;
                padding: 12px 24px;
                min-width: 100px;
                font-size: 16px;
            }
            QInputDialog QPushButton:hover {
                background-color: #1976D2;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(30)

        # Heading
        heading = QLabel("📌 Help & Safety")
        heading.setStyleSheet("""
            font-size: 32px;
            font-weight: bold;
            color: #2196F3;
            margin: 15px;
        """)
        heading.setAlignment(Qt.AlignCenter)
        layout.addWidget(heading)

        # Scrollable FAQ Section
        self.faq_section = self.create_faq_section()
        layout.addWidget(self.faq_section)

        # Fixed Bottom Buttons
        self.create_fixed_buttons(layout)

    def create_faq_section(self):
        """Creates a scrollable FAQ section with collapsible answers."""
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background: transparent;
            }
            QScrollBar:vertical {
                border: none;
                background: #F0F0F0;
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background: #2196F3;
                border-radius: 6px;
            }
        """)

        faq_container = QWidget()
        faq_layout = QVBoxLayout(faq_container)
        faq_layout.setSpacing(20)

        faqs = [
            ("What is Saathi?", 
             "🔹 Saathi is a **friend-finder app** that helps you connect with like-minded people based on shared **interests, location, and work background**. "
             "It also supports **community-building** and tracks nearby **events**."),
            
            ("How does Saathi verify users?", 
             "🔹 User verification is done through **Aadhaar-based OTP authentication**, ensuring a **safe and trusted environment**."),

            ("What features does Saathi offer?", 
             "🔹 Saathi allows users to:\n"
             "✔ **Build profiles** & upload photos\n"
             "✔ **View photos & chat** with friends\n"
             "✔ **Find people with similar interests**"),

            ("How does Saathi find friends for me?", 
             "🔹 Interest Matching – Connect with people who share your hobbies and passions.\n"
             "🔹 Location-Based Suggestions – Find friends nearby for real-world connections.\n"
             "🔹 Smart Profile Boost – Complete profiles (with bios & pictures) get priority.\n"
             "🔹 Age Compatibility – Meet people in a similar age group for better bonding.\n"
             "🔹 Best Matches First – Saathi highlights your most relevant connections first!"),

            ("How do I report a user?", 
             "🔹 You can **report a user** by clicking on **'Report User'** below and entering their username.\n\n"
             "⚠️ If a user receives **more than 3 reports** from different users, their account gets **banned automatically**."),

            ("How do I delete my account?", 
             "🔹 Click on **'Delete Account'** below and confirm your choice.\n\n"
             "⚠️ This action **CANNOT be undone!**"),
        ]

        for question, answer in faqs:
            faq_layout.addWidget(self.create_faq_item(question, answer))

        faq_layout.addStretch()

        scroll_area.setWidget(faq_container)
        return scroll_area

    def create_faq_item(self, question, answer):
        """Creates a collapsible FAQ item with a toggle button."""
        frame = QFrame()
        frame.setStyleSheet("""
            QFrame {
                border: 2px solid #E3E9FF;
                padding: 15px;
                border-radius: 10px;
                background-color: white;
            }
        """)
        frame_layout = QVBoxLayout(frame)
        frame_layout.setSpacing(15)

        question_label = QPushButton(question)
        question_label.setStyleSheet("""
            QPushButton {
                font-size: 18px;
                font-weight: bold;
                text-align: left;
                background-color: #F5F9FF;
                padding: 20px;
                border: none;
                border-radius: 8px;
                color: #2196F3;
            }
            QPushButton:hover {
                background-color: #E3F2FD;
            }
        """)
        question_label.setCheckable(True)

        answer_label = QLabel(answer)
        answer_label.setWordWrap(True)
        answer_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                color: #333;
                padding: 15px;
                line-height: 1.6;
                font-weight: normal;
                background-color: #FFFFFF;
                border-radius: 8px;
            }
        """)
        answer_label.setVisible(False)

        question_label.clicked.connect(lambda: answer_label.setVisible(not answer_label.isVisible()))

        frame_layout.addWidget(question_label)
        frame_layout.addWidget(answer_label)
        return frame

    def create_fixed_buttons(self, layout):
        """Creates the fixed bottom action buttons."""
        button_container = QFrame()
        button_container.setStyleSheet("""
            QFrame {
                background-color: white;
                padding: 20px;
                border-top: 2px solid #E3E9FF;
            }
            QPushButton {
                background-color: #FF5252;
                color: white;
                font-size: 18px;
                padding: 15px;
                border-radius: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #FF1744;
            }
        """)
        button_layout = QHBoxLayout(button_container)
        button_layout.setSpacing(20)

        # Report User Button
        report_btn = QPushButton("🚨 Report User")
        report_btn.setFixedSize(300, 60)
        report_btn.clicked.connect(self.report_user)

        # Delete Account Button
        delete_btn = QPushButton("❌ Delete Account")
        delete_btn.setFixedSize(300, 60)
        delete_btn.clicked.connect(self.delete_account)

        button_layout.addWidget(report_btn)
        button_layout.addWidget(delete_btn)

        layout.addWidget(button_container)

    def report_user(self):
        """Opens a dialog to report a user and handles the reporting process."""
        if not self.current_user:
            QMessageBox.warning(self, "Error", "Please log in to report a user.")
            return

        username, ok = QInputDialog.getText(self, "Report User", "Enter the username of the user you want to report:")
        if ok and username:
            try:
                # Check if reported user exists
                cursor = self.db.connection.cursor()
                cursor.execute("SELECT id, reports_filed FROM users WHERE name = %s", (username,))
                user_data = cursor.fetchone()

                if not user_data:
                    QMessageBox.warning(self, "Error", f"User '{username}' not found.")
                    return

                user_id, reports = user_data
                reports = 0 if reports is None else reports
                new_reports = reports + 1

                # Update reports count
                cursor.execute("UPDATE users SET reports_filed = %s WHERE id = %s", (new_reports, user_id))
                self.db.connection.commit()

                if new_reports >= 3:
                    # Delete user if they have 3 or more reports
                    cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
                    self.db.connection.commit()
                    QMessageBox.information(self, "Success", 
                        f"User '{username}' has been removed from the platform due to multiple reports.")
                else:
                    QMessageBox.information(self, "Success", 
                        f"User '{username}' has been reported. They have {new_reports} report(s).")

            except Exception as e:
                self.db.connection.rollback()
                QMessageBox.critical(self, "Error", f"Failed to report user: {str(e)}")
            finally:
                cursor.close()

    def delete_account(self):
        """Handles the account deletion process."""
        if not self.current_user:
            QMessageBox.warning(self, "Error", "No user logged in.")
            return

        reply = QMessageBox.question(self, "Confirm Deletion", 
            "Are you sure you want to delete your account? This action cannot be undone.",
            QMessageBox.Yes | QMessageBox.No)

        if reply == QMessageBox.Yes:
            try:
                cursor = self.db.connection.cursor()
                cursor.execute("DELETE FROM users WHERE name = %s", (self.current_user,))
                self.db.connection.commit()
                QMessageBox.information(self, "Success", "Your account has been deleted successfully.")
                
                # Navigate back to Welcome Page
                from WelcomePage2 import Ui_MainWindow
                welcome_window = QMainWindow()
                welcome_ui = Ui_MainWindow()
                welcome_ui.setupUi(welcome_window)
                
                # Get the main window
                main_window = self.window()
                if main_window:
                    main_window.close()
                
                welcome_window.show()

            except Exception as e:
                self.db.connection.rollback()
                QMessageBox.critical(self, "Error", f"Failed to delete account: {str(e)}")
            finally:
                cursor.close()

class SafetyPage(QWidget):
    def __init__(self, current_user=None):
        super().__init__()
        self.current_user = current_user
        self.setFixedSize(774, 768)  # Adjusted for 1024x768 with sidebar
        
        # Create main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        # Safety tips section
        tips_frame = QFrame()
        tips_frame.setStyleSheet("""
            QFrame {
                background: white;
                border-radius: 8px;
                border: 1px solid #E3E9FF;
            }
        """)
        
        tips_layout = QVBoxLayout(tips_frame)
        tips_layout.setContentsMargins(20, 20, 20, 20)
        tips_layout.setSpacing(15)
        
        tips_title = QLabel("Safety Tips")
        tips_title.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: bold;
                color: #1E88E5;
            }
        """)
        
        tips_text = QTextEdit()
        tips_text.setReadOnly(True)
        tips_text.setStyleSheet("""
            QTextEdit {
                border: none;
                font-size: 14px;
                color: #666;
                background: transparent;
            }
        """)
        tips_text.setHtml("""
            <h3>Online Safety Tips:</h3>
            <ul>
                <li>Never share personal information with strangers</li>
                <li>Be cautious when meeting new people online</li>
                <li>Report any suspicious behavior</li>
                <li>Use strong passwords and enable two-factor authentication</li>
            </ul>
            
            <h3>Meeting in Person:</h3>
            <ul>
                <li>Meet in public places</li>
                <li>Tell a friend or family member about your plans</li>
                <li>Trust your instincts</li>
                <li>Have a way to leave if you feel uncomfortable</li>
            </ul>
        """)
        
        tips_layout.addWidget(tips_title)
        tips_layout.addWidget(tips_text)
        
        # Emergency contacts section
        contacts_frame = QFrame()
        contacts_frame.setStyleSheet("""
            QFrame {
                background: white;
                border-radius: 8px;
                border: 1px solid #E3E9FF;
            }
        """)
        
        contacts_layout = QVBoxLayout(contacts_frame)
        contacts_layout.setContentsMargins(20, 20, 20, 20)
        contacts_layout.setSpacing(15)
        
        contacts_title = QLabel("Emergency Contacts")
        contacts_title.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: bold;
                color: #1E88E5;
            }
        """)
        
        # Emergency numbers
        numbers_layout = QVBoxLayout()
        numbers_layout.setSpacing(10)
        
        police = QLabel("Police: 100")
        ambulance = QLabel("Ambulance: 102")
        women_helpline = QLabel("Women Helpline: 1091")
        
        for label in [police, ambulance, women_helpline]:
            label.setStyleSheet("""
                QLabel {
                    font-size: 16px;
                    color: #666;
                }
            """)
            numbers_layout.addWidget(label)
        
        contacts_layout.addWidget(contacts_title)
        contacts_layout.addLayout(numbers_layout)
        
        # Report section
        report_frame = QFrame()
        report_frame.setStyleSheet("""
            QFrame {
                background: white;
                border-radius: 8px;
                border: 1px solid #E3E9FF;
            }
        """)
        
        report_layout = QVBoxLayout(report_frame)
        report_layout.setContentsMargins(20, 20, 20, 20)
        report_layout.setSpacing(15)
        
        report_title = QLabel("Report an Issue")
        report_title.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: bold;
                color: #1E88E5;
            }
        """)
        
        self.report_text = QTextEdit()
        self.report_text.setPlaceholderText("Describe the issue...")
        self.report_text.setStyleSheet("""
            QTextEdit {
                border: 1px solid #E3E9FF;
                border-radius: 4px;
                padding: 10px;
                font-size: 14px;
                min-height: 100px;
            }
        """)
        
        submit_btn = QPushButton("Submit Report")
        submit_btn.setStyleSheet("""
            QPushButton {
                background: #1E88E5;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 10px;
                font-size: 14px;
            }
            QPushButton:hover {
                background: #1976D2;
            }
        """)
        submit_btn.clicked.connect(self.submit_report)
        
        report_layout.addWidget(report_title)
        report_layout.addWidget(self.report_text)
        report_layout.addWidget(submit_btn)
        
        # Add widgets to main layout
        main_layout.addWidget(tips_frame)
        main_layout.addWidget(contacts_frame)
        main_layout.addWidget(report_frame)
        
    def submit_report(self):
        report_text = self.report_text.toPlainText()
        if report_text.strip():
            # Here you would typically send the report to your backend
            QMessageBox.information(self, "Report Submitted", "Thank you for your report. We will review it shortly.")
            self.report_text.clear()
        else:
            QMessageBox.warning(self, "Empty Report", "Please describe the issue before submitting.")

if __name__ == "__main__":
    app = QApplication([])
    window = HelpSafetyPage()
    window.show()
    app.exec_()
