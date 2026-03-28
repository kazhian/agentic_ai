"""
AutoGPT Concepts - Basic Autonomous Agent Implementation

This script demonstrates the fundamental concepts of autonomous agents
inspired by AutoGPT. It shows how to create an agent that can:
1. Take a high-level goal
2. Break it down into smaller tasks
3. Execute tasks using tools
4. Maintain memory and context
5. Make decisions about next steps

Key Concepts Demonstrated:
- Goal decomposition
- Tool usage
- Memory management
- Autonomous decision making
- Self-reflection and iteration
"""

import os
import json
from datetime import datetime
from typing import List, Dict, Any
from dataclasses import dataclass, field

from langchain_openai import ChatOpenAI
from langchain.agents.factory import create_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import Tool, tool
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage


from dotenv import load_dotenv

# Load environment variables
load_dotenv()

@dataclass
class Task:
    """Represents a single task in the autonomous agent's plan"""
    id: str
    description: str
    status: str = "pending"  # pending, in_progress, completed, failed
    result: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "description": self.description,
            "status": self.status,
            "result": self.result,
            "created_at": self.created_at.isoformat()
        }

@dataclass
class AgentMemory:
    """Simple memory system for the autonomous agent"""
    short_term: List[str] = field(default_factory=list)
    long_term: List[str] = field(default_factory=list)
    tasks: List[Task] = field(default_factory=list)
    
    def add_short_term(self, content: str):
        """Add to short-term memory (recent actions/thoughts)"""
        self.short_term.append(f"[{datetime.now().strftime('%H:%M:%S')}] {content}")
        # Keep only last 10 items in short-term memory
        if len(self.short_term) > 10:
            self.short_term.pop(0)
    
    def add_long_term(self, content: str):
        """Add important information to long-term memory"""
        self.long_term.append(f"[{datetime.now().strftime('%Y-%m-%d %H:%M')}] {content}")
    
    def get_context(self) -> str:
        """Get current context for decision making"""
        context = "=== CURRENT CONTEXT ===\n"
        
        if self.tasks:
            context += "\nActive Tasks:\n"
            for task in self.tasks:
                if task.status != "completed":
                    context += f"- {task.description} [{task.status}]\n"
        
        if self.short_term:
            context += "\nRecent Actions:\n"
            for item in self.short_term[-5:]:  # Last 5 actions
                context += f"- {item}\n"
        
        if self.long_term:
            context += "\nKey Information:\n"
            for item in self.long_term[-3:]:  # Last 3 key findings
                context += f"- {item}\n"
        
        return context

class AutonomousAgent:
    """Basic autonomous agent implementation inspired by AutoGPT concepts"""
    
    def __init__(self, goal: str, max_iterations: int = 10):
        self.goal = goal
        self.max_iterations = max_iterations
        self.memory = AgentMemory()
        self.iteration = 0
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.1)
        
        # Initialize memory
        self.memory.add_long_term(f"Primary Goal: {goal}")
        self.memory.add_short_term(f"Agent initialized with goal: {goal}")
        
        # Create tools
        self.tools = self._create_tools()
        
        # Create agent
        self.agent_executor = self._create_agent()
    
    def _create_tools(self) -> List[Tool]:
        """Create tools for the autonomous agent"""
        
        @tool
        def web_search(query: str) -> str:
            """Search the web for information"""
            try:
                from tavily import TavilyClient
                client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
                result = client.search(query, max_results=3)
                
                search_results = []
                for article in result["results"]:
                    search_results.append(f"Title: {article['title']}\nContent: {article['content'][:200]}...\nURL: {article['url']}")
                
                return "\n\n".join(search_results)
            except Exception as e:
                return f"Search failed: {str(e)}"
        
        @tool
        def save_to_file(content: str, filename: str) -> str:
            """Save content to a file. Provide content and filename"""
            try:
                filepath = f"autonomous_agent_output/{filename}"
                os.makedirs("autonomous_agent_output", exist_ok=True)
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                self.memory.add_long_term(f"Saved file: {filename}")
                return f"Successfully saved to {filepath}"
            except Exception as e:
                return f"Failed to save file: {str(e)}"
        
        @tool
        def read_file(filename: str) -> str:
            """Read content from a file"""
            try:
                filepath = f"autonomous_agent_output/{filename}"
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                return content
            except Exception as e:
                return f"Failed to read file: {str(e)}"
        
        @tool
        def update_task(task_id: str, status: str, result: str = "") -> str:
            """Update task status and result. Provide task_id, status, and optional result"""
            for task in self.memory.tasks:
                if task.id == task_id:
                    task.status = status
                    if result:
                        task.result = result
                    self.memory.add_short_term(f"Updated task {task_id}: {status}")
                    return f"Task {task_id} updated to {status}"
            return f"Task {task_id} not found"
        
        @tool
        def create_task(description: str) -> str:
            """Create a new task with a description"""
            task_id = f"task_{len(self.memory.tasks) + 1}"
            task = Task(id=task_id, description=description)
            self.memory.tasks.append(task)
            self.memory.add_short_term(f"Created task: {description}")
            return f"Created task {task_id}: {description}"
        
        @tool
        def list_tasks() -> str:
            """List all current tasks and their status"""
            if not self.memory.tasks:
                return "No tasks created yet"
            
            task_list = []
            for task in self.memory.tasks:
                task_list.append(f"{task.id}: {task.description} [{task.status}]")
            
            return "\n".join(task_list)
        
        @tool
        def get_current_time() -> str:
            """Get the current time"""
            return f"Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        return [
            web_search,
            save_to_file,
            read_file,
            create_task,
            update_task,
            list_tasks,
            get_current_time
        ]
    
    def _create_agent(self):
        """Create the agent with planning and execution capabilities"""
        
        # System prompt that emphasizes autonomous behavior
        system_prompt = """You are an autonomous agent working towards a goal. Your capabilities include:

1. **Planning**: Break down complex goals into smaller, manageable tasks
2. **Execution**: Use available tools to complete tasks
3. **Memory**: Maintain context and learn from previous actions
4. **Adaptation**: Adjust your approach based on results

Your primary goal is: {goal}

Current context:
{context}

Guidelines:
- Always think step by step
- Create tasks before executing them
- Update task status as you work
- Save important findings to files
- Learn from failures and try different approaches
- Work autonomously - make decisions without waiting for input
- Be methodical and thorough

Available tools: {tools}

Think about what you need to do next, then use the appropriate tool to do it."""

        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", "{input}"),
        ])
        
        agent = create_agent(self.llm, self.tools)
        return prompt | agent
    
    def _create_plan(self) -> str:
        """Create an initial plan to achieve the goal"""
        planning_prompt = f"""You are an autonomous planning agent. Your goal is: {self.goal}

Create a detailed plan with 3-5 specific, actionable tasks. Each task should:
1. Be clear and specific
2. Have a measurable outcome
3. Contribute to the overall goal
4. Be achievable with available tools

Format your response as a numbered list of tasks."""

        response = self.llm.invoke([
            SystemMessage(content="You are an expert planner who breaks down complex goals into actionable steps."),
            HumanMessage(content=planning_prompt)
        ])
        
        return response.content
    
    def _make_decision(self) -> str:
        """Decide what to do next based on current state"""
        decision_prompt = f"""You are an autonomous agent deciding your next action.

Goal: {self.goal}
Current iteration: {self.iteration}/{self.max_iterations}

Current context:
{self.memory.get_context()}

Based on your current state, decide what to do next. Consider:
1. Are there pending tasks to complete?
2. Do you need to create new tasks?
3. Should you search for more information?
4. Is it time to synthesize results?
5. Have you achieved the goal?

Respond with a clear, specific action you should take next."""

        response = self.llm.invoke([
            SystemMessage(content="You are an autonomous decision-making agent. Always choose the most logical next step."),
            HumanMessage(content=decision_prompt)
        ])
        
        return response.content
    
    def run(self) -> Dict[str, Any]:
        """Run the autonomous agent"""
        print(f"🚀 Starting Autonomous Agent")
        print(f"📋 Goal: {self.goal}")
        print(f"🔄 Max iterations: {self.max_iterations}")
        print("-" * 50)
        
        # Create initial plan
        print("📝 Creating initial plan...")
        plan = self._create_plan()
        print(f"Initial Plan:\n{plan}")
        
        # Create tasks from plan
        self.memory.add_short_term("Created initial plan")
        
        # Main autonomous loop
        while self.iteration < self.max_iterations:
            self.iteration += 1
            print(f"\n🔄 Iteration {self.iteration}/{self.max_iterations}")
            
            # Make decision about next action
            next_action = self._make_decision()
            print(f"🤔 Decision: {next_action}")
            
            # Execute the decision
            try:
                context = self.memory.get_context()
                
                # Execute with proper format for new LangChain API
                result = self.agent_executor.invoke({
                    "input": next_action,
                    "goal": self.goal,
                    "context": context,
                    "tools": ", ".join([tool.name for tool in self.tools])
                })
                
                self.memory.add_short_term(f"Executed: {next_action}")
                
                # Handle different result types from new LangChain API
                if isinstance(result, dict) and 'output' in result:
                    output_text = result['output']
                elif isinstance(result, dict) and 'messages' in result:
                    # Extract from messages if present
                    messages = result['messages']
                    output_text = messages[-1].content if messages else "No output"
                elif hasattr(result, 'content'):
                    # AIMessage or similar
                    output_text = result.content
                else:
                    # String or other type
                    output_text = str(result)
                
                print(f"✅ Result: {output_text[:200] if output_text else 'Completed'}...")
                
            except Exception as e:
                self.memory.add_short_term(f"Error: {str(e)}")
                print(f"❌ Error: {str(e)}")
            
            # Check if goal is achieved
            completed_tasks = [t for t in self.memory.tasks if t.status == "completed"]
            if len(completed_tasks) >= 3:  # Simple completion check
                print("\n🎉 Goal appears to be achieved!")
                break
        
        # Generate final summary
        summary = self._generate_summary()
        
        return {
            "goal": self.goal,
            "iterations": self.iteration,
            "tasks": [task.to_dict() for task in self.memory.tasks],
            "memory": {
                "short_term": self.memory.short_term,
                "long_term": self.memory.long_term
            },
            "summary": summary
        }
    
    def _generate_summary(self) -> str:
        """Generate a final summary of the agent's work"""
        summary_prompt = f"""You are an autonomous agent providing a final summary of your work.

Goal: {self.goal}
Tasks completed: {len([t for t in self.memory.tasks if t.status == 'completed'])}
Total tasks: {len(self.memory.tasks)}

Tasks:
{[f"- {t.description}: {t.status}" for t in self.memory.tasks]}

Key findings from memory:
{self.memory.long_term[-5:] if self.memory.long_term else "No key findings recorded"}

Provide a comprehensive summary of:
1. What you accomplished
2. Key findings and insights
3. Any challenges encountered
4. Recommendations for next steps"""

        response = self.llm.invoke([
            SystemMessage(content="You are an autonomous reporting agent providing comprehensive summaries."),
            HumanMessage(content=summary_prompt)
        ])
        
        return response.content

def main():
    """Main function to demonstrate the autonomous agent"""
    
    # Example goals you can try:
    goals = [
        "Research the latest trends in artificial intelligence and write a summary report",
        "Find information about renewable energy advancements and create a fact sheet",
        "Research Python best practices for 2024 and create a guide"
    ]
    
    # For testing, hardcode goal
    goal = goals[0]
    
    print(f"\n🎯 Selected Goal: {goal}")
    
    # Create and run the autonomous agent
    agent = AutonomousAgent(goal=goal, max_iterations=2)
    result = agent.run()
    
    # Create output directory if it doesn't exist
    os.makedirs("autonomous_agent_output", exist_ok=True)
    
    # Save results
    results_file = f"autonomous_agent_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(f"autonomous_agent_output/{results_file}", 'w') as f:
        json.dump(result, f, indent=2, default=str)
    
    print(f"\n📊 Results saved to: autonomous_agent_output/{results_file}")
    if "summary" in result:
        print("\n📋 Final Summary:")
        print(result["summary"])
    else:
        print("\n📋 Execution completed. Check the saved results file.")

if __name__ == "__main__":
    main()
