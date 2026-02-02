from typing import List

import ollama
from smolagents.models import Model, ChatMessage


class OllamaChatModel(Model):
    """
    Adapter that allows smolagents to use a local Ollama model.

    This class translates smolagent's ChatMessage-based interface into
    a plain-text prompt compatible with Ollama, and converts the model
    response back into a ChatMessage.

    It enforces a strict prompt contract and is intentionally minimal:
    no tool calling, no reasoning orchestration, only text in / text out.
    """
    def __init__(self, model_name: str, system_prompt: str):
        """
        Initialize the Ollama-backed chat model.

        Args:
            model_name: Name of the Ollama model to use (e.g. "qwen3:4b").
            system_prompt: System-level prompt defining the translation contract.
        """
        self.system_prompt = system_prompt
        self.model_name = model_name

    def generate(
        self,
        messages: List[ChatMessage],
        stop_sequences=None,
        **kwargs
    ) -> ChatMessage:
        """
        Generate a response using the local Ollama model.

        This method:
        1. Converts ChatMessage objects into a single text prompt
        2. Sends the prompt to Ollama
        3. Converts the raw text response back into a ChatMessage

        Args:
            messages: List of ChatMessage objects provided by the agent.
            stop_sequences: Optional list of strings that truncate the output.
            **kwargs: Ignored (kept for interface compatibility).

        Returns:
            A ChatMessage containing the model's response.
        """

        prompt = self._messages_to_prompt(messages)

        response = ollama.generate(
            model=self.model_name,
            prompt=prompt,
            stream=False,
            options={
                "temperature": 0.2,
            }
        )

        text = response["response"]

        if stop_sequences:
            for stop in stop_sequences:
                if stop in text:
                    text = text.split(stop)[0]

        # ✅ DEVOLVER ChatMessage
        return ChatMessage(
            role="assistant",
            content=text.strip()
        )

    def _messages_to_prompt(self, messages: List[ChatMessage]):
        """
        Convert agent messages into a single text prompt for Ollama.

        Design decisions:
        - The system prompt is always prepended as a strict contract.
        - Only user messages are included in the prompt.
        - Agent thoughts or intermediate messages are intentionally ignored.

        This keeps the model behavior deterministic and avoids agent loops.
        """
        prompt = ""

        # 1. System prompt explícito (el contrato)
        text = self._content_to_text(self.system_prompt)
        prompt += text + "\n\n"

        # 2. Mensajes del agente
        for m in messages:
            if m.role == "user":
                prompt += "INPUT JAVA CODE:\n"
                prompt += self._content_to_text(m.content) + "\n\n"

        # 3. Forzar el formato de salida
        prompt += "OUTPUT (Python code only or ERROR):\n"

        return prompt

    def _content_to_text(self, content) -> str:
        """
        Normalize ChatMessage content into plain text.

        smolagents may represent content as strings, lists, or structured
        objects. This method extracts textual information and ensures
        compatibility with Ollama, which only accepts plain text prompts.
        """
        if isinstance(content, str):
            return content

        if isinstance(content, list):
            text_parts = []
            for item in content:
                if isinstance(item, str):
                    text_parts.append(item)
                elif isinstance(item, dict) and "text" in item:
                    text_parts.append(item["text"])
            return "\n".join(text_parts)

        return str(content)


