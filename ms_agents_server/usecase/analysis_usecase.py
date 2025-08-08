from ms_agents_server.graph.graph import GraphSupervisor
from ms_agents_server.service.messages_service import pretty_print_messages, pretty_print_tools_only
import logging

logging.basicConfig(level=logging.INFO)

async def conversation_analysis_usecase(input_message, show_tools_only=False):

    graph_supervisor_analysis = await GraphSupervisor.analysis_supervisor_graph()

    async for chunk in graph_supervisor_analysis.astream(
    {
        "messages": [
            {
                "role": "user",
                "content": f"{input_message}",
            }
        ]
        },
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
if __name__ == "__main__":
    import asyncio
    result = asyncio.run(conversation_analysis_usecase("acesse as compras do banco e preveja de forma simples qual cliente pode comprar bastante nos próximos meses."))
    print(result)