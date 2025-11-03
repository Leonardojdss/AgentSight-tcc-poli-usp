import requests
from dotenv import load_dotenv
from utils.default_messages import FALLBACK_MESSAGE
import os

load_dotenv()

class ConversationHandler:
    def __init__(self, client_id: str, message: str):
        self.api_url = os.getenv("AGENT_API_URL", "http://localhost:8000/ms_agent_server/V1/agent_conversation/")
        self.client_id = client_id
        self.message = message

    def send_message(self) -> str:
        try:
            json = {
                "message_input": self.message,
                "client_id": self.client_id
            }
            response = requests.post(self.api_url, json=json)
            response.raise_for_status()
            return response.json().get("message", "")
        except Exception as e:
            print(f"Erro ao enviar mensagem para o agente: {e}")
            return FALLBACK_MESSAGE