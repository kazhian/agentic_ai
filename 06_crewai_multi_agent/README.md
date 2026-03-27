# CrewAI Multi-Agent Systems

Welcome to the CrewAI multi-agent orchestration module! This section teaches you how to coordinate multiple AI agents to work together on complex tasks.

## 🎯 Learning Objectives

- Understand CrewAI's agent orchestration concepts
- Learn to define roles, goals, and backstories for agents
- Implement task delegation and collaboration
- Create tools for agent capabilities
- Handle crew execution and result processing

## 📋 Prerequisites

Before starting this module, ensure you've completed:
- `01_setup/` - Basic environment configuration
- `02_langchain/` - LangChain fundamentals
- `05_multi_step_agent/` - Multi-step agent workflows

## 🚀 Quick Start

### Install Dependencies
```bash
pip install crewai
```

### Verify Setup
```bash
python 06_crewai_multi_agent/01_basic_crew.py
```

## 📁 Module Structure

```
06_crewai_multi_agent/
├── README.md                    # This file
├── 01_basic_crew.py            # Simple 2-agent system
├── 02_research_crew.py         # 3-agent research workflow
├── 03_content_creation_crew.py # 4-agent content pipeline
└── utils/
    ├── crew_tools.py           # Shared tools and utilities
    └── markdown_display.py     # Markdown formatting utilities
```

## 🎯 Learning Path

### 1. Basic Crew (`01_basic_crew.py`)
**Concept**: Simple agent collaboration
- **Researcher Agent**: Gathers information
- **Writer Agent**: Creates content based on research
- **Key Learning**: Basic CrewAI setup and task handoff
- **Output**: `basic_crew_output.md` with formatted results

### 2. Research Crew (`02_research_crew.py`)
**Concept**: Multi-step research workflow
- **Researcher**: Web search and data collection
- **Analyst**: Analyzes and organizes findings
- **Summarizer**: Creates comprehensive summary
- **Key Learning**: Sequential task processing and tool integration
- **Output**: `research_crew_output.md` with research summary

### 3. Content Creation Crew (`03_content_creation_crew.py`)
**Concept**: Complete content production pipeline
- **Planner**: Outlines content structure
- **Researcher**: Gathers supporting information
- **Writer**: Creates draft content
- **Reviewer**: Quality control and improvements
- **Key Learning**: Complex workflows with quality assurance
- **Output**: `content_creation_output.md` with final content and review

## 📝 Output Display

All CrewAI scripts now include **automatic markdown formatting** for better result presentation:

### Features
- **Automatic File Generation**: Results saved as `.md` files
- **Timestamped Output**: Each file includes generation time
- **Formatted Headers**: Professional document structure
- **Console Display**: Shows results in terminal + file option

### Viewing Options
1. **VS Code Preview**: Open `.md` file → Press `Ctrl+Shift+V` (Windows/Linux) or `Cmd+Shift+V` (Mac)
2. **GitHub/GitLab**: Upload files to see rendered markdown
3. **Online Viewers**: Use [markdownlivepreview.com](https://markdownlivepreview.com/) or similar
4. **Terminal Enhancement**: Run `python utils/markdown_display.py` for installation tips

### Output Files
- `basic_crew_output.md` - From 2-agent demo
- `research_crew_output.md` - From 3-agent research workflow  
- `content_creation_output.md` - From 4-agent content pipeline

## 🔄 Crew Evolution & Comparison

### **High-Level Overview**

| Crew | Purpose | Workflow | Complexity | Real-World Analogy |
|------|---------|-----------|------------|-------------------|
| **Basic Crew** | Simple collaboration | Researcher → Writer | 2 agents, linear | 2-person team |
| **Research Crew** | Information pipeline | Gather → Analyze → Summarize | 3 agents, with tools | Research department |
| **Content Crew** | Production pipeline | Plan → Research → Write → Review | 4 agents, with QA | Content agency |

### **Key Differences**

#### **01_basic_crew.py - Simple Collaboration**
- **What it does**: Researcher finds info → Writer makes it readable
- **Purpose**: Demonstrates basic agent handoff and coordination
- **Use Case**: Simple content creation tasks
- **Learning Focus**: Understanding CrewAI fundamentals

#### **02_research_crew.py - Information Pipeline**
- **What it does**: Gather data → Analyze patterns → Create summary
- **Purpose**: Shows research workflow with web search integration
- **Use Case**: Research projects, market analysis, academic work
- **Learning Focus**: Tool integration and sequential processing

#### **03_content_creation_crew.py - Production Pipeline**
- **What it does**: Plan → Research → Write → Review quality
- **Purpose**: Demonstrates complete content production with quality assurance
- **Use Case**: Professional content creation, publishing workflows
- **Learning Focus**: Complex workflows with QA and multi-stage review

### **Evolution Pattern**

```
Simple Handoff → Research Workflow → Production Pipeline
     ↓                ↓                    ↓
  2 Agents        3 Agents + Tools     4 Agents + QA
```

**Progressive Complexity**: Each crew builds upon previous concepts while adding new capabilities:
- **Basic**: Agent coordination
- **Research**: Tool integration + data processing
- **Content**: Quality control + complete workflow

## 🔧 Key Concepts

### Agents
- **Role**: What the agent does (e.g., "Researcher")
- **Goal**: What the agent wants to achieve
- **Backstory**: Context for the agent's behavior
- **Tools**: Capabilities the agent can use

### Tasks
- **Description**: What needs to be done
- **Expected Output**: Format and content requirements
- **Agent**: Who performs the task
- **Dependencies**: Order of execution

### Crews
- **Process**: How tasks are executed (sequential, parallel, hierarchical)
- **Memory**: Whether agents remember previous interactions
- **Planning**: How crews approach complex problems

## 🛠️ Common Patterns

### Sequential Processing
```python
crew = Crew(
    agents=[agent1, agent2, agent3],
    tasks=[task1, task2, task3],
    process=Process.sequential
)
```

### Parallel Processing
```python
crew = Crew(
    agents=[agent1, agent2, agent3],
    tasks=[task1, task2, task3],
    process=Process.parallel
)
```

### Tool Integration
```python
search_tool = TavilySearchResults()
agent = Agent(
    role='Researcher',
    goal='Find accurate information',
    tools=[search_tool],
    llm=llm
)
```

## 🎯 Real-World Applications

- **Content Creation**: Blog posts, articles, documentation
- **Research Analysis**: Market research, academic papers
- **Customer Support**: Multi-tier support systems
- **Project Management**: Planning, execution, review cycles

## ⚡ Performance Tips

1. **Model Selection**: Use GPT-3.5 for cost efficiency, GPT-4 for quality
2. **Token Management**: Monitor usage for longer workflows
3. **Task Design**: Clear, specific task descriptions improve results
4. **Tool Selection**: Choose appropriate tools for each agent's role

## 🔍 Troubleshooting

### Common Issues
- **API Key Problems**: Verify OpenAI key in `.env` file
- **Memory Issues**: Reduce conversation context for longer workflows
- **Tool Failures**: Check internet connectivity for search tools
- **Agent Confusion**: Refine role descriptions and goals

### Debug Mode
```python
crew.kickoff(inputs={'topic': 'your topic'}, verbose=True)
```

## 📚 Next Steps

After completing this module:
1. Experiment with custom agent roles
2. Create your own tools for specific domains
3. Build industry-specific crews
4. Explore advanced CrewAI features

## 🎓 Learning Goal

Master the art of orchestrating multiple AI agents to collaborate on complex tasks, creating systems that are more capable than any single agent working alone.

---

**Ready to start?** Begin with `01_basic_crew.py` to understand the fundamentals!
