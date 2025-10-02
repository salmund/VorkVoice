"""Gestion de la transcription avec l'API."""

import requests
from client_whisper.config import SERVER_URL, FICHIER_AUDIO, FICHIER_AUDIO_PARTIEL

class TranscriptionService:
    @staticmethod
    def transcribe_audio(partial=False):
        """Envoyer le fichier audio au serveur et récupérer la transcription."""
        filename = FICHIER_AUDIO_PARTIEL if partial else FICHIER_AUDIO
        
        try:
            with open(filename, "rb") as f:
                response = requests.post(SERVER_URL, files={"audio": f})
            response.raise_for_status()
            return response.json().get("text", "")
        except requests.exceptions.RequestException as e:
            error_message = f"⚠ Erreur serveur : {e}"
            print(error_message)
            return error_message