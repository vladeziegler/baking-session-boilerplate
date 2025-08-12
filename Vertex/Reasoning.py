import vertexai
from vertexai.preview import reasoning_engines

reasoning_engine = reasoning_engines.ReasoningEngine('projects/852431231686/locations/us-central1/reasoningEngines/3821436225219198976')
print(reasoning_engine.query(a=1, b=2))    
