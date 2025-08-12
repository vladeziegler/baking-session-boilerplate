"""Main entry point for running the ZadkGuide agent."""

import asyncio
import logging
import uuid
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from .root_agent.agent import root_agent
from .utils import call_agent_async


async def main_async():
    """Initializes the session service and runs the main async chat loop."""
    # 1. Enable DEBUG Logging
    # logging.basicConfig(level=logging.INFO)
    # logging.getLogger("google.adk").setLevel(logging.INFO)

    # 2. Initialize the Session Service
    session_service = InMemorySessionService()

    # 3. Define the initial state for new sessions
    initial_state = {
        "username": "test_user",
        "email": "user@example.com",
        "list_of_variables": [
            {"variable": "initial_var", "value": 100, "time": "2023-01-01"}
        ],
    }

    # 4. Create a new session
    APP_NAME = "ZadkGuide"
    USER_ID = "test_user_id"  # A unique identifier for the user
    session_id = str(uuid.uuid4())
    await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=session_id,
        state=initial_state,
    )

    # 5. Agent Runner Setup
    runner = Runner(
        agent=root_agent,
        app_name=APP_NAME,
        session_service=session_service,
    )

    print("--- ZadkGuide Agent ---")
    print(f"Session started with ID: {session_id}")
    print("Enter 'exit' or 'quit' to end the session.")

    # 6. Start the interactive chat loop
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Session ended. Goodbye!")
            break

        if not user_input:
            continue

        await call_agent_async(runner, USER_ID, session_id, user_input)


if __name__ == "__main__":
    asyncio.run(main_async())
