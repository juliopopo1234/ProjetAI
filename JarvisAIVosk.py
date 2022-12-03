from vosk import Model, KaldiRecognizer
import pyaudio

model = Model("C:\Users\Dragonlord-PC3060\Documents\ProjetAIvosk\ProjetAI\vosk_speech_engine\model\vosk-model-fr-0.22")
recogniser = KaldiRecognizer(model, 16000)

mic = pyaudio.PyAudio()
