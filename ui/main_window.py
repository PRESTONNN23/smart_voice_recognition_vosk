from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QLabel, QPushButton, QVBoxLayout, QWidget
import pyqtgraph as pg

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Smart Voice Intelligence Console")
        self.setGeometry(100, 100, 800, 400)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout()

        # Waveform
        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setYRange(-32768, 32767)
        layout.addWidget(self.plot_widget)

        # Live transcript
        self.transcript_label = QLabel("Transcript will appear here")
        layout.addWidget(self.transcript_label)

        # Start / Stop
        self.start_button = QPushButton("Start")
        self.stop_button = QPushButton("Stop")
        layout.addWidget(self.start_button)
        layout.addWidget(self.stop_button)

        self.central_widget.setLayout(layout)