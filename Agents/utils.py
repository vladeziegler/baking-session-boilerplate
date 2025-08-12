"""Utility functions for agent interaction."""

import asyncio

from google.genai import types
from google.adk.runners import Runner


# ANSI color codes for terminal output
class Colors:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    BLUE = "\033[34m"
    CYAN = "\033[36m"
    BG_BLUE = "\033[44m"
    WHITE = "\033[37m"
    BG_GREEN = "\033[42m"
    BLACK = "\033[30m"
    BG_RED = "\033[41m"


async def process_agent_response(event):
    """Process and display agent response events."""
    final_response = None
    if event.is_final_response():
        if (
            event.content
            and event.content.parts
            and hasattr(event.content.parts[0], "text")
            and event.content.parts[0].text
        ):
            final_response = event.content.parts[0].text.strip()
            print(
                f"\n{Colors.BG_BLUE}{Colors.WHITE}{Colors.BOLD}╔══ AGENT RESPONSE ═════════════════════════════════════════{Colors.RESET}"
            )
            print(f"{Colors.CYAN}{Colors.BOLD}{final_response}{Colors.RESET}")
            print(
                f"{Colors.BG_BLUE}{Colors.WHITE}{Colors.BOLD}╚═════════════════════════════════════════════════════════════{Colors.RESET}\n"
            )
    else:
        # Log intermediate steps
        if event.content and event.content.parts:
            for part in event.content.parts:
                if hasattr(part, "tool_code"):
                    print(f"  [Tool Call]: {part.tool_code.name}({part.tool_code.args})")
                elif hasattr(part, "tool_response"):
                    print(f"  [Tool Response]: {part.tool_response.name} -> {part.tool_response.output}")

    return final_response


async def call_agent_async(runner: Runner, user_id: str, session_id: str, query: str):
    """Call the agent asynchronously with the user's query."""
    content = types.Content(role="user", parts=[types.Part(text=query)])
    print(
        f"\n{Colors.BG_GREEN}{Colors.BLACK}{Colors.BOLD}--- Running Query: {query} ---{Colors.RESET}"
    )

    try:
        async for event in runner.run_async(
            user_id=user_id, session_id=session_id, new_message=content
        ):
            await process_agent_response(event)
    except Exception as e:
        print(f"Error during agent call: {e}")
