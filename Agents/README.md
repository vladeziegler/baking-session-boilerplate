# ZadkGuide A2A Agent

This directory contains the ZadkGuide agent converted to run as an A2A Protocol remote agent server.

## Features

The ZadkGuide agent provides the following capabilities through the A2A protocol:

- **Data Analysis and Visualization**: Complex data analysis, calculations, and visualizations
- **Coding and Development Support**: Code generation, debugging, and technical guidance  
- **Vertex AI Integration**: Advanced AI/ML capabilities through Google Vertex AI
- **General Task Management**: Multi-agent orchestration for complex tasks

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables:
```bash
# For Google AI Studio
export GOOGLE_API_KEY="your_api_key_here"

# OR for Vertex AI
export GOOGLE_GENAI_USE_VERTEXAI="TRUE"
```

## Running the Server

From the ZadkGuide project root:

```bash
python -m Agents
```

The server will start on `http://localhost:9999` and the Agent Card will be available at:
`http://localhost:9999/.well-known/agent-card.json`

## Architecture

- **`__main__.py`**: A2A server setup with agent card, skills, capabilities, and request handler
- **`agent_executor.py`**: Handles task lifecycle, agent invocation, and message conversion between A2A and ADK formats  
- **`root_agent/`**: The core multi-agent system with specialized sub-agents
- **`utils.py`**: Utility functions for agent interaction

## A2A Protocol Integration

This agent implements the A2A Protocol specification to enable:

- Agent discovery through the Agent Card
- Standardized skill definitions and capabilities
- Remote agent invocation and task management
- Streaming responses and real-time updates
- Cross-platform agent communication

The agent exposes its capabilities through well-defined skills that other A2A-compatible systems can discover and utilize.
