from smolagents import CodeAgent
from adapters.ollama_chat_model import OllamaChatModel
from prompts.system_prompt import SYSTEM_PROMPT

ollama_model = OllamaChatModel(
    model_name="qwen3:4b",
    system_prompt=SYSTEM_PROMPT,
)
agent = CodeAgent(
    model=ollama_model,
    tools= [],
    max_steps=5,
)

print(agent.run("System.out.println(\"Hello World!\")"))


