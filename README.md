# PROJECT: Autonomous Agentic PR Code Reviewer ("AutoReview")

## 1. Project Vision
We are building an autonomous PR Code Reviewer. Instead of just piping a `git diff` into an LLM, this agent uses a "Self-Thought" reflection loop. It reads a PR diff, autonomously decides it needs more context, uses tools to fetch surrounding code, drafts a review, critiques its own draft to remove hallucinations/pedantry, and outputs a senior-level code review.

## 2. Tech Stack & Azure Integration
- **The Brain (LLM):** Azure AI Studio Serverless API (Deploying open-source models like Phi-3-mini-128k or Llama-3-8B to save credits while maintaining high tool-calling performance).
- **The SDK:** `azure-ai-inference` (for LLM) and `langchain` / `langgraph` (for orchestration).
- **The Context Engine (MVP):** Local file system reading (Python `ast` and `pathlib`).
- **The Context Engine (V2):** Azure AI Search (Vector RAG for massive codebases).
- **The State Machine:** LangGraph (Python) to manage the cyclic "Self-Thought" workflow.
- **Hosting (V2):** Azure Container Apps (to host a FastAPI webhook listener).

