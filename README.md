# ProjetAI - jarvis Assistant Vocal

Assistant vocal intelligent en Python utilisant la reconnaissance vocale Whisper de Hugging Face pour contrôler votre ordinateur via commandes vocales en français.

## 📋 Description

jarvis est un assistant vocal qui utilise l'intelligence artificielle pour reconnaître vos commandes vocales et exécuter diverses tâches sur votre ordinateur Windows. Il utilise le modèle Whisper-base de Hugging Face pour la reconnaissance vocale et pyttsx3 pour la synthèse vocale.

## 🛠️ Technologies Utilisées

- **Python 3.7+**
- **Hugging Face Transformers** - Modèle Whisper-base pour la reconnaissance vocale
- **PyTorch** - Framework d'apprentissage automatique
- **PyAudio** - Capture audio depuis le microphone
- **pyttsx3** - Synthèse vocale (TTS)
- **keyboard** - Contrôle du clavier
- **plyer** - Notifications système
- **pyjokes** - Génération de blagues

## 📦 Prérequis

- Python 3.7 ou supérieur
- pip (gestionnaire de paquets Python)
- Microphone fonctionnel
- Windows (pour pyttsx3 avec SAPI5)
- Connexion Internet (pour télécharger le modèle Whisper au premier lancement)

## 🚀 Installation

### 1. Télécharger le projet

```bash
# Option 1 : Cloner le dépôt Git
git clone <votre-url-depot>

# Option 2 : Télécharger le ZIP depuis le dépôt
```

### 2. Installer Python et pip

Assurez-vous d'avoir Python installé. Vérifiez avec :
```bash
python --version
pip --version
```

### 3. Installer les dépendances

Ouvrez un terminal (CMD ou PowerShell) dans le dossier du projet et exécutez :

```bash
pip install -r requirements.txt
```

**Note importante pour PyAudio :** Si l'installation de PyAudio échoue, vous pouvez :
- Télécharger le wheel depuis [pythonlibs](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio)
- Ou utiliser : `pip install pipwin` puis `pipwin install pyaudio`

## ▶️ Utilisation

### Lancer jarvis

Dans le terminal, exécutez :

```bash
python JarvisAIVosk.py
```

**Note :** Le nom du fichier est `JarvisAIVosk.py` (avec un V majuscule).

### Premier lancement

Au premier lancement, le modèle Whisper-base sera automatiquement téléchargé (environ 290 Mo). Cela peut prendre quelques minutes selon votre connexion.

### Arrêter jarvis

- **Méthode vocale :** Dites "stop jarvis" ou "éteins toi jarvis"
- **Méthode clavier :** Appuyez sur `Ctrl+C` dans le terminal

## 🎤 Commandes Disponibles

### Commandes de base

| Commande | Description |
|----------|-------------|
| `stop jarvis` / `éteins toi jarvis` | Arrête l'assistant |
| `attends jarvis` | Met en pause (appuyez sur Espace pour reprendre) |
| `comment t'appelles-tu` / `quel est ton nom` / `qui es-tu` | Présentation de jarvis |
| `comment ça va jarvis` / `quoi de beau jarvis` | Demande l'état de jarvis |
| `je t'aime jarvis` | Réponse amicale |

### Informations

| Commande | Description |
|----------|-------------|
| `il est quelle heure jarvis` | Affiche l'heure actuelle |
| `on est quelle date jarvis` / `on est quel jour jarvis` | Affiche la date actuelle |

### Navigation et fenêtres

| Commande | Description |
|----------|-------------|
| `change de fenêtre jarvis` | Change de fenêtre active (Alt+Tab) |
| `commande clavier jarvis` | Enregistre les touches jusqu'à Shift |

### Applications web

| Commande | Description |
|----------|-------------|
| `ouvre google jarvis` / `montre moi google jarvis` | Ouvre Google dans le navigateur |
| `ouvre youtube jarvis` / `montre-moi youtube` | Ouvre YouTube |
| `ouvre la chaîne de mastu` | Ouvre la chaîne YouTube de Mastu |
| `ouvre gmail jarvis` / `montre-moi mes mails jarvis` | Ouvre Gmail |
| `fait trembler les murs jarvis` / `balance des basses jarvis` | Ouvre un mix musical sur YouTube |

### Applications système

| Commande | Description |
|----------|-------------|
| `ouvre la boîte noire` | Ouvre Cmder (terminal) |
| `ouvre le bloc-notes jarvis` | Ouvre le Bloc-Notes Windows |
| `ouvre la calculette jarvis` | Ouvre la calculatrice |
| `vérouille l'ordinateur jarvis` | Verrouille l'écran (Windows+L) |

### Divertissement

| Commande | Description |
|----------|-------------|
| `dis une blague jarvis` / `dis une blague` | Raconte une blague (en anglais) |

### Commandes de jeu

| Commande | Description |
|----------|-------------|
| `demande l'appontage jarvis` / `demande la pontage jarvis` | Commande pour Elite Dangerous |

## ⚙️ Configuration

### Modifier la voix

Dans le fichier `JarvisAIVosk.py`, ligne 26-27 :
```python
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  # 0 = Masculin, 1 = Féminin
```

### Modifier le débit de parole

Ligne 22 :
```python
engine.setProperty('rate', 220)  # Ajustez la valeur (défaut: 220)
```

### Modifier le volume

Ligne 24 :
```python
engine.setProperty('volume', 1.2)  # Ajustez entre 0.0 et 1.0
```

### Modifier la durée d'enregistrement

Ligne 99 :
```python
buffer_duration = 3  # Durée en secondes avant transcription
```

## 🔧 Dépannage

### Le microphone n'est pas détecté
- Vérifiez que votre microphone est connecté et activé
- Vérifiez les paramètres de confidentialité Windows pour autoriser l'accès au microphone

### Erreur lors du téléchargement du modèle
- Vérifiez votre connexion Internet
- Le modèle sera téléchargé dans le cache Hugging Face (généralement `~/.cache/huggingface/`)

### PyAudio ne s'installe pas
- Installez Visual C++ Build Tools
- Ou utilisez `pipwin install pyaudio`

### Le script ne répond pas immédiatement à Ctrl+C
- Attendez la fin de la transcription en cours (quelques secondes)
- Appuyez une deuxième fois sur Ctrl+C si nécessaire

## 📝 Notes

- Le modèle Whisper-base est optimisé pour le français mais peut reconnaître d'autres langues
- La transcription se fait toutes les 3 secondes par défaut
- Le script utilise le GPU si disponible, sinon le CPU
- Certaines commandes nécessitent des chemins spécifiques (ex: Cmder, calculatrice) - modifiez-les dans le code si nécessaire

## 👤 Auteur

Créé par Dragonlord07

## 📄 Licence

Aucune Ma Gueule !

## 🔮 Améliorations futures

- [ ] Remplacement de pyttsx3 par ElevenLabs pour une voix plus naturelle
- [ ] Implémentation de l'historique des commandes
- [ ] Ajout d'un wake word (mot d'activation)
- [ ] Support multi-langues amélioré
- [ ] Interface graphique
