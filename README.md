# Shopping Assistant Agent

An AI-powered ReAct shopping assistant designed for retail stores. It helps customers with shopping inquiries, recommends products, and assists registered users in redeeming single-use discount codes and earning loyalty points.

## Tech Stack
*   **Core Framework**: [Google Agent Development Kit (ADK) 2.0](https://adk.dev/)
*   **LLM Provider**: Gemini (`gemini-flash-latest` via Vertex AI / Google GenAI SDK)
*   **Language**: Python 3.12
*   **Package Management**: `uv` (fast Python package installer and resolver)
*   **Linter & Formatter**: Ruff, Codespell, and Ty type checker
*   **Security Scanning**: Semgrep (custom API key regex scanner) and pre-commit hooks
*   **Web Framework**: FastAPI (boilerplate web server for local/A2A hosting)

## Local Execution Instructions

### Prerequisites
Before you start, make sure you have:
1.  **uv**: Install via `curl -LsSf https://astral.sh/uv/install.sh | sh`.
2.  **agents-cli**: Install via `uv tool install google-agents-cli`.
3.  **Google Cloud CLI (gcloud)**: Ensure you are logged in and application default credentials (ADC) are configured.

### Step-by-Step Setup and Execution

1.  **Initialize Project Virtual Environment**:
    Navigate into the project directory and run `uv sync` to create a virtual environment and install all dependencies:
    ```bash
    cd shopping-assistant
    uv sync
    ```

2.  **Install & Setup Pre-Commit Hooks**:
    To activate the local formatting, whitespace, and Semgrep security scanners before commits, run:
    ```bash
    uv run pre-commit install --config .pre-commit-config.yaml
    ```

3.  **Run Lint and Formatting Checks**:
    Ensure the codebase adheres to quality standards:
    ```bash
    uv run agents-cli lint
    ```

4.  **Run the Test Suite**:
    Run all unit, integration, and security tests:
    ```bash
    uv run pytest
    ```

5.  **Start the Interactive Playground**:
    Launch the local development playground in your browser to chat with the agent:
    ```bash
    uv run agents-cli playground
    ```

6.  **Start the Local API Server**:
    Launch the FastAPI app server:
    ```bash
    uv run uvicorn app.fast_api_app:app --reload
    ```
