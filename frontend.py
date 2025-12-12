import streamlit
from conversation_agent import ConversationAgent 
from config import LLM_MODELS
from tts_gemini import text_to_speech


if "conversation_agent" not in streamlit.session_state:
    streamlit.session_state.conversation_agent = ConversationAgent()


@streamlit.cache_data(show_spinner=False)
def get_tts_audio(text: str) -> bytes:
    """Cache le TTS pour ne pas regénérer l'audio à chaque rerun."""
    return text_to_speech(text)


def init_header():
    streamlit.set_page_config(page_title="Jarvis", page_icon="🤖")
    streamlit.title("🤖 Jarvis ton baron préféré !")
    streamlit.write("Il est un peu enervé, fais attention à ce que tu racontes...")


def show_discussion_history(history_placeholder):
    container = history_placeholder.container()
    with container:
        for message in streamlit.session_state.conversation_agent.history:
            if message["role"] != "system":
                with streamlit.chat_message(message["role"]):
                    streamlit.write(message["content"])
                    if message["role"] == "assistant":
                        audio_bytes = get_tts_audio(message["content"])
                        streamlit.audio(audio_bytes, format="audio/wav")


def user_interface():
    init_header()
    history_placeholder = streamlit.empty()
    show_discussion_history(history_placeholder)

    with streamlit.container():

        user_input = streamlit.chat_input("N'oublie pas à qui tu parle !")

        _, col2 = streamlit.columns([2, 1])
        with col2:
            streamlit.empty()
            selected_model = streamlit.selectbox(
                "Choisis ton modèle gamin...", LLM_MODELS
            )
            audio_file = streamlit.audio_input(
                "🎤 Note vocale", label_visibility="collapsed"
            )

    # TEXTE
    if user_input:
        streamlit.session_state.conversation_agent.ask_llm(
            user_interaction=user_input,
            model=selected_model,
        )
        show_discussion_history(history_placeholder)

    # AUDIO (note vocale)
    if audio_file is not None:
        audio_bytes = audio_file.read()
        mime_type = audio_file.type
        extension = mime_type.split("/")[-1]
        filename = f"audio.{extension}"

        streamlit.session_state.conversation_agent.ask_llm_from_audio(
            audio_bytes=audio_bytes,
            model=selected_model,
            mime_type="audio/wav",
            filename=filename,
        )
        show_discussion_history(history_placeholder)


if __name__ == "__main__":
    user_interface()