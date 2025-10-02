"""Package des gestionnaires pour l'application de dictée vocale."""

from client_whisper.ui.managers.recording_manager import RecordingManager
from client_whisper.ui.managers.notification_manager import NotificationManager

__all__ = ['RecordingManager', 'NotificationManager']