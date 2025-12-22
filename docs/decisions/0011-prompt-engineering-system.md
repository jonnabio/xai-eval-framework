# 11. Prompt Engineering System Using Jinja2

**Date**: 2025-12-19
**Status**: Accepted

## Context
Evaluating XAI explanations (SHAP/LIME) using LLMs requires constructing complex, structured prompts. These prompts need to inject dynamic data such as:
- Model predictions (Probabilities/Labels)
- True labels
- Explanation details (Feature importance lists)
- Task descriptions

Hardcoding strings or using Python f-strings becomes unmanageable as prompts grow in complexity or require logic (e.g., "if feature list is empty, say X"). We need a robust templating system.

## Decision
We decided to implement a **Prompt Engineering System** based on **Jinja2**.

### Components
1.  **Template Directory**: Store prompts as `.j2` files in `src/prompts/templates/`. This separates prompt logic from Python code.
2.  **PromptEngine Class**: A wrapper around `jinja2.Environment` to handle loading and safe rendering.
3.  **Strict Context**: Prompts require specific context variables. The engine manages this context injection.

## Consequences
### Positive
- **Flexibility**: Prompts can be edited without changing code.
- **Logic**: Jinja2 supports conditionals and loops (e.g., iterating over top attributes).
- **Maintainability**: Clear separation of concerns (Code vs. Prompt).

### Negative
- **Dependency**: Adds `jinja2` as a dependency.
- **Complexity**: Requires understanding Jinja2 syntax.

## Implementation Details
- `eval_instruction.j2`: The base template for evaluating explanation quality (Intuitiveness, Clarity).
- The `PromptEngine.render()` method is the single entry point for generating prompt strings.
