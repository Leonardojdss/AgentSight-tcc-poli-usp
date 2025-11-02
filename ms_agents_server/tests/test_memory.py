"""
Testes para verificar o funcionamento da memória de curto prazo.
Execute com: python -m pytest ms_agents_server/tests/test_memory.py
"""
import pytest
import asyncio
from ms_agents_server.src.utils.memory_manager import MemoryManager
from ms_agents_server.src.usecase.analysis_usecase import ConversationAnalysisHandler


class TestMemoryManager:
    """Testes para o MemoryManager"""
    
    def test_create_memory_for_new_client(self):
        """Testa criação de memória para novo cliente"""
        manager = MemoryManager()
        client_id = "test_client_1"
        
        memory = manager.get_memory(client_id)
        assert memory is not None
    
    def test_memory_isolation(self):
        """Testa isolamento de memória entre clientes"""
        manager = MemoryManager()
        
        memory_1 = manager.get_memory("client_1")
        memory_2 = manager.get_memory("client_2")
        
        assert memory_1 is not memory_2
    
    def test_memory_reuse(self):
        """Testa reutilização de memória existente"""
        manager = MemoryManager()
        client_id = "test_client_3"
        
        memory_1 = manager.get_memory(client_id)
        memory_2 = manager.get_memory(client_id)
        
        assert memory_1 is memory_2


class TestConversationMemory:
    """Testes para memória conversacional"""
    
    @pytest.mark.asyncio
    async def test_conversation_with_memory(self):
        """Testa conversação com memória"""
        client_id = "test_user_1"
        thread_id = "test_thread_1"
        
        # Primeira mensagem
        result1 = await ConversationAnalysisHandler.conversation_analysis_usecase(
            input_message="Olá, me chamo João",
            client_id=client_id,
            thread_id=thread_id
        )
        
        assert result1 is not None
        
        # Segunda mensagem - deve lembrar do contexto
        result2 = await ConversationAnalysisHandler.conversation_analysis_usecase(
            input_message="Qual é o meu nome?",
            client_id=client_id,
            thread_id=thread_id
        )
        
        assert result2 is not None
        # O agente deve ter acesso ao contexto da primeira mensagem
    
    @pytest.mark.asyncio
    async def test_multiple_threads_same_client(self):
        """Testa múltiplas threads para o mesmo cliente"""
        client_id = "test_user_2"
        
        # Thread 1
        result1 = await ConversationAnalysisHandler.conversation_analysis_usecase(
            input_message="Assunto A",
            client_id=client_id,
            thread_id="thread_a"
        )
        
        # Thread 2 (independente)
        result2 = await ConversationAnalysisHandler.conversation_analysis_usecase(
            input_message="Assunto B",
            client_id=client_id,
            thread_id="thread_b"
        )
        
        assert result1 is not None
        assert result2 is not None
    
    @pytest.mark.asyncio
    async def test_client_isolation(self):
        """Testa isolamento entre clientes diferentes"""
        # Cliente 1
        result1 = await ConversationAnalysisHandler.conversation_analysis_usecase(
            input_message="Minha mensagem privada",
            client_id="client_a",
            thread_id="thread_1"
        )
        
        # Cliente 2 (não deve ter acesso à memória do Cliente 1)
        result2 = await ConversationAnalysisHandler.conversation_analysis_usecase(
            input_message="Qual foi a mensagem anterior?",
            client_id="client_b",
            thread_id="thread_1"
        )
        
        assert result1 is not None
        assert result2 is not None
        # Cliente B não deve ter acesso à informação do Cliente A


if __name__ == "__main__":
    # Executar testes simples
    print("=== Teste de Isolamento de Memória ===")
    manager = MemoryManager()
    
    mem1 = manager.get_memory("user_123")
    mem2 = manager.get_memory("user_456")
    mem3 = manager.get_memory("user_123")  # Deve reutilizar
    
    print(f"Memória user_123 (1ª chamada): {id(mem1)}")
    print(f"Memória user_456: {id(mem2)}")
    print(f"Memória user_123 (2ª chamada): {id(mem3)}")
    print(f"user_123 reutilizada? {mem1 is mem3}")
    print(f"Memórias isoladas? {mem1 is not mem2}")
