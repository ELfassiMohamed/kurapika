# 🤖 AI Code Review Agent

An autonomous, local-first AI agent designed to review code changes, catch bugs, and provide structured feedback directly within the Git workflow. This project evolves from a lightweight local CLI tool into a scalable, enterprise-grade cloud deployment.

## 📖 Overview

This project aims to build a secure, context-aware code review agent. It starts by proving core agent logic locally using Git hooks and lightweight LLMs, then expands its capabilities using the Model Context Protocol (MCP), and finally scales to a robust cloud architecture for enterprise CI/CD integration.

---

## 🗺️ Project Roadmap

### Phase 1: The Local-First Foundation 
**Goal:** Prove the core agent logic and local execution loop without framework bloat or infrastructure overhead.

* **Architecture:**
  * Pure Python CLI script interacting with local Git hooks (`pre-push`).
  * Ollama running locally, hosting a lightweight model (`qwen2.5-coder:7b`).
  * Direct file parsing for `git diff` with strict JSON output formatting.

* **Execution Steps:**
  1. Write the core diff-extraction and prompt-formatting engine in Python using built-in libraries.
  2. Implement local JSON schema validation so the script fails gracefully if the model outputs malformed text.
  3. Bind the script to the local Git repository using `.git/hooks/pre-push`.

* **✅ Exit Criterion:** 
  > You can push code locally, have the model catch a synthetic bug, and print structured JSON findings to your terminal in under 30 seconds without crashing your system.

---

### Phase 2: Context & Tooling Expansion via MCP 
**Goal:** Transform the script from a basic text-prompter into an autonomous agent using standardized protocol layers.

* **Architecture:**
  * Adopt **Model Context Protocol (MCP)** to securely expose local resources (filesystem, git history, local SAST linter logs) to the agent.
  * Integrate a fast local linter (e.g., `gitleaks` or a static analyzer) to run *before* the LLM sees the code, reducing hallucination vectors.

* **Execution Steps:**
  1. Build a custom local MCP server that allows the agent to query project configuration files or read surrounding code context beyond just the single git diff.
  2. Decouple the prompt logic from the execution logic: the agent suggests a patch, but a deterministic verification script checks if the patch applies cleanly via `git apply`.

* **✅ Exit Criterion:** 
  > The agent doesn't just read the diff—it queries local workspace context via MCP to verify if variable names or imports match the broader codebase before issuing feedback.

---

### Phase 3: Hybrid & Scalable Production Architecture 
**Goal:** Scale the agent away from local hardware constraints toward a robust, enterprise-grade deployment model while retaining strict security boundaries.

* **Architecture:**
  * **Inference Layer Migration:** Shift heavy model inference off local machines to a dedicated Azure VM hosting a secure, private endpoint (or leverage Groq for high-speed cloud inference on massive PRs).
  * **Orchestration Layer:** Move from local Git hooks to a self-hosted CI/CD runner (e.g., a lightweight GitHub Actions runner or a dedicated webhook listener).

* **Execution Steps:**
  1. Containerize the agent application using Docker, ensuring environment parity between local testing and remote execution.
  2. Provision a secure networking layer (e.g., restricted inbound rules or an internal virtual network) if deploying the inference engine to Azure to prevent data leaks.
  3. Implement strict authorization policies: the agent creates draft Pull Requests and runs automated tests via the GitHub API, but *never* holds auto-merge privileges.

* **✅ Exit Criterion:** 
  > Pushing code to a remote repository triggers the agent pipeline on a cloud infrastructure worker, posts structured review comments directly to a GitHub Pull Request, and enforces zero-trust token isolation.

---

## 🛠️ Tech Stack

| Category | Technologies |
| :--- | :--- |
| **Core Logic** | Python, Git Hooks (`pre-push`), JSON Schema Validation |
| **LLM / Inference** | Ollama (`qwen2.5-coder:7b`), Azure VM, Groq |
| **Protocols & Tools** | Model Context Protocol (MCP), `gitleaks`, SAST Linters |
| **Infrastructure** | Docker, GitHub Actions / Webhooks, GitHub API |


