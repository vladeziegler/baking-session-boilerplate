import asyncio
import os
import uuid

import vertexai
from google.adk.agents import Agent
from google.adk.memory import VertexAiMemoryBankService
from google.adk.runner import Runner
from google.adk.sessions import VertexAiSessionService
import google.generativeai as genai
from google.generativeai.types import content_types

# --- Configuration ---
# Make sure to set these environment variables before running the script
# export GOOGLE_CLOUD_PROJECT="your-gcp-project-id"
# export GOOGLE_CLOUD_LOCATION="your-gcp-location"

try:
    PROJECT_ID = os.environ["GOOGLE_CLOUD_PROJECT"]
    LOCATION = os.environ["GOOGLE_CLOUD_LOCATION"]
except KeyError:
    print("ERROR: Please set the GOOGLE_CLOUD_PROJECT and GOOGLE_CLOUD_LOCATION environment variables.")
    exit(1)

# A unique ID for your application to distinguish it from others
APP_NAME = "my_vertex_agent_app"


class VertexAgent(Agent):
    """
    A simple agent that uses Vertex AI for memory and generation.
    """
    async def run(self, request: content_types.Content, **kwargs) -> content_types.Content:
        """
        The main execution logic for the agent.
        """
        user_query = ""
        if request.parts:
            user_query = request.parts[0].text

        print(f"-> You: {user_query}")

        # 1. Search for memories related to the current query.
        # The ADK will automatically use the configured embedding model.
        search_result = await self.search_memory(query=user_query)

        # 2. Build a context from the retrieved memories to enhance the prompt.
        if search_result.memories:
            print("... Found relevant memories.")
            memory_context = "\n".join([memory.text for memory in search_result.memories])
            prompt = f"""
Here is some information from my memory that might be relevant:
---
{memory_context}
---

Based on the information above, please answer the user's question: {user_query}
"""
        else:
            print("... No relevant memories found.")
            prompt = f"Please answer the user's question: {user_query}"

        # 3. Generate a response using the configured LLM.
        print("... Generating response.")
        response = await self.llm.generate_content_async(prompt)
        
        # The ADK runner will automatically save the user query and the agent's
        # response to the memory bank.
        
        return response


async def main():
    """
    Initializes and runs the Vertex AI agent.
    """
    print("Initializing Vertex AI Agent...")

    # Initialize the Vertex AI client.
    vertexai.init(project=PROJECT_ID, location=LOCATION)

    # The Agent Engine provides access to Vertex AI's managed services.
    # This will create a new agent engine instance if one doesn't exist.
    client = vertexai.Client(project=PROJECT_ID, location=LOCATION)
    agent_engine = client.agent_engines.create()
    agent_engine_id = agent_engine.api_resource.name.split("/")[-1]

    print(f"Using Agent Engine ID: {agent_engine_id}")

    # 1. Configure the session service to manage conversation state.
    session_service = VertexAiSessionService(
        project=PROJECT_ID,
        location=LOCATION,
        agent_engine_id=agent_engine_id
    )

    # 2. Configure the memory service (Vector Database).
    memory_service = VertexAiMemoryBankService(
        project=PROJECT_ID,
        location=LOCATION,
        agent_engine_id=agent_engine_id
    )

    # 3. Configure the LLM for generation.
    # Using Gemini 1.0 Pro model.
    llm = genai.GenerativeModel(model_name="gemini-1.0-pro")

    # 4. Configure the Embedding Model.
    # Using the recommended model for Vertex AI Search.
    embedding_model = genai.GenerativeModel(model_name="text-embedding-004")

    # 5. Instantiate the agent.
    agent = VertexAgent(
        llm=llm,
        embedding_model=embedding_model,
    )
    
    # A unique session ID for the current conversation.
    session_id = str(uuid.uuid4())
    print(f"Starting new session: {session_id}\n")


    # 6. Initialize the ADK Runner.
    runner = Runner(
        agent=agent,
        app_name=APP_NAME,
        session_id=session_id,
        session_service=session_service,
        memory_service=memory_service,
    )

    print("Agent is ready. Type 'exit' or 'quit' to end the conversation.")
    print("-" * 20)

    while True:
        try:
            user_input = input("You: ")
            if user_input.lower() in ["exit", "quit"]:
                print("Ending session. Goodbye!")
                break
            
            response = await runner.run_sync(user_input)
            
            response_text = ""
            if response and response.parts:
                response_text = response.parts[0].text

            print(f"Agent: {response_text}")

        except (KeyboardInterrupt, EOFError):
            print("\nEnding session. Goodbye!")
            break

if __name__ == "__main__":
    asyncio.run(main())
