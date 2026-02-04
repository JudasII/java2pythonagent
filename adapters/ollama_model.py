import json

import requests
from typing import List, Dict, Any


class OllamaModel:
    """
    Low-level client for interacting with a local Ollama server via HTTP.

    This class is responsible only for:
    - Sending chat-style messages to Ollama
    - Returning the raw text response from the model

    It does NOT implement prompt engineering, agent logic, or framework-specific
    abstractions. Those concerns are handled at higher layers.
    """
    def __init__(
        self,
        model_name: str,
        base_url: str = "http://localhost:11434",
        temperature: float = 0.2,
        max_tokens: int = 1024,
        timeout: int = 60,
        stream: bool = True,
    ):
        """
        Initialize the Ollama model client.

        Args:
            stream: whether to show or not the trace of the response( debug mode )
            model_name: Name of the Ollama model to use (e.g. "qwen3:4b").
            base_url: Base URL of the Ollama server.
            temperature: Sampling temperature for generation.
            max_tokens: Maximum number of tokens to generate (mapped to Ollama's `num_predict`).
            timeout: HTTP request timeout in seconds.
        """
        self.stream = stream
        self.model_name = model_name
        self.base_url = base_url.rstrip("/")
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.timeout = timeout

    def _build_prompt(self, messages: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """
        Prepare messages for Ollama's chat API.

        Messages are expected to follow the format:
        [{ "role": "system" | "user" | "assistant", "content": "..." }]

        This method currently acts as a pass-through, but exists to allow
        future adaptation or normalization of message formats without
        changing the public API.
        """
        return messages

    def generate(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """
        Send a chat request to the Ollama server and return the raw text response.

        Args:
            messages: A list of role-based message dictionaries.
            **kwargs: Reserved for future extensions (ignored).

        Returns:
            The model's response as plain text.

        Raises:
            RuntimeError: If the HTTP request fails or returns an error.
        """
        payload = {
            "model": self.model_name,
            "messages": self._build_prompt(messages),
            "stream": False,
            "options": {
                "temperature": self.temperature,
                "num_predict": self.max_tokens,
            },
        }

        try:
            response = requests.post(
                f"{self.base_url}/api/chat",
                json=payload,
                stream=self.stream,
                timeout=self.timeout,
            )

            if self.stream:
                return self._parse_stream(response)
            else:
                return self._parse_non_stream(response)
        except requests.RequestException as e:
            raise RuntimeError(f"Ollama request failed: {e}")

    def _parse_stream(self, response) -> str:
        full_text = ""

        for line in response.iter_lines(decode_unicode=True):
            if not line:
                continue

            print("RAW:", line)

            chunk = json.loads(line)

            if "message" in chunk:
                content = chunk["message"].get("content")
                if content:
                    full_text += content + "\n\n"

            if chunk.get("done"):
                break

        return full_text

    def _parse_non_stream(self, response) -> str:
        data = response.json()
        return data["message"]["content"]
