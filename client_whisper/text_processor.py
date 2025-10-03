"""
Module pour le post-traitement du texte transcrit.
"""

from mappings import DEFAULT_MAPPINGS
from client_whisper.user_mappings import UserMappingsManager

class TextProcessor:
    """
    Applique les remplacements de texte (par défaut et personnalisés) 
    sur une chaîne de caractères.
    """

    @staticmethod
    def apply_mappings(text: str) -> str:
        """
        Applique les remplacements au texte transcrit.

        Les mappings personnalisés ont la priorité sur les mappings par défaut.

        Args:
            text: Le texte à traiter.

        Returns:
            Le texte après application des remplacements.
        """
        # Charger les mappings personnalisés
        user_mappings_manager = UserMappingsManager()
        user_mappings = dict(user_mappings_manager.load_mappings())

        # Combiner les mappings en donnant la priorité aux mappings utilisateur
        # On ajoute d'abord les mappings par défaut, puis on les écrase avec 
        # les mappings utilisateur s'il y a des clés en commun.
        combined_mappings = DEFAULT_MAPPINGS.copy()
        combined_mappings.update(user_mappings)

        # Appliquer les remplacements
        for source, target in combined_mappings.items():
            # Utiliser \b pour s'assurer qu'on remplace des mots entiers
            # et être insensible à la casse pour la source
            # (le remplacement se fait avec la casse de la cible)
            # Note: re.escape est important si les clés contiennent des caractères spéciaux
            import re
            pattern = r'\b' + re.escape(source) + r'\b'
            text = re.sub(pattern, target, text, flags=re.IGNORECASE)
            
        return text
