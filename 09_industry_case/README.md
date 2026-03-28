# Customer Support Agent

This directory contains a customer support agent demo built with LangGraph that demonstrates an industry-specific use case for AI agents.

## Features

### 🤖 **Agent Capabilities**
- **Interactive Console**: Real-time customer support via command line
- **Multi-turn Conversations**: Maintains context across interactions
- **Issue Classification**: Automatically categorizes customer problems
- **Urgency Assessment**: Determines priority levels
- **Knowledge Base Search**: Finds relevant help articles
- **Ticket Management**: Creates and tracks support tickets
- **Escalation Handling**: Routes complex issues to senior agents

### 🛠️ **Technical Components**
- **LangGraph Workflow**: State-based processing pipeline
- **Memory Persistence**: Session continuity with MemorySaver
- **Tool Integration**: Specialized support tools
- **Conditional Routing**: Dynamic workflow decisions
- **State Management**: Comprehensive tracking of support interactions

### 📋 **Support Tools**
1. **Ticket Creation**: `create_support_ticket()`
2. **Knowledge Search**: `search_knowledge_base()`
3. **Order Status**: `check_order_status()`
4. **Issue Escalation**: `escalate_issue()`
5. **Follow-up Scheduling**: `schedule_follow_up()`

## Quick Start

### 1. Environment Setup
```bash
# Ensure you have the required packages
pip install langchain langchain-openai langgraph python-dotenv

# Set up your .env file with API keys
OPENAI_API_KEY=your_openai_api_key_here
```

### 2. Run the Agent
```bash
cd 09_industry_case
python customer_support_agent.py
```

### 3. Interactive Session
```
🤖 Customer Support Agent - Interactive Console
============================================================
Type 'quit' to exit, 'help' for commands
============================================================

Enter your customer ID (or press Enter for guest): CUST12345

🎯 New Support Session Started
👤 Customer ID: CUST12345
🔗 Thread ID: support_CUST12345_20260324
============================================================

💬 How can I help you today?
------------------------------------------------------------

👤 You: I can't log into my account

🤖 Processing...
🔍 Classifying issue...
📋 Issue Category: account
⚡ Assessing urgency...
🚨 Urgency Level: medium
📚 Searching knowledge base...
📖 Knowledge base search completed
🎫 Creating support ticket...
🎫 Ticket Created: TICKET-20260324-123
   Customer: CUST12345
   Urgency: medium
   Status: Open
🔍 Checking escalation requirements...
✅ No escalation needed
💬 Generating response...

🤖 Support Agent: I understand you're having trouble logging into your account. I've created support ticket TICKET-20260324-123 for you.

Based on our knowledge base, here are some common login solutions:
1. Check that you're using the correct email and password
2. Clear your browser cache and cookies
3. Try resetting your password using the "Forgot Password" link
4. Disable any VPN or proxy services you might be using

If these steps don't resolve the issue, please let me know and I can provide additional assistance or escalate this to our technical team.
```

## Workflow Architecture

### 🔄 **Support Pipeline**
```
START → Classify Issue → Assess Urgency → Search Knowledge Base → Create Ticket → Check Escalation → [Escalate OR Respond] → END
```

### 📊 **State Management**
The agent tracks:
- **Customer Information**: ID, session details
- **Issue Details**: Category, urgency, description
- **Ticket Management**: ID, status, assignments
- **Knowledge Base**: Search results and recommendations
- **Escalation**: Status and routing decisions

### 🎯 **Decision Logic**
- **Issue Classification**: Keyword-based categorization
- **Urgency Assessment**: Priority level detection
- **Escalation Criteria**: High priority + technical issues
- **Response Generation**: Context-aware AI responses

## Usage Examples

### Password Reset Request
```
👤 You: I forgot my password and can't log in
🤖 Support Agent: I can help you reset your password! Here's how...
```

### Billing Inquiry
```
👤 You: I was charged twice for my subscription
🤖 Support Agent: I understand your concern about the duplicate charge...
```

### Technical Issue
```
👤 You: The app keeps crashing when I try to upload files
🤖 Support Agent: I'm sorry you're experiencing this technical issue...
```

### Order Status Check
```
👤 You: What's the status of order #12345?
🤖 Support Agent: Let me check that for you...
```

## Commands

### Interactive Console Commands
- `help` - Show available commands
- `quit` - Exit the support session
- `status` - Check current session status

### Supported Topics
- Password reset and login issues
- Billing and payment problems
- Account management
- Order tracking and delivery
- Technical troubleshooting
- General inquiries

## Industry Applications

This customer support agent can be adapted for:
- **E-commerce**: Product support and order management
- **SaaS Platforms**: Technical support and user onboarding
- **Financial Services**: Account issues and transaction support
- **Healthcare**: Patient support and appointment management
- **Telecommunications**: Service issues and billing inquiries

## Technical Features

### 🧠 **Memory & Context**
- Persistent session memory using LangGraph's MemorySaver
- Thread-based conversation tracking
- Multi-turn dialogue support

### 🔧 **Tool Integration**
- Modular tool architecture for extensibility
- Real-time API integration capabilities
- Database connectivity for ticket management

### 🚀 **Scalability**
- Stateless graph design for horizontal scaling
- Configurable escalation thresholds
- Customizable knowledge base integration

## Customization

### Adding New Tools
```python
@tool
def custom_support_function(param: str) -> str:
    """Custom support tool description."""
    # Implementation here
    return result
```

### Modifying Workflow
```python
# Add new nodes to the graph
builder.add_node("new_node", new_node_function)
builder.add_edge("existing_node", "new_node")
```

### Updating Classification Logic
```python
# Modify the classify_issue_node function
categories = {
    "new_category": ["keyword1", "keyword2"],
    # Add more categories
}
```

## Requirements

- Python 3.8+
- LangChain
- LangGraph
- OpenAI API key
- Python-dotenv

## Future Enhancements

- **Sentiment Analysis**: Detect customer emotions
- **Multi-language Support**: International customer service
- **Integration APIs**: Connect to CRM systems
- **Analytics Dashboard**: Support metrics and insights
- **Email Integration**: Automated follow-up communications

This demo showcases how LangGraph can be used to build sophisticated, industry-specific AI agents that provide real business value in customer support scenarios.
