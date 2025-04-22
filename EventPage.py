import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QCalendarWidget, QVBoxLayout, 
                            QPushButton, QLineEdit, QLabel, QDialog, QTabWidget, 
                            QListWidget, QTextEdit, QMessageBox)
from PyQt5.QtGui import QTextCharFormat, QBrush, QColor
from PyQt5.QtCore import QDate

class EventDetailsDialog(QDialog):
    def __init__(self, date, event, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Event Details")
        self.setGeometry(550, 300, 600, 400)  # Increased size

        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        date_label = QLabel(f"Event on {date}:")
        date_label.setStyleSheet("font-weight: bold; font-size: 24px;")
        layout.addWidget(date_label)

        event_text = QTextEdit()
        event_text.setReadOnly(True)
        event_text.setText(event)
        event_text.setStyleSheet("font-size: 18px;")
        layout.addWidget(event_text)

        self.setLayout(layout)

class CalendarApp(QWidget):
    def __init__(self):
        super().__init__()
        self.events = {
            "2025-03-31": "Topic: Plant Trees\nTime: 10:00 AM\nLocation: National Park, Borivali\nAdress Link: https://maps.app.goo.gl/omteBSxhpAayHS6e9\n---------------------------------------------------------------------------------------------------\n",
            "2025-04-03": "Topic: Recycle\n Time: 11:00 AM\nLocation: Borivali West\nAdress Link: https://maps.app.goo.gl/omteBSxhpAayHS6e9\n---------------------------------------------------------------------------------------------------\n",
            "2025-04-11": "Topic: Save Water\nTime: 10:00 AM\nLocation: Borivali East\nAdress Link: https://maps.app.goo.gl/omteBSxhpAayHS6e9\n---------------------------------------------------------------------------------------------------\n",   
            "2025-04-19": "Topic: Animal shelter\nTime: 10:00 AM\nLocation: Borivali West\nAdress Link: https://maps.app.goo.gl/omteBSxhpAayHS6e9\n---------------------------------------------------------------------------------------------------\n",
            "2025-04-20": "Topic: Blood Donation Drive \nTime: 10:00 AM\nLocation: Borivali East\nAdress Link: https://maps.app.goo.gl/omteBSxhpAayHS6e9\n---------------------------------------------------------------------------------------------------\n",
            "2025-04-22": "Group Meetup",
            "2025-03-28": "Beach Cleanup", 
            "2025-04-25": "Fundraiser",
            "2025-04-27": "Community Cleanup",
            "2025-04-14": "Career Growth Workshop",
        }

        self.initUI()
        self.load_events()

    def initUI(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(25)

        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #E3E9FF;
                border-radius: 8px;
                background: white;
            }
            QTabBar::tab {
                padding: 12px 20px;
                font-size: 16px;
                font-weight: bold;
                background: #F5F9FF;
                border: 1px solid #E3E9FF;
                border-bottom: none;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                margin-right: 4px;
            }
            QTabBar::tab:selected {
                background: white;
                border-bottom: 2px solid #2196F3;
                color: #2196F3;
            }
        """)
        layout.addWidget(self.tabs)

        self.calendar_tab = QWidget()
        self.upcoming_events_tab = QWidget()
        self.upcoming_events_tab.setStyleSheet("font-weight: bold; font-size: 20px;")
        self.tabs.addTab(self.calendar_tab, "Calendar")
        self.tabs.addTab(self.upcoming_events_tab, "Upcoming Events")

        self.initCalendarTab()
        self.initUpcomingEventsTab()

    def initCalendarTab(self):
        layout = QVBoxLayout(self.calendar_tab)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        self.calendar = QCalendarWidget()
        self.calendar.setStyleSheet("""
            QCalendarWidget {
                background: white;
                border: 1px solid #E3E9FF;
                border-radius: 8px;
            }
            QCalendarWidget QToolButton {
                height: 30px;
                width: 80px;
                color: #1E88E5;
                font-size: 14px;
                icon-size: 20px, 20px;
                background: transparent;
            }
            QCalendarWidget QMenu {
                width: 150px;
                left: 20px;
                color: #1E88E5;
                font-size: 14px;
                background: white;
            }
            QCalendarWidget QSpinBox {
                width: 50px;
                font-size: 14px;
                color: #1E88E5;
                background: transparent;
                selection-background-color: #1E88E5;
                selection-color: white;
            }
            QCalendarWidget QAbstractItemView:enabled {
                font-size: 14px;
                color: #1E88E5;
                background: white;
                selection-background-color: #1E88E5;
                selection-color: white;
            }
        """)
        self.calendar.setGridVisible(True)
        self.calendar.clicked.connect(self.show_date)

        layout.addWidget(self.calendar)

        self.event_label = QLabel("Event: ", self)
        self.event_label.setStyleSheet("font-weight: bold; font-size: 20px;")
        layout.addWidget(self.event_label)

    def initUpcomingEventsTab(self):
        layout = QVBoxLayout(self.upcoming_events_tab)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        self.upcoming_events_list = QListWidget()
        self.upcoming_events_list.setStyleSheet("""
            QListWidget {
                background-color: white;
                border: 1px solid #E3E9FF;
                border-radius: 8px;
                font-size: 16px;
                padding: 10px;
            }
            QListWidget::item {
                padding: 12px;
                border-bottom: 1px solid #E3E9FF;
            }
            QListWidget::item:selected {
                background-color: #F5F9FF;
                color: #2196F3;
            }
        """)
        layout.addWidget(self.upcoming_events_list)

        self.update_upcoming_events()

    def load_events(self):
        for date in self.events.keys():
            self.highlight_date(date)

    def highlight_date(self, date_str):
        date = QDate.fromString(date_str, "yyyy-MM-dd")
        format = QTextCharFormat()
        format.setBackground(QBrush(QColor("#FFF9C4")))  # Light yellow
        self.calendar.setDateTextFormat(date, format)

    def show_date(self, date):
        selected_date = date.toString("yyyy-MM-dd")
        event = self.events.get(selected_date)
    
        if event:
            self.event_label.setText(f"Event: {event}")
            self.event_label.setStyleSheet("font-weight: bold; font-size: 20px;")   
            dialog = EventDetailsDialog(selected_date, event, self)
            dialog.exec()
        else:
            self.event_label.setText("Event: No event")

    def update_upcoming_events(self):
        self.upcoming_events_list.clear()
        for date_str, event in sorted(self.events.items()):
            self.upcoming_events_list.addItem(f"{date_str}: {event}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QMainWindow()
    calendar = CalendarApp()
    window.setCentralWidget(calendar)
    window.setGeometry(400, 200, 1024, 768)
    window.show()
    sys.exit(app.exec())