import vertexai
from vertexai.generative_models import GenerativeModel
from vertexai import rag
import os
import dotenv
import json
from pypdf import PdfReader

# Load environment variables
dotenv.load_dotenv()

# --- Configuration ---
PROJECT_ID = os.getenv("PROJECT_ID")
LOCATION = "us-central1"
CORPUS_DISPLAY_NAME = "agent-bake-off-demo"
PDF_FILE_PATH = "Apify_Invoice_demo.pdf"

def main():
    """
    This script performs two main tasks:
    1. Extracts structured data (amount, currency, topic) from a local PDF invoice using a Gemini model.
    2. Uploads the same PDF to a Vertex AI RAG corpus to make it searchable.
    """
    if not PROJECT_ID:
        raise ValueError("PROJECT_ID environment variable not set.")

    print("Initializing Vertex AI...")
    vertexai.init(project=PROJECT_ID, location=LOCATION)

    # --- Corpus Management ---
    print(f"Looking for RAG corpus with display name: {CORPUS_DISPLAY_NAME}")
    corpora = rag.list_corpora()
    rag_corpus = next((c for c in corpora if c.display_name == CORPUS_DISPLAY_NAME), None)

    if rag_corpus:
        print(f"Found existing corpus: {rag_corpus.name}")
    else:
        print("Corpus not found. Creating a new one...")
        rag_corpus = rag.create_corpus(display_name=CORPUS_DISPLAY_NAME)
        print(f"Created new corpus: {rag_corpus.name}")

    corpus_name = rag_corpus.name

    # --- 1. Structured Data Extraction ---
    print(f"\n--- Starting Step 1: Extracting structured data from {PDF_FILE_PATH} ---")
    try:
        # Extract text from the PDF
        print(f"Reading text from '{PDF_FILE_PATH}'...")
        reader = PdfReader(PDF_FILE_PATH)
        pdf_text = ""
        for page in reader.pages:
            pdf_text += page.extract_text()

        if not pdf_text:
            raise ValueError("Could not extract text from the PDF.")
        
        print("Successfully extracted text from PDF.")

        # Use Gemini to extract structured data
        print("Calling Gemini model for data extraction...")
        model = GenerativeModel(model_name="gemini-2.0-flash-001")
        
        prompt = f"""
        Extract the following information from this invoice text:
        - amount (the total amount due)
        - currency (e.g., USD, EUR)
        - topic (a brief description of what the invoice is for)

        Return the information in a valid JSON object with the keys "amount", "currency", and "topic".

        Invoice text:
        ---
        {pdf_text}
        ---
        """

        response = model.generate_content(prompt)
        
        # Clean up the response to get a valid JSON string
        json_string = response.text.strip().replace("```json", "").replace("```", "").strip()
        
        extracted_data = json.loads(json_string)

        print("\nSuccessfully extracted structured data:")
        print(json.dumps(extracted_data, indent=2))

    except Exception as e:
        print(f"An error occurred during structured data extraction: {e}")

    # --- 2. Upload to RAG Corpus ---
    print(f"\n--- Starting Step 2: Uploading {PDF_FILE_PATH} to RAG Corpus ---")
    try:
        uploaded_file = rag.upload_file(
            corpus_name=corpus_name,
            path=PDF_FILE_PATH,
            display_name="Apify Invoice Demo",
            description="An example invoice from Apify for RAG processing.",
        )
        print(f"Successfully uploaded file to RAG corpus.")
        print(f"Uploaded file resource name: {uploaded_file.name}")
    except Exception as e:
        print(f"An error occurred during file upload to RAG: {e}")


if __name__ == "__main__":
    main()
