from agno.models.ollama import Ollama

model_llama = "llama3.2"
model_gemma = "gemma3:27b"

# Initialize the Ollama model
llm_model=Ollama(id=model_llama)