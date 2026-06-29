import logging
import requests
from typing import List, Dict, Any, Optional
from app.config import settings
from fastapi import HTTPException, status

logger = logging.getLogger("app.services.OllamaService")

class OllamaService:
    def __init__(self):
        self.base_url = settings.OLLAMA_BASE_URL
        self.model = settings.OLLAMA_MODEL

    def chat(self, messages: List[Dict[str, str]], options: Optional[Dict[str, Any]] = None) -> str:
        """
        Sends a list of role/content message dictionaries to the Ollama chat API.
        """
        url = f"{self.base_url}/api/chat"
        payload = {
            "model": self.model,
            "messages": messages,
            "stream": False
        }
        if options:
            payload["options"] = options

        try:
            logger.info(f"Sending request to Ollama model '{self.model}' at {url}")
            response = requests.post(url, json=payload, timeout=180.0)
            response.raise_for_status()
            
            result = response.json()
            # Extract content from response
            chat_response = result.get("message", {}).get("content", "")
            return chat_response
        except requests.exceptions.Timeout:
            logger.error("Ollama API request timed out.")
            raise HTTPException(
                status_code=status.HTTP_504_GATEWAY_TIMEOUT,
                detail="AI Model provider (Ollama) request timed out."
            )
        except requests.exceptions.ConnectionError:
            logger.error("Failed to connect to Ollama service. Ensure Ollama is running.")
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Unable to connect to Ollama service. Please make sure it is running."
            )
        except Exception as e:
            logger.error(f"Error querying Ollama API: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An error occurred while calling the AI model: {str(e)}"
            )

    def get_embedding(self, text: str) -> List[float]:
        """
        Retrieves vector embeddings for a given piece of text.
        """
        url = f"{self.base_url}/api/embeddings"
        payload = {
            "model": self.model,
            "prompt": text
        }
        try:
            response = requests.post(url, json=payload, timeout=10.0)
            response.raise_for_status()
            return response.json().get("embedding", [])
        except Exception as e:
            logger.warning(f"Failed to generate embedding from Ollama: {str(e)}")
            return []
