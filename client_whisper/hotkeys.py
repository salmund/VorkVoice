"""Gestion des raccourcis clavier."""

import keyboard
from PyQt6.QtCore import QObject, pyqtSignal
from client_whisper.config import HOTKEY, PAUSE_HOTKEY, CANCEL_HOTKEY

class HotkeyHandler(QObject):
    """Classe pour gérer les raccourcis clavier et envoyer des signaux à l'interface Qt"""
    toggle_signal = pyqtSignal()
    pause_signal = pyqtSignal()
    cancel_signal = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.active = False
        self.cancel_hooked = False
        self.pause_hooked = False
        
    def setup_hotkey(self):
        # Raccourci principal pour démarrer/arrêter
        keyboard.add_hotkey(HOTKEY, self.toggle_recording, suppress=True)
        
    def setup_cancel_hotkey(self):
        # Raccourci pour annuler (uniquement actif pendant l'enregistrement)
        if not self.cancel_hooked:
            keyboard.add_hotkey(CANCEL_HOTKEY, self.cancel_recording, suppress=True)
            self.cancel_hooked = True
            
    def remove_cancel_hotkey(self):
        # Supprimer le raccourci d'annulation quand pas en enregistrement
        if self.cancel_hooked:
            keyboard.remove_hotkey(CANCEL_HOTKEY)
            self.cancel_hooked = False
    
    def setup_pause_hotkey(self):
        # Raccourci pour mettre en pause/reprendre
        if not self.pause_hooked:
            keyboard.add_hotkey(PAUSE_HOTKEY, self.pause_recording, suppress=True)
            self.pause_hooked = True
            
    def remove_pause_hotkey(self):
        # Supprimer le raccourci de pause quand pas en enregistrement
        if self.pause_hooked:
            keyboard.remove_hotkey(PAUSE_HOTKEY)
            self.pause_hooked = False
        
    def toggle_recording(self):
        self.toggle_signal.emit()
        return False  # Empêche la propagation du caractère
        
    def cancel_recording(self):
        self.cancel_signal.emit()
        return False  # Empêche la propagation de la touche
        
    def pause_recording(self):
        self.pause_signal.emit()
        return False  # Empêche la propagation du caractère