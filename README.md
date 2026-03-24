# Agentic AI Learning Project

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
pip install langchain langchain-openai langgraph langchain-community python-dotenv tavily-python
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

#### 5. Configure Environment
```bash
# Copy the template file
cp template.env .env

# Edit the .env file with your actual API keys
# OPENAI_API_KEY='sk-proj-your-actual-key-here'
# TAVILY_API_KEY='tvly-your-actual-key-here'
```

#### 6. Verify Setup
```bash
# Test your configuration
python 01_setup/01_direct_interaction.py
```

If the setup is correct, you'll see a successful AI response. If not, check your API keys and Python installation.

## 📁 Project Structure

```
├── 01_setup/           # Basic setup and direct API interaction
├── 02_langchain/       # LangChain fundamentals and chains
├── 03_lc_tool_integ/   # Tool integration examples
├── 04_lc_memory/       # Memory and conversation persistence
├── 05_multi_step_agent/# Multi-step agent workflows
├── 09_industry_case/   # Real-world industry applications
└── 11_ethical_consideration/ # AI ethics and safety
```

## 🎯 Learning Path

1. **Start Here**: `01_setup/` - Verify your environment works
2. **Basics**: `02_langchain/` - Learn LangChain fundamentals
3. **Tools**: `03_lc_tool_integ/` - Add external capabilities
4. **Memory**: `04_lc_memory/` - Enable conversation persistence
5. **Workflows**: `05_multi_step_agent/` - Build multi-step agents
6. **Applications**: `09_industry_case/` - Real-world implementations
7. **Ethics**: `11_ethical_consideration/` - Responsible AI development

## 🛠️ Key Technologies

- **LangChain**: Framework for building AI applications
- **LangGraph**: Stateful workflow orchestration
- **OpenAI**: GPT models for language understanding
- **Tavily**: Web search and information retrieval
- **Python**: Core programming language

## 📚 What You'll Learn

- Building conversational AI agents
- Creating multi-step workflows
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
pip install langchain langchain-openai langgraph langchain-community python-dotenv tavily-python

# 6. Set up your API keys in .env file
cp template.env .env
# Edit .env with your actual keys

# 7. Test everything works
python 01_setup/01_direct_interaction.py
```

## 📖 Additional Resources

- [LangChain Documentation](https://python.langchain.com/docs/)
- [LangGraph Guide](https://langchain-ai.github.io/langgraph/)
- [OpenAI API Docs](https://platform.openai.com/docs)
- [Tavily API Guide](https://tavily.com/docs)

---

**🎓 Learning Goal**: Master the art of building intelligent AI agents that can reason, remember, and act autonomously in real-world scenarios.

Start with the setup verification, then progress through the numbered directories to build your skills progressively!
