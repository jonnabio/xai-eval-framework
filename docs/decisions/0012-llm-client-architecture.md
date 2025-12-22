# 12. Unified LLM Client Architecture

**Date**: 2025-12-19
**Status**: Accepted

## Context
To evaluate explanations, we need to query Large Language Models (LLMs). We plan to use multiple providers (OpenAI GPT-4, Google Gemini) to verify that our evaluation metrics are robust to the evaluator choice. Each provider has a different API SDK.

We need a unified interface so the evaluation script (`run_llm_eval.py`) doesn't need to know which provider is being used.

## Decision
We decided to implement a **Unified LLM Client** using a **Factory Pattern**.

### Architecture
1.  **`BaseLLMClient` (Abstract Base Class)**: Defines the contract:
    - `generate(prompt: str) -> str`
2.  **Concrete Implementations**:
    - `OpenAIClient`: Wraps `openai` Python SDK.
    - `GeminiClient`: Wraps `google-generativeai` SDK.
3.  **`LLMClientFactory`**: A static factory that takes an `LLMConfig` object and returns the appropriate client instance.

## Consequences
### Positive
- **Interchangeability**: Switching checks is as simple as changing `provider: openai` to `provider: gemini` in the config.
- **Testability**: We can easily mock `BaseLLMClient` for unit tests.
- **Consistency**: Error handling and logging are centralized in the wrappers.

### Negative
- **Maintenance**: We must maintain wrappers for each SDK. API changes in SDKs require updates here.

## Compliance
- All clients must handle API keys via environment variables for security (`OPENAI_API_KEY`, `GOOGLE_API_KEY`).
- Clients must use `LLMConfig` (Pydantic) for validation of parameters like `temperature` and `max_tokens`.
