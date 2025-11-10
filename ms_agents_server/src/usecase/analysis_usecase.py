from ms_agents_server.src.workflow_agentic.graph import GraphSupervisor
from langfuse.langchain import CallbackHandler
from ms_agents_server.src.service.messages_service import pretty_print_messages, pretty_print_tools_only
from ms_agents_server.src.utils.memory_manager import memory_manager
import logging
import uuid

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
 
# Initialize the Langfuse handler
# langfuse_handler = CallbackHandler()

class ConversationAnalysisHandler:
    """
    Class for handling conversation analysis use case.
    """
    
    @staticmethod
    async def conversation_analysis_usecase(
        input_message: str, 
        client_id: str,
        thread_id: str = None,
        show_tools_only: bool = False,
        max_messages: int = 6
    ):
        """
        Processa análise conversacional com memória de curto prazo isolada por cliente.
        
        Args:
            input_message: Mensagem de entrada do usuário
            client_id: Identificador único do cliente (obrigatório para isolamento de memória)
            thread_id: Identificador da thread de conversação (opcional, será gerado se não fornecido)
            show_tools_only: Se True, mostra apenas as chamadas de ferramentas
            max_messages: Número máximo de mensagens a manter no contexto (padrão: 6)
            
        Returns:
            str: Resposta do agente
        """
        # Gerar thread_id único se não fornecido
        if thread_id is None:
            thread_id = client_id
                
        # Criar grafo com memória específica do cliente e limite de mensagens
        graph_supervisor_analysis = await GraphSupervisor.analysis_supervisor_graph(
            client_id=client_id,
            max_messages=max_messages
        )

        # Configuração com thread_id para isolar conversas
        config = {
            #"callbacks": [langufuse_handler],  
            "configurable": {
                "thread_id": thread_id
            }
        }

        async for chunk in graph_supervisor_analysis.astream(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": f"{input_message}",
                    }
                ]
            },
            config=config
        ):
            if show_tools_only:
                pretty_print_tools_only(chunk)
            else:
                pretty_print_messages(chunk, last_message=False)

        final_message_history = chunk["supervisor_analysis"]["messages"]
        if final_message_history and len(final_message_history) > 0:
            last_message = final_message_history[-1]
            if hasattr(last_message, 'content'):
                return last_message.content
            else:
                return str(last_message)
        
        return "Nenhuma resposta encontrada"

# teste
# if __name__ == "__main__":
#     import asyncio
# 
#     test_client_id = "client_123"
#     result = asyncio.run(ConversationAnalysisHandler.conversation_analysis_usecase(
#         input_message="""
#         qual é o nome da companhia que mais teve vendas convertidas? faça uma análise descritiva e preditiva.
#         """,
#         client_id=test_client_id
#     ))