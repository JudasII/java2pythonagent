from adapters.ollama_model import OllamaModel
from prompts.system_prompt import TRANSLATE_THIS_CODE
from prompts.input_java import javaCode

model = OllamaModel(
    model_name="qwen3:4b",
    temperature=0.1,
)

response = model.generate([
    {"role": "system", "content": TRANSLATE_THIS_CODE},
    {"role": "user", "content": javaCode},
])

def extract_code_block(text: str) -> str:
    start = text.find("<code>")
    end = text.find("</code>")

    if start == -1 or end == -1:
        raise ValueError("No <code> block found")

    return text[start + 6 : end].strip()
def write_python_file(path: str, code: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        f.write(code)

python_code = extract_code_block(response)

write_python_file("../outputs/output.py", python_code)
print("✅ Translation written to output.py")

print(response)