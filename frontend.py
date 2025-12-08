import streamlit
from conversation_agent import ConversationAgent 

if "conversation_agent" not in streamlit.session_state :
	streamlit.session_state.conversation_agent = ConversationAgent()


def init_header():
	# initialisation de la page
	streamlit.set_page_config(page_title="Jarvis", page_icon="🤖")
	streamlit.title("🤖 Jarvis ton baron préféré !")
	streamlit.write("Il est un peu enervé, fais attention à ce que tu racontes...")



def show_discussion_history():
	for message in streamlit.session_state.conversation_agent.history:
		if message["role"] != "system":
			with streamlit.chat_message(message["role"]):
				streamlit.write(message["content"])



def user_interface():
	init_header()
	user_input = streamlit.chat_input("N'oublie pas à qui tu parle !")
	if user_input:
		streamlit.session_state.conversation_agent.ask_llm(user_interaction=user_input)
		show_discussion_history()

if __name__ == "__main__":
	user_interface()
