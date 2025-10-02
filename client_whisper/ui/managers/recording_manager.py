"""Gestionnaire d'enregistrement audio pour l'application de dictée vocale."""

from PyQt6.QtCore import QTimer
from client_whisper.transcription import TranscriptionService

class RecordingManager:
    """Gère l'état et le processus d'enregistrement audio"""
    
    def __init__(self, ui_handler, audio_recorder):
        """Initialise le gestionnaire d'enregistrement
        
        Args:
            ui_handler: L'instance de DictationUI
            audio_recorder: L'instance d'AudioRecorder
        """
        self.ui = ui_handler
        self.audio_recorder = audio_recorder
        self.recording = True
        self.time_elapsed = 0
        
        # Timer pour suivre le temps d'enregistrement
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)
        
    def start_recording(self):
        """Démarre l'enregistrement audio"""
        self.time_elapsed = 0
        self.recording = True
        
        # Mettre à jour l'interface
        self.ui.update_pause_button(False)
        self.ui.update_status_label("🗣 Enregistrement en cours...")
        self.ui.timer_label.setText("⏳ Temps : 0s")
        
        # Démarrer le timer et l'enregistreur
        self.timer.start(1000)
        self.audio_recorder.start()
        
    def stop_recording(self):
        """Arrête l'enregistrement et nettoie les ressources"""
        self.audio_recorder.stop()
        self.timer.stop()
        
    def toggle_pause(self):
        """Bascule entre pause et reprise"""
        if self.recording:
            # Mettre en pause
            self.recording = False
            self.audio_recorder.recording = False
            self.ui.update_pause_button(True)
            self.ui.update_status_label("⏸ En pause...")
        else:
            # Reprendre
            self.recording = True
            self.audio_recorder.recording = True
            self.ui.update_pause_button(False)
            self.ui.update_status_label("🗣 Enregistrement en cours...")
            
        return self.recording
        
    def update_time(self):
        """Met à jour le compteur de temps"""
        if self.recording:
            self.time_elapsed += 1
            mins, secs = divmod(self.time_elapsed, 60)
            self.ui.update_timer_label(mins, secs)
            
    def transcribe_recording(self):
        """Transcrit l'enregistrement complet"""
        self.ui.update_status_label("🔄 Transcription en cours...")
        
        if self.audio_recorder.save_to_file():
            # Obtenir la transcription
            texte = TranscriptionService.transcribe_audio()
            return texte
        return None