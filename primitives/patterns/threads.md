# The 6 Agentic Threads (Thread Based Engineering)

| Thread Type | Focus | Goal |
| :--- | :--- | :--- |
| **Exploration** | RAG, Code Search, Docs | Find the "where" and "how." |
| **Implementation** | Feature development | Write the code using Exploration data. |
| **Refactor** | Code Quality | Clean up logic without changing outcomes. |
| **Debugging** | Bug fixing | Resolve specific errors or failing tests. |
| **Review** | Validation | Critically audit code from other threads. |
| **Meta** | System Building | Build the skills/agents that do the work. |

## Integration Strategy
- **Isolation**: Each thread should have its own context window.
- **handoff**: Use a "Report" primitive to pass context between threads.
- **Cleanup**: Discard Exploration and Debugging threads immediately after use.