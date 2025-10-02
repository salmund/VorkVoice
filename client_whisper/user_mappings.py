"""Gestionnaire des mappings personnalisés de l'utilisateur."""

import json
import os
from pathlib import Path

class UserMappingsManager:
    """Gère le chargement et la sauvegarde des mappings personnalisés."""
    
    def __init__(self):
        """Initialise le gestionnaire de mappings."""
        # Chemin vers le fichier de configuration utilisateur
        self.config_dir = Path.home() / ".vorkvoice"
        self.mappings_file = self.config_dir / "user_mappings.json"
        self._ensure_config_dir()
        
    def _ensure_config_dir(self):
        """S'assure que le dossier de configuration existe."""
        if not self.config_dir.exists():
            self.config_dir.mkdir(parents=True)
    
    def load_mappings(self):
        """Charge les mappings depuis le fichier JSON.
        
        Returns:
            list: Liste de tuples (source, remplacement)
        """
        if not self.mappings_file.exists():
            return []
        
        try:
            with open(self.mappings_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Convertir la liste de listes en liste de tuples
                return [(item[0], item[1]) for item in data]
        except (json.JSONDecodeError, IOError) as e:
            print(f"Erreur lors du chargement des mappings: {e}")
            return []
    
    def save_mappings(self, mappings):
        """Sauvegarde les mappings dans le fichier JSON.
        
        Args:
            mappings: Liste de tuples (source, remplacement)
        """
        try:
            # Convertir les tuples en listes pour la sérialisation JSON
            data = [[source, target] for source, target in mappings]
            with open(self.mappings_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except IOError as e:
            print(f"Erreur lors de la sauvegarde des mappings: {e}")
            raise
    
    def get_all_mappings(self):
        """Retourne tous les mappings (par défaut + utilisateur).
        
        Returns:
            list: Liste combinée de tuples (source, remplacement)
        """
        # Importer les mappings par défaut
        from mappings import list_mapping as default_mappings
        
        # Charger les mappings utilisateur
        user_mappings = self.load_mappings()
        
        # Combiner les deux listes (utilisateur en premier pour priorité)
        return user_mappings + default_mappings
