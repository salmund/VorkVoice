"""Configuration globale de l'application de dictée vocale."""

# Fichiers audio
FICHIER_AUDIO = "record.wav"
FICHIER_AUDIO_PARTIEL = "partial_record.wav"

# Configuration audio
SAMPLERATE = 16000
CANAL = 1

# API
SERVER_URL = "http://127.0.0.1:8000/transcribe/"

# Raccourcis clavier
HOTKEY = "²"  # Raccourci global pour démarrer/arrêter
PAUSE_HOTKEY = "shift+²"  # Raccourci pour pause/reprendre
CANCEL_HOTKEY = "esc"  # Raccourci pour annuler la transcription
TRANSCRIBE_PARTIAL_HOTKEY = "ctrl+shift+²"  # Raccourci pour transcription partielle