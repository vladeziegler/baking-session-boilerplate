from google.adk.agents import Agent
from .prompt import TRANSFORM_AGENT_PROMPT
# from google.adk.code_executors import BuiltInCodeExecutor
from google.adk.agents import Agent
from ..calculator_agent.agent import calculator_agent
from ..coding_agent.agent import coding_agent
from google.adk.tools import agent_tool
# from google.adk.tools import CodeExecutionTool

from pydantic import BaseModel, Field

class Variable(BaseModel):
    variable: str = Field(
        description="The variable name. Should be concise and descriptive. Should be in snake_case."
    )
    value: int = Field(
        description="The value of the variable. Should be an integer."
    )

class Data(BaseModel):
    list_of_variables: list[Variable] = Field(
        description="The list of variables. Should be a list of Variable objects."
    )

transform_agent = Agent(
    name="transform_agent",
    model="gemini-2.5-flash",
    description="An agent that can perform calculations using tools. Your ultimate role is to transform output from coding agent into list of variables.",
    instruction=TRANSFORM_AGENT_PROMPT,
    tools=[agent_tool.AgentTool(coding_agent)]
    # output_key="list_of_variables"
    # tools=[CodeExecutionTool()]
) 