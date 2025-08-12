from google.adk.agents import Agent
from google.adk.tools import FunctionTool
import google.generativeai as genai

# --- 1. Define the Remote Agent's Tool ---
def say_hello(name: str) -> str:
    """Returns a friendly greeting to the given name."""
    return f"Hello, {name}! It's a pleasure to meet you."

hello_tool = FunctionTool(say_hello)

# --- 2. Create the Remote Agent ---
# This agent has a specific skill (greeting) that it will expose.
# The `adk api_server` command will look for a variable named `agent`.
agent = Agent(
    llm=genai.GenerativeModel(model_name="gemini-pro"),
    tools=[hello_tool],
    description="An agent that is an expert at saying hello.",
)
