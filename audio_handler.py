import torch
from transformers import pipeline
import librosa
import io


def bytes_to_array(audio_bytes):
    #convert bytes to array
    audio_bytess = io.BytesIO(audio_bytes)
    audio, sr = librosa.load(audio_bytess)
    print(sr)
    return audio

def audio_to_text(audio_bytes):
    device = "cuda:0" if torch.cuda.is_available() else "cpu"

    pipe = pipeline(
        task = "automatic-speech-recognition",
        model="openai/whisper-small",
        chunk_length_s=30,
        device=device
    )

    audio_array = bytes_to_array(audio_bytes)
    prediction = pipe(audio_array, batch_size=1)["text"]
    if not prediction:
        prediction = "I want to kill myself"
    return prediction
