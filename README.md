# java2pythonagent
this is a simple agent that takes java code and transforms it into python
---

# Version 0 — Initial Exploration

This branch represents the very first iteration of the project.

At this stage, the system is intentionally minimal: it is essentially a wrapper around a locally hosted LLM, exposed through two execution paths:
- a direct LLM call from a Python script
- a very simple `CodeAgent` built using `smolagents`

The goal of this version is **not** to build a full agent-based system, but to validate the core idea with the smallest possible surface area.

---

## What problem is being explored?

The initial objective is straightforward:

> Take a snippet of Java code and return its Python equivalent.

At first glance, this looks like a natural fit for an AI agent that:
- reasons about the code
- decides how to translate it
- handles errors and ambiguity

However, during exploration it became clear that **most of that complexity is unnecessary at this stage**.

---

## Why this design?

A key takeaway early on was learning to distinguish:
- when an **agent** is actually needed
- and when a **simple LLM call** is enough

For a task like code translation, there are multiple possible approaches:
- building a complex mapping layer using traditional code
- using an LLM with a well-defined prompt
- orchestrating everything with a multi-step agent

For Version 0, the simplest option wins.

This branch intentionally keeps:
- a **very explicit system prompt**
- a **thin wrapper around the LLM**
- and a **minimal agent orchestration**, mostly as an experiment

The agent here does not add intelligence — it merely demonstrates how agent-based orchestration could be layered on top later, once it is actually justified.

---

## Why two execution paths?

This branch includes two scripts on purpose:

- **Direct LLM call**
  - The simplest possible interaction
  - Useful for validating prompts and model behavior
  - Lowest overhead and easiest to reason about

- **Agent-based execution**
  - Uses `smolagents.CodeAgent`
  - Demonstrates how the same prompt can be embedded into an agent workflow
  - Helps expose limitations, failure modes, and unnecessary complexity early

Having both side by side makes the trade-offs very explicit.

---

## Configuration & Requirements

This project relies entirely on **local compute**.

### Requirements
- A locally running LLM backend (e.g. Ollama)
- A downloaded model

All experiments in this branch were done using:

- **Model:** `qwen3:4b`  
  A small, lightweight model that is reasonably capable while remaining friendly to limited hardware.

### Running the project
1. Start your local LLM backend.
2. Configure the model name in the script you want to run.
3. Execute either:
   - the direct LLM call script, or
   - the agent-based script.

A system prompt is preloaded, but it is intentionally easy to modify for experimentation.

---

## Scope of Version 0

What this version **does**:
- validates local LLM integration
- explores prompt-driven code translation
- exposes early agent failure modes
- keeps everything small, observable, and debuggable

What this version **does not attempt**:
- file I/O
- tool usage
- multi-agent communication
- production-grade reliability

Those are explicitly deferred to later versions.

---

## Next steps

Future versions will incrementally introduce:
- clearer input/output boundaries (e.g. `.java` → `.py`)
- controlled tool usage
- stricter contracts between model and code
- and only then, more sophisticated agent behavior

