"""Gestionnaire de configuration pour l'intégration AI (Gemini)."""

import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional


class AIConfigManager:
    """Gère la configuration et le monitoring de l'API Gemini."""
    
    def __init__(self):
        """Initialise le gestionnaire de configuration AI."""
        self.config_dir = Path.home() / ".vorkvoice"
        self.config_file = self.config_dir / "ai_config.json"
        self._ensure_config_dir()
        
    def _ensure_config_dir(self):
        """S'assure que le dossier de configuration existe."""
        if not self.config_dir.exists():
            self.config_dir.mkdir(parents=True)
    
    def load_config(self) -> Dict:
        """Charge la configuration AI depuis le fichier JSON.
        
        Returns:
            dict: Configuration AI avec clés, modèle et usage
        """
        if not self.config_file.exists():
            return self._get_default_config()
        
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
                # S'assurer que la structure est complète
                default_config = self._get_default_config()
                for key in default_config:
                    if key not in config:
                        config[key] = default_config[key]
                return config
        except (json.JSONDecodeError, IOError) as e:
            print(f"Erreur lors du chargement de la config AI: {e}")
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict:
        """Retourne la configuration par défaut.
        
        Returns:
            dict: Configuration par défaut
        """
        return {
            "api_keys": [],
            "current_model": "gemini-1.5-flash",
            "available_models": [
                "gemini-1.5-flash",
                "gemini-1.5-pro",
                "gemini-1.0-pro"
            ],
            "usage_stats": {}
        }
    
    def save_config(self, config: Dict):
        """Sauvegarde la configuration AI dans le fichier JSON.
        
        Args:
            config: Configuration à sauvegarder
        """
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
        except IOError as e:
            print(f"Erreur lors de la sauvegarde de la config AI: {e}")
            raise
    
    def get_api_keys(self) -> List[Dict]:
        """Retourne la liste des clés API configurées.
        
        Returns:
            list: Liste de dictionnaires contenant les clés API et leurs infos
        """
        config = self.load_config()
        return config.get("api_keys", [])
    
    def add_api_key(self, api_key: str, name: str = ""):
        """Ajoute une nouvelle clé API.
        
        Args:
            api_key: La clé API à ajouter
            name: Nom/description de la clé (optionnel)
        """
        config = self.load_config()
        
        # Vérifier si la clé existe déjà
        for key_info in config["api_keys"]:
            if key_info["key"] == api_key:
                return  # Clé déjà présente
        
        # Ajouter la nouvelle clé
        key_info = {
            "key": api_key,
            "name": name or f"Clé {len(config['api_keys']) + 1}",
            "added_date": datetime.now().isoformat(),
            "requests_count": 0,
            "success_count": 0,
            "error_count": 0,
            "last_used": None
        }
        config["api_keys"].append(key_info)
        self.save_config(config)
    
    def remove_api_key(self, api_key: str):
        """Supprime une clé API.
        
        Args:
            api_key: La clé API à supprimer
        """
        config = self.load_config()
        config["api_keys"] = [k for k in config["api_keys"] if k["key"] != api_key]
        self.save_config(config)
    
    def get_active_api_key(self) -> Optional[str]:
        """Retourne une clé API active (avec le moins d'erreurs).
        
        Returns:
            str: Une clé API ou None si aucune disponible
        """
        keys = self.get_api_keys()
        if not keys:
            return None
        
        # Trier par taux de succès (success_count / requests_count)
        # Si aucune requête n'a été faite, donner priorité
        sorted_keys = sorted(keys, key=lambda k: (
            k["success_count"] / max(k["requests_count"], 1),
            -k["requests_count"]
        ), reverse=True)
        
        return sorted_keys[0]["key"] if sorted_keys else None
    
    def record_api_usage(self, api_key: str, success: bool, error_message: str = ""):
        """Enregistre l'utilisation d'une clé API.
        
        Args:
            api_key: La clé API utilisée
            success: Si la requête a réussi
            error_message: Message d'erreur si échec
        """
        config = self.load_config()
        
        for key_info in config["api_keys"]:
            if key_info["key"] == api_key:
                key_info["requests_count"] += 1
                key_info["last_used"] = datetime.now().isoformat()
                
                if success:
                    key_info["success_count"] += 1
                else:
                    key_info["error_count"] += 1
                    # Enregistrer l'erreur dans les stats d'usage
                    if "recent_errors" not in key_info:
                        key_info["recent_errors"] = []
                    key_info["recent_errors"].append({
                        "timestamp": datetime.now().isoformat(),
                        "error": error_message
                    })
                    # Garder seulement les 10 dernières erreurs
                    key_info["recent_errors"] = key_info["recent_errors"][-10:]
                
                break
        
        self.save_config(config)
    
    def get_current_model(self) -> str:
        """Retourne le modèle actuellement sélectionné.
        
        Returns:
            str: Nom du modèle
        """
        config = self.load_config()
        return config.get("current_model", "gemini-1.5-flash")
    
    def set_current_model(self, model: str):
        """Définit le modèle à utiliser.
        
        Args:
            model: Nom du modèle
        """
        config = self.load_config()
        config["current_model"] = model
        self.save_config(config)
    
    def get_available_models(self) -> List[str]:
        """Retourne la liste des modèles disponibles.
        
        Returns:
            list: Liste des noms de modèles
        """
        config = self.load_config()
        return config.get("available_models", ["gemini-1.5-flash"])
