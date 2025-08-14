# A2A Starter Guide: Configuring Server and Host Agents

Based on our implementation, this guide provides a precise, step-by-step process for configuring both A2A Server Agents (the "Doers") and Host Agents (the "Callers").

### The Core Concept: Server vs. Host

1.  **Server Agent (The "Doer")**: This is your main, skilled agent (e.g., `ZadkGuide`). It runs continuously, listens for requests, and performs complex tasks. Its primary job is to expose its abilities to the network via the A2A protocol.

2.  **Host Agent (The "Caller")**: This is a client agent that acts on behalf of a user. Its primary job is to **discover** available Server Agents, understand their skills, and **delegate** user requests to them. It is the orchestrator.

---

## Part 1: How to Configure a Server Agent

This guide follows the pattern we used for the `Agents/` directory.

### Step 1: Define the Core Agent Logic (`root_agent/agent.py`)

This is your standard ADK agent. It defines the agent's model, tools, and sub-agents. This part doesn't need to know anything about the A2A protocol.

```python
# /Users/vladimirdeziegler/Backbase/ZadkGuide/Agents/root_agent/agent.py

from google.adk.agents import Agent
from .sub_agents.calculator_agent.agent import calculator_agent
# ... other sub-agent imports

# This is the core "brain" of your server
root_agent = Agent(
    name="root_agent",
    model="gemini-2.0-flash",
    description="A root agent that delegates tasks to sub-agents...",
    sub_agents=[calculator_agent, ...],
    instruction="You are the root agent..."
)
```

### Step 2: Create the Agent Executor (`agent_executor.py`)

This is the **critical bridge** between the A2A server's requests and your ADK agent. It translates A2A tasks into ADK agent runs.

**Functionality:**
*   Inherits from `a2a.server.agent_execution.AgentExecutor`.
*   Receives A2A `RequestContext` and an `EventQueue`.
*   Uses a `TaskUpdater` to send asynchronous updates (e.g., "working", "completed").
*   Calls the ADK `runner.run_async()` method.
*   **Thing to Watch Out For:** All `TaskUpdater` methods are `async` and **must be awaited**. Failure to do so will result in `RuntimeWarning` errors and prevent the client from receiving responses correctly.

```python
# /Users/vladimirdeziegler/Backbase/ZadkGuide/Agents/agent_executor.py

from a2a.server.agent_execution import AgentExecutor
from a2a.server.tasks import TaskUpdater
from google.adk import Runner

class ZadkGuideAgentExecutor(AgentExecutor):
    def __init__(self, runner: Runner):
        self.runner = runner

    async def execute(self, context, event_queue):
        # ... boilerplate setup ...
        updater = TaskUpdater(event_queue, context.task_id, context.context_id)
        if not context.current_task:
            await updater.submit()  # Must be awaited
        await updater.start_work()  # Must be awaited

        # Run the agent and process events
        async for event in self.runner.run_async(...):
            if event.is_final_response():
                parts = convert_genai_parts_to_a2a(event.content.parts)
                await updater.add_artifact(parts)  # Must be awaited
                await updater.complete()         # Must be awaited
                break
            else:
                # Send intermediate updates
                await updater.update_status(...) # Must be awaited
```

### Step 3: Build the A2A Server Entrypoint (`__main__.py`)

This file ties everything together and exposes it as a web server.

**Functionality:**
1.  **Define Skills & Capabilities**: Describe what your agent can do in a structured way.
2.  **Create Agent Card**: This is the agent's public "business card," which includes its name, description, URL, and skills.
3.  **Initialize ADK Runner**: The engine that will run your `root_agent`.
4.  **Initialize Agent Executor**: Instantiate the bridge class from Step 2.
5.  **Initialize Request Handler**: Use `DefaultRequestHandler`, passing it the executor.
6.  **Launch the App**: Use `A2AStarletteApplication` to create the server and run it with `uvicorn`.

```python
# /Users/vladimirdeziegler/Backbase/ZadkGuide/Agents/__main__.py

import uvicorn
from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.types import AgentCard, AgentSkill, AgentCapabilities
from .agent_executor import ZadkGuideAgentExecutor
from .root_agent.agent import root_agent
from google.adk.runners import Runner

def main():
    # 1. Define Skills
    skill = AgentSkill(id="data_analysis", name="Data Analysis", ...)
    capabilities = AgentCapabilities(streaming=True)

    # 2. Create the Card
    agent_card = AgentCard(name="ZadkGuide Agent", skills=[skill], ...)

    # 3. Create ADK Runner
    runner = Runner(app_name=agent_card.name, agent=root_agent, ...)
    
    # 4. Create the Executor
    agent_executor = ZadkGuideAgentExecutor(runner)

    # 5. Create the Request Handler
    request_handler = DefaultRequestHandler(agent_executor=agent_executor, ...)
    
    # 6. Build and Run the Server
    server = A2AStarletteApplication(agent_card=agent_card, http_handler=request_handler)
    uvicorn.run(server.build(), host="localhost", port=9999)

if __name__ == "__main__":
    main()
```

---

## Part 2: How to Configure a Host Agent (Client)

This guide follows the pattern we used for the `a2a_test_client`.

### Step 1: Define the Host Agent's Core Logic (`agent.py`)

This agent's purpose is to delegate tasks. Its main components are its instructions and a tool to call the remote agent.

**Functionality:**
1.  **Discover Server Agents**: In its initialization (`_async_init_components`), it uses `A2ACardResolver` to fetch the Server Agent's card from the `/.well-known/agent-card.json` endpoint. This is how it learns about the remote agent.
2.  **Define Root Instruction**: The prompt for the Host Agent is critical. It **must** instruct the agent to use its `send_message` tool to delegate tasks, not to answer them itself.
3.  **Implement the `send_message` Tool**: This is the core of the client.
    *   It takes the user's task as input.
    *   It constructs and sends a `SendMessageRequest` to the Server Agent.
    *   It receives the `Task` object as a response.
    *   **It parses the `task.artifacts` field to extract the final text response**. This is a common point of failure if not handled correctly.

```python
# ep2-ai-agent-bake-off/a2a_example/a2a_bake_off_agent/a2a_test_client/agent.py

from a2a.client import A2ACardResolver
from google.adk import Agent

class HostAgent:
    # 1. Discover agents
    async def _async_init_components(self, remote_agent_addresses):
        for address in remote_agent_addresses:
            card_resolver = A2ACardResolver(client, address)
            card = await card_resolver.get_agent_card()
            # Store the connection and card
            self.remote_agent_connections[card.name] = ...

    # 2. Define instructions
    def root_instruction(self, context):
        return f"""
        **Role:** You are the ZadkGuide Host Agent...
        **Task Delegation:** When a user asks any question, use the `send_message` tool to forward their question...
        <Available Agents>
        {self.agents}
        </Available Agents>
        """

    # 3. Implement the tool to call the server
    async def send_message(self, agent_name: str, task: str, tool_context):
        client = self.remote_agent_connections[agent_name]
        message_request = SendMessageRequest(...)
        send_response = await client.send_message(message_request)
        
        # This part is crucial!
        task_obj = send_response.root.result
        response_parts = []
        if task_obj.artifacts:
            for artifact in task_obj.artifacts:
                if artifact.parts:
                    for part in artifact.parts:
                        # Logic to extract text from the part
                        response_parts.append(part.root.text)
        return "\n".join(response_parts)
```

### Step 2: Create the Interactive Client Entrypoint (`test_simple.py`)

This script initializes the `HostAgent` and manages the user-facing conversation.

**Functionality:**
1.  **Set the URL** of the Server Agent.
2.  **Initialize the Host Agent**: `HostAgent.create(...)` triggers the discovery process.
3.  **Interactive Loop**:
    *   Takes user input.
    *   **Formats the input into a tool call string** for the Host Agent's LLM (e.g., `f'send_message(agent_name="ZadkGuide Agent", task="{user_question}")'`). This tells the Host Agent's brain to use its tool.
    *   Calls `host_agent.stream()` with this formatted query to get the final result.

```python
# ep2-ai-agent-bake-off/a2a_example/a2a_bake_off_agent/a2a_test_client/test_simple.py

import asyncio
from agent import HostAgent

async def test_zadkguide_agent():
    # 1. Set the server URL
    remote_agent_url = "http://localhost:9999"

    # 2. Initialize the Host Agent
    host_agent = await HostAgent.create(remote_agent_addresses=[remote_agent_url])
    remote_agent_name = list(host_agent.remote_agent_connections.keys())[0]

    # 3. Start interactive loop
    while True:
        user_question = input("💬 Your question: ").strip()
        if user_question.lower() == 'quit':
            break

        # Format the query to force tool use
        query = f'send_message(agent_name="{remote_agent_name}", task="{user_question}")'

        # Get the streamed response
        async for response in host_agent.stream(query, ...):
            if response.get("is_task_complete"):
                print(f"📋 Response: {response.get('content')}")
                break
```
