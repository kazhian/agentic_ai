# Autonomous Agents Module - Setup Guide

## 🚀 Quick Setup

### 1. Install Dependencies
```bash
# Make sure you're in the project root directory
cd /Users/kazhian/Dev/agentic_ai

# Install all required packages
pip install -r requirements.txt
```

### 2. Set Up Environment Variables
```bash
# Copy the template
cp template.env .env

# Edit the .env file with your API keys
# OPENAI_API_KEY=sk-proj-your-openai-key-here
# TAVILY_API_KEY=tvly-your-tavily-key-here
```

### 3. Run the Demos
```bash
# Run the interactive demo menu
python3 run_autonomous_agents.py

# Or run individual demos directly:
python3 -c "
import sys, os, importlib.util
project_root = os.path.dirname(os.path.abspath('run_autonomous_agents.py'))
spec = importlib.util.spec_from_file_location('autogpt_concepts', f'{project_root}/07_autonomous_agents/01_autogpt_concepts.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
module.main()
"
```

## 🔧 If You Encounter Import Errors

The numeric package names (`07_autonomous_agents`) can cause import issues in Python. Use the provided runner script:

```bash
python3 run_autonomous_agents.py
```

This script handles the imports properly and provides a clean interface to run all demos.

## 📋 Available Demos

1. **AutoGPT Concepts** (`01_autogpt_concepts.py`)
   - Basic autonomous agent implementation
   - Goal decomposition and task management
   - Memory systems and self-reflection

2. **AutoGPT Tools** (`utils/autogpt_tools.py`)
   - Enhanced tools for autonomous agents
   - Safety monitoring and cost tracking
   - Advanced memory management

3. **Limitations & Safety** (`03_limitations_challenges.py`)
   - Safety policies and monitoring
   - Failure analysis and recovery
   - Ethical considerations

## 🎯 Learning Path

1. Start with the **AutoGPT Concepts** demo to understand the basics
2. Explore the **AutoGPT Tools** to see advanced capabilities
3. Review **Limitations & Safety** for responsible AI development

## 💡 Tips

- Make sure your API keys are properly set in the `.env` file
- Start with simpler goals to see how the agent works
- Monitor the usage statistics to understand costs
- Review the safety considerations before running complex tasks

## 🐛 Troubleshooting

**Import Error**: Use `python3 run_autonomous_agents.py` instead of direct imports
**Missing Dependencies**: Run `pip install -r requirements.txt`
**API Key Issues**: Check your `.env` file and ensure keys are valid
**Permission Errors**: Make sure you have write permissions for the output directory
