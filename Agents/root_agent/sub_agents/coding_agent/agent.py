from google.adk.agents import Agent
from .prompt import CODING_AGENT_PROMPT
# from google.adk.code_executors import BuiltInCodeExecutor
from google.adk.agents import Agent
# from google.adk.tools import CodeExecutionTool

from google.adk.code_executors import BuiltInCodeExecutor

coding_agent = Agent(
    model='gemini-2.5-pro',
    description='An agent that can perform calculations using built in code executor.',
    name='CodeAgent',
    code_executor=BuiltInCodeExecutor(),
    instruction=CODING_AGENT_PROMPT
)