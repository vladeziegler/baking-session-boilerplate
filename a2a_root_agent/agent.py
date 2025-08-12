from google.adk.agents import Agent, RemoteA2aAgent
import google.generativeai as genai

# --- 1. Define the Remote Agent Connection ---
# The URL points to the Agent Card of the remote agent that we will run.
# This card tells our root agent everything it needs to know to communicate.
REMOTE_AGENT_CARD_URL = "http://127.0.0.1:8001/.well-known/agent.json"

# --- 2. Create a RemoteA2aAgent instance ---
# This object acts as a local proxy for the remote agent.
remote_hello_agent = RemoteA2aAgent(
    name="GreeterAgent",
    agent_card=REMOTE_AGENT_CARD_URL,
    description="A remote agent that can provide friendly greetings."
)

# --- 3. Create the Root Agent ---
# We register the remote agent as a sub_agent.
# The RootAgent can now delegate tasks to the GreeterAgent.
# The `adk api_server` command will look for a variable named `agent`.
agent = Agent(
    llm=genai.GenerativeModel(model_name="gemini-pro"),
    sub_agents=[remote_hello_agent],
    description="A root agent that can delegate greetings to a remote agent."
)
