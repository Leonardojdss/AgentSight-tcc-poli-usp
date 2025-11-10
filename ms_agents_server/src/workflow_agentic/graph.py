from langgraph.graph import StateGraph, START, MessagesState, END
from langgraph.graph.message import add_messages
from typing import Annotated, TypedDict
from langchain_core.messages import AnyMessage, AIMessage, ToolMessage
from .agents import NetworkAgentsSupervisor
from ..utils.memory_manager import memory_manager
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GraphSupervisor:

    @staticmethod
    def create_messages_reducer(max_messages: int = 6):
        """
        Cria um reducer de mensagens com limite configurável.
        
        Remove tool messages órfãs para evitar erros de validação do OpenAI.
        
        Args:
            max_messages: Número máximo de mensagens a manter (padrão: 6)
            
        Returns:
            Função reducer configurada
        """
        def limit_messages_reducer(left: list[AnyMessage], right: list[AnyMessage]) -> list[AnyMessage]:
            """Reducer que adiciona e limita mensagens de forma segura."""
            # Primeiro, usa o comportamento padrão de add_messages
            combined = add_messages(left, right)
            
            # Se não exceder o limite, retorna tudo
            if len(combined) <= max_messages:
                return combined
            
            # Limita às últimas N mensagens
            trimmed = combined[-max_messages:]
            
            # Remove tool messages órfãs (sem AI message com tool_calls correspondente)
            cleaned = GraphSupervisor._remove_orphan_tool_messages(trimmed)
            
            return cleaned
        
        return limit_messages_reducer

    @staticmethod
    def _remove_orphan_tool_messages(messages: list[AnyMessage]) -> list[AnyMessage]:
        """
        Remove tool messages que não têm uma AI message com tool_calls correspondente.
        
        Isso evita o erro: "messages with role 'tool' must be a response to a
        preceeding message with 'tool_calls'"
        """
        if not messages:
            return messages
        
        # Coleta todos os tool_call_ids válidos
        valid_tool_call_ids = GraphSupervisor._collect_valid_tool_call_ids(messages)
        
        # Filtra tool messages órfãs
        return GraphSupervisor._filter_orphan_tools(messages, valid_tool_call_ids)
    
    @staticmethod
    def _collect_valid_tool_call_ids(messages: list[AnyMessage]) -> set:
        """Coleta IDs de tool calls das AI messages."""
        valid_ids = set()
        
        for msg in messages:
            if not isinstance(msg, AIMessage):
                continue
            
            if not hasattr(msg, 'tool_calls') or not msg.tool_calls:
                continue
            
            for tool_call in msg.tool_calls:
                tool_id = tool_call.get('id') if isinstance(tool_call, dict) else getattr(tool_call, 'id', None)
                if tool_id:
                    valid_ids.add(tool_id)
        
        return valid_ids
    
    @staticmethod
    def _filter_orphan_tools(messages: list[AnyMessage], valid_tool_call_ids: set) -> list[AnyMessage]:
        """Filtra tool messages órfãs."""
        cleaned_messages = []
        orphan_count = 0
        
        for msg in messages:
            if isinstance(msg, ToolMessage):
                tool_call_id = getattr(msg, 'tool_call_id', None)
                if tool_call_id and tool_call_id in valid_tool_call_ids:
                    cleaned_messages.append(msg)
                else:
                    orphan_count += 1
            else:
                cleaned_messages.append(msg)
        
        if orphan_count > 0:
            logger.info(f"Removidas {orphan_count} tool messages órfãs")
        
        return cleaned_messages

    @staticmethod
    def create_state_with_limit(max_messages: int = 6):
        """
        Cria uma classe de estado customizada com limite de mensagens configurável.
        
        Args:
            max_messages: Número máximo de mensagens a manter (padrão: 6)
            
        Returns:
            Classe de estado customizada
        """
        reducer = GraphSupervisor.create_messages_reducer(max_messages)
        
        class LimitedMessagesState(TypedDict):
            """Estado customizado com limite de mensagens."""
            messages: Annotated[list[AnyMessage], reducer]
        
        return LimitedMessagesState

    @staticmethod
    async def analysis_supervisor_graph(client_id: str = "default", max_messages: int = 6):
        """
        Cria o grafo supervisor com memória de curto prazo isolada por client_id.
        
        Args:
            client_id: Identificador único do cliente para isolamento de memória
            max_messages: Número máximo de mensagens a manter no contexto (padrão: 6)
            
        Returns:
            Grafo compilado com checkpointer configurado
        """
        logger.info(f"Criando grafo supervisor para client_id: {client_id}")
        
        # Obter memória específica do cliente
        checkpointer = memory_manager.get_memory(client_id)
        
        # Criar estado customizado com limite de mensagens
        state_class = GraphSupervisor.create_state_with_limit(max_messages)
        
        supervisor_agent = NetworkAgentsSupervisor.supervisor_analysis()
        agent_descriptive = await NetworkAgentsSupervisor.agent_descriptive_analysis()
        agent_diagnostic = await NetworkAgentsSupervisor.agent_diagnostic_analysis()
        agent_predictive = await NetworkAgentsSupervisor.agent_predictive_analysis()
        agent_prescriptive = await NetworkAgentsSupervisor.agent_prescriptive_analysis()

        supervisor_graph = (
            StateGraph(state_class)  # Usando estado dinâmico
            .add_node("supervisor_analysis", supervisor_agent)
            .add_node("agent_descriptive_analysis", agent_descriptive)
            .add_node("agent_diagnostic_analysis", agent_diagnostic)
            .add_node("agent_predictive_analysis", agent_predictive)
            .add_node("agent_prescriptive_analysis", agent_prescriptive)
            .add_edge(START, "supervisor_analysis")
            .add_edge("agent_descriptive_analysis", "supervisor_analysis")
            .add_edge("agent_diagnostic_analysis", "supervisor_analysis")
            .add_edge("agent_predictive_analysis", "supervisor_analysis")
            .add_edge("agent_prescriptive_analysis", "supervisor_analysis")
            .add_edge("supervisor_analysis", END)
            .compile(checkpointer=checkpointer)
        )
        
        return supervisor_graph