import streamlit as st
from utils.message_stream import MessageStreamComportment
from modules.conversation.agent_conversation import ConversationHandler

# Inicializa o histórico de mensagens
if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.title("AgentSight")
    st.markdown("Bem-vindo ao AgentSight! Pergunte ao agente análitico qualquer coisa sobre os dados de vendas.")
    client_id = st.text_input("Insira seu Client ID:", value="default_client")

# Exibe todas as mensagens anteriores
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Pergunte ao agente análitico qualquer coisa sobre os dados de vendas.")

if prompt and client_id:
    # Adiciona mensagem do usuário ao histórico
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Envia mensagem e recebe resposta
    conversation_handler = ConversationHandler(client_id=client_id, message=prompt)
    analysis_request = conversation_handler.send_message()
    
    # Exibe resposta do assistente com efeito de streaming
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        for chunk in MessageStreamComportment.stream_data(analysis_request):
            full_response += chunk
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    
    # Adiciona resposta do assistente ao histórico
    st.session_state.messages.append({"role": "assistant", "content": full_response})