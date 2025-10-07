from fastapi import FastAPI
from ms_agents_server.src.controller.routes import route

app = FastAPI()

app.include_router(route, prefix="/ms_document_intelligence", tags=["Document Intelligence"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)