"""Utility functions for the Vertex AI RAG tools."""
import sys
import os
import vertexai
from vertexai import rag
from google.adk.tools.tool_context import ToolContext

if __package__ is None or __package__ == '':
    # This is a bit of a hack to allow the script to be run standalone
    # and still find its sibling modules.
    _current_dir = os.path.dirname(os.path.abspath(__file__))
    if _current_dir not in sys.path:
        sys.path.append(_current_dir)
    from config import LOCATION, PROJECT_ID, CORPUS_DISPLAY_NAME
else:
    from .config import LOCATION, PROJECT_ID, CORPUS_DISPLAY_NAME


vertexai.init(project=PROJECT_ID, location=LOCATION)

def get_corpus_name(tool_context: ToolContext) -> str:
    """Gets the active corpus name from the tool context or the default."""
    return tool_context.get_tool_state().get("corpus_name", CORPUS_DISPLAY_NAME)


def get_corpus_resource_name(corpus_name: str) -> str:
    """
    Retrieves the full resource name of a RAG Corpus.
    """
    corpora = rag.list_corpora()
    for corpus in corpora:
        if corpus.display_name == corpus_name:
            return corpus.name
    return None


def check_corpus_exists(corpus_name: str, tool_context: ToolContext) -> bool:
    """Check if a corpus exists."""
    return get_corpus_resource_name(corpus_name) is not None
