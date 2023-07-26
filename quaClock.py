import sys
import time
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTabWidget, QLabel, QPushButton, QHBoxLayout, QDesktopWidget
from PyQt5.QtCore import QTimer
import pytz
from datetime import datetime

class ClockTab(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.label = QLabel()
        font = self.label.font()
        font.setPointSize(40)
        self.label.setFont(font)
        layout.addWidget(self.label)

        self.update_time()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)

        self.setLayout(layout)

    def update_time(self):
        current_time = time.strftime("%H:%M:%S")
        self.label.setText(current_time)

class StopwatchTab(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.is_running = False
        self.start_time = 0
        self.elapsed_time = 0
        self.laps = []

        layout = QVBoxLayout()

        self.time_label = QLabel("00:00:00")
        font = self.time_label.font()
        font.setPointSize(40)
        self.time_label.setFont(font)
        layout.addWidget(self.time_label)

        button_layout = QHBoxLayout()
        self.start_stop_button = QPushButton("Başlat")
        self.start_stop_button.clicked.connect(self.start_stop)
        button_layout.addWidget(self.start_stop_button)

        self.reset_button = QPushButton("Sıfırla")
        self.reset_button.clicked.connect(self.reset)
        button_layout.addWidget(self.reset_button)

        layout.addLayout(button_layout)

        self.lap_button = QPushButton("Tur")
        self.lap_button.clicked.connect(self.lap)
        layout.addWidget(self.lap_button)

        self.lap_list = QLabel()
        layout.addWidget(self.lap_list)

        self.setLayout(layout)

    def start_stop(self):
        if not self.is_running:
            self.is_running = True
            self.start_time = time.time() - self.elapsed_time
            self.start_stop_button.setText("Durdur")
            self.timer = QTimer(self)
            self.timer.timeout.connect(self.update_time)
            self.timer.start(10)

        else:
            self.is_running = False
            self.elapsed_time = time.time() - self.start_time
            self.start_stop_button.setText("Başlat")
            self.timer.stop()

    def update_time(self):
        current_time = time.time() - self.start_time
        hours = int(current_time // 3600)
        minutes = int((current_time % 3600) // 60)
        seconds = int(current_time % 60)
        self.time_label.setText(f"{hours:02d}:{minutes:02d}:{seconds:02d}")

    def lap(self):
        if self.is_running:
            lap_time = time.time() - self.start_time - sum(self.laps)
            self.laps.append(lap_time)
            self.update_lap_list()

    def reset(self):
        if self.is_running:
            self.elapsed_time = 0
            self.start_time = time.time()
        else:
            self.start_time = 0
            self.elapsed_time = 0
            self.laps = []
            self.time_label.setText("00:00:00")
            self.lap_list.setText("")

    def update_lap_list(self):
        laps_text = "Turlar:\n"
        for i, lap_time in enumerate(self.laps):
            hours = int(lap_time // 3600)
            minutes = int((lap_time % 3600) // 60)
            seconds = int(lap_time % 60)
            laps_text += f"Tur {i + 1}: {hours:02d}:{minutes:02d}:{seconds:02d}\n"
        self.lap_list.setText(laps_text)

class GlobalClockTab(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.city_labels = []
        cities = {
            "New York": "America/New_York",
            "London": "Europe/London",
            "Tokyo": "Asia/Tokyo",
            "Moscow": "Europe/Moscow",       
            "Istanbul": "Europe/Istanbul",  
            "Berlin": "Europe/Berlin",       
        }

        for city in cities:
            label = QLabel(city)
            font = label.font()
            font.setPointSize(20)
            label.setFont(font)
            self.city_labels.append(label)
            layout.addWidget(label)

        self.cities = cities

        self.update_time()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)

        self.setLayout(layout)

    def update_time(self):
        for label in self.city_labels:
            city_name = label.text().split(":")[0]
            timezone = pytz.timezone(self.cities[city_name])
            current_time = datetime.now(timezone).strftime("%H:%M:%S")
            label.setText(f"{city_name}: {current_time}")

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        tab_widget = QTabWidget()
        tab_widget.addTab(ClockTab(), "Saat")
        tab_widget.addTab(StopwatchTab(), "Kronometre")
        tab_widget.addTab(GlobalClockTab(), "Global Saat")

        layout.addWidget(tab_widget)

        self.setLayout(layout)
        self.setWindowTitle("Qua Saat")
        self.center_window()

    def center_window(self):
        screen_geometry = QDesktopWidget().availableGeometry()
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2
        self.move(x, y)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.showNormal()
    sys.exit(app.exec_())
