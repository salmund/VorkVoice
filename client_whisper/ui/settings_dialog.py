"""Fenêtre de paramètres pour gérer le dictionnaire personnel et la configuration AI."""

from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QTableWidget, QTableWidgetItem, QLabel, QLineEdit,
                             QMessageBox, QHeaderView, QTabWidget, QWidget, QComboBox,
                             QTextEdit)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor

from client_whisper.user_mappings import UserMappingsManager
from client_whisper.ai_config import AIConfigManager
from client_whisper.gemini_service import GeminiService


class SettingsDialog(QDialog):
    """Fenêtre de gestion du dictionnaire personnel et de la configuration AI."""
    
    def __init__(self, parent=None):
        """Initialise la fenêtre de paramètres.
        
        Args:
            parent: Widget parent
        """
        super().__init__(parent)
        self.setWindowTitle("Paramètres")
        self.setGeometry(200, 200, 850, 650)
        self.setWindowFlags(Qt.WindowType.Window)
        
        # Gestionnaires
        self.mappings_manager = UserMappingsManager()
        self.ai_config_manager = AIConfigManager()
        self.gemini_service = GeminiService()
        
        # Initialiser l'interface
        self.setup_ui()
        self.load_mappings()
        self.load_ai_config()
        
    def setup_ui(self):
        """Configure l'interface utilisateur."""
        main_layout = QVBoxLayout()
        
        # Créer le widget à onglets
        self.tabs = QTabWidget()
        
        # Onglet 1: Dictionnaire personnel
        self.dictionary_tab = self.create_dictionary_tab()
        self.tabs.addTab(self.dictionary_tab, "📖 Dictionnaire")
        
        # Onglet 2: Configuration AI
        self.ai_tab = self.create_ai_config_tab()
        self.tabs.addTab(self.ai_tab, "🤖 Configuration IA")
        
        main_layout.addWidget(self.tabs)
        
        # Bouton de fermeture
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
        
        main_layout.addLayout(button_layout)
        
        self.setLayout(main_layout)
        
        # Style global
        self.setStyleSheet("""
            QDialog {
                background-color: #f5f5f7;
                color: #333333;
            }
            QLineEdit {
                border: 1px solid #cccccc;
                border-radius: 5px;
                padding: 5px 10px;
                background-color: white;
                color: #333333;
            }
            QLineEdit:focus {
                border: 2px solid #007bff;
            }
            QTableWidget {
                background-color: white;
                color: #333333;
            }
            QComboBox {
                border: 1px solid #cccccc;
                border-radius: 5px;
                padding: 5px 10px;
                background-color: white;
                color: #333333;
                min-height: 25px;
            }
            QTextEdit {
                border: 1px solid #cccccc;
                border-radius: 5px;
                padding: 5px;
                background-color: white;
                color: #333333;
            }
        """)
    
    def create_dictionary_tab(self):
        """Crée l'onglet du dictionnaire personnel."""
        tab = QWidget()
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
                color: #333333;
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
        
        tab.setLayout(layout)
        return tab
    
    def create_ai_config_tab(self):
        """Crée l'onglet de configuration AI."""
        tab = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(15)
        
        # Titre et description
        title_label = QLabel("Configuration IA - Gemini")
        title_font = QFont("Segoe UI", 14)
        title_font.setBold(True)
        title_label.setFont(title_font)
        layout.addWidget(title_label)
        
        description_label = QLabel(
            "Configurez l'intégration avec l'API Gemini de Google.\n"
            "Ajoutez vos clés API pour traiter les transcriptions avec l'IA."
        )
        description_label.setStyleSheet("color: #555555; margin-bottom: 10px;")
        layout.addWidget(description_label)
        
        # Sélection du modèle
        model_layout = QHBoxLayout()
        model_label = QLabel("Modèle Gemini:")
        model_label.setStyleSheet("font-weight: bold;")
        model_layout.addWidget(model_label)
        
        self.model_combo = QComboBox()
        self.model_combo.currentTextChanged.connect(self.on_model_changed)
        model_layout.addWidget(self.model_combo)
        model_layout.addStretch()
        
        layout.addLayout(model_layout)
        
        # Formulaire d'ajout de clé API
        form_layout = QVBoxLayout()
        form_label = QLabel("Ajouter une nouvelle clé API:")
        form_label.setStyleSheet("font-weight: bold; margin-top: 10px;")
        form_layout.addWidget(form_label)
        
        # Ligne de saisie
        input_layout = QHBoxLayout()
        
        self.api_key_input = QLineEdit()
        self.api_key_input.setPlaceholderText("Entrez votre clé API Gemini")
        self.api_key_input.setMinimumHeight(35)
        self.api_key_input.setEchoMode(QLineEdit.EchoMode.Password)
        input_layout.addWidget(QLabel("Clé API:"))
        input_layout.addWidget(self.api_key_input)
        
        self.api_key_name_input = QLineEdit()
        self.api_key_name_input.setPlaceholderText("Nom (optionnel)")
        self.api_key_name_input.setMinimumHeight(35)
        self.api_key_name_input.setMaximumWidth(150)
        input_layout.addWidget(QLabel("Nom:"))
        input_layout.addWidget(self.api_key_name_input)
        
        self.add_api_key_button = QPushButton("➕ Ajouter")
        self.add_api_key_button.setMinimumHeight(35)
        self.add_api_key_button.clicked.connect(self.add_api_key)
        self.add_api_key_button.setStyleSheet("""
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
        input_layout.addWidget(self.add_api_key_button)
        
        form_layout.addLayout(input_layout)
        layout.addLayout(form_layout)
        
        # Table des clés API
        table_label = QLabel("Vos clés API:")
        table_label.setStyleSheet("font-weight: bold; margin-top: 15px;")
        layout.addWidget(table_label)
        
        self.api_keys_table = QTableWidget()
        self.api_keys_table.setColumnCount(5)
        self.api_keys_table.setHorizontalHeaderLabels(["Nom", "Clé", "Requêtes", "Succès", "Actions"])
        self.api_keys_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        self.api_keys_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.api_keys_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)
        self.api_keys_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)
        self.api_keys_table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)
        self.api_keys_table.setColumnWidth(0, 120)
        self.api_keys_table.setColumnWidth(2, 80)
        self.api_keys_table.setColumnWidth(3, 80)
        self.api_keys_table.setColumnWidth(4, 100)
        self.api_keys_table.setMinimumHeight(200)
        self.api_keys_table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #cccccc;
                border-radius: 5px;
                background-color: white;
                color: #333333;
            }
            QTableWidget::item {
                padding: 5px;
                color: #333333;
            }
        """)
        layout.addWidget(self.api_keys_table)
        
        # Note d'information
        note_label = QLabel(
            "💡 Note: Les clés API sont stockées localement sur votre machine. "
            "L'API Gemini a des limites de quota selon votre clé."
        )
        note_label.setStyleSheet("color: #666666; font-style: italic; font-size: 9pt;")
        note_label.setWordWrap(True)
        layout.addWidget(note_label)
        
        tab.setLayout(layout)
        return tab
    
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
    
    def load_ai_config(self):
        """Charge la configuration AI."""
        # Charger les modèles disponibles
        models = self.ai_config_manager.get_available_models()
        self.model_combo.clear()
        self.model_combo.addItems(models)
        
        # Sélectionner le modèle actuel
        current_model = self.ai_config_manager.get_current_model()
        index = self.model_combo.findText(current_model)
        if index >= 0:
            self.model_combo.setCurrentIndex(index)
        
        # Charger les clés API
        self.load_api_keys()
    
    def load_api_keys(self):
        """Charge les clés API dans la table."""
        keys = self.ai_config_manager.get_api_keys()
        self.api_keys_table.setRowCount(0)
        
        for key_info in keys:
            self.add_api_key_row(key_info)
    
    def add_api_key_row(self, key_info):
        """Ajoute une ligne dans la table des clés API.
        
        Args:
            key_info: Dictionnaire contenant les infos de la clé
        """
        row = self.api_keys_table.rowCount()
        self.api_keys_table.insertRow(row)
        
        # Colonnes de texte
        name_item = QTableWidgetItem(key_info.get("name", ""))
        key_masked = key_info["key"][:8] + "..." + key_info["key"][-4:] if len(key_info["key"]) > 12 else key_info["key"]
        key_item = QTableWidgetItem(key_masked)
        requests_item = QTableWidgetItem(str(key_info.get("requests_count", 0)))
        success_item = QTableWidgetItem(str(key_info.get("success_count", 0)))
        
        # Centrer le texte
        requests_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        success_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.api_keys_table.setItem(row, 0, name_item)
        self.api_keys_table.setItem(row, 1, key_item)
        self.api_keys_table.setItem(row, 2, requests_item)
        self.api_keys_table.setItem(row, 3, success_item)
        
        # Bouton de suppression
        delete_button = QPushButton("🗑️")
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
        delete_button.clicked.connect(lambda checked, k=key_info["key"]: self.delete_api_key(k))
        self.api_keys_table.setCellWidget(row, 4, delete_button)
    
    def on_model_changed(self, model_name):
        """Appelé quand le modèle change.
        
        Args:
            model_name: Nom du nouveau modèle
        """
        if model_name:
            self.ai_config_manager.set_current_model(model_name)
            print(f"✓ Modèle changé pour: {model_name}")
    
    def add_api_key(self):
        """Ajoute une nouvelle clé API."""
        api_key = self.api_key_input.text().strip()
        name = self.api_key_name_input.text().strip()
        
        if not api_key:
            QMessageBox.warning(self, "Erreur", "La clé API ne peut pas être vide.")
            return
        
        # Vérifier si la clé existe déjà
        existing_keys = self.ai_config_manager.get_api_keys()
        for key_info in existing_keys:
            if key_info["key"] == api_key:
                QMessageBox.warning(self, "Erreur", "Cette clé API existe déjà.")
                return
        
        # Ajouter la clé
        try:
            self.ai_config_manager.add_api_key(api_key, name)
            # Recharger la table
            self.load_api_keys()
            # Vider les champs
            self.api_key_input.clear()
            self.api_key_name_input.clear()
            QMessageBox.information(self, "Succès", "Clé API ajoutée avec succès!")
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors de l'ajout: {e}")
    
    def delete_api_key(self, api_key):
        """Supprime une clé API.
        
        Args:
            api_key: La clé API à supprimer
        """
        reply = QMessageBox.question(
            self,
            "Confirmation",
            "Voulez-vous vraiment supprimer cette clé API?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                self.ai_config_manager.remove_api_key(api_key)
                # Recharger la table
                self.load_api_keys()
                QMessageBox.information(self, "Succès", "Clé API supprimée avec succès!")
            except Exception as e:
                QMessageBox.critical(self, "Erreur", f"Erreur lors de la suppression: {e}")
