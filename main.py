"""
Script de rechargement à chaud pour l'application de dictée vocale.

Ce script surveille les modifications dans les fichiers .py du projet et
redémarre automatiquement l'application principale lorsque des changements
sont détectés.
"""

import sys
import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Chemins vers les scripts
SERVER_SCRIPT = "serveur_whisper.py"
CLIENT_SCRIPT = "dictee_vocale.py"

class AppReloader(FileSystemEventHandler):
    """Gestionnaire d'événements pour le rechargement de l'application."""
    
    def __init__(self):
        self.server_process = None
        self.client_process = None
        self.start_server()
        self.start_client()

    def start_server(self):
        """Démarre le serveur Whisper dans un nouveau processus."""
        if self.server_process:
            self.server_process.kill()
        
        print("🚀 Démarrage du serveur Whisper...")
        self.server_process = subprocess.Popen([sys.executable, SERVER_SCRIPT])

    def start_client(self):
        """Démarre l'application client dans un nouveau processus."""
        if self.client_process:
            self.client_process.kill()
        
        print("🚀 Démarrage de l'application client...")
        self.client_process = subprocess.Popen([sys.executable, CLIENT_SCRIPT])

    def on_modified(self, event):
        """Appelé lorsque des fichiers sont modifiés."""
        if not event.src_path.endswith(".py"):
            return

        # Normaliser les chemins pour la comparaison
        modified_path = os.path.normpath(event.src_path)
        
        if modified_path == os.path.normpath(SERVER_SCRIPT):
            print(f"🔄 Serveur modifié détecté: {modified_path}. Rechargement du serveur...")
            self.start_server()
        else:
            print(f"🔄 Fichier client modifié détecté: {modified_path}. Rechargement de l'application...")
            self.start_client()

if __name__ == "__main__":
    # Importer os pour la normalisation des chemins
    import os

    path = "."  # Surveiller le répertoire courant et ses sous-dossiers
    
    event_handler = AppReloader()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    
    print("🔥 Hot-reloader activé. En attente de modifications...")
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        if event_handler.server_process:
            event_handler.server_process.kill()
        if event_handler.client_process:
            event_handler.client_process.kill()
    
    observer.join()
    print("👋 Hot-reloader arrêté.")
