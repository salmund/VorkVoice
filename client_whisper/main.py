"""Point d'entrée principal de l'application de dictée vocale."""

import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QObject

from client_whisper.hotkeys import HotkeyHandler
from client_whisper.ui.main_window import DictationApp
from client_whisper.config import HOTKEY, PAUSE_HOTKEY, TRANSCRIBE_PARTIAL_HOTKEY, CANCEL_HOTKEY

class DictationManager(QObject):
    def __init__(self):
        super().__init__()
        self.app = None
        self.dictation_window = None
        self.hotkey_handler = None
        
    def initialize(self):
        # Créer l'application Qt
        self.app = QApplication(sys.argv)
        self.app.setQuitOnLastWindowClosed(False)
        
        # Créer le gestionnaire de raccourcis
        self.hotkey_handler = HotkeyHandler()
        self.hotkey_handler.toggle_signal.connect(self.toggle_dictation)
        self.hotkey_handler.pause_signal.connect(self.toggle_pause)
        self.hotkey_handler.cancel_signal.connect(self.cancel_dictation)
        self.hotkey_handler.partial_transcribe_signal.connect(self.partial_transcribe)
        self.hotkey_handler.setup_hotkey()
        
        # Créer la fenêtre de dictée (mais ne pas l'afficher)
        self.dictation_window = DictationApp(self.hotkey_handler)
        
        print(f"🎤 Application prête! Appuyez sur {HOTKEY} pour démarrer/arrêter l'enregistrement.")
        print(f"👉 {PAUSE_HOTKEY} : Pause/Reprendre pendant l'enregistrement")
        print(f"👉 {TRANSCRIBE_PARTIAL_HOTKEY} : Transcription partielle (mode interrupteur)")
        print(f"👉 {CANCEL_HOTKEY} : Annuler l'enregistrement en cours")
        
        return self.app.exec()
        
    def toggle_dictation(self):
        """Démarre ou arrête l'enregistrement en fonction de l'état actuel"""
        if self.dictation_window.isVisible():
            # Si la fenêtre est visible, arrêter l'enregistrement
            self.dictation_window.stop_recording()
        else:
            # Sinon, démarrer un nouvel enregistrement
            self.dictation_window.start_recording()
            
    def toggle_pause(self):
        """Bascule entre pause et reprise de l'enregistrement"""
        if self.dictation_window.isVisible():
            # Basculer entre pause et reprise
            self.dictation_window.toggle_pause()
            
    def cancel_dictation(self):
        """Annule l'enregistrement en cours"""
        if self.dictation_window.isVisible():
            # Annuler l'enregistrement en cours
            self.dictation_window.cancel_recording()
            
    def partial_transcribe(self):
        """Déclenche la transcription partielle ou bascule entre pause/reprise"""
        if self.dictation_window.isVisible():
            print("🔄 Déclenchement de la transcription partielle")
            # Lancer une transcription partielle ou reprendre/mettre en pause
            self.dictation_window.partial_transcribe()

if __name__ == "__main__":
    manager = DictationManager()
    sys.exit(manager.initialize())