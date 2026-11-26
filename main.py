
from fastapi import FastAPI
from routers.chat import router as chat_router

app = FastAPI(
    title="Cortex AI Chatbot",
    description="A local AI chatbot powered by Ollama",
    version="1.0.0"
)


@app.get("/")
async def home():
    return {
        "message": "Cortex AI is running",
        "status": "online"
    }


app.include_router(chat_router)
