from google.adk.agents import LlmAgent
from google.adk.tools.agent_tool import AgentTool

from poc_agno.llm_model_config import MODEL_NAME_LLAMA_3

documentation_pro = LlmAgent(
    name="documentation_pro",
    model=MODEL_NAME_LLAMA_3,
    tools=[
        # add tools
    ]
)