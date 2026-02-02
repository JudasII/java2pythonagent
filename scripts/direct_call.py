from adapters.ollama_model import OllamaModel

model = OllamaModel(
    model_name="qwen3:4b",
    temperature=0.1,
)

response = model.generate([
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "can you tell me a good joke?"}
])

print(response)
