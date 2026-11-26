
import httpx
from fastapi import HTTPException

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "qwen3:0.6b"


async def generate_response(message: str) -> str:

    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "user",
                "content": message
            }
        ],
        "stream": False
    }

    try:
        async with httpx.AsyncClient(timeout=180.0) as client:

            response = await client.post(
                OLLAMA_URL,
                json=payload
            )

            response.raise_for_status()

            result = response.json()

            return result["message"]["content"]

    except httpx.ConnectError:
        raise HTTPException(
            status_code=503,
            detail="Cannot connect to Ollama. Make sure it is running."
        )

    except httpx.TimeoutException:
        raise HTTPException(
            status_code=504,
            detail="The AI model took too long to respond."
        )

    except httpx.HTTPStatusError as error:
        raise HTTPException(
            status_code=502,
            detail=f"Ollama error: {error.response.text}"
        )

    except (ValueError, KeyError):
        raise HTTPException(
            status_code=502,
            detail="Invalid response received from Ollama."
        )
