"""
Tools for managing and querying files in a Vertex AI RAG Corpus.
"""

import os
import logging
from google.adk.tools import FunctionTool
from google.adk.tools.tool_context import ToolContext
from vertexai import rag
import sys
import json

# This check allows the script to be run directly for testing.
# When run as a script, it uses direct imports.
# When imported as a module, it uses relative imports.
if __name__ == "__main__" and (__package__ is None or __package__ == ''):
    # This is a bit of a hack to allow the script to be run standalone
    # and still find its sibling modules.
    _current_dir = os.path.dirname(os.path.abspath(__file__))
    if _current_dir not in sys.path:
        sys.path.append(_current_dir)
    from config import DEFAULT_DISTANCE_THRESHOLD, DEFAULT_TOP_K
    from utils import (
        check_corpus_exists,
        get_corpus_resource_name,
        get_corpus_name as get_active_corpus_name,
    )
else:
    from .config import DEFAULT_DISTANCE_THRESHOLD, DEFAULT_TOP_K
    from .utils import (
        check_corpus_exists,
        get_corpus_resource_name,
        get_corpus_name as get_active_corpus_name,
    )


def list_all_files(tool_context: ToolContext) -> dict:
    """Lists all files in the currently active RAG corpus.

    Args:
        tool_context (ToolContext): The tool context.

    Returns:
        dict: A dictionary containing the list of files or an error message.
    """
    try:
        corpus_name = get_active_corpus_name(tool_context)
        corpus_resource_name = get_corpus_resource_name(corpus_name)

        if not corpus_resource_name:
            return {"status": "error", "message": f"Corpus '{corpus_name}' not found."}

        files = rag.list_files(corpus_name=corpus_resource_name)
        if not files:
            return {
                "status": "success",
                "message": "No files found in this corpus.",
                "files": [],
            }

        file_list = [
            {"display_name": file.display_name, "resource_name": file.name}
            for file in files
        ]
        return {
            "status": "success",
            "message": f"Found {len(file_list)} files.",
            "files": file_list,
        }
    except Exception as e:
        logging.error(f"Error listing files: {e}")
        return {"status": "error", "message": str(e)}


def add_file(
    file_path: str, display_name: str, description: str, tool_context: ToolContext
) -> dict:
    """Uploads a local file to the RAG corpus.

    Args:
        file_path (str): The local path to the file to be uploaded.
        display_name (str): The name to display for the file in the corpus.
        description (str): A description of the file's content.
        tool_context (ToolContext): The tool context.

    Returns:
        dict: A dictionary containing the result of the upload operation.
    """
    if not os.path.exists(file_path):
        return {"status": "error", "message": f"File not found at '{file_path}'"}

    try:
        corpus_name = get_active_corpus_name(tool_context)
        corpus_resource_name = get_corpus_resource_name(corpus_name)

        if not corpus_resource_name:
            return {"status": "error", "message": f"Corpus '{corpus_name}' not found."}

        uploaded_file = rag.upload_file(
            corpus_name=corpus_resource_name,
            path=file_path,
            display_name=display_name,
            description=description,
        )
        return {
            "status": "success",
            "message": "File uploaded successfully.",
            "display_name": uploaded_file.display_name,
            "resource_name": uploaded_file.name,
        }
    except Exception as e:
        logging.error(f"Error uploading file: {e}")
        return {"status": "error", "message": str(e)}

def delete_file_by_id(file_name: str, tool_context: ToolContext) -> dict:
    """Deletes a file from the RAG corpus using its full resource name.

    Args:
        file_name (str): The full resource name of the file to delete
                       (e.g., `projects/.../corpora/.../files/...`).
        tool_context (ToolContext): The tool context.

    Returns:
        dict: A dictionary containing the result of the deletion operation.
    """
    try:
        rag.delete_file(name=file_name)
        return {"status": "success", "message": "File deleted successfully."}
    except Exception as e:
        logging.error(f"Error deleting file: {e}")
        return {"status": "error", "message": str(e)}


def query_all_files(query: str, tool_context: ToolContext) -> dict:
    """
    Query a Vertex AI RAG corpus with a user question and return relevant information.

    Args:
        query (str): The text query to search for in the corpus.
        tool_context (ToolContext): The tool context.

    Returns:
        dict: The query results and status.
    """
    try:
        corpus_name = get_active_corpus_name(tool_context)
        if not check_corpus_exists(corpus_name, tool_context):
            return {
                "status": "error",
                "message": f"Corpus '{corpus_name}' does not exist.",
            }

        corpus_resource_name = get_corpus_resource_name(corpus_name)

        rag_retrieval_config = rag.RagRetrievalConfig(
            top_k=DEFAULT_TOP_K,
            filter=rag.Filter(vector_distance_threshold=DEFAULT_DISTANCE_THRESHOLD),
        )

        response = rag.retrieval_query(
            rag_resources=[
                rag.RagResource(
                    rag_corpus=corpus_resource_name,
                )
            ],
            text=query,
            rag_retrieval_config=rag_retrieval_config,
        )

        results = []
        if hasattr(response, "contexts") and response.contexts:
            for ctx_group in response.contexts.contexts:
                result = {
                    "source_uri": (
                        ctx_group.source_uri if hasattr(ctx_group, "source_uri") else ""
                    ),
                    "text": ctx_group.text if hasattr(ctx_group, "text") else "",
                }
                results.append(result)
        
        if not results:
            return {
                "status": "warning",
                "message": f"No results found in corpus '{corpus_name}' for query: '{query}'",
                "results": [],
            }

        return {
            "status": "success",
            "message": f"Successfully queried corpus '{corpus_name}'",
            "results": results,
        }

    except Exception as e:
        logging.error(f"Error querying corpus: {e}")
        return {"status": "error", "message": str(e)}


if __name__ == "__main__":

    class MockToolContext:
        """A mock ToolContext for standalone testing."""

        def __init__(self, state=None):
            self._state = state if state is not None else {}

        def get_tool_state(self):
            return self._state

    def run_tests():
        """Runs a sequence of tests on the RAG tools."""
        print("--- Testing Vertex RAG Tools ---")
        mock_context = MockToolContext()

        # 1. Test list_all_files
        print("\n[1] Testing list_all_files...")
        list_result = list_all_files(mock_context)
        print(json.dumps(list_result, indent=2))

        # 2. Test add_file
        print("\n[2] Testing add_file...")
        test_file_path = "rag_test_file.txt"
        test_file_content = "This is a test file for the RAG agent."
        with open(test_file_path, "w") as f:
            f.write(test_file_content)

        added_file_resource_name = None
        try:
            add_result = add_file(
                file_path=test_file_path,
                display_name="Test File",
                description="A file for testing add_file tool.",
                tool_context=mock_context,
            )
            print(json.dumps(add_result, indent=2))
            if add_result.get("status") == "success":
                added_file_resource_name = add_result.get("resource_name")

            # 3. Test query_all_files (interactive)
            print("\n[3] Testing query_all_files...")
            user_query = input("Enter your query for the RAG system: ")
            if user_query:
                query_result = query_all_files(
                    query=user_query, tool_context=mock_context
                )
                print(json.dumps(query_result, indent=2))
            else:
                print("Query skipped.")

            # 4. Test delete_file_by_id
            if added_file_resource_name:
                print("\n[4] Testing delete_file_by_id...")
                # Prompting for confirmation before deleting
                confirm = input(
                    f"Delete the test file ({added_file_resource_name})? (y/n): "
                )
                if confirm.lower() == "y":
                    delete_result = delete_file_by_id(
                        file_name=added_file_resource_name, tool_context=mock_context
                    )
                    print(json.dumps(delete_result, indent=2))
                else:
                    print("Deletion skipped.")
            else:
                print(
                    "\n[4] Skipping delete_file_by_id (file was not added successfully)."
                )

        finally:
            # Clean up the test file
            if os.path.exists(test_file_path):
                os.remove(test_file_path)
                print(f"\nCleaned up test file: {test_file_path}")

        print("\n--- All tests finished ---")

    run_tests()
