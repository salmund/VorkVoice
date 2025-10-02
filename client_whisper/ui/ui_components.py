"""Composants d'interface utilisateur réutilisables pour l'application de dictée vocale."""

from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QCheckBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from client_whisper.config import HOTKEY, PAUSE_HOTKEY, CANCEL_HOTKEY, TRANSCRIBE_PARTIAL_HOTKEY

class DictationUI:
    """Classe de gestion de l'interface utilisateur de l'application de dictée vocale"""
    
    def __init__(self, parent):
        """Initialise l'interface utilisateur
        
        Args:
            parent: Le widget parent qui contiendra cette interface
        """
        self.parent = parent
        self.create_ui_elements()
        self.setup_layout()
        self.setup_styles()
        
    def create_ui_elements(self):
        """Crée tous les éléments d'interface utilisateur"""
        # Créer une police plus grande pour le titre
        title_font = QFont("Segoe UI", 13)
        title_font.setBold(True)
        
        # Labels
        self.status_label = QLabel("🗣 Enregistrement en cours...", self.parent)
        self.status_label.setFont(title_font)
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.timer_label = QLabel("⏳ Temps : 0s", self.parent)
        self.timer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Checkbox pour auto-paste
        self.autopaste_checkbox = QCheckBox("Coller automatiquement après transcription", self.parent)
        self.autopaste_checkbox.setChecked(True)  # Activé par défaut
        
        # Boutons
        self.pause_button = QPushButton("⏸ Pause", self.parent)
        self.partial_transcribe_button = QPushButton("🗒️ Canvas", self.parent)
        self.stop_button = QPushButton("🛑 Stop & Transcrire", self.parent)
        self.cancel_button = QPushButton("❌ Annuler", self.parent)
        
        # Labels des raccourcis
        self.main_shortcut_label = QLabel(f"• {HOTKEY} : Démarrer/Arrêter")
        self.pause_shortcut_label = QLabel(f"• {PAUSE_HOTKEY} : Pause/Reprendre")
        self.partial_shortcut_label = QLabel(f"• {TRANSCRIBE_PARTIAL_HOTKEY} : Transcription partielle")
        self.cancel_shortcut_label = QLabel(f"• {CANCEL_HOTKEY} : Annuler")
        
        # Définir une hauteur minimale pour les boutons
        for button in [self.pause_button, self.partial_transcribe_button, 
                      self.stop_button, self.cancel_button]:
            button.setMinimumHeight(45)
    
    def setup_layout(self):
        """Configure la mise en page des éléments d'interface"""
        # Layout principal
        self.main_layout = QVBoxLayout()
        
        # Ajouter les éléments au layout
        self.main_layout.addWidget(self.status_label)
        self.main_layout.addWidget(self.timer_label)
        
        # Ajouter une marge autour de la checkbox
        self.main_layout.addSpacing(5)
        self.main_layout.addWidget(self.autopaste_checkbox)
        self.main_layout.addSpacing(5)
        
        # Ajouter les boutons
        self.main_layout.addWidget(self.pause_button)
        self.main_layout.addWidget(self.partial_transcribe_button)
        self.main_layout.addWidget(self.stop_button)
        self.main_layout.addWidget(self.cancel_button)
        
        # Ajouter les labels pour les raccourcis
        shortcuts_layout = QVBoxLayout()
        shortcuts_label = QLabel("Raccourcis clavier:")
        shortcuts_label.setStyleSheet("font-weight: bold; margin-top: 10px;")
        shortcuts_layout.addWidget(shortcuts_label)
        
        shortcut_style = "padding-left: 10px; color: #555;"
        for lbl in [self.main_shortcut_label, self.pause_shortcut_label, 
                   self.partial_shortcut_label, self.cancel_shortcut_label]:
            lbl.setStyleSheet(shortcut_style)
            shortcuts_layout.addWidget(lbl)
            
        self.main_layout.addLayout(shortcuts_layout)
        
        # Appliquer le layout au parent
        self.parent.setLayout(self.main_layout)
    
    def setup_styles(self):
        """Configure les styles CSS des éléments d'interface"""
        # Style des labels
        self.status_label.setStyleSheet("margin-top: 10px; margin-bottom: 5px;")
        self.timer_label.setStyleSheet("font-size: 11pt; margin-bottom: 10px;")
        
        # Style des boutons
        self.pause_button.setStyleSheet("""
            QPushButton {
                background-color: #5a7fad;
                color: white;
                border: none;
                border-radius: 6px;
                font-weight: bold;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #4b6b93;
            }
            QPushButton:pressed {
                background-color: #3c5679;
            }
        """)
        
        self.partial_transcribe_button.setStyleSheet("""
            QPushButton {
                background-color: #34b4eb;
                color: white;
                border: none;
                border-radius: 6px;
                font-weight: bold;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #2a95c3;
            }
            QPushButton:pressed {
                background-color: #207595;
            }
        """)
        
        self.stop_button.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                border: none;
                border-radius: 6px;
                font-weight: bold;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #218838;
            }
            QPushButton:pressed {
                background-color: #1d7430;
            }
        """)
        
        self.cancel_button.setStyleSheet("""
            QPushButton {
                background-color: #dc3545;
                color: white;
                border: none;
                border-radius: 6px;
                font-weight: bold;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #c82333;
            }
            QPushButton:pressed {
                background-color: #bd2130;
            }
        """)
        
    def update_status_label(self, text):
        """Met à jour le texte du label de statut"""
        self.status_label.setText(text)
        
    def update_timer_label(self, mins, secs):
        """Met à jour le label du timer"""
        if mins > 0:
            self.timer_label.setText(f"⏳ Temps : {mins}m {secs}s")
        else:
            self.timer_label.setText(f"⏳ Temps : {secs}s")
            
    def update_pause_button(self, is_paused):
        """Met à jour le bouton de pause en fonction de l'état"""
        if is_paused:
            self.pause_button.setText("▶ Reprendre")
        else:
            self.pause_button.setText("⏸ Pause")
            
    def is_autopaste_enabled(self):
        """Retourne si l'option de collage automatique est activée"""
        return self.autopaste_checkbox.isChecked()