from google.adk.agents import Agent
from .prompt import TRANSFORM_AGENT_PROMPT
from ..coding_agent.agent import coding_agent
from google.adk.tools import agent_tool
from pydantic import BaseModel, Field


class Variable(BaseModel):
    variable: str = Field(
        description="The variable name. Should be concise and descriptive. Should be in snake_case."
    )
    value: int = Field(
        description="The value of the variable. Should be an integer."
    )
    time: str = Field(
        description="The time of the variable. Should be in the format of YYYY-MM-DD."
    )


class Data(BaseModel):
    list_of_variables: list[Variable] = Field(
        description="The list of variables. Should be a list of Variable objects."
    )


class Poem(BaseModel):
    poem: str = Field(description="A poem with values")


transform_agent = Agent(
    name="transform_agent",
    model="gemini-2.5-pro",
    description="An agent that can perform calculations using coding agent as tool.",
    instruction=TRANSFORM_AGENT_PROMPT,
    tools=[agent_tool.AgentTool(coding_agent)],
)

transform_2_agent = Agent(
    name="transform_2_agent",
    model="gemini-2.5-pro",
    description="An agent that uses transform_agent to perform calculations using coding agent as tool. Your ultimate role is to transform output from coding agent into list of variables that get saved in output_key.",
    instruction=TRANSFORM_AGENT_PROMPT,
    sub_agents=[transform_agent],
    output_key="list_of_variables",
)

express_output_key_agent = Agent(
    name="express_output_key_agent",
    model="gemini-2.5-pro",
    description="An agent that make a poem with values found in output_key {list_of_variables}",
    instruction="Simple agent to express saved output_key {list_of_variables} in a poem.",
    output_key="poem",
) 