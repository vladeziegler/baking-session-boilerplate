"""
A command-line toolkit for managing and querying files in a Vertex AI RAG Corpus.

This script provides functions to:
- List all files in a corpus.
- Query all files in a corpus.
- Query a specific file by its ID.
- Add a new local file to the corpus.
- Delete a specific file by its full resource name.
"""
import vertexai
from vertexai import rag
from vertexai.generative_models import GenerativeModel
import os
import dotenv
import time
from vertexai.preview.generative_models import Tool

# --- Configuration ---
dotenv.load_dotenv()
PROJECT_ID = os.getenv("PROJECT_ID")
LOCATION = "us-central1"
CORPUS_DISPLAY_NAME = "agent-bake-off-demo"
# --- End Configuration ---


def get_or_create_corpus(display_name: str) -> str:
    """
    Retrieves the name of an existing RAG Corpus or creates it if it doesn't exist.
    """
    print(f"Looking for RAG corpus with display name: {display_name}")
    corpora = rag.list_corpora()
    rag_corpus = next((c for c in corpora if c.display_name == display_name), None)

    if rag_corpus:
        print(f"Found existing corpus: {rag_corpus.name}")
    else:
        print("Corpus not found. Creating a new one with 'text-embedding-005'...")
        rag_embedding_model_config = rag.RagEmbeddingModelConfig(
            vertex_prediction_endpoint=rag.VertexPredictionEndpoint(
                publisher_model="publishers/google/models/text-embedding-005"
            )
        )
        rag_corpus = rag.create_corpus(
            display_name=display_name,
            backend_config=rag.RagVectorDbConfig(
                rag_embedding_model_config=rag_embedding_model_config
            ),
        )
        print(f"Created new corpus: {rag_corpus.name}")

    return rag_corpus.name


def list_all_files(corpus_name: str):
    """Lists all files in the specified RAG corpus."""
    print(f"\nListing all files in corpus: {corpus_name}...")
    try:
        files = rag.list_files(corpus_name=corpus_name)
        if not files:
            print("No files found in this corpus.")
            return

        print("Found the following files:")
        for i, file in enumerate(files):
            print(f"  [{i+1}] Display Name: {file.display_name}")
            print(f"      Resource Name: {file.name}")
            print("-" * 20)
    except Exception as e:
        print(f"An error occurred while listing files: {e}")


def add_file(corpus_name: str, file_path: str, display_name: str, description: str):
    """Uploads a local file to the specified RAG corpus."""
    print(f"\nAdding file '{file_path}' to corpus: {corpus_name}...")
    if not os.path.exists(file_path):
        print(f"Error: File not found at '{file_path}'")
        return

    try:
        uploaded_file = rag.upload_file(
            corpus_name=corpus_name,
            path=file_path,
            display_name=display_name,
            description=description,
        )
        print(f"Successfully uploaded file.")
        print(f"  Display Name: {uploaded_file.display_name}")
        print(f"  Resource Name: {uploaded_file.name}")
    except Exception as e:
        print(f"An error occurred during file upload: {e}")


def delete_file_by_id(file_name: str):
    """Deletes a file from the RAG corpus using its full resource name."""
    print(f"\nDeleting file: {file_name}...")
    try:
        rag.delete_file(name=file_name)
        print(f"Successfully deleted file.")
    except Exception as e:
        print(f"An error occurred during file deletion: {e}")


def query_all_files(corpus_name: str, query_text: str):
    """Performs a retrieval query across all files in the corpus."""
    print(f"\nQuerying all files in '{corpus_name}' with: '{query_text}'")
    try:
        # Create a RAG retrieval tool
        rag_retrieval_tool = Tool.from_retrieval(
            retrieval=rag.Retrieval(
                source=rag.VertexRagStore(
                    rag_resources=[
                        rag.RagResource(
                            rag_corpus=corpus_name,
                        )
                    ],
                ),
            )
        )

        # Create a Gemini model instance with the RAG tool
        model = GenerativeModel(
            model_name="gemini-2.0-flash-001", tools=[rag_retrieval_tool]
        )
        
        # Generate response
        response = model.generate_content(query_text)

        print("\n--- Query Response ---")
        print(response.text)
        print("----------------------")
    except Exception as e:
        print(f"An error occurred during the query: {e}")


def query_specific_file(corpus_name: str, file_id: str, query_text: str):
    """Performs a retrieval query on a single, specific file."""
    print(f"\nQuerying specific file_id '{file_id}' with: '{query_text}'")
    try:
        # Create a RAG retrieval tool for a specific file
        rag_retrieval_tool = Tool.from_retrieval(
            retrieval=rag.Retrieval(
                source=rag.VertexRagStore(
                    rag_resources=[
                        rag.RagResource(
                            rag_corpus=corpus_name,
                            # Supply the specific file ID to narrow the search
                            rag_file_ids=[file_id],
                        )
                    ],
                ),
            )
        )
        
        # Create a Gemini model instance with the RAG tool
        model = GenerativeModel(
            model_name="gemini-2.0-flash-001", tools=[rag_retrieval_tool]
        )

        # Generate response
        response = model.generate_content(query_text)
        
        print("\n--- Query Response ---")
        print(response.text)
        print("----------------------")
    except Exception as e:
        print(f"An error occurred during the specific query: {e}")


def main():
    """
    Main function to drive the RAG file management script.
    It provides a simple command-line interface to choose an action.
    """
    if not PROJECT_ID:
        raise ValueError("PROJECT_ID environment variable not set.")

    print("Initializing Vertex AI...")
    vertexai.init(project=PROJECT_ID, location=LOCATION)

    corpus_name = get_or_create_corpus(CORPUS_DISPLAY_NAME)

    # --- CLI ---
    print("\nWhat would you like to do?")
    print("1: List all files")
    print("2: Query all files")
    print("3: Query a specific file")
    print("4. Add a new file")
    print("5. Delete a file")
    choice = input("Enter the number of your choice: ")

    if choice == '1':
        list_all_files(corpus_name)

    elif choice == '2':
        query = input("Enter your query for all files: ")
        query_all_files(corpus_name, query)

    elif choice == '3':
        file_id = input("Enter the file ID (e.g., '5498505293422206784' from the resource name): ")
        query = input(f"Enter your query for file {file_id}: ")
        query_specific_file(corpus_name, file_id, query)

    elif choice == '4':
        # Create a dummy file for uploading if it doesn't exist
        dummy_path = "another_doc.txt"
        if not os.path.exists(dummy_path):
            with open(dummy_path, "w") as f:
                f.write("This is another document about different topics.")
            print(f"Created a sample file: '{dummy_path}'")
        
        file_path = input(f"Enter the local path of the file to add (default: {dummy_path}): ") or dummy_path
        display_name = input("Enter a display name for the file: ")
        description = input("Enter a description for the file: ")
        add_file(corpus_name, file_path, display_name, description)

    elif choice == '5':
        resource_name = input("Enter the full resource name of the file to delete (e.g., projects/.../ragFiles/...): ")
        if resource_name:
            confirm = input(f"Are you sure you want to delete {resource_name}? (y/n): ")
            if confirm.lower() == 'y':
                delete_file_by_id(resource_name)
            else:
                print("Deletion cancelled.")
    else:
        print("Invalid choice. Please run the script again.")


if __name__ == "__main__":
    main()
