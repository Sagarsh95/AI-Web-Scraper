from langchain_community.llms import Ollama
import logging

logger = logging.getLogger(__name__)

class LLMClient:
    def __init__(self, model_name: str = "llama3.2", base_url: str = "http://localhost:11434"):
        self.output_parser = None # Future extension
        self.llm = Ollama(
            model=model_name,
            base_url=base_url,
            temperature=0  # Deterministic outputs for RAG
        )
        logger.info(f"LLM Client initialized with model: {model_name}")

    def generate_response(self, prompt_text: str) -> str:
        """
        Generates a direct response from the LLM.
        """
        try:
            response = self.llm.invoke(prompt_text)
            return response
        except Exception as e:
            logger.error(f"LLM Generation Error: {e}")
            return f"Error generating response: {str(e)}"

    def stream_response(self, prompt_text: str):
        """
        Yields tokens from the LLM.
        """
        try:
            for chunk in self.llm.stream(prompt_text):
                yield chunk
        except Exception as e:
            logger.error(f"LLM Streaming Error: {e}")
            yield f"Error streaming response: {str(e)}"

    def check_connection(self) -> bool:
        """
        Simple verify call.
        """
        try:
            self.llm.invoke("Hi")
            return True
        except Exception:
            return False
