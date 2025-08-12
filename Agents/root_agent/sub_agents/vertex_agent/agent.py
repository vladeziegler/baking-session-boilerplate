from google.adk.agents import Agent
from google.adk.tools import google_search
from google.adk.tools.agent_tool import AgentTool

from .prompt import VERTEX_AGENT_PROMPT

vertex_agent = Agent(
    name="vertex_agent",
    model="gemini-2.0-flash",
    description="An agent that can answer questions about Google's Vertex AI or Palantir.",
    instruction=VERTEX_AGENT_PROMPT,
    tools=[google_search]
)