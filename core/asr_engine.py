from vosk import Model, KaldiRecognizer
import json

class ASREngine:
    def __init__(self, model_path):
        self.model = Model(model_path)
        self.rec = KaldiRecognizer(self.model, 16000)
        self.rec.SetWords(True)

    def accept_audio(self, data):
        if self.rec.AcceptWaveform(data):
            result = json.loads(self.rec.Result())
            return {"type": "final", "text": result.get("text", "")}
        else:
            partial = json.loads(self.rec.PartialResult())
            return {"type": "partial", "text": partial.get("partial", "")}