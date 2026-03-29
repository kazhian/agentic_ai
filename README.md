# AgenticAI: An Experimental Approach to Autonomous Intelligence

A comprehensive collection of AI agent implementations demonstrating various LangChain and LangGraph capabilities for building intelligent, multi-step systems.

## 🚀 Quick Start

### Prerequisites
- Python 3.8+ installed
- Basic command line knowledge
- Recommended IDE: Visual Studio Code

### Clone Repository & Setup Environment

#### 1. Clone the Git Repository
```bash
# Clone the repository
git clone https://github.com/kazhian/agentic_ai.git

# Navigate into the project directory
cd agentic_ai
```

#### 2. Create Virtual Environment
```bash
# Create virtual environment (recommended)
python -m venv .venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

# Verify activation (you should see (.venv) in your prompt)
```

**Why Virtual Environment?**
- Isolates project dependencies
- Prevents conflicts with system packages
- Easy to recreate and share
- Best practice for Python development

### IDE Setup (Recommended)

**Visual Studio Code Setup:**
```bash
# Install VS Code (if not already installed)
# Visit: https://code.visualstudio.com/

# Install essential VS Code extensions:
# 1. Python Extension (Microsoft)
# 2. Jupyter Extension (Microsoft)
# 3. Python Docstring Generator
# 4. GitLens (for better code navigation)
```

**Why VS Code?**
- Excellent Python support with IntelliSense
- Built-in Jupyter notebook support
- Integrated terminal for running commands
- Great debugging capabilities
- Free and widely used

### Setup Instructions

#### 3. Install Python Dependencies
```bash
# Install required packages (make sure .venv is activated)
pip install langchain langchain-openai langgraph langchain-community python-dotenv tavily-python crewai
```

#### 4. Get API Keys

**OpenAI API Key:**
- Visit [OpenAI Platform](https://platform.openai.com/api-keys)
- Sign up/login and create a new API key
- Copy the key (starts with `sk-proj-`)

**Tavily API Key:**
- Visit [Tavily AI](https://tavily.com/api)
- Sign up and get your API key
- Copy the key (starts with `tvly-`)

**LangSmith API Key:**
- Visit [LangSmith](https://smith.langchain.com/) or [LangChain LangSmith](https://www.langchain.com/langsmith)
- Sign up/login and create a new API key
- Copy the key

#### 5. Configure Environment
```bash
# Copy the template file
cp template.env .env

# Edit the .env file with your actual API keys
# OPENAI_API_KEY='sk-proj-your-actual-key-here'
# TAVILY_API_KEY='tvly-your-actual-key-here'
# LANGSMITH_API_KEY='your-langsmith-api-key-here'
```

#### 6. Verify Setup
```bash
# Test your configuration
python 01_setup/01_direct_interaction.py
```

If the setup is correct, you'll see a successful AI response. If not, check your API keys and Python installation.

#### 7. Setup Markdown Display (Optional)

For better markdown rendering when viewing CrewAI outputs:

**VS Code Built-in Preview** (Recommended):
- Open any .md file in VS Code
- Press Ctrl+Shift+V (Windows/Linux) or Cmd+Shift+V (Mac)
- Or click the preview icon in the top right

**Python Libraries for Enhanced Display**:
```bash
# For terminal rendering
pip install rich

# For HTML conversion
pip install markdown
```

**Desktop Apps**:
- Typora (paid, beautiful)
- Mark Text (free)
- Obsidian (free, powerful)

**Online Viewers**:
- https://markdownlivepreview.com/
- https://dillinger.io/
- GitHub Gists

## 📁 Project Structure

```
├── 01_setup/              # Basic setup and direct API interaction
├── 02_langchain/          # LangChain fundamentals and chains
├── 03_lc_tool_integ/      # Tool integration examples
├── 04_lc_memory/          # Memory and conversation persistence
├── 05_multi_step_agent/   # Multi-step agent workflows
├── 06_crewai_multi_agent/ # CrewAI multi-agent orchestration
├── 07_autonomous_agents/  # AutoGPT-style autonomous agents
├── 08_agent_evaluation/   # Evaluation and LangSmith tracing
├── 09_industry_case/      # Real-world industry applications
└── 11_ethical_consideration/ # AI ethics and safety
```

## 🧭 Course Module Map

This course is organized around the topics for **AgenticAI: An Experimental Approach to Autonomous Intelligence**.

1. **Setting up Agentic AI Development Environment**
   - Covers virtual environments, dependency installation, API key configuration, and direct model interaction.
2. **Building Agents with LangChain: Simple Question Answering**
   - Includes basic LangChain agent patterns and Q&A examples.
3. **Tool Integration with LangChain Agents: Web Search**
   - Demonstrates how to add external tool capabilities like web search.
4. **Memory Management in LangChain Agents: Conversational History**
   - Teaches agent memory, chat history, and session persistence.
5. **Creating Multi-Step Agents with LangChain Chains**
   - Shows how to build multi-step workflows and chain-based agents.
6. **Orchestrating Multi-Agent Systems with CrewAI**
   - Walks through coordinated multi-agent workflows using CrewAI.
7. **Exploring Autonomous Agents with AutoGPT**
   - Introduces autonomous agent concepts and AutoGPT-style execution.
8. **Evaluating Agent Performance using LangSmith (or similar tools)**
   - Covers tracing and evaluation concepts using notebooks and examples.
9. **Building an Agent for a Specific Industry Use Case — Customer Support**
   - Demonstrates a customer support agent workflow and practical application.
10. **Building an Agent for a Specific Industry Use Case — Financial Data Analysis**
   - Describes a potential extension for building a domain-specific financial agent.
11. **Exploring Ethical Considerations in Agent Behavior**
   - Covers accountability, transparency, bias, privacy, and safety.
12. **Final Project: Developing an Agentic AI Application for a Real-World Problem**
   - The capstone project concept is to combine these modules into a complete, real-world agentic application.

> Note: Module `08_agent_evaluation/` has been added to provide dedicated LangSmith tracing and agent evaluation content.

## 🎯 Learning Path

1. **Start Here**: `01_setup/` - Verify your environment works
2. **Basics**: `02_langchain/` - Learn LangChain fundamentals
3. **Tools**: `03_lc_tool_integ/` - Add external capabilities
4. **Memory**: `04_lc_memory/` - Enable conversation persistence
5. **Workflows**: `05_multi_step_agent/` - Build multi-step agents
6. **Multi-Agent**: `06_crewai_multi_agent/` - Orchestrate agent crews
7. **Autonomous**: `07_autonomous_agents/` - Explore AutoGPT-style autonomous agents
8. **Applications**: `09_industry_case/` - Real-world implementations
9. **Ethics**: `11_ethical_consideration/` - Responsible AI development

## 🛠️ Key Technologies

- **LangChain**: Framework for building AI applications
- **LangGraph**: Stateful workflow orchestration
- **CrewAI**: Multi-agent collaboration and orchestration
- **OpenAI**: GPT models for language understanding
- **Tavily**: Web search and information retrieval
- **Python**: Core programming language

## 📚 What You'll Learn

- Building conversational AI agents
- Creating multi-step workflows
- Orchestrating multi-agent systems
- Integrating external tools and APIs
- Managing conversation memory
- Implementing industry-specific solutions
- Understanding AI ethics and safety

## 🔧 Common Issues

**API Key Problems:**
- Ensure keys are copied correctly without extra spaces
- Check that your OpenAI account has credits
- Verify Tavily API key is valid

**Python Issues:**
- Use Python 3.8 or higher
- Install packages in a virtual environment (recommended)
- Update pip: `pip install --upgrade pip`

**Virtual Environment Issues:**
- Make sure you activated the virtual environment before installing packages
- If activation fails, try: `python -m venv .venv --clear` then reactivate
- On Windows, use PowerShell or Command Prompt as Administrator

**VS Code Issues:**
- Restart VS Code after installing Python extension
- Select correct Python interpreter: `Ctrl+Shift+P` → "Python: Select Interpreter"
- For Jupyter notebooks, ensure Jupyter extension is installed

**Import Errors:**
- Make sure you're in the project root directory
- Check that all packages installed successfully
- Restart your terminal after installation

## 🎯 Get Started Now

```bash
# 1. Clone the repository
git clone https://github.com/kazhian/agentic_ai.git
cd agentic_ai

# 2. Create and activate virtual environment
python -m venv .venv
# On Windows: .venv\Scripts\activate
# On macOS/Linux: source .venv/bin/activate

# 3. Install VS Code: https://code.visualstudio.com/
# 4. Install VS Code extensions: Python, Jupyter, Python Docstring Generator, GitLens

# 5. Install dependencies (in virtual environment)
pip install langchain langchain-openai langgraph langchain-community python-dotenv tavily-python crewai

# 6. Set up your API keys in .env file
cp template.env .env
# Edit .env with your actual keys

# 7. Test everything works
python 01_setup/01_direct_interaction.py

# 8. Setup markdown display (optional)
# Follow the "Setup Markdown Display" section above
```

## 📖 Additional Resources

- [LangChain Documentation](https://python.langchain.com/docs/)
- [LangGraph Guide](https://langchain-ai.github.io/langgraph/)
- [OpenAI API Docs](https://platform.openai.com/docs)
- [Tavily API Guide](https://tavily.com/docs)

---

**🎓 Learning Goal**: Master the art of building intelligent AI agents that can reason, remember, and act autonomously in real-world scenarios.

Start with the setup verification, then progress through the numbered directories to build your skills progressively!
