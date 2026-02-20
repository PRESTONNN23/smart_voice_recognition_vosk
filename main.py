from PyQt6 import QtCore, QtWidgets
from ui.main_window import MainWindow
from core.audio_stream import AudioStream
from core.asr_engine import ASREngine
import sys
import numpy as np

MODEL_PATH = "models/vosk-model-small-ru-0.22"

class AudioWorker(QtCore.QThread):
    waveform_signal = QtCore.pyqtSignal(np.ndarray)
    transcript_signal = QtCore.pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.audio = AudioStream()
        self.engine = ASREngine(MODEL_PATH)
        self.running = False

    def run(self):
        self.audio.start()
        self.running = True
        while self.running:
            try:
                data = self.audio.read()
                result = self.engine.accept_audio(data)
                waveform = np.frombuffer(data, dtype=np.int16)
                self.waveform_signal.emit(waveform)
                if result["type"] in ["partial", "final"]:
                    self.transcript_signal.emit(result["text"])
            except Exception:
                continue
        self.audio.stop()

    def stop(self):
        self.running = False
        self.quit()
        self.wait()

# ---------------- App controller ----------------
class AppController:
    def __init__(self, window: MainWindow):
        self.window = window
        self.worker = AudioWorker()

        self.window.start_button.clicked.connect(self.start)
        self.window.stop_button.clicked.connect(self.stop)

        self.plot = self.window.plot_widget.plot(np.zeros(8000), pen='c')

        self.worker.waveform_signal.connect(self.update_waveform)
        self.worker.transcript_signal.connect(self.update_transcript)

    def start(self):
        if not self.worker.isRunning():
            self.worker.start()

    def stop(self):
        if self.worker.isRunning():
            self.worker.stop()

    def update_waveform(self, data):
        self.plot.setData(data)

    def update_transcript(self, text):
        self.window.transcript_label.setText(text)

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    controller = AppController(window)
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()