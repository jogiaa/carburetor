from agno.models.ollama import Ollama

model_llama3 = "llama3.2"
model_llama4 = "llama4"
model_gemma327 = "gemma3:27b"
model_gemma31 = "gemma3:1b"


llm_model=Ollama(id=model_llama3)


# API-KEY - gpt-4o-mini
# openai_model = OpenAIChat(
#     id = "gpt-4o-mini",
#     api_key=get(OPEN_AI_API_KEY),
# )