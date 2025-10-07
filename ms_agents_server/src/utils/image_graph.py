import os
import asyncio
import aiofiles
from ms_agents_server.src.workflow_agentic.graph import GraphSupervisor

graph = GraphSupervisor()

class ImageGraph:
    
    @staticmethod
    async def generate_workflow_image():
        workflow_graph = await graph.analysis_supervisor_graph()
        graph_image = workflow_graph.get_graph().draw_mermaid_png()
        image_path = os.path.join("workflow_graph.png")
        async with aiofiles.open(image_path, "wb") as f:
            await f.write(graph_image)
            
if __name__ == "__main__":
    asyncio.run(ImageGraph.generate_workflow_image())