from fastapi import FastAPI
from ms_agents_server.src.controller.routes import router

app = FastAPI()

app.include_router(router, prefix="/ms_agent_server", tags=["conversation analysis"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)