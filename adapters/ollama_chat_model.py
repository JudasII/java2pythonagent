from typing import List, Optional
import ollama
from smolagents.models import Model, ChatMessage


class OllamaChatModel(Model):
    """
    Ollama adapter with LEVEL 1 observability:

    - No streaming
    - No token-by-token output
    - Full final RAW snapshot (post-hoc)
    - Clean contract: text in / text out
    """

    def __init__(
        self,
        model_name: str,
        system_prompt: str,
        *,
        temperature: float = 0.2,
        show_raw: bool = True,
        include_thinking: bool = False,
    ):
        self.model_name = model_name
        self.system_prompt = system_prompt
        self.temperature = temperature
        self.show_raw = show_raw
        self.include_thinking = include_thinking

    def generate(
        self,
        messages: List[ChatMessage],
        stop_sequences: Optional[List[str]] = None,
        **kwargs
    ) -> ChatMessage:
        # 1. Build prompt deterministically
        prompt = self._messages_to_prompt(messages)

        # 2. Call Ollama (NO streaming)
        response = ollama.generate(
            model=self.model_name,
            prompt=prompt,
            stream=False,
            options={
                "temperature": self.temperature,
            },
        )

        # 3. LEVEL 1 OBSERVABILITY (final snapshot only)
        raw = response.model_dump(exclude_none=False)

        if self.show_raw:
            print("\n===== OLLAMA FINAL RAW OBJECT =====")
            for k, v in raw.items():
                if k == "context":
                    continue
                print(f"{k}={repr(v)}")
            print("==================================\n")

        # 4. Clean contract: extract assistant text only
        text = response.response or ""

        # 5. Apply stop sequences (defensive, optional)
        if stop_sequences:
            for stop in stop_sequences:
                if stop in text:
                    text = text.split(stop)[0]

        # 6. Optional thinking surfacing (DEV MODE ONLY)
        if self.include_thinking and response.thinking:
            text = (
                "<thinking>\n"
                + response.thinking.strip()
                + "\n</thinking>\n\n"
                + text
            )

        # 7. Return clean ChatMessage to the agent
        return ChatMessage(
            role="assistant",
            content=text.strip()
        )

    def _messages_to_prompt(self, messages: List[ChatMessage]) -> str:
        prompt = ""

        # 1. System contract
        prompt += self._content_to_text(self.system_prompt) + "\n\n"

        # 2. User input only (explicit)
        for m in messages:
            if m.role == "user":
                prompt += "INPUT JAVA CODE:\n"
                prompt += self._content_to_text(m.content) + "\n\n"

        # 3. Forced output contract
        prompt += "OUTPUT (Python code only or ERROR):\n"

        return prompt

    def _content_to_text(self, content) -> str:
        if isinstance(content, str):
            return content

        if isinstance(content, list):
            parts = []
            for item in content:
                if isinstance(item, str):
                    parts.append(item)
                elif isinstance(item, dict) and "text" in item:
                    parts.append(item["text"])
            return "\n".join(parts)

        return str(content)
