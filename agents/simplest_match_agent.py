from agno.tools.calculator import CalculatorTools
from agno.agent import Agent

from llm_model_config import llm_model

math_agent = Agent(
    name="Math Agent",
    role="Perform mathematical calculations",
    model=llm_model,
    tools=[CalculatorTools()],
    # instructions="Show all steps in calculations",
    instructions="Use markdown for mathematical expressions and all the steps in calculations",
    show_tool_calls=False,
    markdown=False,
)
