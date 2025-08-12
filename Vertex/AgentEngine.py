import vertexai
from vertexai.preview import reasoning_engines

# TODO(developer): Update and un-comment below lines
PROJECT_ID = "agent-bake-off"
staging_bucket = "gs://bakeoff1208"
vertexai.init(
    project=PROJECT_ID, location="us-central1", staging_bucket=staging_bucket
)

class SimpleAdditionApp:
    def query(self, a: int, b: int) -> str:
        """Query the application.
        Args:
            a: The first input number
            b: The second input number
        Returns:
            int: The additional result.
        """
        return f"{int(a)} + {int(b)} is {int(a + b)}"

# Locally test
app = SimpleAdditionApp()

# Create a remote app with Reasoning Engine.
# This may take 1-2 minutes to finish.
reasoning_engine = reasoning_engines.ReasoningEngine.create(
    SimpleAdditionApp(),
    display_name="Demo Addition App",
    description="A simple demo addition app",
    requirements=["cloudpickle==3"],
    extra_packages=[],
)
# Example response:
# Using bucket YOUR_BUCKET_NAME
# Writing to gs://YOUR_BUCKET_NAME/reasoning_engine/reasoning_engine.pkl
# ...
# ReasoningEngine created. Resource name: projects/123456789/locations/us-central1/reasoningEngines/123456
# To use this ReasoningEngine in another session:
# reasoning_engine = vertexai.preview.reasoning_engines.ReasoningEngine('projects/123456789/locations/...