from langgraph.graph import StateGraph, START, MessagesState, END
from .agents import NetworkAgentsSupervisor
from ..utils.memory_manager import memory_manager
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GraphSupervisor:

    @staticmethod
    async def analysis_supervisor_graph(client_id: str = "default"):
        """
        Cria o grafo supervisor com memória de curto prazo isolada por client_id.
        
        Args:
            client_id: Identificador único do cliente para isolamento de memória
            
        Returns:
            Grafo compilado com checkpointer configurado
        """
        logger.info(f"Criando grafo supervisor para client_id: {client_id}")
        
        # Obter memória específica do cliente
        checkpointer = memory_manager.get_memory(client_id)
        
        supervisor_agent = NetworkAgentsSupervisor.supervisor_analysis()
        agent_descriptive = await NetworkAgentsSupervisor.agent_descriptive_analysis()
        agent_diagnostic = await NetworkAgentsSupervisor.agent_diagnostic_analysis()
        agent_predictive = await NetworkAgentsSupervisor.agent_predictive_analysis()
        agent_prescriptive = await NetworkAgentsSupervisor.agent_prescriptive_analysis()

        supervisor_graph = (
            StateGraph(MessagesState)
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