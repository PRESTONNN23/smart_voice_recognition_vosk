import sounddevice as sd
import queue

class AudioStream:
    def __init__(self, samplerate=16000, channels=1, blocksize=8000):
        self.samplerate = samplerate
        self.channels = channels
        self.blocksize = blocksize
        self.q = queue.Queue()
        self.stream = sd.InputStream(
            samplerate=self.samplerate,
            channels=self.channels,
            blocksize=self.blocksize,
            dtype='int16',
            callback=self.callback
        )

    def callback(self, indata, frames, time, status):
        if status:
            print(status)
        self.q.put(bytes(indata))

    def start(self):
        self.stream.start()

    def stop(self):
        self.stream.stop()

    def read(self):
        return self.q.get_nowait()