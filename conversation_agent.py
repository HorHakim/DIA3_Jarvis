from groq import Groq
from dotenv import load_dotenv
import os
import base64
from io import BytesIO

# TTS (Gemini)
try:
    from google import genai
    from google.genai import types as genai_types
except ImportError:
    genai = None
    genai_types = None

# Fallback gTTS
try:
    from gtts import gTTS
except ImportError:
    gTTS = None


class ConversationAgent:
    def __init__(self):
        load_dotenv()
        self.client = Groq(api_key=os.environ["GROQ_KEY"])
        self.gemini_key = os.getenv("GEMINI_KEY")
        self.tts_client = genai.Client(api_key=self.gemini_key) if genai and self.gemini_key else None
        self.initiate_history()


    @staticmethod
    def read_file(file_path):
        with open(file_path , "r") as file:
            return file.read()


    def initiate_history(self):
        self.history = [
            {
                "role": "system",
                "content": ConversationAgent.read_file("./context.txt")
            }]


    def update_history(self, role, content):
         self.history.append(
                {
                    "role": role,
                    "content": content,
                })


    def synthesize_tts(self, text, voice_name: str = "Kore"):
        """Convertit le texte en audio via Gemini TTS, sinon fallback gTTS.
        Retourne dict {data, mime_type} ou None.
        """
        # Tentative Gemini
        if self.tts_client and genai_types:
            try:
                resp = self.tts_client.models.generate_content(
                    model="gemini-2.5-flash-preview-tts",
                    contents=text,
                    config=genai_types.GenerateContentConfig(
                        response_modalities=["AUDIO"],
                        speech_config=genai_types.SpeechConfig(
                            voice_config=genai_types.VoiceConfig(
                                prebuilt_voice_config=genai_types.PrebuiltVoiceConfig(
                                    voice_name=voice_name,
                                )
                            )
                        ),
                    ),
                )
                part = resp.candidates[0].content.parts[0].inline_data
                audio_bytes = part.data
                mime_type = getattr(part, "mime_type", None) or "audio/wav"

                # Normalisation du payload
                if isinstance(audio_bytes, str):
                    audio_bytes = base64.b64decode(audio_bytes)
                elif isinstance(audio_bytes, memoryview):
                    audio_bytes = audio_bytes.tobytes()

                if audio_bytes and len(audio_bytes) > 0:
                    if "mpeg" in mime_type or "mp3" in mime_type:
                        mime_type = "audio/mpeg"
                    elif "wav" in mime_type or "wave" in mime_type:
                        mime_type = "audio/wav"
                    return {"data": audio_bytes, "mime_type": mime_type}
            except Exception:
                pass

        # Fallback gTTS
        if gTTS:
            try:
                buf = BytesIO()
                gTTS(text=text, lang="fr").write_to_fp(buf)
                audio_bytes = buf.getvalue()
                if audio_bytes and len(audio_bytes) > 0:
                    return {"data": audio_bytes, "mime_type": "audio/mpeg"}
            except Exception:
                pass

        return None


    def ask_llm(self, user_interaction, model, include_audio: bool = False):

        self.update_history(role="user", content=user_interaction)

        response = self.client.chat.completions.create(
            messages=self.history,
            model=model
        ).choices[0].message.content
        
        self.update_history(role="assistant", content=response)

        if include_audio:
            audio_payload = self.synthesize_tts(response)
            if audio_payload:
                return {
                    "text": response,
                    "audio": audio_payload["data"],
                    "audio_len": len(audio_payload["data"]),
                    "mime_type": audio_payload.get("mime_type", "audio/wav"),
                }
            return {"text": response, "audio": None, "audio_len": 0}

        return response



    def terminal_user_interface(self, model):
        while True:
            user_interaction = input("Vous : ")
            if user_interaction.lower() == "exit":
                break
            elif user_interaction == "":
                print("Jarvis : Vous n'avez rien à dire ?")
            else:
                response = self.ask_llm(user_interaction=user_interaction, model=model)
                print(f"Jarvis : {response}")





if __name__ == "__main__":
    conversation_agent = ConversationAgent()
    conversation_agent.terminal_user_interface(model="openai/gpt-oss-120b")