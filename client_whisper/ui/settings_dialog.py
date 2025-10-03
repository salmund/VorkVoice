"""Fenêtre de paramètres pour gérer le dictionnaire personnel."""

from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QTableWidget, QTableWidgetItem, QLabel, QLineEdit,
                             QMessageBox, QHeaderView)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from client_whisper.user_mappings import UserMappingsManager


class SettingsDialog(QDialog):
    """Fenêtre de gestion du dictionnaire personnel de remplacements."""
    
    def __init__(self, parent=None):
        """Initialise la fenêtre de paramètres.
        
        Args:
            parent: Widget parent
        """
        super().__init__(parent)
        self.setWindowTitle("Paramètres - Dictionnaire personnel")
        self.setGeometry(200, 200, 800, 600)
        self.setWindowFlags(Qt.WindowType.Window)
        
        # Gestionnaire de mappings
        self.mappings_manager = UserMappingsManager()
        
        # Initialiser l'interface
        self.setup_ui()
        self.load_mappings()
        
    def setup_ui(self):
        """Configure l'interface utilisateur."""
        layout = QVBoxLayout()
        layout.setSpacing(15)
        
        # Titre et description
        title_label = QLabel("Dictionnaire personnel")
        title_font = QFont("Segoe UI", 14)
        title_font.setBold(True)
        title_label.setFont(title_font)
        layout.addWidget(title_label)
        
        description_label = QLabel(
            "Gérez vos remplacements de mots et expressions.\n"
            "Ces remplacements seront appliqués automatiquement lors de la transcription."
        )
        description_label.setStyleSheet("color: #555555; margin-bottom: 10px;")
        layout.addWidget(description_label)
        
        # Formulaire d'ajout
        form_layout = QVBoxLayout()
        form_label = QLabel("Ajouter un nouveau remplacement:")
        form_label.setStyleSheet("font-weight: bold; margin-top: 10px;")
        form_layout.addWidget(form_label)
        
        # Ligne de saisie
        input_layout = QHBoxLayout()
        
        self.source_input = QLineEdit()
        self.source_input.setPlaceholderText("Texte à remplacer (ex: 'Maya')")
        self.source_input.setMinimumHeight(35)
        input_layout.addWidget(QLabel("De:"))
        input_layout.addWidget(self.source_input)
        
        self.target_input = QLineEdit()
        self.target_input.setPlaceholderText("Texte de remplacement (ex: 'Maïa')")
        self.target_input.setMinimumHeight(35)
        input_layout.addWidget(QLabel("Vers:"))
        input_layout.addWidget(self.target_input)
        
        self.add_button = QPushButton("➕ Ajouter")
        self.add_button.setMinimumHeight(35)
        self.add_button.clicked.connect(self.add_mapping)
        self.add_button.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                border: none;
                border-radius: 5px;
                font-weight: bold;
                padding: 5px 15px;
            }
            QPushButton:hover {
                background-color: #218838;
            }
        """)
        input_layout.addWidget(self.add_button)
        
        form_layout.addLayout(input_layout)
        layout.addLayout(form_layout)
        
        # Table des mappings
        table_label = QLabel("Vos remplacements personnalisés:")
        table_label.setStyleSheet("font-weight: bold; margin-top: 15px;")
        layout.addWidget(table_label)
        
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Texte source", "Remplacement", "Actions"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)
        self.table.setColumnWidth(2, 100)
        self.table.setMinimumHeight(300)
        self.table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #cccccc;
                border-radius: 5px;
                background-color: white;
            }
            QTableWidget::item {
                padding: 5px;
                color: #333333; /* Assure que le texte est sombre */
            }
        """)
        layout.addWidget(self.table)
        
        # Note sur les mappings par défaut
        note_label = QLabel(
            "💡 Note: Les mappings par défaut du système sont toujours actifs. "
            "Vos mappings personnalisés ont la priorité."
        )
        note_label.setStyleSheet("color: #666666; font-style: italic; font-size: 9pt;")
        note_label.setWordWrap(True)
        layout.addWidget(note_label)
        
        # Boutons de bas de page
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        self.close_button = QPushButton("Fermer")
        self.close_button.setMinimumHeight(35)
        self.close_button.clicked.connect(self.close)
        self.close_button.setStyleSheet("""
            QPushButton {
                background-color: #6c757d;
                color: white;
                border: none;
                border-radius: 5px;
                font-weight: bold;
                padding: 5px 20px;
            }
            QPushButton:hover {
                background-color: #5a6268;
            }
        """)
        button_layout.addWidget(self.close_button)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        
        # Style global
        self.setStyleSheet("""
            QDialog {
                background-color: #f5f5f7;
            }
            QLineEdit {
                border: 1px solid #cccccc;
                border-radius: 5px;
                padding: 5px 10px;
                background-color: white;
            }
            QLineEdit:focus {
                border: 2px solid #007bff;
            }
        """)
    
    def load_mappings(self):
        """Charge les mappings dans la table."""
        mappings = self.mappings_manager.load_mappings()
        self.table.setRowCount(0)
        
        for source, target in mappings:
            self.add_table_row(source, target)
    
    def add_table_row(self, source, target):
        """Ajoute une ligne dans la table.
        
        Args:
            source: Texte source
            target: Texte de remplacement
        """
        row = self.table.rowCount()
        self.table.insertRow(row)
        
        # Colonnes de texte
        source_item = QTableWidgetItem(source)
        target_item = QTableWidgetItem(target)
        self.table.setItem(row, 0, source_item)
        self.table.setItem(row, 1, target_item)
        
        # Bouton de suppression
        delete_button = QPushButton("🗑️ Supprimer")
        delete_button.setStyleSheet("""
            QPushButton {
                background-color: #dc3545;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 5px 10px;
                font-size: 9pt;
            }
            QPushButton:hover {
                background-color: #c82333;
            }
        """)
        delete_button.clicked.connect(lambda checked, r=row: self.delete_mapping(r))
        self.table.setCellWidget(row, 2, delete_button)
    
    def add_mapping(self):
        """Ajoute un nouveau mapping."""
        source = self.source_input.text().strip()
        target = self.target_input.text().strip()
        
        if not source:
            QMessageBox.warning(self, "Erreur", "Le texte source ne peut pas être vide.")
            return
        
        if not target:
            QMessageBox.warning(self, "Erreur", "Le texte de remplacement ne peut pas être vide.")
            return
        
        # Charger les mappings existants
        mappings = self.mappings_manager.load_mappings()
        
        # Vérifier si le mapping existe déjà
        for existing_source, _ in mappings:
            if existing_source == source:
                reply = QMessageBox.question(
                    self, 
                    "Remplacement existant",
                    f"Un remplacement existe déjà pour '{source}'.\nVoulez-vous le remplacer?",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                )
                if reply == QMessageBox.StandardButton.No:
                    return
                # Supprimer l'ancien mapping
                mappings = [(s, t) for s, t in mappings if s != source]
                break
        
        # Ajouter le nouveau mapping
        mappings.append((source, target))
        
        # Sauvegarder
        try:
            self.mappings_manager.save_mappings(mappings)
            # Recharger la table
            self.load_mappings()
            # Vider les champs
            self.source_input.clear()
            self.target_input.clear()
            QMessageBox.information(self, "Succès", "Remplacement ajouté avec succès!")
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors de la sauvegarde: {e}")
    
    def delete_mapping(self, row):
        """Supprime un mapping.
        
        Args:
            row: Numéro de ligne à supprimer
        """
        source_item = self.table.item(row, 0)
        if not source_item:
            return
        
        source = source_item.text()
        
        reply = QMessageBox.question(
            self,
            "Confirmation",
            f"Voulez-vous vraiment supprimer le remplacement '{source}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            # Charger les mappings
            mappings = self.mappings_manager.load_mappings()
            # Filtrer pour supprimer le mapping
            mappings = [(s, t) for s, t in mappings if s != source]
            # Sauvegarder
            try:
                self.mappings_manager.save_mappings(mappings)
                # Recharger la table
                self.load_mappings()
                QMessageBox.information(self, "Succès", "Remplacement supprimé avec succès!")
            except Exception as e:
                QMessageBox.critical(self, "Erreur", f"Erreur lors de la suppression: {e}")
