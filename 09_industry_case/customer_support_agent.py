#!/usr/bin/env python3
"""
Customer Support Agent - Industry Use Case Demo

This script demonstrates a customer support agent built with LangGraph that provides:
- Interactive console-based support
- Multi-turn conversations with memory
- Specialized tools for common support tasks
- Ticket creation and tracking
- Knowledge base search
- Escalation handling
"""

import os
import sys
import json
from pathlib import Path
from typing import Dict, List, Optional, TypedDict, Literal
from datetime import datetime

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

# Load environment variables
def load_env():
    """Load environment variables from multiple possible locations"""
    possible_paths = [
        Path.cwd().parent.parent / '.env',  # Grandparent directory
        Path.cwd().parent / '.env',         # Parent directory
        Path.cwd() / '.env',               # Current directory
        Path('.env')                       # Relative path
    ]
    
    for path in possible_paths:
        if path.exists():
            load_dotenv(dotenv_path=path)
            print(f"✅ Loaded .env from: {path}")
            break
    else:
        print("⚠️  No .env file found - some features may not work")
    
    # Verify critical environment variables
    openai_key = os.getenv("OPENAI_API_KEY")
    if openai_key:
        print("✅ OPENAI_API_KEY loaded")
    else:
        print("❌ OPENAI_API_KEY not found - Please set up your API key")
        return False
    
    return True

# State definition for customer support
class SupportState(TypedDict):
    """State for customer support workflow"""
    messages: List[HumanMessage | AIMessage | SystemMessage]
    customer_id: Optional[str]
    ticket_id: Optional[str]
    issue_category: Optional[str]
    urgency_level: Optional[str]
    resolution_status: Optional[str]
    escalation_needed: bool
    knowledge_base_results: Optional[str]
    follow_up_required: bool
    conversation_summary: Optional[str]

# Customer Support Tools
@tool
def create_support_ticket(customer_id: str, issue_description: str, urgency: str = "medium") -> str:
    """Create a new support ticket."""
    ticket_id = f"TICKET-{datetime.now().strftime('%Y%m%d')}-{len(issue_description) % 1000:03d}"
    
    ticket_data = {
        "ticket_id": ticket_id,
        "customer_id": customer_id,
        "issue_description": issue_description,
        "urgency": urgency,
        "status": "open",
        "created_at": datetime.now().isoformat(),
        "assigned_to": None
    }
    
    # In a real system, this would save to a database
    print(f"🎫 Ticket Created: {ticket_id}")
    print(f"   Customer: {customer_id}")
    print(f"   Urgency: {urgency}")
    print(f"   Status: Open")
    
    return json.dumps(ticket_data, indent=2)

@tool
def search_knowledge_base(query: str) -> str:
    """Search the knowledge base for relevant articles."""
    # Simulated knowledge base
    kb_articles = {
        "password": "Article: How to Reset Your Password\n1. Go to login page\n2. Click 'Forgot Password'\n3. Enter your email\n4. Follow the reset link",
        "login": "Article: Common Login Issues\n- Check credentials\n- Clear browser cache\n- Disable VPN\n- Contact support if issues persist",
        "billing": "Article: Billing and Payment Issues\n- Update payment method in account settings\n- Check for subscription status\n- Review recent transactions",
        "account": "Article: Account Management\n- Update profile information\n- Manage subscriptions\n- View usage statistics\n- Security settings",
        "technical": "Article: Technical Troubleshooting\n- Check system requirements\n- Update software\n- Clear cache and cookies\n- Restart application"
    }
    
    query_lower = query.lower()
    results = []
    
    for key, article in kb_articles.items():
        if key in query_lower:
            results.append(article)
    
    if not results:
        results.append("No specific articles found. Please contact support for personalized assistance.")
    
    return "\n\n".join(results)

@tool
def check_order_status(order_id: str) -> str:
    """Check the status of a customer's order."""
    # Simulated order status check
    statuses = ["processing", "shipped", "delivered", "cancelled"]
    status = statuses[hash(order_id) % len(statuses)]
    
    response = f"Order Status for {order_id}:\n"
    response += f"Status: {status.upper()}\n"
    response += f"Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    
    if status == "shipped":
        response += "Tracking Number: TRK" + str(abs(hash(order_id)) % 1000000) + "\n"
        response += "Estimated Delivery: 2-3 business days\n"
    elif status == "delivered":
        response += "Delivered on: " + (datetime.now().replace(hour=14, minute=30)).strftime('%Y-%m-%d %H:%M:%S') + "\n"
    
    return response

@tool
def escalate_issue(ticket_id: str, reason: str, priority: str = "high") -> str:
    """Escalate an issue to a senior support agent."""
    escalation_id = f"ESC-{datetime.now().strftime('%Y%m%d')}-{len(ticket_id) % 100:03d}"
    
    escalation_data = {
        "escalation_id": escalation_id,
        "ticket_id": ticket_id,
        "reason": reason,
        "priority": priority,
        "escalated_to": "Senior Support Team",
        "escalated_at": datetime.now().isoformat(),
        "status": "pending_review"
    }
    
    print(f"🚨 Issue Escalated: {escalation_id}")
    print(f"   Ticket: {ticket_id}")
    print(f"   Reason: {reason}")
    print(f"   Priority: {priority}")
    
    return json.dumps(escalation_data, indent=2)

@tool
def schedule_follow_up(customer_id: str, ticket_id: str, follow_up_time: str) -> str:
    """Schedule a follow-up with the customer."""
    follow_up_id = f"FU-{datetime.now().strftime('%Y%m%d')}-{len(customer_id) % 100:03d}"
    
    follow_up_data = {
        "follow_up_id": follow_up_id,
        "customer_id": customer_id,
        "ticket_id": ticket_id,
        "scheduled_time": follow_up_time,
        "status": "scheduled",
        "created_at": datetime.now().isoformat()
    }
    
    print(f"📅 Follow-up Scheduled: {follow_up_id}")
    print(f"   Customer: {customer_id}")
    print(f"   Time: {follow_up_time}")
    
    return json.dumps(follow_up_data, indent=2)

# Workflow Nodes
def classify_issue_node(state: SupportState) -> SupportState:
    """Classify the customer's issue and determine category."""
    print("🔍 Classifying issue...")
    
    last_message = state["messages"][-1].content if state["messages"] else ""
    
    # Simple keyword-based classification
    categories = {
        "technical": ["error", "bug", "crash", "slow", "not working", "broken"],
        "billing": ["payment", "charge", "refund", "billing", "cost", "price"],
        "account": ["login", "password", "account", "profile", "access"],
        "order": ["order", "delivery", "shipping", "tracking", "package"],
        "general": ["help", "question", "information", "how to"]
    }
    
    issue_category = "general"
    for category, keywords in categories.items():
        if any(keyword in last_message.lower() for keyword in keywords):
            issue_category = category
            break
    
    state["issue_category"] = issue_category
    print(f"📋 Issue Category: {issue_category}")
    
    return state

def determine_urgency_node(state: SupportState) -> SupportState:
    """Determine the urgency level of the issue."""
    print("⚡ Assessing urgency...")
    
    last_message = state["messages"][-1].content if state["messages"] else ""
    
    urgency_keywords = {
        "urgent": ["urgent", "emergency", "critical", "immediately", "asap"],
        "high": ["important", "priority", "need help", "stuck"],
        "medium": ["question", "how to", "information"],
        "low": ["when", "maybe", "curious", "suggestion"]
    }
    
    urgency_level = "medium"
    for urgency, keywords in urgency_keywords.items():
        if any(keyword in last_message.lower() for keyword in keywords):
            urgency_level = urgency
            break
    
    state["urgency_level"] = urgency_level
    print(f"🚨 Urgency Level: {urgency_level}")
    
    return state

def search_knowledge_node(state: SupportState) -> SupportState:
    """Search knowledge base for relevant information."""
    print("📚 Searching knowledge base...")
    
    last_message = state["messages"][-1].content if state["messages"] else ""
    
    # Use the knowledge base search tool
    kb_results = search_knowledge_base.invoke({"query": last_message})
    state["knowledge_base_results"] = kb_results
    
    print("📖 Knowledge base search completed")
    
    return state

def create_ticket_node(state: SupportState) -> SupportState:
    """Create a support ticket if needed."""
    print("🎫 Creating support ticket...")
    
    last_message = state["messages"][-1].content if state["messages"] else ""
    customer_id = state.get("customer_id", "GUEST")
    urgency = state.get("urgency_level", "medium")
    
    # Create ticket
    ticket_result = create_support_ticket.invoke({
        "customer_id": customer_id,
        "issue_description": last_message,
        "urgency": urgency
    })
    
    # Extract ticket ID from result
    ticket_data = json.loads(ticket_result)
    state["ticket_id"] = ticket_data["ticket_id"]
    
    return state

def provide_response_node(state: SupportState) -> SupportState:
    """Generate a response to the customer."""
    print("💬 Generating response...")
    
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
    
    # Build context for response
    context_parts = []
    
    if state.get("issue_category"):
        context_parts.append(f"Issue Category: {state['issue_category']}")
    
    if state.get("urgency_level"):
        context_parts.append(f"Urgency: {state['urgency_level']}")
    
    if state.get("ticket_id"):
        context_parts.append(f"Ticket ID: {state['ticket_id']}")
    
    if state.get("knowledge_base_results"):
        context_parts.append(f"Knowledge Base Results:\n{state['knowledge_base_results']}")
    
    context = "\n".join(context_parts)
    
    # Get the last customer message
    last_message = state["messages"][-1].content if state["messages"] else ""
    
    # Generate response
    response_prompt = f"""
    You are a helpful customer support agent. Respond to the customer's query based on the context provided.
    
    Context:
    {context}
    
    Customer Message:
    {last_message}
    
    Guidelines:
    - Be empathetic and professional
    - Provide clear, actionable solutions
    - Reference the ticket ID if available
    - Suggest next steps
    - If the issue is complex, mention that you're escalating it
    - Keep responses concise but comprehensive
    
    Response:
    """
    
    response = llm.invoke([HumanMessage(content=response_prompt)])
    
    # Add the response to messages
    state["messages"].append(AIMessage(content=response.content))
    state["resolution_status"] = "responded"
    
    return state

def check_escalation_node(state: SupportState) -> SupportState:
    """Check if escalation is needed."""
    print("🔍 Checking escalation requirements...")
    
    urgency = state.get("urgency_level", "medium")
    category = state.get("issue_category", "general")
    
    # Escalation criteria
    escalation_needed = (
        urgency in ["urgent", "high"] or 
        category == "technical" and urgency != "low"
    )
    
    state["escalation_needed"] = escalation_needed
    
    if escalation_needed:
        print("🚨 Escalation required")
    else:
        print("✅ No escalation needed")
    
    return state

def escalate_node(state: SupportState) -> SupportState:
    """Escalate the issue to senior support."""
    print("🚨 Escalating issue...")
    
    ticket_id = state.get("ticket_id", "UNKNOWN")
    reason = f"High priority issue in category: {state.get('issue_category', 'unknown')}"
    
    escalation_result = escalate_issue.invoke({
        "ticket_id": ticket_id,
        "reason": reason,
        "priority": state.get("urgency_level", "high")
    })
    
    # Add escalation message
    escalation_msg = f"I've escalated your issue (Ticket: {ticket_id}) to our senior support team. They will review your case and get back to you within 2-4 hours."
    state["messages"].append(AIMessage(content=escalation_msg))
    
    return state

def should_escalate(state: SupportState) -> Literal["escalate", "respond"]:
    """Determine if escalation is needed."""
    return "escalate" if state.get("escalation_needed", False) else "respond"

def create_support_graph() -> StateGraph:
    """Create the customer support workflow graph."""
    
    # Build the graph
    builder = StateGraph(SupportState)
    
    # Add nodes
    builder.add_node("classify", classify_issue_node)
    builder.add_node("urgency", determine_urgency_node)
    builder.add_node("search_kb", search_knowledge_node)
    builder.add_node("create_ticket", create_ticket_node)
    builder.add_node("check_escalation", check_escalation_node)
    builder.add_node("respond", provide_response_node)
    builder.add_node("escalate", escalate_node)
    
    # Define the workflow
    builder.add_edge(START, "classify")
    builder.add_edge("classify", "urgency")
    builder.add_edge("urgency", "search_kb")
    builder.add_edge("search_kb", "create_ticket")
    builder.add_edge("create_ticket", "check_escalation")
    
    # Conditional edge for escalation
    builder.add_conditional_edges(
        "check_escalation",
        should_escalate,
        {
            "escalate": "escalate",
            "respond": "respond"
        }
    )
    
    builder.add_edge("escalate", END)
    builder.add_edge("respond", END)
    
    # Compile with memory
    memory = MemorySaver()
    graph = builder.compile(checkpointer=memory)
    
    return graph

class CustomerSupportAgent:
    """Main customer support agent class."""
    
    def __init__(self):
        self.graph = create_support_graph()
        self.current_customer_id = None
        self.thread_id = None
    
    def start_session(self, customer_id: str = None):
        """Start a new support session."""
        self.current_customer_id = customer_id or f"CUST-{datetime.now().strftime('%H%M%S')}"
        self.thread_id = f"support_{self.current_customer_id}_{datetime.now().strftime('%Y%m%d')}"
        
        print(f"\n🎯 New Support Session Started")
        print(f"👤 Customer ID: {self.current_customer_id}")
        print(f"🔗 Thread ID: {self.thread_id}")
        print("=" * 60)
    
    def process_message(self, message: str) -> str:
        """Process a customer message and return the response."""
        
        # Initialize state
        state = SupportState(
            messages=[HumanMessage(content=message)],
            customer_id=self.current_customer_id,
            ticket_id=None,
            issue_category=None,
            urgency_level=None,
            resolution_status=None,
            escalation_needed=False,
            knowledge_base_results=None,
            follow_up_required=False,
            conversation_summary=None
        )
        
        # Configure thread for memory
        config = {"configurable": {"thread_id": self.thread_id}}
        
        # Process through the graph
        try:
            result = self.graph.invoke(state, config)
            
            # Return the last AI message
            ai_messages = [msg for msg in result["messages"] if isinstance(msg, AIMessage)]
            if ai_messages:
                return ai_messages[-1].content
            else:
                return "I apologize, but I couldn't process your request. Please try again."
        
        except Exception as e:
            return f"I encountered an error: {str(e)}. Please try again or contact our support team directly."
    
    def end_session(self):
        """End the current support session."""
        print(f"\n📋 Support Session Ended")
        print(f"👤 Customer: {self.current_customer_id}")
        print("=" * 60)

def interactive_console():
    """Run the interactive console-based customer support."""
    
    print("🤖 Customer Support Agent - Interactive Console")
    print("=" * 60)
    print("Type 'quit' to exit, 'help' for commands")
    print("=" * 60)
    
    # Initialize the agent
    agent = CustomerSupportAgent()
    
    # Get customer ID
    customer_id = input("Enter your customer ID (or press Enter for guest): ").strip()
    if not customer_id:
        customer_id = f"GUEST-{datetime.now().strftime('%H%M%S')}"
    
    agent.start_session(customer_id)
    
    print("\n💬 How can I help you today?")
    print("-" * 60)
    
    while True:
        try:
            # Get user input
            user_input = input("\n👤 You: ").strip()
            
            # Check for commands
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("\n👋 Thank you for contacting support. Have a great day!")
                agent.end_session()
                break
            
            elif user_input.lower() == 'help':
                print("\n📖 Available commands:")
                print("  help  - Show this help message")
                print("  quit  - Exit the support session")
                print("  status - Check current session status")
                print("\n💬 You can also ask about:")
                print("  • Password reset")
                print("  • Login issues")
                print("  • Billing problems")
                print("  • Order status")
                print("  • Technical support")
                continue
            
            elif user_input.lower() == 'status':
                print(f"\n📊 Session Status:")
                print(f"  Customer ID: {agent.current_customer_id}")
                print(f"  Thread ID: {agent.thread_id}")
                print(f"  Session Active: ✅")
                continue
            
            elif not user_input:
                print("⚠️  Please enter a message or type 'help' for commands.")
                continue
            
            # Process the message
            print("\n🤖 Processing...")
            response = agent.process_message(user_input)
            
            print(f"\n🤖 Support Agent: {response}")
            print("-" * 60)
        
        except KeyboardInterrupt:
            print("\n\n👋 Session interrupted. Goodbye!")
            agent.end_session()
            break
        
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")
            print("Please try again or type 'quit' to exit.")

def main():
    """Main function to run the customer support agent."""
    print("🚀 Starting Customer Support Agent...")
    
    # Load environment
    if not load_env():
        print("❌ Failed to load environment. Exiting...")
        return
    
    print("\n✅ Environment loaded successfully!")
    
    # Start interactive console
    interactive_console()

if __name__ == "__main__":
    main()
