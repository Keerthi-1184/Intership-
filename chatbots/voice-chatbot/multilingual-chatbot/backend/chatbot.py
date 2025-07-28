# import requests

# def generate_response(prompt: str, model_name: str) -> str:
#     print(f"Prompt: {prompt}, Model: {model_name}")
#     """
#     Generate a response from the specified language model using a local model server (e.g., Ollama).

#     Parameters:
#     - prompt (str): The user's input text.
#     - model_name (str): Name of the model to use (e.g., 'deepseek-r1:1.5b').

#     Returns:
#     - str: The model's generated response text.
#     """
#     try:
#         # Post request to local Ollama/vLLM compatible endpoint
#         response = requests.post(
#             "http://localhost:11434/api/generate",
#             json={
#                 "model": model_name,
#                 "prompt": prompt,
#                 "stream": False
#             },
#             timeout=45
#         )

#         # If successful, parse response
#         if response.status_code == 200:
#             result = response.json()
#             return result.get("response", "No response generated.")
#         else:
#             print(f"Error {response.status_code}: {response.text}")
#             return f"Model returned error code {response.status_code}"

#     except requests.exceptions.Timeout:
#         return "Error: Model server timed out."
#     except requests.exceptions.ConnectionError:
#         return "Error: Cannot connect to the model server at localhost:11434."
#     except Exception as e:
#         print(f"Exception: {str(e)}")
#         return "Error: Failed to generate response from the model."

import requests
import logging
from typing import Optional

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def generate_response(prompt: str, model_name: str) -> str:
    try:
        logger.info(f"Sending prompt to model server: {prompt}, Model: {model_name}")
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": model_name, "prompt": prompt, "stream": False},
            timeout=60  # Increased from 45s
        )
        response.raise_for_status()
        result = response.json()
        if "response" not in result:
            logger.error(f"Model server response missing 'response' field: {result}")
            raise ValueError("Invalid response from model server")
        logger.info(f"Model response: {result['response']}")
        return result["response"]
    except requests.exceptions.Timeout:
        logger.error("Model server timed out")
        raise TimeoutError("Model server timed out")
    except requests.exceptions.ConnectionError as e:
        logger.error(f"Model server connection error: {str(e)}")
        raise ConnectionError(f"Model server connection error: {str(e)}")
    except Exception as e:
        logger.error(f"Error generating response: {str(e)}")
        raise