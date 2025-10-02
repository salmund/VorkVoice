"""Fenêtre de transcription partielle (aussi appelée Canvas)."""

import pyperclip
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                            QPushButton, QTextEdit, QFrame, QSizePolicy, QApplication)
from PyQt6.QtCore import Qt, QTimer, QEvent

from client_whisper.config import TRANSCRIBE_PARTIAL_HOTKEY


class PartialTranscriptionDialog(QDialog):
    """Fenêtre pop-up séparée pour afficher la transcription partielle"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Transcription en cours")
        self.setGeometry(150, 150, 700, 500)  # Taille initiale plus grande
        # Définir comme fenêtre indépendante avec son propre bouton dans la barre des tâches
        self.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.WindowStaysOnTopHint)
        
        # Style global
        self.setStyleSheet("""
            QDialog {
                background-color: #ffffff;
                border: 1px solid #cccccc;
                border-radius: 8px;
            }
            QTextEdit {
                border: 1px solid #e0e0e0;
                border-radius: 5px;
                padding: 10px;
                background-color: #fcfcfc;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 12pt;
                line-height: 1.5;
            }
            QPushButton {
                border-radius: 5px;
                padding: 10px;
                font-weight: bold;
                min-height: 40px;
            }
            QLabel {
                font-family: 'Segoe UI', Arial, sans-serif;
            }
        """)
        
        # Layout principal avec des marges pour un meilleur design
        layout = QVBoxLayout()
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)
        
        # Header avec titre et statut
        header_layout = QHBoxLayout()
        
        # Icône et titre
        title_layout = QHBoxLayout()
        title_icon = QLabel("📝")
        title_icon.setStyleSheet("font-size: 18pt; margin-right: 10px;")
        title_label = QLabel("Document en cours")
        title_label.setStyleSheet("font-size: 14pt; font-weight: bold;")
        title_layout.addWidget(title_icon)
        title_layout.addWidget(title_label)
        title_layout.addStretch()
        
        # Status avec indicateur coloré
        self.status_indicator = QLabel("●")
        self.status_indicator.setStyleSheet("color: #FF9800; font-size: 14pt;")
        self.status_label = QLabel("En pause")
        self.status_label.setStyleSheet("color: #666666; font-style: italic;")
        status_layout = QHBoxLayout()
        status_layout.addWidget(self.status_indicator)
        status_layout.addWidget(self.status_label)
        
        header_layout.addLayout(title_layout)
        header_layout.addLayout(status_layout)
        layout.addLayout(header_layout)
        
        # Séparateur horizontal
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        separator.setStyleSheet("background-color: #e0e0e0; max-height: 1px; margin: 10px 0px;")
        layout.addWidget(separator)
        
        # Zone de texte éditable pour la transcription
        self.text_display = QTextEdit()
        self.text_display.setReadOnly(False)
        self.text_display.setMinimumHeight(300)  # Hauteur minimale plus grande
        layout.addWidget(self.text_display, 1)  # Affectation d'un facteur d'étirement de 1
        
        # Instruction pour l'édition
        self.info_label = QLabel("Vous pouvez modifier le texte directement dans cette zone.")
        self.info_label.setStyleSheet("color: #757575; font-style: italic; margin-top: 5px; font-size: 10pt;")
        layout.addWidget(self.info_label)
        
        # Raccourci clavier
        shortcut_label = QLabel(f"Appuyez sur {TRANSCRIBE_PARTIAL_HOTKEY} pour alterner entre enregistrement et pause")
        shortcut_label.setStyleSheet("color: #555555; margin-top: 5px; font-size: 10pt;")
        layout.addWidget(shortcut_label)
        
        # Boutons avec meilleur design
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)
        
        self.copy_button = QPushButton("📋 Copier")
        self.copy_button.clicked.connect(self.copy_text)
        self.copy_button.setStyleSheet("""
            QPushButton {
                background-color: #f5f5f5;
                color: #333333;
                border: 1px solid #e0e0e0;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
        """)
        
        self.toggle_button = QPushButton("▶️ Continuer l'enregistrement")
        self.toggle_button.clicked.connect(self.accept)
        self.toggle_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
            }
            QPushButton:hover {
                background-color: #388E3C;
            }
        """)
        
        button_layout.addWidget(self.copy_button)
        button_layout.addWidget(self.toggle_button)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        
        # Activer le redimensionnement automatique
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        # Installer un gestionnaire d'événements pour Echap
        self.installEventFilter(self)
        
    def set_text(self, text):
        """Définit le texte dans la zone d'édition et ajuste la taille de la fenêtre"""
        self.text_display.setPlainText(text)
        # Placer le curseur à la fin du texte
        cursor = self.text_display.textCursor()
        cursor.movePosition(cursor.MoveOperation.End)
        self.text_display.setTextCursor(cursor)
        
        # Ajuster automatiquement la hauteur de la fenêtre en fonction du contenu
        doc_height = self.text_display.document().size().height()
        margins = self.text_display.contentsMargins()
        content_height = doc_height + margins.top() + margins.bottom() + 50  # Ajout d'une marge
        
        # Limiter la taille maximale pour ne pas dépasser l'écran
        screen = QApplication.primaryScreen().availableGeometry()
        max_height = screen.height() * 0.8  # Utiliser 80% de la hauteur d'écran maximale
        
        # Calculer la nouvelle hauteur (au moins le minimum, pas plus que le max)
        new_height = min(max(content_height + 250, 500), max_height)  # 250 pour les autres widgets
        
        # Récupérer la géométrie actuelle
        current_geometry = self.geometry()
        
        # Définir la nouvelle géométrie (même position, même largeur, nouvelle hauteur)
        self.setGeometry(current_geometry.x(), current_geometry.y(), 
                         current_geometry.width(), int(new_height))
        
    def get_text(self):
        """Récupère le texte depuis la zone d'édition"""
        return self.text_display.toPlainText()
        
    def copy_text(self):
        """Copie le texte actuel dans le presse-papier"""
        text = self.text_display.toPlainText()
        pyperclip.copy(text)
        # Afficher un message temporaire
        current_text = self.copy_button.text()
        self.copy_button.setText("✅ Copié!")
        QTimer.singleShot(1000, lambda: self.copy_button.setText(current_text))
        
    def update_status(self, status):
        """Met à jour l'indicateur de statut et le bouton en fonction de l'état actuel"""
        if status == "recording":
            self.status_indicator.setStyleSheet("color: #F44336; font-size: 14pt;")
            self.status_label.setText("Enregistrement en cours")
            self.toggle_button.setText("⏸️ Mettre en pause")
            self.toggle_button.setStyleSheet("""
                QPushButton {
                    background-color: #FF5722;
                    color: white;
                    border: none;
                }
                QPushButton:hover {
                    background-color: #E64A19;
                }
            """)
        elif status == "transcribing":
            self.status_indicator.setStyleSheet("color: #2196F3; font-size: 14pt;")
            self.status_label.setText("Transcription en cours")
            self.toggle_button.setEnabled(False)
            self.toggle_button.setText("🔄 Transcription...")
            self.toggle_button.setStyleSheet("""
                QPushButton {
                    background-color: #2196F3;
                    color: white;
                    border: none;
                }
            """)
        elif status == "paused":
            self.status_indicator.setStyleSheet("color: #FF9800; font-size: 14pt;")
            self.status_label.setText("En pause")
            self.toggle_button.setEnabled(True)
            self.toggle_button.setText("▶️ Continuer l'enregistrement")
            self.toggle_button.setStyleSheet("""
                QPushButton {
                    background-color: #4CAF50;
                    color: white;
                    border: none;
                }
                QPushButton:hover {
                    background-color: #388E3C;
                }
            """)
    
    def eventFilter(self, obj, event):
        """Gère les événements de touche comme Echap pour fermer la fenêtre"""
        # Intercepter la touche Échap
        if event.type() == QEvent.Type.KeyPress and event.key() == Qt.Key.Key_Escape:
            # Copier le texte automatiquement
            pyperclip.copy(self.text_display.toPlainText())
            # Fermer la fenêtre sans confirmation
            self.accept()
            return True
        return super().eventFilter(obj, event)
            
    def closeEvent(self, event):
        """Gère l'événement de fermeture de la fenêtre"""
        # Copier automatiquement le texte avant de fermer
        pyperclip.copy(self.text_display.toPlainText())
        # Pas de confirmation, fermer directement
        event.accept()