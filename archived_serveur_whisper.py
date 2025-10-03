from fastapi import FastAPI, File, UploadFile
import torch
import whisper
import uvicorn
from faster_whisper import WhisperModel
import soundfile as sf
import io
import numpy as np
import sys
import os
from pathlib import Path

# Ajouter le chemin du client pour accéder au gestionnaire de mappings
sys.path.insert(0, str(Path(__file__).parent))

from mappings import list_mapping
from client_whisper.user_mappings import UserMappingsManager

app = FastAPI()

# Gestionnaire de mappings utilisateur
mappings_manager = UserMappingsManager()

# 🔥 Charger le modèle Whisper UNE FOIS au démarrage
USE_GPU = torch.cuda.is_available()
print(f"🚀 GPU disponible : {USE_GPU}")

# model = whisper.load_model(r"C:\Users\louis\.cache\whisper\large-v3-french.pt")
model = WhisperModel(r"C:\Users\louis\models\whisper-large-v3-french\ctranslate2", device="cuda", compute_type="float16")  # Run on GPU with FP16

# if USE_GPU:
#     model = model.to("cuda")
if model:
    print("✅ Modèle chargé avec succès")
# print("✅ Modèle chargé avec succès")

@app.post("/transcribe/")
async def transcribe_audio(audio: UploadFile = File(...)):
    """ Reçoit un fichier audio et retourne la transcription """
    print("🎤 Réception du fichier audio...")

    # Optimiser la lecture audio
    audio_data = await audio.read()
    audio_array, sr = sf.read(io.BytesIO(audio_data))
    
    # Conversion optimisée
    if len(audio_array.shape) > 1:
        audio_array = audio_array.mean(axis=1)  # Convert to mono if stereo
    
    # Normalisation plus rapide
    audio_array = audio_array.astype(np.float32) / np.max(np.abs(audio_array))

    # 🔥 Transcription
    segments, info = model.transcribe(audio_array, beam_size=2)

    # 🔥 Extraction du texte
    texte = " ".join(segment.text for segment in segments).replace("  ", "\n")

    # 🔥 Remplacement des mots (chargement dynamique des mappings)
    all_mappings = mappings_manager.get_all_mappings()
    for mapping in all_mappings:
        texte = texte.replace(mapping[0], mapping[1])

    print(f"✅ Transcription : {texte}")
    return {"text": texte}

@app.get("/health")
async def health_check():
    """Endpoint pour vérifier que le serveur fonctionne"""
    return {"status": "ok", "mappings_count": len(mappings_manager.get_all_mappings())}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)