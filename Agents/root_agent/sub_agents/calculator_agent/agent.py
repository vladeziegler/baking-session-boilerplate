from google.adk.agents import Agent
from .prompt import CALCULATOR_AGENT_PROMPT
# from google.adk.code_executors import BuiltInCodeExecutor
from google.adk.agents import Agent
# from google.adk.tools import CodeExecutionTool

calculator_agent = Agent(
    name="calculator_agent",
    model="gemini-2.0-flash",
    description="An agent that can perform mathematical calculations.",
    instruction=CALCULATOR_AGENT_PROMPT,
    # tools=[CodeExecutionTool()]
) 