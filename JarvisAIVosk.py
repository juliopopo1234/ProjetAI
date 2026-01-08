# Reconnaissance vocale avec Hugging Face Whisper-base
import pyaudio
import os
import pyttsx3
#A remplacer par ElevenLabs 
#voix de jarvis
import datetime
import time
import webbrowser
from plyer import notification
import keyboard
import json
import pyjokes
import numpy as np
from transformers import WhisperProcessor, WhisperForConditionalGeneration
import torch


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
# définition de la parole de jarvisIA
def speak(audio):
    engine.say(audio)
    print('jarvis IA :' + audio)
    engine.runAndWait() 
# Initialisation du modèle Whisper-base de Hugging Face
print("Chargement du modèle Whisper-base...")
processor = WhisperProcessor.from_pretrained("openai/whisper-base")
model_whisper = WhisperForConditionalGeneration.from_pretrained("openai/whisper-base")
# Utiliser le GPU si disponible, sinon CPU
device = "cuda" if torch.cuda.is_available() else "cpu"
model_whisper.to(device)
print(f"Modèle Whisper chargé sur {device}")

###################################################################
# Fonctionnalité de jarvisIA
##################################################################
def DireLheure():
    speak("Il est "+heure+":"+min)

def AccueilHote():
    if (int(heure) > 6) and (int(heure) < 17):
        speak(f"Bonjour Monsieur!")
    elif (int(heure) > 18) and (int(heure) < 24):
        speak(f"Bonsoir Monsieur.")
    DireLheure()


def transcribe_audio(audio_data, sample_rate=16000):
    """Transcrit l'audio en texte avec Whisper"""
    try:
        # Convertir les données audio en numpy array
        audio_np = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32) / 32768.0
        
        # Traiter l'audio avec le processeur Whisper
        inputs = processor(audio_np, sampling_rate=sample_rate, return_tensors="pt")
        inputs = {k: v.to(device) for k, v in inputs.items()}
        
        # Générer la transcription
        with torch.no_grad():
            generated_ids = model_whisper.generate(**inputs, language="fr", task="transcribe")
        
        # Décoder la transcription
        transcription = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
        return transcription.strip().lower()
    except Exception as e:
        print(f"Erreur lors de la transcription: {e}")
        return ""

def jarvisAI():
    print("")
    print("Je vous écoute ...")
    print("Appuyez sur Ctrl+C pour arrêter")
    print("")
    mic = None
    stream = None
    try:
        mic = pyaudio.PyAudio()
        # Configuration audio pour Whisper (16kHz, mono)
        sample_rate = 16000
        chunk_size = 8000
        stream = mic.open(format=pyaudio.paInt16, channels=1, rate=sample_rate, input=True, frames_per_buffer=chunk_size)
        stream.start_stream()
        
        p = " "
        historique = ""
        audio_buffer = []
        buffer_duration = 3  # Enregistrer 3 secondes d'audio avant de transcrire
        frames_per_second = sample_rate // chunk_size
        
        while True:
            try:
                data = stream.read(chunk_size, exception_on_overflow=False)
                if len(data) == 0:
                    break
                
                audio_buffer.append(data)
                
                # Transcrire toutes les 3 secondes (ou quand le buffer est plein)
                if len(audio_buffer) >= buffer_duration * frames_per_second:
                    # Concaténer les frames audio
                    audio_data = b''.join(audio_buffer)
                    
                    # Transcrire avec Whisper
                    p = transcribe_audio(audio_data, sample_rate)
                    
                    if p and len(p) > 0:
                        print(f"Vous avez dit: {p}")
                        # Ajouter à l'historique
                        historique += p + " | "
                        
                        #Fonction stop jarvisIA#
                        if "stop jarvis" in p or "éteins toi jarvis" in p:
                            if (int(heure) >= 6) and (int(heure) <= 17):
                                speak("Merci pour votre temps Monsieur, passez une bonne journée !")
                                stream.stop_stream()
                                stream.close()
                                mic.terminate()
                                break
                            elif (int(heure) >= 18) and (int(heure) < 24):
                                speak("Merci pour votre temps Monsieur, passez une bonne soirée !")
                                stream.stop_stream()
                                stream.close()
                                mic.terminate()
                                break
                            else :
                                speak("Merci pour votre temps Monsieur, passez une bonne nuit.")
                                stream.stop_stream()
                                stream.close()
                                mic.terminate()
                                break

                        #Fonction attente#
                        elif "attends jarvis" in p:
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
                            speak('Je me nomme jarvis, Je suis un assistant virtuel créer par Timothé Iskander pour l\'assister dans plusieurs tâches')
                            p = ""
                            stream.start_stream()

                        #Réponse comment va jarvis#
                        elif "comment ça va jarvis" in p or "quoi de beau jarvis" in p:
                            stream.stop_stream()
                            speak("Je vais bien. Merci de poser la question. J\'attends juste une requête")
                            p = ""
                            stream.start_stream()

                        #Réponse Heure#
                        elif "il est quelle heure jarvis" in p:
                            stream.stop_stream()
                            DireLheure()
                            p = ""
                            stream.start_stream()

                        #Réponse Date#
                        elif "on est quelle date jarvis" in p or "on est quel jour jarvis" in p:
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
                        elif "change de fenêtre jarvis" in p:
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
                        elif "ouvre google jarvis" in p or "montre moi google jarvis" in p:
                            stream.stop_stream()
                            speak("J'ouvre Google")
                            webbrowser.open("www.google.com")
                            p = ""
                            stream.start_stream()

                        #Ouvre Youtube#
                        elif "ouvre youtube jarvis" in p or "montre-moi youtube" in p:
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

                        #Fais trembler les murs jarvis#
                        elif "fait trembler les murs jarvis" in p or "balance des basses jarvis" in p:
                            stream.stop_stream()
                            speak("J'ouvre un mix de rezz qui fracasse")
                            webbrowser.open("https://www.youtube.com/watch?v=28R9VXI2Btw&t=1183s")
                            p = ""
                            stream.start_stream()

                        #Ouvre Gmail#
                        elif "ouvre gmail jarvis" in p or "montre-moi mes mails jarvis" in p or "ouvre gmail" in p:
                            stream.stop_stream()
                            speak("J'ouvre Gmail")
                            gmail = "https://mail.google.com/mail/u/1/?pli=1#inbox" #A Tester
                            webbrowser.open("https://mail.google.com/mail/u/0/#inbox")
                            p = ""
                            stream.start_stream()

                        #Ouvre le Bloc-Notes#
                        elif "ouvre le bloc-notes jarvis" in p :
                            stream.stop_stream()
                            speak("J'ouvre le Bloc Notes")
                            os.startfile("C:\\WINDOWS\\system32\\notepad.exe")
                            p = ""
                            stream.start_stream()

                        #Réponse Je t'aime jarvis#
                        elif "je t'aime jarvis" in p :
                            stream.stop_stream()
                            speak("Moi aussi je vous aime !")
                            p = ""
                            stream.start_stream()

                        #Dit une blague# (en anglais) =/
                        elif "dis une blague jarvis" in p or "dis une blague" in p:
                            stream.stop_stream()
                            joke = pyjokes.get_joke()
                            speak(joke)
                            p = ""
                            stream.start_stream()
                        #Ouvre calculette
                        elif "ouvre la calculette jarvis" in p:
                            stream.stop_stream()
                            speak("J'ouvre la calculette")
                            os.startfile("Calculator\\dist\\Calculator\\Calculator.exe")
                            p = ""
                            stream.start_stream()
                        #vérouille l'ordinateur (wind + L)
                        elif " vérouille l'ordinateur jarvis" in p:
                            stream.stop_stream()
                            speak("Écran vérouillé monsieur")
                        #######       Commande Jeux         ###############
                        #Elite Dangerous Appontage(A tester)
                        elif "demande l'appontage jarvis" in p or "demande la pontage jarvis" in p:
                            stream.stop_stream()
                            keyboard.press_and_release("& + e + e + d + space")
                            speak("Appontage demandé")
                            p = ""
                            stream.start_stream()
                    
                    # Réinitialiser le buffer
                    audio_buffer = []
            
            except KeyboardInterrupt:
                raise  # Remonter l'exception pour qu'elle soit gérée au niveau supérieur
            except Exception as e:
                print(f"Erreur dans la boucle principale: {e}")
                # Continuer la boucle même en cas d'erreur
                time.sleep(0.1)
    
    except KeyboardInterrupt:
        print("\n\nArrêt de jarvis...")
        speak("Au revoir Monsieur")
    except Exception as e:
        print(f"\nErreur fatale: {e}")
    finally:
        # Nettoyer les ressources audio de manière sécurisée
        if stream is not None:
            try:
                if stream.is_active():
                    stream.stop_stream()
                stream.close()
            except:
                pass
        if mic is not None:
            try:
                mic.terminate()
            except:
                pass
        print("Ressources libérées. jarvis s'est arrêté.")

####################################################################################################################################
# Début des opérations jarvis 
############################################################################################################
if __name__ == '__main__':
    try:
        clear = lambda: os.system('cls')

        clear()
        notification.notify(title="jarvis", message="Décollage de jarvis. Pret à l'emploi", timeout=10, app_icon=(r"jarvis.ico"))
        AccueilHote()
        jarvisAI()  # jarvisAI gère maintenant sa propre boucle et son arrêt
    except KeyboardInterrupt:
        print("\n\nArrêt demandé par l'utilisateur.")
    except Exception as e:
        print(f"\nErreur critique: {e}")
    finally:
        print("\nProgramme terminé.")