from agno.team import Team

from agents.simplest_match_agent import math_agent
from agents.web_search_ddg_agent import web_agent
from llm_model_config import llm_model

agent_team = Team(
    mode="coordinate",
    members=[web_agent, math_agent],
    model=llm_model,
    description="I search for recipes and estimate their calorie content.",
    success_criteria="Find the calorie count using web search and calculations.",
    instructions=[
        "Search web for 5 recipes of the dish",
        "Extract common ingredients from the recipes",
        "List their carbs count",
        "Determine how recipe is prepared , cooking time, and serving size",
        "Based on the preparation instruction and serving size, estimate the total carbs",
        "before sending carbs to calculator make sure they are only numbers",
        "Use markdown for mathematical expressions and show all steps in calculations",
        "Provide a clear and concise answer with sources",
        "If the recipe is not found, provide a general estimate based on common ingredients"
    ],
    show_tool_calls=True,
    markdown=True,
)

if __name__ == "__main__":
    agent_team.print_response("Find carbs of one bowl of Mutton Haleem?", stream=True)
