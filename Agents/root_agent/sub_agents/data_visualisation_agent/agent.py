from google.adk.agents import Agent
from .prompt import DATA_VISUALISATION_AGENT_PROMPT
from .tools import create_bar_chart, create_table_chart

data_visualisation_agent = Agent(
    name="data_visualisation_agent",
    model="gemini-2.5-pro",
    description="An agent that can visualise data.",
    instruction=DATA_VISUALISATION_AGENT_PROMPT,
    tools=[create_bar_chart, create_table_chart],
)