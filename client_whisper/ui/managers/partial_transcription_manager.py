"""Gestionnaire de transcription partielle pour l'application de dictée vocale."""

from client_whisper.ui.partial_dialog import PartialTranscriptionDialog
from client_whisper.transcription import TranscriptionService

class PartialTranscriptionManager:
    """Gère la fonctionnalité de transcription partielle"""
    
    def __init__(self, ui_handler, audio_recorder):
        """Initialise le gestionnaire de transcription partielle
        
        Args:
            ui_handler: L'instance de DictationUI
            audio_recorder: L'instance d'AudioRecorder
        """
        self.ui = ui_handler
        self.audio_recorder = audio_recorder
        self.partial_dialog = None
        self.transcription_text = ""
        self.partial_mode_active = False
        
    def handle_partial_transcribe(self, recording_state):
        """Gère la transcription partielle
        
        Args:
            recording_state: Indique si l'enregistrement est actuellement actif
            
        Returns:
            bool: Nouvel état d'enregistrement
        """
        if recording_state:
            # Nous sommes en train d'enregistrer, nous allons mettre en pause et transcrire
            new_state = False
            self.audio_recorder.recording = False
            self.ui.update_pause_button(True)
            self.ui.update_status_label("🔄 Transcription partielle en cours...")
            
            # Sauvegarder dans un fichier partiel
            if not self.audio_recorder.save_to_file(partial=True):
                self.ui.update_status_label("⏸ En pause...")
                return new_state
                
            # Transcription via le service
            nouveau_texte = TranscriptionService.transcribe_audio(partial=True)
                
            # Créer la fenêtre pop-up si elle n'existe pas encore
            if self.partial_dialog is None or not self.partial_dialog.isVisible():
                self.partial_dialog = PartialTranscriptionDialog(None)
                self.partial_mode_active = True
                
                # Premier segment
                self.transcription_text = nouveau_texte
            else:
                # Récupérer le texte modifié par l'utilisateur
                self.transcription_text = self.partial_dialog.get_text()
                
                # Ajouter un nouveau paragraphe
                self.transcription_text += "\n\n" + nouveau_texte
            
            # Mettre à jour le texte dans la fenêtre
            self.partial_dialog.set_text(self.transcription_text)
            self.partial_dialog.update_status("paused")
            self.partial_dialog.show()
            self.ui.update_status_label("⏸ En pause...")
                
        else:
            # Nous sommes actuellement en pause, reprendre l'enregistrement
            new_state = True
            self.audio_recorder.recording = True
            self.ui.update_pause_button(False)
            self.ui.update_status_label("🗣 Enregistrement en cours...")
            
            # Mettre à jour l'état de la fenêtre pop-up si elle existe
            if self.partial_dialog is not None and self.partial_dialog.isVisible():
                self.partial_dialog.update_status("recording")
                
        return new_state
                
    def cleanup_partial_mode(self):
        """Nettoie les ressources de la transcription partielle"""
        if self.partial_dialog is not None:
            self.partial_dialog.close()
            self.partial_dialog = None
        self.transcription_text = ""
        self.partial_mode_active = False
        
    def is_partial_mode_active(self):
        """Vérifie si le mode transcription partielle est actif"""
        return self.partial_mode_active and self.partial_dialog is not None and self.partial_dialog.isVisible()
        
    def get_partial_text(self):
        """Récupère le texte de la transcription partielle"""
        if self.partial_dialog is not None:
            return self.partial_dialog.get_text()
        return ""