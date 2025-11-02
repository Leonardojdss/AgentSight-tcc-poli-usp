"""
Gerenciador de memória de curto prazo para agentes.
Mantém instâncias separadas de InMemorySaver por client_id.
"""
from langgraph.checkpoint.memory import InMemorySaver
from typing import Dict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MemoryManager:
    """
    Gerencia memória de curto prazo separada por client_id.
    Cada cliente tem sua própria instância de InMemorySaver.
    """
    
    def __init__(self):
        self._memories: Dict[str, InMemorySaver] = {}
    
    def get_memory(self, client_id: str) -> InMemorySaver:
        """
        Obtém ou cria uma instância de InMemorySaver para o client_id.
        
        Args:
            client_id: Identificador único do cliente
            
        Returns:
            InMemorySaver: Instância de memória para o cliente
        """
        if client_id not in self._memories:
            logger.info(f"Criando nova memória para client_id: {client_id}")
            self._memories[client_id] = InMemorySaver()
        
        return self._memories[client_id]


# Instância global do gerenciador de memória
memory_manager = MemoryManager()
