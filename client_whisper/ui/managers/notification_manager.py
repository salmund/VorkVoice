"""Gestionnaire de notifications système pour l'application de dictée vocale."""

from PyQt6.QtWidgets import QSystemTrayIcon
from PyQt6.QtGui import QIcon

class NotificationManager:
    """Gère les notifications système"""
    
    @staticmethod
    def show_notification(title, message, duration=3000):
        """Affiche une notification système
        
        Args:
            title: Titre de la notification
            message: Contenu de la notification
            duration: Durée d'affichage en millisecondes
        """
        if QSystemTrayIcon.isSystemTrayAvailable():
            try:
                tray_icon = QSystemTrayIcon()
                tray_icon.setIcon(QIcon.fromTheme("audio-input-microphone"))
                tray_icon.show()
                tray_icon.showMessage(
                    title, 
                    message,
                    QSystemTrayIcon.MessageIcon.Information, 
                    duration)
            except Exception as e:
                print(f"Erreur lors de l'affichage de la notification: {e}")