from fastapi import FastAPI, File, UploadFile, HTTPException
import torch
import whisper
import uvicorn
from faster_whisper import WhisperModel, BatchedInferencePipeline
import io
import numpy as np
import traceback
import logging
from typing import Optional
import sys
import tempfile
from pathlib import Path
import time
import re

# ⚡ Vire les suites de mots répétés (≥3 fois)
def dedup(text: str, max_repeat: int = 2) -> str:
    words = text.split()
    cleaned = []
    last = None
    streak = 0
    for w in words:
        if w.lower() == last:
            streak += 1
            if streak <= max_repeat:
                cleaned.append(w)
        else:
            last = w.lower()
            streak = 1
            cleaned.append(w)
    result = " ".join(cleaned)
    # Ajout : remplacer les doubles espaces par un saut de ligne
    result = result.replace("  ", "\n")
    return result

def insert_newlines_on_double_space(text: str) -> str:
    """Remplace chaque double espace par un saut de ligne."""
    return text.replace("  ", "\n")

# Configuration du système pour utiliser UTF-8
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("whisper-server")
logger.info("💬 Configuration avec encodage UTF-8")

app = FastAPI()

# 🔥 Charger le modèle Whisper UNE FOIS au démarrage
USE_GPU = torch.cuda.is_available()
logger.info(f"🚀 GPU disponible : {USE_GPU}")

model = None
try:
    model = WhisperModel(r"C:\Users\louis\models\whisper-large-v3-french\ctranslate2", device="cuda", compute_type="float16")
    logger.info("✅ Modèle chargé avec succès")
except Exception as e:
    logger.error(f"❌ Erreur lors du chargement du modèle: {e}")
    logger.error(traceback.format_exc())



@app.get("/ping")
async def ping():
    """Vérifie si le serveur est en ligne et si un modèle est chargé"""
    return {
        "status": "online",
        "model_loaded": model is not None,
        "gpu_available": USE_GPU,
        "device": "cuda" if USE_GPU else "cpu"
    }

@app.post("/transcribe/")
async def transcribe_audio(audio: UploadFile = File(...)):
    """ Reçoit un fichier audio et retourne la transcription """
    if model is None:
        logger.error("❌ Impossible de transcrire : modèle non chargé")
        raise HTTPException(status_code=503, detail="Modèle non chargé")

    # Save the uploaded file to a temporary location
    try:
        suffix = Path(audio.filename).suffix if audio.filename else ".tmp"
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file_obj:
            temp_file_path = Path(temp_file_obj.name)
            content = await audio.read()
            if not content:
                logger.error("❌ Fichier audio vide reçu")
                raise HTTPException(status_code=400, detail="Fichier audio vide")
            temp_file_obj.write(content)
            logger.info(f"🎤 Fichier audio temporaire créé: {temp_file_path}, Taille: {len(content)} octets")

    except Exception as e:
        logger.error(f"❌ Erreur lors de la création du fichier temporaire: {e}") 
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Erreur lors de la sauvegarde du fichier: {str(e)}")

    try:
        logger.info("🔍 Début de la transcription...")
        start_time = time.perf_counter()

        # Création d'un pipeline batché pour une meilleure utilisation du GPU
        batched_model = BatchedInferencePipeline(model=model)
        
        # Transcription using batched pipeline with batch_size=8
        segments, info = batched_model.transcribe(
            str(temp_file_path),
            batch_size=8,  # Utilisation du batching pour améliorer les performances
            beam_size=5,
            vad_filter=True,
            vad_parameters=dict(min_silence_duration_ms=500),
            temperature=[0.0, 0.2, 0.4],
            compression_ratio_threshold=2.4,
            best_of=5,
            language="fr"
        )

        # Extraction et traitement du texte
        texte = " ".join(seg.text for seg in segments)
        logger.info(f"📝 Transcription brute: {texte}...")
        # texte = dedup(texte)  # 🔥 post-dedup, fini les « Je Je Je … »
        texte = insert_newlines_on_double_space(texte)  # 🔥 saut de ligne sur double espace
        latency = time.perf_counter() - start_time
        logger.info(f"✅ Transcription réussie en {latency:.2f}s: {texte[:50]}...")

        return {"latency_s": round(latency, 2), "text": texte}

    except Exception as e:
        logger.error(f"❌ Erreur lors de la transcription: {e}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Erreur de transcription: {str(e)}")

    finally:
        # Ensure the temporary file is deleted
        if 'temp_file_path' in locals() and temp_file_path.exists():
            try:
                temp_file_path.unlink()
                logger.info(f"🗑️ Fichier temporaire supprimé: {temp_file_path}")
            except Exception as e:
                logger.error(f"⚠️ Erreur lors de la suppression du fichier temporaire {temp_file_path}: {e}")


if __name__ == "__main__":
    try:
        logger.info("🚀 Démarrage du serveur Whisper...")
        # Configuration d'Uvicorn pour utiliser UTF-8
        uvicorn.run(
            app, 
            host="0.0.0.0", 
            port=8000, 
            log_level="info",
            # Corrected log_config dictionary format
            log_config={
                "version": 1,
                "disable_existing_loggers": False, # Added to prevent conflicts
                "formatters": {
                    "default": {
                        "()": "uvicorn.logging.DefaultFormatter",
                        "fmt": "%(levelprefix)s %(asctime)s - %(message)s", # Simplified format
                        "use_colors": True,
                    },
                    "access": { # Added access formatter
                        "()": "uvicorn.logging.AccessFormatter",
                        "fmt": '%(levelprefix)s %(client_addr)s - "%(request_line)s" %(status_code)s',
                        "use_colors": True,
                    },
                },
                "handlers": {
                    "default": {
                        "formatter": "default",
                        "class": "logging.StreamHandler",
                        "stream": "ext://sys.stdout",
                    },
                    "access": { # Added access handler
                        "formatter": "access",
                        "class": "logging.StreamHandler",
                        "stream": "ext://sys.stdout",
                    },
                },
                "loggers": {
                    "uvicorn": {"handlers": ["default"], "level": "INFO", "propagate": False}, # Corrected logger config
                    "uvicorn.error": {"level": "INFO"}, # Corrected logger config
                    "uvicorn.access": {"handlers": ["access"], "level": "INFO", "propagate": False}, # Corrected logger config
                },
            },
        )
    except Exception as e: # Added except block
        logger.error(f"❌ Erreur lors du démarrage du serveur: {e}")
        logger.error(traceback.format_exc())
