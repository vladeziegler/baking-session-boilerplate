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

