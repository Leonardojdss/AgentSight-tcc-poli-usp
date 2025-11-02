import os
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.INFO)

load_dotenv()

class ConnectionAzureOpenai():
    
    @staticmethod
    def llm_azure_openai(model: str = "azure_openai:gpt-4.1"):
        llm = init_chat_model(
            model,
            azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
        )
        return llm
    
    @staticmethod
    def llm_openai_platform(model: str = "openai:gpt-4.1"):
        llm = init_chat_model(
            model,
            openai_api_key=os.getenv("OPENAI_API_KEY"),
        )
        return llm