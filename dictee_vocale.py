#!/usr/bin/env python3
"""
Lanceur pour l'application de dictée vocale
Permet d'exécuter l'application depuis le dossier racine
"""

import sys
from client_whisper.main import DictationManager

if __name__ == "__main__":
    manager = DictationManager()
    sys.exit(manager.initialize())