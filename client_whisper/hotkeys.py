"""Gestion des raccourcis clavier."""

import keyboard
from PyQt6.QtCore import QObject, pyqtSignal, QTimer
from client_whisper.config import HOTKEY, PAUSE_HOTKEY, CANCEL_HOTKEY, TRANSCRIBE_PARTIAL_HOTKEY

class HotkeyHandler(QObject):
    """Classe pour gérer les raccourcis clavier et envoyer des signaux à l'interface Qt"""
    toggle_signal = pyqtSignal()
    pause_signal = pyqtSignal()
    cancel_signal = pyqtSignal()
    partial_transcribe_signal = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.active = False
        self.main_hooked = False
        self.cancel_hooked = False
        self.pause_hooked = False
        self.partial_transcribe_hooked = False
        
        # Timer pour vérifier périodiquement que le raccourci principal est toujours actif
        self.watchdog_timer = QTimer()
        self.watchdog_timer.timeout.connect(self._check_main_hotkey)
        self.watchdog_timer.start(5000)  # Vérifier toutes les 5 secondes
        
    def setup_hotkey(self):
        """Raccourci principal pour démarrer/arrêter - avec gestion d'erreur"""
        try:
            if not self.main_hooked:
                keyboard.add_hotkey(HOTKEY, self.toggle_recording, suppress=True)
                self.main_hooked = True
                print(f"✅ Raccourci {HOTKEY} enregistré avec succès")
        except Exception as e:
            print(f"❌ Erreur lors de l'enregistrement du raccourci {HOTKEY}: {e}")
            self.main_hooked = False
    
    def _check_main_hotkey(self):
        """Vérifie périodiquement que le raccourci principal est toujours actif et le ré-enregistre si nécessaire"""
        try:
            # Si le raccourci devrait être enregistré mais ne l'est pas, le ré-enregistrer
            if self.main_hooked:
                # Tenter de supprimer et ré-enregistrer le raccourci
                try:
                    keyboard.remove_hotkey(HOTKEY)
                except:
                    pass  # Le raccourci n'existait peut-être plus
                
                self.main_hooked = False
                self.setup_hotkey()
        except Exception as e:
            # En cas d'erreur, tenter simplement de ré-enregistrer
            print(f"⚠️ Tentative de ré-enregistrement du raccourci principal: {e}")
            self.main_hooked = False
            self.setup_hotkey()
        
    def setup_cancel_hotkey(self):
        """Raccourci pour annuler (uniquement actif pendant l'enregistrement) - avec gestion d'erreur"""
        if not self.cancel_hooked:
            try:
                keyboard.add_hotkey(CANCEL_HOTKEY, self.cancel_recording, suppress=True)
                self.cancel_hooked = True
            except Exception as e:
                print(f"❌ Erreur lors de l'enregistrement du raccourci d'annulation: {e}")
                self.cancel_hooked = False
            
    def remove_cancel_hotkey(self):
        """Supprimer le raccourci d'annulation quand pas en enregistrement"""
        if self.cancel_hooked:
            try:
                keyboard.remove_hotkey(CANCEL_HOTKEY)
            except Exception as e:
                print(f"⚠️ Erreur lors de la suppression du raccourci d'annulation: {e}")
            finally:
                self.cancel_hooked = False
    
    def setup_pause_hotkey(self):
        """Raccourci pour mettre en pause/reprendre - avec gestion d'erreur"""
        if not self.pause_hooked:
            try:
                keyboard.add_hotkey(PAUSE_HOTKEY, self.pause_recording, suppress=True)
                self.pause_hooked = True
            except Exception as e:
                print(f"❌ Erreur lors de l'enregistrement du raccourci de pause: {e}")
                self.pause_hooked = False
            
    def remove_pause_hotkey(self):
        """Supprimer le raccourci de pause quand pas en enregistrement"""
        if self.pause_hooked:
            try:
                keyboard.remove_hotkey(PAUSE_HOTKEY)
            except Exception as e:
                print(f"⚠️ Erreur lors de la suppression du raccourci de pause: {e}")
            finally:
                self.pause_hooked = False
            
    def setup_partial_transcribe_hotkey(self):
        """Raccourci pour transcription partielle - avec gestion d'erreur"""
        if not self.partial_transcribe_hooked:
            try:
                keyboard.add_hotkey(TRANSCRIBE_PARTIAL_HOTKEY, self.partial_transcribe, suppress=True)
                self.partial_transcribe_hooked = True
                print(f"✅ Raccourci {TRANSCRIBE_PARTIAL_HOTKEY} pour transcription partielle activé")
            except Exception as e:
                print(f"❌ Erreur lors de l'enregistrement du raccourci de transcription partielle: {e}")
                self.partial_transcribe_hooked = False
            
    def remove_partial_transcribe_hotkey(self):
        """Supprimer le raccourci de transcription partielle"""
        if self.partial_transcribe_hooked:
            try:
                keyboard.remove_hotkey(TRANSCRIBE_PARTIAL_HOTKEY)
                print(f"❌ Raccourci {TRANSCRIBE_PARTIAL_HOTKEY} pour transcription partielle désactivé")
            except Exception as e:
                print(f"⚠️ Erreur lors de la suppression du raccourci de transcription partielle: {e}")
            finally:
                self.partial_transcribe_hooked = False
        
    def toggle_recording(self):
        self.toggle_signal.emit()
        return False  # Empêche la propagation du caractère
        
    def cancel_recording(self):
        self.cancel_signal.emit()
        return False  # Empêche la propagation de la touche
        
    def pause_recording(self):
        self.pause_signal.emit()
        return False  # Empêche la propagation du caractère
        
    def partial_transcribe(self):
        print("🔄 Signal de transcription partielle envoyé")
        self.partial_transcribe_signal.emit()
        return False  # Empêche la propagation du caractère