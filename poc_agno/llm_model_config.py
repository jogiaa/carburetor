from agno.debug import enable_debug_mode
from agno.models.ollama import Ollama

MODEL_NAME_LLAMA_3 = "llama3.2"
MODEL_NAME_GEMMA_3_1B = "gemma3:1b"

MODEL_NAME_CODE_LLAMA_7b = "codellama:7b"

MODEL_NAME_CODE_GEMMA_7b = "codegemma:7b"

MODEL_NAME_DEEPSEEK_R_1_8B = "deepseek-r1:8b"
enable_debug_mode()

llm_model = Ollama(id=MODEL_NAME_LLAMA_3)

# this can work without tools option
code_model = Ollama(
    id=MODEL_NAME_CODE_GEMMA_7b,
    options={
        "temperature": 0.0,
        "top_p": 1.0,
        "frequency_penalty": 0.0,
        "presence_penalty": 0.0,
    }
)

# API-KEY - gpt-4o-mini
# openai_model = OpenAIChat(
#     id = "gpt-4o-mini",
#     api_key=get(OPEN_AI_API_KEY),
# )
