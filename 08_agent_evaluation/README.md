# Evaluating Agent Performance with LangSmith

## Learning objectives

This module shows how to evaluate LangChain and autonomous agents using LangSmith or a similar evaluation and tracing platform.

By the end of this module, you will know how to:
- Configure LangSmith tracing for agent executions
- Capture and inspect agent traces, logs, and tool usage
- Define evaluation metrics for task success, reliability, and quality
- Compare agent responses against expected outputs
- Build simple evaluation dashboards for agent performance

## Why evaluation matters

Agent development is not complete until you can measure how well an agent performs. Evaluation makes it possible to:
- validate whether an agent solves the right task
- identify failure modes and tool misuse
- compare different agent prompts, tools, or model settings
- monitor performance regressions over time

## Module structure

```
08_agent_evaluation/
├── README.md
├── 01_langsmith_tracing.ipynb
├── 02_evaluation_metrics.ipynb
├── 03_agent_testing.ipynb
├── 04_evaluation_dashboard.ipynb
└── utils/
    ├── evaluation_tools.py
    └── langsmith_helpers.py
```

## Lessons

1. `01_langsmith_tracing.ipynb` — Set up LangSmith tracing for LangChain agents and inspect execution traces.
2. `02_evaluation_metrics.ipynb` — Define agent performance metrics and compute reusable evaluation scores.
3. `03_agent_testing.ipynb` — Learn how to test agents with expected prompts, responses, and pass/fail assertions.
4. `04_evaluation_dashboard.ipynb` — Build a simple dashboard for trace exploration, performance trends, and evaluation reports.

## Getting started

1. Create a LangSmith account and obtain an API key.
2. Set `LANGSMITH_API_KEY` in your `.env` file or environment before running the notebooks.
3. Review the LangSmith setup in `01_langsmith_tracing.ipynb`.
4. If you do not have a LangSmith account, adapt the examples to another tracing/evaluation tool.
5. Use `utils/langsmith_helpers.py` and `utils/evaluation_tools.py` to reuse the module’s evaluation logic.

> Note: Without a valid `LANGSMITH_API_KEY`, the tracing examples will fail to upload runs and return unauthorized errors. If you only want to run the exercises locally, skip the LangSmith tracer configuration or comment out the tracer usage.

## Notes

- This module is designed to complement the agent-building lessons in `07_autonomous_agents/`.
- If LangSmith is unavailable, the same evaluation principles apply to other platforms such as OpenAI Function calling traces, custom logging layers, or third-party metric dashboards.
