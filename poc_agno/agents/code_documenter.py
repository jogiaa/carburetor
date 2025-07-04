from textwrap import dedent

from pydantic import BaseModel

from poc_agno.llm_model_config import llm_model, code_model
from agno.agent import Agent


class DocumentedResult(BaseModel):
    original_code: str
    modified_code: str


# Single-agent system that adds doc comments to code snippets
code_doc_agent = Agent(
    name="Code Documentation Agent",
    role="Add documentation comments to functions, methods, or classes",
    model=code_model,
    instructions="""
    You are a code documentation assistant. Given a code snippet (in any language),
    identify the language and annotate it with appropriate documentation comments.

    Use:
    - appropriate documentation comments to identify the language and annotate it with appropriate documentation comments
    - Proper formatting
    - If code is in Kotlin then use KDoc conventions
    - If its Python code then use Python conventions to be used with Sphinx
    Only add comments where needed (before function, class, params).
    Never change the actual code logic.
    """,
    response_model=DocumentedResult,
    show_tool_calls=False,
    markdown=True,
)

if __name__ == "__main__":
    response = code_doc_agent.run(f"Add comments to {dedent("""
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

    
    """)} ")
    print(response.content.modified_code)
