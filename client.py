import requests
import uuid

# --- 1. Use the Correct Endpoint for the ADK Session Server ---
ROOT_AGENT_URL = "http://127.0.0.1:65004/v1/sessions:run"

# The message we want to send to the agent.
user_prompt = "Please say hello to the world."

# --- 2. Use the Correct Session-Based Payload Format ---
session_id = str(uuid.uuid4())
payload = {
    # The session is identified by a unique ID
    "session": f"sessions/{session_id}",
    # The "request" field contains the user's input
    "request": {
        "parts": [
            {"text": user_prompt}
        ]
    }
}

print(f"Sending prompt: '{user_prompt}' to {ROOT_AGENT_URL}")

try:
    # --- 3. Use a Streaming Request to get the Response ---
    # The session endpoint streams the response back.
    response = requests.post(ROOT_AGENT_URL, json=payload, stream=True)
    response.raise_for_status()

    print("\nAgent Response:")
    for line in response.iter_lines():
        if line:
            # The actual content is in a JSON object on each line.
            # We look for the 'text' field within the 'response' -> 'parts'.
            try:
                # The line is a byte string, so it needs to be decoded.
                data = line.decode('utf-8')
                # A simple but effective way to find and extract the text.
                if '"text":' in data:
                    text_part = data.split('"text": "')[1].split('"')[0]
                    # Print the part without a newline, as it streams word by word.
                    print(text_part, end="", flush=True)
            except (ValueError, IndexError):
                # Ignore lines that aren't part of the main text response.
                pass
    # Add a final newline for clean formatting.
    print("\n")

except requests.exceptions.RequestException as e:
    print(f"\nAn error occurred: {e}")
