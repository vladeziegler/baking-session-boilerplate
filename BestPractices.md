**Vertex**
1. Enable Vertex AI (and billing)
2. Create bucket
3. Add gs link
4. Grant permissions to Data Agent

*Mistakes to avoid*
- Replace LLM models with more recent ones

**Agent Engine**
1. Create App
2. Deploy App
3. Call App

**Built-in tools**
*Mistakes to avoid*
You need to only have code_executor=BuiltInCodeExecutor() in agent, remove tool parameter
You can only have one built-in tool per agent


**MultiAIAgent**
1. Root agent
2. Subagents as directory
3. Then extra folders

*Mistakes to avoid*
Wrap built-in tools as AgenTool



**Steps**
0. Access GCP
1. Agents
2. Tools
3. Sessions
4. ToolContext
5. Streams

5. API Service

6. Create UI
7. Add stores
8. Connect to Components
9. Add middleware
10. Connect to backend


useful urls:  uvicorn Agents.api:app --reload

