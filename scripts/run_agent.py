from smolagents import CodeAgent
from adapters.ollama_chat_model import OllamaChatModel
from prompts.system_prompt import SYSTEM_PROMPT, TRANSLATE_WITH_TOOLS

ollama_model = OllamaChatModel(
    model_name="qwen3:4b",
    system_prompt=TRANSLATE_WITH_TOOLS,
    show_raw=True,
    include_thinking=False,
)
agent = CodeAgent(
    model=ollama_model,
    tools= [],
    max_steps=5,
)

print(agent.run("System.out.println(\"Hello World!\")"))


