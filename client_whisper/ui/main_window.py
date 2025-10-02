"""Interface principale de l'application de dictée vocale."""

import pyperclip
import keyboard
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt

from client_whisper.audio_manager import AudioRecorder
from client_whisper.ui.ui_components import DictationUI
from client_whisper.ui.managers.recording_manager import RecordingManager
from client_whisper.ui.managers.notification_manager import NotificationManager


class DictationApp(QWidget):
    """Application principale de dictée vocale, utilise une architecture modulaire."""
    
    def __init__(self, hotkey_handler):
        """Initialise l'application de dictée vocale
        
        Args:
            hotkey_handler: Gestionnaire des raccourcis clavier
        """
        super().__init__()
        
        # Configuration de base de la fenêtre
        self.setWindowTitle("Dictée vocale")
        self.setGeometry(100, 100, 380, 320)
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)  # Toujours au premier plan
        
        # Style global de l'application
        self.setStyleSheet("""
            QWidget {
                font-family: 'Segoe UI', Arial, sans-serif;
                background-color: #f5f5f7;
            }
            QLabel {
                color: #333;
            }
            QCheckBox {
                spacing: 8px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
            }
        """)
        
        # Composants principaux
        self.hotkey_handler = hotkey_handler
        self.audio_recorder = AudioRecorder()
        
        # Interface utilisateur
        self.ui = DictationUI(self)
        
        # Gestionnaires
        self.recording_manager = RecordingManager(self.ui, self.audio_recorder)
        
        # État de l'application
        self.recording = True
        
        # Connexion des signaux
        self.connect_signals()
    
    def connect_signals(self):
        """Connecte les événements de l'interface aux méthodes de l'application"""
        self.ui.pause_button.clicked.connect(self.toggle_pause)
        self.ui.stop_button.clicked.connect(self.stop_recording)
        self.ui.cancel_button.clicked.connect(self.cancel_recording)
        
    def start_recording(self):
        """Démarre l'enregistrement"""
        # Réinitialiser les variables
        self.recording = True
        
        # Activer les raccourcis
        self.hotkey_handler.setup_cancel_hotkey()
        self.hotkey_handler.setup_pause_hotkey()
        
        # Démarrer l'enregistrement
        self.recording_manager.start_recording()
        self.show()

    def toggle_pause(self):
        """Basculer entre pause et reprise"""
        self.recording = self.recording_manager.toggle_pause()

    def stop_recording(self):
        """Arrêter l'enregistrement et transcrire"""
        # Désactiver les raccourcis spéciaux
        self.hotkey_handler.remove_cancel_hotkey()
        self.hotkey_handler.remove_pause_hotkey()
        
        # Arrêter l'enregistrement
        self.recording_manager.stop_recording()
        
        # Transcription via le gestionnaire d'enregistrement
        texte = self.recording_manager.transcribe_recording()
        
        if texte:
            # Copier dans le presse-papier
            pyperclip.copy(texte)
            
            # Si auto-paste est activé, simuler Ctrl+V
            if self.ui.is_autopaste_enabled():
                keyboard.press_and_release('ctrl+v')
                notification_message = "Texte collé automatiquement"
                console_message = "📝 Texte transcrit et collé automatiquement"
            else:
                notification_message = "Texte copié dans le presse-papier (Ctrl+V pour coller)"
                console_message = "📝 Texte copié dans le presse-papier"

            # Notification
            # NotificationManager.show_notification("Transcription terminée", notification_message)
            print(console_message)
        
        # Réinitialiser l'état et cacher la fenêtre
        self.recording = True
        self.hide()
        
    def cancel_recording(self):
        """Annuler l'enregistrement en cours"""
        # Désactiver les raccourcis spéciaux
        self.hotkey_handler.remove_cancel_hotkey()
        self.hotkey_handler.remove_pause_hotkey()
        
        # Arrêter l'enregistrement
        self.recording_manager.stop_recording()
        
        print("❌ Enregistrement annulé")
        NotificationManager.show_notification("Enregistrement annulé", "L'enregistrement a été annulé", 2000)
                
        # Cacher la fenêtre
        self.hide()
        self.recording = True
        
    def closeEvent(self, event):
        """Gestion de la fermeture de la fenêtre"""
        # Désactiver les raccourcis spéciaux
        self.hotkey_handler.remove_cancel_hotkey()
        self.hotkey_handler.remove_pause_hotkey()
        
        # Arrêter l'enregistrement
        self.recording_manager.stop_recording()
        
        event.accept()