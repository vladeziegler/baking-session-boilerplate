"""Configuration for the Vertex AI RAG agent."""

import os
import dotenv

dotenv.load_dotenv()

PROJECT_ID = os.getenv("PROJECT_ID")
LOCATION = "us-central1"
CORPUS_DISPLAY_NAME = "agent-bake-off-demo"

# Default RAG query parameters
DEFAULT_TOP_K = 3
DEFAULT_DISTANCE_THRESHOLD = 0.5
