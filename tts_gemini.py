"""
tts_gemini.py
Module pour convertir du texte en audio (WAV) avec Gemini TTS.
"""

import os
import io
import wave

from google import genai
from google.genai import types

# Modèle TTS Gemini
GEMINI_TTS_MODEL = "gemini-2.5-flash-preview-tts"
VOICE_NAME_DEFAULT = "Kore"

SAMPLE_RATE = 24000
CHANNELS = 1
SAMPLE_WIDTH = 2  # 16 bits

_client: genai.Client | None = None


def _get_client() -> genai.Client:
    global _client
    if _client is None:
        api_key = os.getenv("GEMINI_KEY")
        if not api_key:
            raise RuntimeError(
                "GEMINI_KEY n'est pas défini dans l'environnement."
            )
        _client = genai.Client(api_key=api_key)
    return _client


def _pcm_to_wav_bytes(
    pcm: bytes,
    channels: int = CHANNELS,
    rate: int = SAMPLE_RATE,
    sample_width: int = SAMPLE_WIDTH,
) -> bytes:
    buffer = io.BytesIO()
    with wave.open(buffer, "wb") as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(sample_width)
        wf.setframerate(rate)
        wf.writeframes(pcm)
    return buffer.getvalue()


def text_to_speech(
    text: str,
    voice_name: str = VOICE_NAME_DEFAULT,
    as_wav: bool = True,
) -> bytes:
    if not text or not text.strip():
        raise ValueError("text_to_speech: le texte ne doit pas être vide.")

    client = _get_client()

    resp = client.models.generate_content(
        model=GEMINI_TTS_MODEL,
        contents=text,
        config=types.GenerateContentConfig(
            response_modalities=["AUDIO"],
            speech_config=types.SpeechConfig(
                voice_config=types.VoiceConfig(
                    prebuilt_voice_config=types.PrebuiltVoiceConfig(
                        voice_name=voice_name
                    )
                )
            ),
        ),
    )

    part = resp.candidates[0].content.parts[0].inline_data
    pcm_bytes: bytes = part.data

    if as_wav:
        return _pcm_to_wav_bytes(pcm_bytes)

    return pcm_bytes


if __name__ == "__main__":
    demo = "Bonjour, ici le Baron Jarvis. Je parle grâce à Gemini."
    audio = text_to_speech(demo, voice_name="Kore", as_wav=True)
    out = "jarvis_demo.wav"
    with open(out, "wb") as f:
        f.write(audio)
    print(f"Fichier généré : {out}")
