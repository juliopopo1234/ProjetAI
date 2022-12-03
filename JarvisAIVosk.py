from vosk import Model, KaldiRecognizer
import pyaudio

#config_AnaelBM = 
config_Dragonlord = "C:/Users/Dragonlord-PC3060/Documents/ProjetAIvosk/ProjetAI/vosk_speech_engine/model/vosk-model-fr-0.22"

model = Model(config_Dragonlord)
recogniser = KaldiRecognizer(model, 16000)

mic = pyaudio.PyAudio()
stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
stream.start_stream()

def Listen():
    print("")
    print("Listening...")
    print("")

    while True:

        data = stream.read(4096)

        if recogniser.AcceptWaveform(data):
            text = recogniser.Result()
            p = text[14:-3]
            print(f"Vous avez dit : {p}")

            if len(p)>0:
                return p
            
            else:
                break

while True :
    Listen()