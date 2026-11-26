from fastapi import FastAPI, HTTPException
import httpx


app = FastAPI(title="Cortex AI Chatbot")

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "qwen3:0.6b"

@app.get("/")
async def home():
    return {"message" : "Cortex AI is running"}

@app.post("/chat")
async def chat(message: str):

    payload = {
        "model" : MODEL,
        "messages": [
            {
                "role": "user",
                "content": message
            }
        ],
        "stream": False
    }
    try: 
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(
                OLLAMA_URL,
                json=payload
        )

            response.raise_for_status()

            # Inspect the raw response before parsing JSON
            print("OLLAMA RESPONSE:", response.text[:500])

            result = response.json()

            return {
                "user_message": message,
                "response": result["message"]["content"]
            }

            result = response.json()

            return {
                "user_message": message,
                "response": result["message"]["content"]
            }
    except httpx.HTTPError as error:
        raise HTTPException(status_code=502, detail=str(error))

    except (ValueError, KeyError) as error:
        raise HTTPException(
            status_code=502,
            detail=f"Invalid Ollama response: {error}"
        )