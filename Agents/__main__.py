"""Main entry point for running the ZadkGuide agent as an A2A Protocol remote agent server."""

import logging
import os

import uvicorn
from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import (
    AgentCapabilities,
    AgentCard,
    AgentSkill,
)
from .agent_executor import ZadkGuideAgentExecutor
from google.adk.artifacts import InMemoryArtifactService
from google.adk.memory.in_memory_memory_service import InMemoryMemoryService
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from .root_agent.agent import root_agent

logger = logging.getLogger(__name__)

class MissingAPIKeyError(Exception):
    """Exception raised when required API key is missing."""
    pass


def main():
    """Starts the ZadkGuide agent A2A server."""
    host = "localhost"
    port = 9999
    
    try:
        # Check for API key only if Vertex AI is not configured
        if not os.getenv("GOOGLE_GENAI_USE_VERTEXAI") == "TRUE":
            if not os.getenv("GOOGLE_API_KEY"):
                raise MissingAPIKeyError(
                    "GOOGLE_API_KEY environment variable not set and GOOGLE_GENAI_USE_VERTEXAI is not TRUE."
                )

        # Define Agent Capabilities
        capabilities = AgentCapabilities(streaming=True)
        
        # Define Agent Skills
        skills = [
            AgentSkill(
                id="data_analysis",
                name="Data Analysis and Visualization",
                description="Performs complex data analysis, calculations, and creates visualizations using various sub-agents including transform, visualization, and calculator agents.",
                tags=["data", "analysis", "visualization", "calculations", "charts"],
                examples=[
                    "Analyze this dataset and create a visualization",
                    "Calculate the statistical summary of these numbers",
                    "Create a chart showing the trend in this data",
                    "Transform this data and perform calculations"
                ],
            ),
            AgentSkill(
                id="coding_assistance",
                name="Coding and Development Support",
                description="Provides coding assistance, code generation, debugging help, and technical guidance using specialized coding sub-agents.",
                tags=["coding", "programming", "development", "debugging", "code generation"],
                examples=[
                    "Help me debug this Python code",
                    "Generate a function to process this data",
                    "Review and improve this code",
                    "Explain how this algorithm works"
                ],
            ),
            AgentSkill(
                id="vertex_ai_integration",
                name="Vertex AI Integration",
                description="Integrates with Google Vertex AI services for advanced AI/ML capabilities and model interactions.",
                tags=["vertex ai", "machine learning", "ai models", "google cloud"],
                examples=[
                    "Use Vertex AI to analyze this data",
                    "Generate content using Vertex AI models",
                    "Perform ML inference with Vertex AI"
                ],
            ),
            AgentSkill(
                id="general_assistance",
                name="General Task Management",
                description="Provides general assistance by orchestrating multiple specialized sub-agents to handle complex multi-step tasks.",
                tags=["task management", "orchestration", "multi-agent", "general assistance"],
                examples=[
                    "Help me solve this complex problem",
                    "Break down this task into steps",
                    "Coordinate multiple operations for me"
                ],
            )
        ]
        
        # Create Agent Card
        agent_card = AgentCard(
            name="ZadkGuide Agent",
            description="A comprehensive multi-agent system that provides data analysis, visualization, coding assistance, and Vertex AI integration capabilities through specialized sub-agents.",
            url=f"http://{host}:{port}/",
            version="1.0.0",
            defaultInputModes=["text/plain"],
            defaultOutputModes=["text/plain"],
            capabilities=capabilities,
            skills=skills,
        )

        # Create ADK Runner with the root agent
        runner = Runner(
            app_name=agent_card.name,
            agent=root_agent,
            artifact_service=InMemoryArtifactService(),
            session_service=InMemorySessionService(),
            memory_service=InMemoryMemoryService(),
        )
        
        # Create Agent Executor
        agent_executor = ZadkGuideAgentExecutor(runner)

        # Create Default Request Handler
        request_handler = DefaultRequestHandler(
            agent_executor=agent_executor,
            task_store=InMemoryTaskStore(),
        )
        
        # Create A2A Starlette Application
        server = A2AStarletteApplication(
            agent_card=agent_card, 
            http_handler=request_handler
        )

        logger.info(f"Starting ZadkGuide A2A Agent Server on {host}:{port}")
        logger.info(f"Agent Card available at: http://{host}:{port}/.well-known/agent-card.json")
        
        # Start the server
        uvicorn.run(server.build(), host=host, port=port)
        
    except MissingAPIKeyError as e:
        logger.error(f"Error: {e}")
        exit(1)
    except Exception as e:
        logger.error(f"An error occurred during server startup: {e}")
        exit(1)


if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    logging.getLogger("google.adk").setLevel(logging.INFO)
    main()
