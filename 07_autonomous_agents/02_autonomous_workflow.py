"""
Advanced Autonomous Workflow with LangGraph

This script demonstrates a sophisticated autonomous agent implementation
using LangGraph for state management and workflow orchestration. It builds
upon the basic AutoGPT concepts to create a more robust and production-ready
autonomous agent.

Key Features:
- LangGraph-based state management
- Sophisticated planning and execution cycles
- Advanced memory and learning capabilities
- Error handling and recovery mechanisms
- Real-time monitoring and observability
"""

import os
import json
import time
from datetime import datetime
from typing import List, Dict, Any, Optional, TypedDict, Annotated
from dataclasses import dataclass, field

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver

from dotenv import load_dotenv

# Import our custom tools
from utils.autogpt_tools import AutoGPTTools, SafetyConfig, get_autogpt_tools

# Load environment variables
load_dotenv()


class AgentState(TypedDict):
    """State definition for the autonomous agent workflow"""
    # Goal and planning
    goal: str
    original_goal: str
    plan: List[Dict[str, Any]]
    current_task_index: int
    
    # Execution state
    messages: List[Dict[str, Any]]
    current_action: Optional[str]
    action_result: Optional[str]
    
    # Memory and learning
    working_memory: List[str]
    key_findings: List[str]
    completed_tasks: List[str]
    failed_tasks: List[str]
    
    # Monitoring and control
    iteration_count: int
    max_iterations: int
    total_cost: float
    errors: List[str]
    
    # Decision making
    last_decision: str
    decision_rationale: str
    next_action_type: str  # 'plan', 'execute', 'reflect', 'finalize'
    
    # Status
    status: str  # 'planning', 'executing', 'reflecting', 'completed', 'failed'
    completion_confidence: float


class AdvancedAutonomousAgent:
    """Advanced autonomous agent using LangGraph for workflow management"""
    
    def __init__(self, goal: str, max_iterations: int = 15, safety_config: Optional[SafetyConfig] = None):
        self.goal = goal
        self.max_iterations = max_iterations
        self.safety_config = safety_config or SafetyConfig()
        
        # Initialize components
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.1)
        self.tools_manager = AutoGPTTools(safety_config)
        self.tools = self.tools_manager.get_all_tools()
        self.tool_node = ToolNode(self.tools)
        
        # Initialize state
        self.initial_state = AgentState(
            goal=goal,
            original_goal=goal,
            plan=[],
            current_task_index=0,
            messages=[],
            current_action=None,
            action_result=None,
            working_memory=[],
            key_findings=[],
            completed_tasks=[],
            failed_tasks=[],
            iteration_count=0,
            max_iterations=max_iterations,
            total_cost=0.0,
            errors=[],
            last_decision="",
            decision_rationale="",
            next_action_type="plan",
            status="planning",
            completion_confidence=0.0
        )
        
        # Build the workflow graph
        self.workflow = self._build_workflow()
        self.memory = MemorySaver()
        
        # Initialize working memory
        self.tools_manager.memory_manager.add_working_memory(f"Agent initialized with goal: {goal}")
    
    def _build_workflow(self) -> StateGraph:
        """Build the LangGraph workflow for autonomous operation"""
        
        workflow = StateGraph(AgentState)
        
        # Add nodes
        workflow.add_node("planner", self._planner_node)
        workflow.add_node("executor", self._executor_node)
        workflow.add_node("reflector", self._reflector_node)
        workflow.add_node("decision_maker", self._decision_maker_node)
        workflow.add_node("finalizer", self._finalizer_node)
        workflow.add_node("tools", self.tool_node)
        
        # Add conditional edges
        workflow.add_conditional_edges(
            "decision_maker",
            self._route_decision,
            {
                "plan": "planner",
                "execute": "executor",
                "reflect": "reflector",
                "finalize": "finalizer",
                "end": END
            }
        )
        
        workflow.add_conditional_edges(
            "executor",
            self._route_execution,
            {
                "decision": "decision_maker",
                "tools": "tools",
                "end": END
            }
        )
        
        # Add regular edges
        workflow.add_edge("planner", "decision_maker")
        workflow.add_edge("reflector", "decision_maker")
        workflow.add_edge("finalizer", END)
        workflow.add_edge("tools", "decision_maker")
        
        # Set entry point
        workflow.set_entry_point("planner")
        
        return workflow.compile(checkpointer=self.memory)
    
    def _planner_node(self, state: AgentState) -> AgentState:
        """Planning node - creates and refines the execution plan"""
        print(f"\n📋 [PLANNER] Creating plan for: {state['goal']}")
        
        # Get context from memory
        relevant_memory = self.tools_manager.memory_manager.get_relevant_memory(state['goal'])
        
        planning_prompt = f"""You are an expert planning AI. Your task is to create a detailed plan for achieving the following goal:

GOAL: {state['goal']}

CONTEXT:
{self._format_context(state)}

RELEVANT MEMORY:
{self._format_memory(relevant_memory)}

Create a plan with 3-5 specific, actionable tasks. Each task should:
1. Be clear and measurable
2. Have a specific deliverable
3. Be achievable with available tools
4. Contribute meaningfully to the overall goal

Format your response as a JSON object:
{{
    "plan": [
        {{
            "id": "task_1",
            "description": "Specific task description",
            "priority": "high|medium|low",
            "estimated_difficulty": "easy|medium|hard",
            "dependencies": []
        }}
    ],
    "rationale": "Explanation of why this plan will achieve the goal"
}}"""

        try:
            response = self.llm.invoke([
                SystemMessage(content="You are an expert strategic planner. Always respond with valid JSON."),
                HumanMessage(content=planning_prompt)
            ])
            
            # Parse the plan
            plan_data = json.loads(response.content)
            state['plan'] = plan_data.get('plan', [])
            state['status'] = 'executing'
            
            # Store plan in memory
            self.tools_manager.memory_manager.add_long_term_memory(
                f"Created plan: {plan_data.get('rationale', 'No rationale')}",
                "planning"
            )
            
            print(f"✅ Plan created with {len(state['plan'])} tasks")
            
        except Exception as e:
            error_msg = f"Planning failed: {str(e)}"
            state['errors'].append(error_msg)
            print(f"❌ {error_msg}")
            
            # Fallback plan
            state['plan'] = self._create_fallback_plan(state['goal'])
        
        state['working_memory'].append(f"Planned {len(state['plan'])} tasks")
        return state
    
    def _executor_node(self, state: AgentState) -> AgentState:
        """Executor node - carries out the current task"""
        if state['current_task_index'] >= len(state['plan']):
            state['next_action_type'] = 'reflect'
            return state
        
        current_task = state['plan'][state['current_task_index']]
        task_desc = current_task['description']
        
        print(f"\n⚡ [EXECUTOR] Executing task: {task_desc}")
        
        # Determine if we need to use tools or can handle directly
        execution_prompt = f"""You are executing this task: "{task_desc}"

Available tools: {[tool.name for tool in self.tools]}

CONTEXT:
{self._format_context(state)}

Decide what action to take:
1. If you need to search, save files, or use other tools - respond with "USE_TOOLS: your specific instruction"
2. If you can complete the task with reasoning - respond with "DIRECT: your reasoning and result"

Be specific and actionable."""

        try:
            response = self.llm.invoke([
                SystemMessage(content="You are an efficient task executor. Always be direct and specific."),
                HumanMessage(content=execution_prompt)
            ])
            
            response_text = response.content.strip()
            
            if response_text.startswith("USE_TOOLS:"):
                # Route to tools
                instruction = response_text.replace("USE_TOOLS:", "").strip()
                state['current_action'] = instruction
                state['next_action_type'] = 'tools'
                
            elif response_text.startswith("DIRECT:"):
                # Direct execution
                result = response_text.replace("DIRECT:", "").strip()
                state['action_result'] = result
                state['completed_tasks'].append(task_desc)
                state['current_task_index'] += 1
                state['next_action_type'] = 'decision'
                
                # Store result
                self.tools_manager.memory_manager.add_episodic_memory(
                    f"Execute task: {task_desc}",
                    result,
                    "direct_execution"
                )
                
                print(f"✅ Task completed directly")
                
            else:
                # Default to tools if unclear
                state['current_action'] = response_text
                state['next_action_type'] = 'tools'
            
        except Exception as e:
            error_msg = f"Execution failed: {str(e)}"
            state['errors'].append(error_msg)
            state['failed_tasks'].append(task_desc)
            state['current_task_index'] += 1
            state['next_action_type'] = 'decision'
            
            print(f"❌ {error_msg}")
        
        state['working_memory'].append(f"Executed: {task_desc}")
        return state
    
    def _reflector_node(self, state: AgentState) -> AgentState:
        """Reflector node - analyzes progress and learns"""
        print(f"\n🤔 [REFLECTOR] Analyzing progress")
        
        reflection_prompt = f"""You are reflecting on the progress toward this goal: {state['original_goal']}

PROGRESS SUMMARY:
- Completed tasks: {len(state['completed_tasks'])}
- Failed tasks: {len(state['failed_tasks'])}
- Current iteration: {state['iteration_count']}/{state['max_iterations']}

COMPLETED TASKS:
{chr(10).join(f"- {task}" for task in state['completed_tasks'])}

KEY FINDINGS:
{chr(10).join(f"- {finding}" for finding in state['key_findings'])}

ERRORS ENCOUNTERED:
{chr(10).join(f"- {error}" for error in state['errors'])}

Analyze the progress and provide:
1. Overall assessment (0-100% complete)
2. Key insights learned
3. Major challenges encountered
4. Recommendations for next steps
5. Whether the goal is achievable in remaining iterations

Format as JSON:
{{
    "completion_percentage": 85,
    "insights": ["key insight 1", "key insight 2"],
    "challenges": ["challenge 1", "challenge 2"],
    "recommendations": ["recommendation 1"],
    "goal_achievable": true,
    "confidence_score": 0.85
}}"""

        try:
            response = self.llm.invoke([
                SystemMessage(content="You are an analytical reflector. Always respond with valid JSON."),
                HumanMessage(content=reflection_prompt)
            ])
            
            reflection_data = json.loads(response.content)
            
            # Update state with reflection insights
            state['completion_confidence'] = reflection_data.get('confidence_score', 0.5)
            
            # Add insights to key findings
            for insight in reflection_data.get('insights', []):
                if insight not in state['key_findings']:
                    state['key_findings'].append(insight)
                    self.tools_manager.memory_manager.add_long_term_memory(insight, "insight")
            
            print(f"📊 Completion confidence: {state['completion_confidence']:.2f}")
            
        except Exception as e:
            print(f"❌ Reflection failed: {str(e)}")
        
        state['working_memory'].append("Completed reflection cycle")
        return state
    
    def _decision_maker_node(self, state: AgentState) -> AgentState:
        """Decision maker node - determines next action"""
        print(f"\n🎯 [DECISION] Determining next action")
        
        decision_prompt = f"""You are the decision maker for an autonomous agent working on: {state['original_goal']}

CURRENT STATE:
- Status: {state['status']}
- Iteration: {state['iteration_count']}/{state['max_iterations']}
- Tasks completed: {len(state['completed_tasks'])}
- Tasks remaining: {len(state['plan']) - state['current_task_index']}
- Confidence: {state['completion_confidence']:.2f}

CONTEXT:
{self._format_context(state)}

Decide the next action type:
- "plan": Need to create or revise the plan
- "execute": Continue executing current plan
- "reflect": Need to analyze progress and learn
- "finalize": Goal is complete or should be finalized
- "end": Stop execution (due to errors or limits)

Consider:
1. Are we making good progress?
2. Do we have remaining tasks?
3. Are we hitting iteration limits?
4. Is confidence high enough to finalize?

Respond with just the action type (one word)."""

        try:
            response = self.llm.invoke([
                SystemMessage(content="You are a decisive AI. Always respond with a single action type."),
                HumanMessage(content=decision_prompt)
            ])
            
            decision = response.content.strip().lower()
            valid_decisions = ['plan', 'execute', 'reflect', 'finalize', 'end']
            
            if decision in valid_decisions:
                state['next_action_type'] = decision
                state['last_decision'] = decision
            else:
                state['next_action_type'] = 'execute'  # Default
                state['last_decision'] = 'execute (default)'
            
            print(f"🎯 Decision: {state['next_action_type']}")
            
        except Exception as e:
            print(f"❌ Decision making failed: {str(e)}")
            state['next_action_type'] = 'execute'
        
        state['iteration_count'] += 1
        return state
    
    def _finalizer_node(self, state: AgentState) -> AgentState:
        """Finalizer node - creates final summary and results"""
        print(f"\n🎉 [FINALIZER] Creating final summary")
        
        finalization_prompt = f"""You are finalizing the work on this goal: {state['original_goal']}

WORK SUMMARY:
- Total iterations: {state['iteration_count']}
- Tasks completed: {len(state['completed_tasks'])}
- Tasks failed: {len(state['failed_tasks'])}
- Confidence score: {state['completion_confidence']:.2f}

COMPLETED TASKS:
{chr(10).join(f"- {task}" for task in state['completed_tasks'])}

KEY FINDINGS:
{chr(10).join(f"- {finding}" for finding in state['key_findings'])}

Create a comprehensive final report including:
1. Executive summary of what was accomplished
2. Detailed methodology and approach
3. Key findings and insights
4. Challenges and how they were overcome
5. Recommendations for further work
6. Assessment of goal achievement

Make it professional and well-structured."""

        try:
            response = self.llm.invoke([
                SystemMessage(content="You are an expert report writer creating comprehensive summaries."),
                HumanMessage(content=finalization_prompt)
            ])
            
            final_report = response.content
            
            # Save final report
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"final_report_{timestamp}.md"
            self.tools_manager.save_file(final_report, filename, "reports")
            
            state['action_result'] = final_report
            state['status'] = 'completed'
            
            print(f"✅ Final report saved as {filename}")
            
        except Exception as e:
            error_msg = f"Finalization failed: {str(e)}"
            state['errors'].append(error_msg)
            print(f"❌ {error_msg}")
        
        return state
    
    def _route_decision(self, state: AgentState) -> str:
        """Route based on decision maker output"""
        return state['next_action_type']
    
    def _route_execution(self, state: AgentState) -> str:
        """Route based on executor needs"""
        return state['next_action_type']
    
    def _format_context(self, state: AgentState) -> str:
        """Format state context for prompts"""
        context = f"""
Current Status: {state['status']}
Iteration: {state['iteration_count']}/{state['max_iterations']}
Current Task Index: {state['current_task_index']}

Recent Actions:
{chr(10).join(f"- {action}" for action in state['working_memory'][-5:])}
"""
        return context
    
    def _format_memory(self, memory_entries: List[Dict]) -> str:
        """Format memory entries for prompts"""
        if not memory_entries:
            return "No relevant memory found."
        
        formatted = []
        for entry in memory_entries[:5]:  # Top 5 entries
            content = entry.get('content', entry.get('action', ''))
            formatted.append(f"- {content[:100]}...")
        
        return chr(10).join(formatted)
    
    def _create_fallback_plan(self, goal: str) -> List[Dict[str, Any]]:
        """Create a simple fallback plan"""
        return [
            {
                "id": "fallback_1",
                "description": f"Research information about {goal}",
                "priority": "high",
                "estimated_difficulty": "medium",
                "dependencies": []
            },
            {
                "id": "fallback_2",
                "description": f"Analyze key aspects of {goal}",
                "priority": "high",
                "estimated_difficulty": "medium",
                "dependencies": ["fallback_1"]
            },
            {
                "id": "fallback_3",
                "description": f"Create summary report about {goal}",
                "priority": "medium",
                "estimated_difficulty": "easy",
                "dependencies": ["fallback_2"]
            }
        ]
    
    def run(self) -> Dict[str, Any]:
        """Run the advanced autonomous agent"""
        print("🚀 Starting Advanced Autonomous Agent")
        print(f"📋 Goal: {self.goal}")
        print(f"🔄 Max iterations: {self.max_iterations}")
        print("=" * 60)
        
        # Create config for the workflow
        config = {"configurable": {"thread_id": "autonomous_agent"}}
        
        try:
            # Run the workflow
            result = self.workflow.invoke(self.initial_state, config=config)
            
            print("\n" + "=" * 60)
            print("🎉 Autonomous Agent Execution Complete!")
            print(f"📊 Final Status: {result['status']}")
            print(f"🔄 Total Iterations: {result['iteration_count']}")
            print(f"✅ Tasks Completed: {len(result['completed_tasks'])}")
            print(f"❌ Tasks Failed: {len(result['failed_tasks'])}")
            print(f"🎯 Confidence Score: {result['completion_confidence']:.2f}")
            
            # Get usage statistics
            usage_stats = self.tools_manager.get_usage_stats()
            print(f"\n{usage_stats}")
            
            return result
            
        except Exception as e:
            print(f"\n❌ Agent execution failed: {str(e)}")
            return {"status": "failed", "error": str(e)}


def main():
    """Main function to demonstrate the advanced autonomous agent"""
    
    print("🤖 Advanced Autonomous Agent Demo")
    print("=" * 50)
    
    # Example goals
    goals = [
        "Research the latest developments in quantum computing and create a comprehensive report",
        "Analyze current trends in renewable energy and identify key opportunities",
        "Investigate the impact of AI on healthcare and create a strategic analysis",
        "Study the future of work in the age of automation and provide recommendations"
    ]
    
    print("\nAvailable goals:")
    for i, goal in enumerate(goals, 1):
        print(f"{i}. {goal}")
    print("5. Custom goal")
    
    choice = input("\nSelect a goal (1-5): ").strip()
    
    if choice == "5":
        custom_goal = input("Enter your goal: ").strip()
        goal = custom_goal if custom_goal else goals[0]
    elif choice in ["1", "2", "3", "4"]:
        goal = goals[int(choice) - 1]
    else:
        goal = goals[0]
    
    print(f"\n🎯 Selected Goal: {goal}")
    
    # Configure safety settings
    safety_config = SafetyConfig(
        max_searches_per_session=15,
        max_file_operations=30,
        max_tokens_per_session=50000
    )
    
    # Create and run the advanced agent
    agent = AdvancedAutonomousAgent(
        goal=goal,
        max_iterations=12,
        safety_config=safety_config
    )
    
    result = agent.run()
    
    # Save results
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    results_file = f"advanced_agent_results_{timestamp}.json"
    
    try:
        with open(f"autonomous_agent_output/{results_file}", 'w') as f:
            json.dump(result, f, indent=2, default=str)
        print(f"\n📊 Results saved to: autonomous_agent_output/{results_file}")
    except Exception as e:
        print(f"Failed to save results: {e}")


if __name__ == "__main__":
    main()
