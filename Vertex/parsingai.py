  from vertexai import rag
  import vertexai

  PROJECT_ID = os.getenv("PROJECT_ID")
  CORPUS_NAME = "agent-bake-off-demo"
  LOCATION = "us-central1"
  MODEL_ID = "text-embedding-005"
  MODEL_NAME = "projects/{PROJECT_ID}/locations/{LOCATION}/publishers/google/models/{MODEL_ID}"
  MAX_PARSING_REQUESTS_PER_MIN = 100 # Optional
  CUSTOM_PARSING_PROMPT = "Your custom prompt" # Optional

  PATHS = ["gs://bakeoff1208/dummy.txt"]

  # Initialize Vertex AI API once per session
  vertexai.init(project={PROJECT_ID}, location={LOCATION})

  transformation_config = rag.TransformationConfig(
      chunking_config=rag.ChunkingConfig(
          chunk_size=1024, # Optional
          chunk_overlap=200, # Optional
      ),
  )

  llm_parser_config = rag.LlmParserConfig(
      model_name = MODEL_NAME,
      max_parsing_requests_per_min=MAX_PARSING_REQUESTS_PER_MIN, # Optional
      custom_parsing_prompt=CUSTOM_PARSING_PROMPT, # Optional
  )

  rag.import_files(
      CORPUS_NAME,
      PATHS,
      llm_parser=llm_parser_config,
      transformation_config=transformation_config,
  )