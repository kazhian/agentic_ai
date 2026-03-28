# Agentic AI Development: Three Approaches

This project demonstrates three different approaches to building AI applications with OpenAI and LangChain, progressing from basic chat completion to advanced agentic systems.

## Approaches Overview

### 1. Direct API Approach (`01_direct_api.py`)
**Low-Level Implementation**
- Direct OpenAI API integration using `openai.OpenAI()` client
- Manual prompt construction and message handling
- Full control over API calls and response parsing
- Best for: Maximum control, minimal dependencies

### 2. LangChain Message Approach (`02_langchain_messages.ipynb`)
**Structured Chat Framework**
- LangChain abstraction using `HumanMessage` objects
- Simplified model invocation with built-in message handling
- Clean, structured conversation flow
- Best for: Clean code structure without agent complexity

### 3. Agentic Approach (`03_langchain_agent.ipynb`)
**Tool-Enabled Agent System**
- Agent framework with tool integration capabilities
- Autonomous decision-making and multi-step reasoning
- Can call external functions and APIs
- Best for: Complex tasks requiring tool usage and automation

## Key Differences

| Feature | Direct API | LangChain Messages | Agentic |
|---------|------------|-------------------|---------|
| **Abstraction Level** | Low | Medium | High |
| **Tool Support** | Manual | Manual | Built-in |
| **Control** | Maximum | Structured | Framework-guided |
| **Complexity** | High | Medium | Low |
| **Use Case** | Simple tasks | Clean conversations | Complex automation |

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up your OpenAI API key:
```bash
export OPENAI_API_KEY=your_api_key_here
```

## Usage

Each approach is self-contained and can be run independently:
- Run the Python script for Direct API approach
- Execute the Jupyter notebooks for LangChain approaches

## Learning Path

1. Start with **Direct API** to understand the fundamentals
2. Progress to **LangChain Messages** for cleaner code structure
3. Advance to **Agentic Approach** for building intelligent agents

## Dependencies

- `openai` - Direct OpenAI API access
- `langchain` - Core LangChain framework
- `langchain-openai` - OpenAI integration for LangChain
- `langgraph` - Agent framework for complex workflows