# VorkVoice 🎙️

VorkVoice est une application de dictée vocale de bureau conçue pour offrir une transcription rapide et précise directement sur votre ordinateur. Elle utilise une architecture client-serveur locale pour exploiter la puissance des modèles Whisper tout en restant réactive et intégrée à votre environnement de travail.

L'application se compose de deux parties principales :
1.  **Un serveur FastAPI local** qui charge un modèle Whisper optimisé pour des performances maximales.
2.  **Une application cliente en PyQt6** qui capture l'audio, communique avec le serveur et gère l'interaction avec l'utilisateur.

## ✨ Fonctionnalités

- **Transcription Haute Performance** : Utilise le modèle `whisper-large-v3` en français, optimisé avec `ctranslate2` et `float16` pour une exécution rapide sur GPU (CUDA).
- **Serveur Local** : Pas de dépendance à une API externe. Tout tourne sur votre machine, garantissant confidentialité et rapidité.
- **Interface Intuitive** : Une petite fenêtre de contrôle permet de démarrer, mettre en pause, reprendre et annuler l'enregistrement.
- **Raccourcis Clavier** : Contrôlez l'enregistrement sans quitter votre application en cours.
- **Dictionnaire Personnel** : Créez des remplacements personnalisés (ex: "Maya" -> "Maïa") pour corriger automatiquement les transcriptions.
- **Auto-Collage (Optionnel)** : Le texte transcrit peut être automatiquement collé dans l'application active.
- **Hot-Reload pour le Développement** : Un script de rechargement à chaud (`main.py`) redémarre automatiquement le client ou le serveur lors de la modification des fichiers sources, facilitant le développement.

## 🛠️ Stack Technique

- **Client (Frontend)** : Python, PyQt6
- **Serveur (Backend)** : Python, FastAPI, Uvicorn
- **Modèle de Transcription** : `faster-whisper` avec le modèle `whisper-large-v3-french`
- **Dépendances Clés** : `torch`, `pyperclip`, `keyboard`, `watchdog`

## 🚀 Installation

### Prérequis

- **Python 3.9+**
- **Un GPU NVIDIA** avec CUDA installé est fortement recommandé pour des performances optimales.
- **Git**

### 1. Cloner le Dépôt

```bash
git clone <URL_DU_DEPOT>
cd <NOM_DU_DOSSIER>
```

### 2. Créer un Environnement Virtuel

Il est recommandé d'utiliser un environnement virtuel pour isoler les dépendances du projet.

```bash
python -m venv .venv
# Activer l'environnement
# Sur Windows (PowerShell)
.venv\Scripts\Activate.ps1
# Sur macOS/Linux
source .venv/bin/activate
```

### 3. Installer les Dépendances

Installez toutes les bibliothèques nécessaires avec le fichier `requirements.txt`.

```bash
pip install -r requirements.txt
```
*(Note : Si `requirements.txt` n'existe pas, vous pouvez l'installer manuellement : `pip install PyQt6 fastapi uvicorn "faster-whisper" torch --extra-index-url https://download.pytorch.org/whl/cu118 watchdog pyperclip keyboard`)*

### 4. Télécharger le Modèle Whisper

L'application est configurée pour utiliser une version optimisée de `whisper-large-v3`.

1.  Vous devez télécharger le modèle converti au format `ctranslate2`. Vous pouvez suivre les instructions de conversion de `faster-whisper` ou trouver des modèles pré-convertis sur le Hugging Face Hub.
2.  Placez les fichiers du modèle dans un dossier accessible.
3.  Mettez à jour le chemin dans `serveur_whisper.py` pour pointer vers votre modèle :

    ```python
    # Dans serveur_whisper.py
    model = WhisperModel(r"C:\chemin\vers\votre\modele\whisper-large-v3-french\ctranslate2", device="cuda", compute_type="float16")
    ```

## 🏃‍♂️ Utilisation

### Pour le Développement (avec Hot-Reload)

Le point d'entrée `main.py` est configuré pour lancer à la fois le serveur et le client, et pour les recharger automatiquement lorsque vous modifiez le code.

1.  Assurez-vous que votre environnement virtuel est activé.
2.  Lancez le script `main.py` :

    ```bash
    python main.py
    ```

Le script démarrera le serveur Whisper en arrière-plan, puis l'application cliente. Toute modification d'un fichier `.py` rechargera la partie concernée.

### En Production (Lancement Manuel)

Si vous n'avez pas besoin du rechargement à chaud, vous pouvez lancer le serveur et le client séparément.

1.  **Terminal 1 : Lancer le serveur**
    ```bash
    python serveur_whisper.py
    ```

2.  **Terminal 2 : Lancer le client**
    ```bash
    python dictee_vocale.py
    ```

### Comment ça marche ?

1.  Utilisez le raccourci clavier (configurable dans `client_whisper/config.py`) pour démarrer un enregistrement.
2.  La fenêtre de l'application apparaît. Parlez.
3.  Utilisez les boutons ou les raccourcis pour mettre en pause, arrêter ou annuler.
4.  Lorsque vous arrêtez, l'audio est envoyé au serveur local, transcrit, et le texte résultant est copié dans votre presse-papiers.

## 📂 Structure du Projet

```
.
├── main.py                 # Point d'entrée pour le dev (hot-reload)
├── serveur_whisper.py      # Serveur FastAPI pour la transcription
├── dictee_vocale.py        # Point d'entrée de l'application client
├── mappings.py             # Mappings de remplacement par défaut
├── client_whisper/         # Code source de l'application cliente
│   ├── main.py             # Logique principale du client
│   ├── audio_manager.py    # Gestion de l'enregistrement audio
│   ├── config.py           # Fichier de configuration (raccourcis, etc.)
│   ├── hotkeys.py          # Gestion des raccourcis clavier globaux
│   ├── transcription.py    # Service pour communiquer avec le serveur
│   ├── user_mappings.py    # Gestion du dictionnaire personnel
│   └── ui/                 # Modules de l'interface utilisateur (PyQt6)
│       ├── main_window.py
│       ├── settings_dialog.py
│       └── ...
└── README.md               # Ce fichier
```
