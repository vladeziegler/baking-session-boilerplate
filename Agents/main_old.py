"""Main entry point for running the ZadkGuide agent as a command-line tool."""

import asyncio
import logging
from google.adk.runners import Runner
from google.adk.sessions import DatabaseSessionService
from .root_agent.agent import root_agent
from .utils import call_agent_async


async def main_async():
    """Initializes the session service and runs the main async chat loop."""
    # 1. Enable Logging to see agent steps
    logging.basicConfig(level=logging.INFO)
    logging.getLogger("google.adk").setLevel(logging.INFO)

    # 2. Initialize Persistent Session Service (same as the API)
    db_url = "sqlite:///./agent_api_data.db"
    session_service = DatabaseSessionService(db_url=db_url)

    # 3. Define the initial state for new sessions
    initial_state = {
        "username": "local_cli_user",
        "email": "cli@example.com",
        "list_of_variables": [
            {"variable": "initial_var", "value": 100, "time": "2023-01-01"}
        ],
    }
    
    # 4. Session Management: Find an existing session or create a new one
    APP_NAME = "ZadkGuide"
    USER_ID = "cli_user"  # A unique identifier for the command-line user

    existing_sessions = await session_service.list_sessions(
        app_name=APP_NAME, user_id=USER_ID
    )

    if existing_sessions and len(existing_sessions.sessions) > 0:
        session_id = existing_sessions.sessions[0].id
        print(f"Resuming existing session: {session_id}")
    else:
        new_session = await session_service.create_session(
            app_name=APP_NAME, user_id=USER_ID, state=initial_state
        )
        session_id = new_session.id
        print(f"Created new session: {session_id}")


    # 5. Agent Runner Setup
    runner = Runner(
        agent=root_agent,
        app_name=APP_NAME,
        session_service=session_service,
    )

    print("\n--- ZadkGuide Agent CLI ---")
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
