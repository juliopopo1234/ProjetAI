from vosk import Model, KaldiRecognizer
import pyaudio
import subprocess as sp
import os
import pyttsx3
import datetime
import time
import webbrowser
from plyer import notification
import keyboard
import json
import pyjokes


#INITIALISATION DU MODULE DE RÉPONSE PYTTSX3
engine = pyttsx3.init('sapi5')
# Set Débit de parole
engine.setProperty('rate', 220)
# Set Volume
engine.setProperty('volume', 1.2)
# Set Voice (Male 0) (Female 1)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
# variable Lié à l'heure
now = datetime.datetime.now()
heure = now.strftime("%H")
min = now.strftime("%M")
date_time = now.strftime("%d/%m/%Y, %H:%M:%S")
# définition de la parole de VisionIA
def speak(audio):
    engine.say(audio)
    print('Vision IA :' + audio)
    engine.runAndWait() 
# config_AnaelBM =
config_Dragonlord = "C:/Users/Dragonlord-PC3060/Documents/ProjetAIvosk/ProjetAI/vosk_speech_engine/model/vosk-model-fr-0.22"
# Initialisation de l'instance de vosk et de son Model de reconnaissance vocale
model = Model(config_Dragonlord)
recogniser = KaldiRecognizer(model, 16000)

###################################################################
# Fonctionnalité de VisionIA
##################################################################
def DireLheure():
    speak("Il est "+heure+":"+min)

def AccueilHote():
    if (int(heure) > 6) and (int(heure) < 17):
        speak(f"Bonjour Monsieur!")
    elif (int(heure) > 18) and (int(heure) < 24):
        speak(f"Bonsoir Monsieur.")
    DireLheure()


def VisionAI():
    print("")
    print("Je vous écoute ...")
    print("")
    mic = pyaudio.PyAudio()
    stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
    stream.start_stream()
    text= " "
    p= " "
    historique= ""
    while True:
            data = stream.read(8000,exception_on_overflow = False)
            if len(data) == 0:
                break
            if recogniser.AcceptWaveform(data):
                #TO DO(Voir Historique de Paroles)
                # jres = json.loads(recogniser.Result())
                # historique = historique + jres['historique']
                text = recogniser.Result()
                p = text[14:-3]
                print(p)
            
            #Fonction stop VisionIA#
            if "stop vision" in p or "éteins toi vision" in p:
                if (int(heure) >= 6) and (int(heure) <= 17):
                    speak("Merci pour votre temps Monsieur, passez une bonne journée !")
                    stream.stop_stream()
                elif (int(heure) >= 18) and (int(heure) < 24):
                    speak("Merci pour votre temps Monsieur, passez une bonne soirée !")
                    stream.stop_stream()
                else :
                    speak("Merci pour votre temps Monsieur, passez une bonne nuit.")
                    stream.stop_stream()

            #Fonction attente#
            elif "at tends vision" in p:
                stream.stop_stream()
                speak("Ok j'attend, appuyez sur espace pour reprendre quand vous le souhaiterez")
                keyboard.wait("space") 
                speak("Reprise")
                p = ""
                stream.start_stream()

            #Réponses insultes#
            elif "va te faire enculer" in p:
                stream.stop_stream()
                speak("Toi va te faire enculer")
                p = ""
                stream.start_stream()
            elif "gros con" in p or "sale con" in p or "pauvre con" in p or "abruti" in p:
                stream.stop_stream()
                speak("Pardon Monsieur de vous avoir déçu.")
                speak("Je fais de mon mieux pour m'améliorer tous les jours")
                p = ""
                stream.start_stream()

            #Historique de paroles   TO DO
            # elif "affiche moi toute les commandes passées" in p:
            #     stream.stop_stream()
            #     print(f"Vous avez dit : {historique}")
            #     p = ""
            #     stream.start_stream()

            #Ouvre le cmd#
            elif 'ouvre la boîte noire' in p:
                stream.stop_stream()
                speak("Ouverture du CMD")
                os.startfile("C:\\Users\\Dragonlord-PC3060\\Downloads\\cmder\\Cmder.exe")
                p = ""
                stream.start_stream()

            #Réponse qui es tu ?#
            elif "comment t'appelles-tu" in p or "quel est ton nom" in p or "qui es-tu" in p:
                stream.stop_stream()
                speak('Je me nomme Vision, Je suis un assistant virtuel créer par Timothé Iskander pour l\'assister dans plusieurs tâches')
                p = ""
                stream.start_stream()

            #Réponse comment va Vision#
            elif "comment ça va vision" in p or "quoi de beau vision" in p:
                stream.stop_stream()
                speak("Je vais bien. Merci de poser la question. J\'attends juste une requête")
                p = ""
                stream.start_stream()

            #Réponse Heure#
            elif "il est quelle heure vision" in p:
                stream.stop_stream()
                DireLheure()
                p = ""
                stream.start_stream()

            #Réponse Date#
            elif "on est quelle date vision" in p or "on est quel jour vision" in p:
                stream.stop_stream()
                speak("Nous sommes le " + date_time)
                p = ""
                stream.start_stream()

            #Changer de bureau (se lance auto et ne reviens pas sur l'autre bureau(GROS BEUG))
                # elif "bureau droite" in p or "change de bureau à droite":
                #     stream.stop_stream()    
                #     keyboard.press_and_release("ctrl + windows + droite")
                #     p = ""
                #     stream.start_stream()

            #Change de fenêtre#
            elif "change de fenêtre vision" in p:
                stream.stop_stream()
                keyboard.press_and_release("alt + tab")
                p = ""
                stream.start_stream() 

            #Scan clavier#
            elif "commande clavier" in p:
                stream.stop_stream()
                rk = keyboard.record(until="shift")
                print(rk)
                p = ""
                stream.start_stream()

            #Ouvre Google#
            elif "ouvre google vision" in p or "montre moi google vision" in p:
                stream.stop_stream()
                speak("J'ouvre Google")
                webbrowser.open("www.google.com")
                p = ""
                stream.start_stream()

            #Ouvre Youtube#
            elif "ouvre youtube vision" in p or "montre-moi youtube" in p:
                stream.stop_stream()
                speak("J'ouvre Youtube")
                webbrowser.open("www.youtube.com")
                p = ""
                stream.start_stream()

            #Lié à youtube (Chaîne)
            elif "ouvre la chaîne de mastu" in p:
                stream.stop_stream()
                speak("j'ouvre la chaîne de mastu")
                webbrowser.open("www.youtube.com/@Mastu")
                p = ""
                stream.start_stream()

            #Fais trembler les murs vision#
            elif "fait trembler les murs vision" in p or "balance des basses vision" in p:
                stream.stop_stream()
                speak("J'ouvre un mix de rezz qui fracasse")
                webbrowser.open("https://www.youtube.com/watch?v=28R9VXI2Btw&t=1183s")
                p = ""
                stream.start_stream()

            #Ouvre Gmail#
            elif "ouvre gmail vision" in p or "montre-moi mes mails vision" in p or "ouvre gmail" in p:
                stream.stop_stream()
                speak("J'ouvre Gmail")
                gmail = "https://mail.google.com/mail/u/1/?pli=1#inbox" #A Tester
                webbrowser.open("https://mail.google.com/mail/u/0/#inbox")
                p = ""
                stream.start_stream()

            #Ouvre le Bloc-Notes#
            elif "ouvre le bloc-notes vision" in p :
                stream.stop_stream()
                speak("J'ouvre le Bloc Notes")
                os.startfile("C:\\WINDOWS\\system32\\notepad.exe")
                p = ""
                stream.start_stream()

            #Réponse Je t'aime vision#
            elif "je t'aime vision" in p :
                stream.stop_stream()
                speak("Moi aussi je vous aime !")
                p = ""
                stream.start_stream()

            #Dit une blague# (en anglais) =/
            elif "dis une blague vision" in p or "dis une blague" in p:
                stream.stop_stream()
                joke = pyjokes.get_joke()
                speak(joke)
                p = ""
                stream.start_stream()
            #Ouvre calculette
            elif "ouvre la calculette vision" in p:
                stream.stop_stream()
                speak("J'ouvre la calculette")
                os.startfile("Calculator\\dist\\Calculator\\Calculator.exe")
                p = ""
                stream.start_stream()
            #vérouille l'ordinateur (wind + L)
            elif " vérouille l'ordinateur vision" in p:
                stream.stop_stream()

                speak("Écran vérouillé monsieur")
            #######       Commande Jeux         ###############
            #Elite Dangerous Appontage(A tester)
            elif "demande l'appontage vision" in p or "demande la pontage vision" in p:
                stream.stop_stream()
                keyboard.press_and_release("& + e + e + d + space")
                speak("Appontage demandé")
                p = ""
                stream.start_stream()
                
                

####################################################################################################################################
# Début des opérations Vision 
############################################################################################################
if __name__ == '__main__':
    clear = lambda: os.system('cls')

    clear()
    notification.notify(title="Vision", message="Décollage de Vision. Pret à l'emploi", timeout=10, app_icon=(r"C:\\Users\\Dragonlord-PC3060\\Documents\\ProjetAIvosk\\ProjetAI\\jarvis.ico"))
    AccueilHote()
    while True:
        VisionAI()