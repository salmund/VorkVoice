"""Service pour l'intégration avec l'API Gemini de Google."""

from typing import Optional
from client_whisper.ai_config import AIConfigManager


class GeminiService:
    """Service pour interagir avec l'API Gemini."""
    
    def __init__(self):
        """Initialise le service Gemini."""
        self.config_manager = AIConfigManager()
        self._genai = None
    
    def _initialize_genai(self, api_key: str):
        """Initialise la bibliothèque google.generativeai avec la clé API.
        
        Args:
            api_key: La clé API à utiliser
        """
        try:
            import google.generativeai as genai
            genai.configure(api_key=api_key)
            self._genai = genai
            return True
        except ImportError:
            print("⚠️ La bibliothèque google-generativeai n'est pas installée.")
            print("   Installez-la avec : pip install google-generativeai")
            return False
        except Exception as e:
            print(f"⚠️ Erreur lors de l'initialisation de Gemini: {e}")
            return False
    
    def process_with_ai(self, transcription: str) -> Optional[str]:
        """Envoie la transcription à Gemini et retourne la réponse.
        
        Args:
            transcription: Le texte transcrit à traiter
            
        Returns:
            str: La réponse de Gemini ou None en cas d'erreur
        """
        # Récupérer une clé API active
        api_key = self.config_manager.get_active_api_key()
        if not api_key:
            error_msg = "Aucune clé API configurée. Ajoutez une clé dans les paramètres."
            print(f"⚠️ {error_msg}")
            return None
        
        # Initialiser genai si nécessaire
        if self._genai is None:
            if not self._initialize_genai(api_key):
                return None
        
        # Récupérer le modèle configuré
        model_name = self.config_manager.get_current_model()
        
        try:
            # Créer le modèle
            model = self._genai.GenerativeModel(model_name)
            
            # Générer la réponse
            print(f"🤖 Envoi à Gemini ({model_name})...")
            response = model.generate_content(transcription)
            
            # Extraire le texte de la réponse
            result_text = response.text
            
            # Enregistrer le succès
            self.config_manager.record_api_usage(api_key, success=True)
            
            print("✅ Réponse reçue de Gemini")
            return result_text
            
        except Exception as e:
            error_msg = str(e)
            print(f"⚠️ Erreur lors de l'appel à Gemini: {error_msg}")
            
            # Enregistrer l'erreur
            self.config_manager.record_api_usage(api_key, success=False, error_message=error_msg)
            
            # Retourner un message d'erreur informatif
            return f"⚠️ Erreur Gemini: {error_msg}"
    
    def test_api_key(self, api_key: str) -> tuple[bool, str]:
        """Teste si une clé API est valide.
        
        Args:
            api_key: La clé API à tester
            
        Returns:
            tuple: (succès, message)
        """
        if not self._initialize_genai(api_key):
            return False, "Impossible d'initialiser la bibliothèque Gemini"
        
        try:
            # Essayer une requête simple
            model = self._genai.GenerativeModel(self.config_manager.get_current_model())
            response = model.generate_content("Hello")
            
            if response.text:
                return True, "Clé API valide ✓"
            else:
                return False, "Pas de réponse du modèle"
                
        except Exception as e:
            return False, f"Erreur: {str(e)}"
