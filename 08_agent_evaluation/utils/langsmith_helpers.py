"""Helper utilities for agent tracing and evaluation."""

from typing import Optional, Dict

try:
    from langchain_core.tracers import LangChainTracer
except ImportError:  # pragma: no cover
    LangChainTracer = None


def create_langsmith_tracer(
    project_name: str = "agentic-ai-evaluation",
    session_name: Optional[str] = None,
    run_name: Optional[str] = None,
):
    """Create and return a LangChain tracer for agent executions."""
    if LangChainTracer is None:
        raise ImportError(
            "langchain_core is not installed. Install `langchain-core` to use tracing."
        )

    tracer = LangChainTracer(project_name=project_name)
    return tracer


def format_trace_summary(trace: Dict) -> Dict:
    """Build a lightweight summary of a trace object."""
    return {
        "session_name": trace.get("session_name"),
        "run_name": trace.get("run_name"),
        "success": trace.get("success"),
        "start_time": trace.get("start_time"),
        "end_time": trace.get("end_time"),
        "tool_calls": len(trace.get("tool_calls", [])),
    }
