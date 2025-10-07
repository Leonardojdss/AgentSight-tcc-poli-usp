from langgraph.graph import StateGraph, START, MessagesState, END
from .agents import NetworkAgentsSupervisor


class GraphSupervisor:

    @staticmethod
    async def analysis_supervisor_graph():
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
            .compile()
        )
        
        return supervisor_graph