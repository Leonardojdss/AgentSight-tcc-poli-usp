from langgraph.prebuilt import create_react_agent
from ms_agents_server.src.infrastructure.connection_openai import ConnectionAzureOpenai
from typing import Annotated
from langchain_core.tools import tool, InjectedToolCallId
from langgraph.prebuilt import InjectedState, create_react_agent
from langgraph.graph import MessagesState, END
from langgraph.types import Command
from langgraph.prebuilt import create_react_agent
from .tools import DatabaseSQLTool

llm = ConnectionAzureOpenai.llm_azure_openai()
tool_sql = DatabaseSQLTool().tool_sql()

class NetworkAgentsSupervisor:

    @staticmethod
    def prompt(path):
        with open(path, "r") as file:
            return file.read()

    @staticmethod
    def create_handoff_tool(*, agent_name: str, description: str | None = None):
        name = f"transfer_to_{agent_name}"
        description = description or f"Ask {agent_name} for help."

        @tool(name, description=description)
        def handoff_tool(
            state: Annotated[MessagesState, InjectedState],
            tool_call_id: Annotated[str, InjectedToolCallId],
        ) -> Command:
            tool_message = {
                "role": "tool",
                "content": f"Successfully transferred to {agent_name}",
                "name": name,
                "tool_call_id": tool_call_id,
            }
            return Command(
                goto=agent_name,  
                update={**state, "messages": state["messages"] + [tool_message]},  
                graph=Command.PARENT,  
            )

        return handoff_tool

    agent_descriptive_analysis_prompt = prompt("ms_agents_server/src/prompts/analise_descritiva_prompt.txt")

    @staticmethod
    async def agent_descriptive_analysis():
        descriptive_analysis_agent = create_react_agent(
            model=llm,
            tools=tool_sql,
            prompt=NetworkAgentsSupervisor.agent_descriptive_analysis_prompt,
            name="agent_descriptive_analysis",
        )
        return descriptive_analysis_agent

    assign_to_agent_descriptive_analysis = create_handoff_tool(
        agent_name="agent_descriptive_analysis",
        description="Atribuir tarefa a um agente de análise descritiva.",
    )

    agent_diagnostic_analysis_prompt = prompt("ms_agents_server/src/prompts/analise_diagnostica_prompt.txt")

    @staticmethod
    async def agent_diagnostic_analysis():
        diagnostic_analysis_agent = create_react_agent(
            model=llm,
            tools=tool_sql,
            prompt=NetworkAgentsSupervisor.agent_diagnostic_analysis_prompt,
            name="agent_diagnostic_analysis",
        )
        return diagnostic_analysis_agent


    assign_to_agent_diagnostic_analysis = create_handoff_tool(
        agent_name="agent_diagnostic_analysis",
        description="Atribuir tarefa a um agente de análise diagnóstica.",
    )

    agent_predictive_analysis_prompt = prompt("ms_agents_server/src/prompts/analise_preditiva_prompt.txt")

    @staticmethod
    async def agent_predictive_analysis():
        predictive_analysis_agent = create_react_agent(
            model=llm,
            tools=tool_sql,
            prompt=NetworkAgentsSupervisor.agent_predictive_analysis_prompt,
            name="agent_predictive_analysis",
        )
        return predictive_analysis_agent
    
    assign_to_agent_predictive_analysis = create_handoff_tool(
        agent_name="agent_predictive_analysis",
        description="Atribuir tarefa a um agente de análise preditiva.",
    )

    agent_prescriptive_analysis_prompt = prompt("ms_agents_server/src/prompts/analise_prescritiva_prompt.txt")

    @staticmethod
    async def agent_prescriptive_analysis():                    
        prescriptive_analysis_agent = create_react_agent(
            model=llm,
            tools=tool_sql,
            prompt=NetworkAgentsSupervisor.agent_prescriptive_analysis_prompt,
            name="agent_prescriptive_analysis",
        )
        return prescriptive_analysis_agent

    assign_to_agent_prescriptive_analysis = create_handoff_tool(
        agent_name="agent_prescriptive_analysis",
        description="Atribuir tarefa a um agente de análise prescritiva.",
    )

    prompt_agent_supervisor = prompt("ms_agents_server/src/prompts/supervisor_prompt.txt")

    @staticmethod
    def supervisor_analysis():
        supervisor_analysis_agent = create_react_agent(
            model=llm,
            tools=[
            NetworkAgentsSupervisor.assign_to_agent_descriptive_analysis,
            NetworkAgentsSupervisor.assign_to_agent_diagnostic_analysis,
            NetworkAgentsSupervisor.assign_to_agent_predictive_analysis,
            NetworkAgentsSupervisor.assign_to_agent_prescriptive_analysis
            ],
            prompt=NetworkAgentsSupervisor.prompt_agent_supervisor,
            name="supervisor_analysis"
        )
        return supervisor_analysis_agent