from google.adk.agents import Agent
from .prompt import ROOT_AGENT_PROMPT
from .sub_agents.transform_agent.agent import transform_2_agent, express_output_key_agent
from .sub_agents.data_visualisation_agent.agent import data_visualisation_agent
from .sub_agents.vertex_agent.agent import vertex_agent
from .sub_agents.calculator_agent.agent import calculator_agent
from google.adk.tools import agent_tool

root_agent = Agent(
    name="root_agent",
    model="gemini-2.0-flash",
    description="A root agent that delegates tasks to sub-agents. You can use transform_agent if you need to perform calculations.",
    sub_agents=[transform_2_agent, express_output_key_agent, data_visualisation_agent, vertex_agent],
    instruction=ROOT_AGENT_PROMPT
)