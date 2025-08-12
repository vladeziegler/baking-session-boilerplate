from google.adk.agents import Agent
from .prompt import VERTEX_AGENT_PROMPT
from .tools import (
    list_all_files,
    add_file,
    delete_file_by_id,
    query_all_files,
)

vertex_agent = Agent(
    name="vertex_agent",
    model="gemini-2.5-pro",
    description="An agent that can manage and query files in a Vertex AI RAG Corpus.",
    instruction=VERTEX_AGENT_PROMPT,
    tools=[list_all_files, add_file, delete_file_by_id, query_all_files],
)