# VorkVoice 🎙️

VorkVoice est une application de dictée vocale de bureau conçue pour offrir une transcription en temps réel de haute qualité, spécifiquement optimisée pour la langue française. Elle s'appuie sur un modèle Whisper fine-tuné pour garantir une précision et une réactivité exceptionnelles, le tout en fonctionnant localement sur votre machine.

## ✨ Fonctionnalités

- **Transcription de haute qualité** : Utilise un modèle Whisper fine-tuné pour le français, assurant une retranscription précise de votre voix.
- **Fonctionnement local** : L'ensemble du processus, de l'enregistrement à la transcription, s'exécute sur votre ordinateur. Vos données restent privées.
- **Intégration au flux de travail** :
    - **Copier-coller automatique** : Le texte transcrit peut être automatiquement collé dans l'application active.
    - **Copie dans le presse-papiers** : Si le collage automatique est désactivé, le texte est copié dans le presse-papiers pour une utilisation manuelle.
- **Contrôle par raccourcis clavier** :
    - Démarrez, mettez en pause, reprenez et arrêtez l'enregistrement sans quitter votre application en cours.
- **Interface discrète** : Une petite fenêtre s'affiche pendant l'enregistrement, vous donnant un contrôle visuel sur le processus.

## 🛠️ Architecture

VorkVoice est basé sur une architecture client-serveur simple :

1.  **Le Serveur (`serveur_whisper.py`)** :
    - C'est le cœur de l'application. Il charge le modèle de reconnaissance vocale Whisper.
    - Il expose une API simple qui attend un fichier audio.
    - Lorsqu'il reçoit un fichier, il le traite avec le modèle et renvoie le texte transcrit.

2.  **Le Client (`client_whisper/`)** :
    - C'est l'application de bureau avec laquelle vous interagissez, développée avec PyQt6.
    - Il gère l'enregistrement audio à partir de votre microphone.
    - Il communique avec le serveur en lui envoyant le fichier audio enregistré.
    - Il reçoit le texte transcrit et effectue les actions correspondantes (copier-coller, notification).
    - Il gère les raccourcis clavier globaux pour une utilisation transparente.

## 🚀 Démarrage

1.  **Lancer le serveur** :
    Exécutez le script `serveur_whisper.py`. Un terminal s'ouvrira, indiquant que le serveur est prêt à recevoir des requêtes.

    ```bash
    python serveur_whisper.py
    ```

2.  **Lancer le client** :
    Exécutez le script `main.py` dans le dossier `client_whisper`.

    ```bash
    python client_whisper/main.py
    ```
    L'icône de l'application apparaîtra dans la barre des tâches.

3.  **Utilisation** :
    - Appuyez sur le raccourci clavier configuré pour démarrer l'enregistrement.
    - Parlez.
    - Appuyez à nouveau sur le raccourci pour arrêter. Le texte apparaîtra là où vous écrivez.

## ⚙️ Configuration

La configuration (raccourcis, comportement du collage, etc.) peut être ajustée directement dans les fichiers de configuration du client.
