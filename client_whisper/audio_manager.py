"""Gestion de l'enregistrement et du traitement audio."""

import numpy as np
import sounddevice as sd
import wave
from client_whisper.config import SAMPLERATE, CANAL, FICHIER_AUDIO, FICHIER_AUDIO_PARTIEL

class AudioRecorder:
    def __init__(self):
        self.recording = False
        self.audio_data = []
        self.stream = None
        
    def start(self):
        """Démarrer l'enregistrement audio."""
        # Réinitialiser les variables
        self.audio_data = []
        self.recording = True
        
        # Démarrer le stream
        self.stream = sd.InputStream(
            samplerate=SAMPLERATE, 
            channels=CANAL,
            dtype=np.int16, 
            callback=self.audio_callback
        )
        self.stream.start()
        
    def stop(self):
        """Arrêter l'enregistrement audio."""
        if self.stream is not None:
            try:
                self.stream.stop()
                self.stream.close()
                self.stream = None
            except Exception as e:
                print(f"Erreur lors de l'arrêt du stream: {e}")
    
    def audio_callback(self, indata, frames, time, status):
        """Callback pour récupérer les données audio."""
        if self.recording:
            self.audio_data.append(indata.copy())
            
    def save_to_file(self, partial=False):
        """Enregistrer les données audio dans un fichier WAV."""
        if not self.audio_data:
            return False
            
        try:
            filename = FICHIER_AUDIO_PARTIEL if partial else FICHIER_AUDIO
            full_audio = np.concatenate(self.audio_data, axis=0)
            with wave.open(filename, 'wb') as wf:
                wf.setnchannels(CANAL)
                wf.setsampwidth(2)
                wf.setframerate(SAMPLERATE)
                wf.writeframes(full_audio.tobytes())
            
            # Optionnel: effacer les données si c'est une transcription partielle
            if partial:
                self.audio_data = []
                
            return True
                
        except Exception as e:
            print(f"Erreur lors de la sauvegarde audio: {e}")
            return False