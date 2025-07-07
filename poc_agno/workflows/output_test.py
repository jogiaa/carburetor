from fastapi import FastAPI

from poc_agno.llm_model_config import llm_model

app = FastAPI()

@app.get('/ask')
def ask(prompt: str):
    """This function is used to ask the model a question and get the response from the language model.

Args:
    prompt (str): The input prompt for the model.

Returns:
    A dictionary containing the response from the language model."""
    return {'response': llm_model.invoke(prompt)}