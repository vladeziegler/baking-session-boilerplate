"""API service for the ZadkGuide agent, using FastAPI."""

import json
import logging
from fastapi import FastAPI
from pydantic import BaseModel
from starlette.responses import StreamingResponse

from google.adk.runners import Runner
from google.adk.sessions import DatabaseSessionService
from google.genai import types

from .root_agent.agent import root_agent

# --- 1. Application Setup ---
logging.basicConfig(level=logging.INFO)
logging.getLogger("google.adk").setLevel(logging.INFO)

app = FastAPI(
    title="ZadkGuide Agent API",
    description="API for interacting with the ZadkGuide multi-agent system.",
    version="1.0.0",
)

# Use DatabaseSessionService with a local SQLite file for robust session management.
DB_URL = "sqlite:///./agent_api_data.db"
session_service = DatabaseSessionService(db_url=DB_URL)

APP_NAME = "ZadkGuideAPI"
runner = Runner(
    agent=root_agent,
    app_name=APP_NAME,
    session_service=session_service,
)

# --- 2. API Data Models ---
class ChatRequest(BaseModel):
    """Defines the structure of a chat request from the client."""
    session_id: str
    user_input: str


# --- 3. Streaming Logic ---
async def stream_agent_responses(user_id: str, session_id: str, user_input: str):
    """An async generator that yields agent events as they happen."""
    content = types.Content(role="user", parts=[types.Part(text=user_input)])

    try:
        async for event in runner.run_async(
            user_id=user_id, session_id=session_id, new_message=content
        ):
            # Determine event type based on event properties
            if event.is_final_response():
                event_type = "FINAL_RESPONSE"
            else:
                event_type = "INTERMEDIATE"
            
            response_data = {"event_type": event_type, "data": {}}
            
            if event.content and event.content.parts:
                part = event.content.parts[0]
                if hasattr(part, "tool_code") and part.tool_code:
                    response_data["data"] = {
                        "tool_name": part.tool_code.name,
                        "tool_args": part.tool_code.args,
                    }
                elif hasattr(part, "tool_response") and part.tool_response:
                    response_data["data"] = {
                        "tool_name": part.tool_response.name,
                        "output": part.tool_response.output,
                    }
                elif hasattr(part, "function_call") and part.function_call:
                    response_data["data"] = {
                        "function_name": part.function_call.name,
                        "function_args": part.function_call.args,
                    }
                elif hasattr(part, "function_response") and part.function_response:
                    response_data["data"] = {
                        "function_name": part.function_response.name,
                        "function_id": part.function_response.id,
                        "response": part.function_response.response,
                    }
                elif hasattr(part, "text") and part.text:
                    response_data["data"] = {"text": part.text.strip()}
            
            # Add event metadata
            response_data["data"]["event_id"] = event.id
            response_data["data"]["author"] = event.author
            
            yield json.dumps(response_data) + "\n"

    except Exception as e:
        error_data = {"event_type": "ERROR", "data": {"message": str(e)}}
        yield json.dumps(error_data) + "\n"


# --- 4. API Endpoint ---
@app.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    """
    Main endpoint for interacting with the agent.
    """
    USER_ID = "api_user"

    # Follow the working reference pattern with proper async/await
    try:
        # Try to get the existing session (DatabaseSessionService methods are async)
        session = await session_service.get_session(
            app_name=APP_NAME, user_id=USER_ID, session_id=request.session_id
        )
        actual_session_id = session.id
        logging.info(f"Found existing session: {actual_session_id}")
    except Exception:
        # If get_session fails, the session does not exist. Create it.
        logging.info(f"Session '{request.session_id}' not found. Creating a new one.")
        initial_state = {
            "username": "API User",
            "email": "api@example.com",
            "list_of_variables": [],
        }
        # Create session and capture the returned session object (also async)
        new_session = await session_service.create_session(
            app_name=APP_NAME,
            user_id=USER_ID,
            session_id=request.session_id,
            state=initial_state,
        )
        # Use the actual session ID from the returned session object
        actual_session_id = new_session.id
        logging.info(f"Created new session with ID: {actual_session_id}")

    return StreamingResponse(
        stream_agent_responses(USER_ID, actual_session_id, request.user_input),
        media_type="application/x-json-stream",
    )
