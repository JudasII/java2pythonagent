from smolagents import CodeAgent
from adapters.ollama_chat_model import OllamaChatModel
from prompts.system_prompt import TRANSLATION_CONTRACT_WITH_TOOLS, TRANSLATE_WITH_TOOLS
from tools.io_tools import iotool,usefulliotool,readfile, writefile

ollama_model = OllamaChatModel(
    model_name="qwen3:4b",
    system_prompt=TRANSLATION_CONTRACT_WITH_TOOLS,
    show_raw=True,
    include_thinking=False,
)
agent = CodeAgent(
    model=ollama_model,
    tools= [readfile,writefile],
    max_steps=3,
)

print(agent.run("translate the content of ../inputs/HelloWorld.java"))
