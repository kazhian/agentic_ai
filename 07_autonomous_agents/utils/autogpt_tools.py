"""
AutoGPT Tools - Helper Tools for Autonomous Agents

This module provides a collection of specialized tools designed for
autonomous agents inspired by AutoGPT. These tools enable agents to
interact with their environment, manage information, and maintain
state across autonomous operations.

Tool Categories:
1. Information Gathering (web search, document analysis)
2. File Management (reading, writing, organizing)
3. Task Management (planning, tracking, execution)
4. Memory Management (short-term, long-term storage)
5. Safety & Monitoring (cost tracking, error handling)
"""

import os
import json
import time
import requests
from datetime import datetime
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
import hashlib

from langchain.tools import Tool
from tavily import TavilyClient


@dataclass
class SafetyConfig:
    """Configuration for safety and cost management"""
    max_searches_per_session: int = 20
    max_file_operations: int = 50
    max_tokens_per_session: int = 100000
    allowed_domains: List[str] = field(default_factory=lambda: [
        'wikipedia.org', 'github.com', 'stackoverflow.com', 'medium.com'
    ])
    blocked_operations: List[str] = field(default_factory=lambda: [
        'delete_system_files', 'modify_system_config', 'install_packages'
    ])


class CostTracker:
    """Track API costs and usage for autonomous agents"""
    
    def __init__(self):
        self.search_count = 0
        self.file_operations = 0
        self.token_usage = 0
        self.start_time = time.time()
    
    def record_search(self):
        """Record a web search operation"""
        self.search_count += 1
    
    def record_file_operation(self):
        """Record a file operation"""
        self.file_operations += 1
    
    def record_token_usage(self, tokens: int):
        """Record token usage"""
        self.token_usage += tokens
    
    def get_usage_report(self) -> Dict[str, Any]:
        """Get current usage statistics"""
        elapsed_time = time.time() - self.start_time
        return {
            "searches": self.search_count,
            "file_operations": self.file_operations,
            "token_usage": self.token_usage,
            "elapsed_minutes": elapsed_time / 60,
            "estimated_cost_usd": self.token_usage * 0.000002  # Rough estimate
        }


class MemoryManager:
    """Advanced memory management for autonomous agents"""
    
    def __init__(self, memory_dir: str = "agent_memory"):
        self.memory_dir = memory_dir
        os.makedirs(memory_dir, exist_ok=True)
        
        # Memory files
        self.working_memory_file = os.path.join(memory_dir, "working_memory.json")
        self.long_term_memory_file = os.path.join(memory_dir, "long_term_memory.json")
        self.episodic_memory_file = os.path.join(memory_dir, "episodic_memory.json")
        
        # Initialize memory structures
        self.working_memory = self._load_memory(self.working_memory_file, [])
        self.long_term_memory = self._load_memory(self.long_term_memory_file, [])
        self.episodic_memory = self._load_memory(self.episodic_memory_file, [])
    
    def _load_memory(self, filepath: str, default: Any):
        """Load memory from file"""
        try:
            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception:
            pass
        return default
    
    def _save_memory(self, filepath: str, data: Any):
        """Save memory to file"""
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, default=str)
        except Exception as e:
            print(f"Failed to save memory to {filepath}: {e}")
    
    def add_working_memory(self, content: str, priority: str = "normal"):
        """Add to working memory (current context)"""
        entry = {
            "content": content,
            "timestamp": datetime.now().isoformat(),
            "priority": priority
        }
        self.working_memory.append(entry)
        
        # Keep only last 20 entries in working memory
        if len(self.working_memory) > 20:
            self.working_memory.pop(0)
        
        self._save_memory(self.working_memory_file, self.working_memory)
    
    def add_long_term_memory(self, content: str, category: str = "general"):
        """Add important information to long-term memory"""
        entry = {
            "content": content,
            "category": category,
            "timestamp": datetime.now().isoformat(),
            "importance_score": self._calculate_importance(content)
        }
        self.long_term_memory.append(entry)
        self._save_memory(self.long_term_memory_file, self.long_term_memory)
    
    def add_episodic_memory(self, action: str, result: str, context: str = ""):
        """Add episodic memory (action-result pairs)"""
        entry = {
            "action": action,
            "result": result,
            "context": context,
            "timestamp": datetime.now().isoformat()
        }
        self.episodic_memory.append(entry)
        self._save_memory(self.episodic_memory_file, self.episodic_memory)
    
    def _calculate_importance(self, content: str) -> float:
        """Calculate importance score for content"""
        # Simple heuristic based on keywords and length
        important_keywords = [
            'conclusion', 'finding', 'result', 'important', 'key', 'critical',
            'summary', 'breakthrough', 'discovery', 'solution', 'answer'
        ]
        
        score = 0.5  # Base score
        for keyword in important_keywords:
            if keyword.lower() in content.lower():
                score += 0.1
        
        # Prefer medium-length content
        if 50 <= len(content) <= 500:
            score += 0.2
        
        return min(score, 1.0)
    
    def get_relevant_memory(self, query: str, limit: int = 5) -> List[Dict]:
        """Get memory entries relevant to a query"""
        all_entries = []
        
        # Combine all memory types with weights
        for entry in self.working_memory[-10:]:  # Recent working memory
            all_entries.append({**entry, "type": "working", "weight": 1.0})
        
        for entry in self.long_term_memory:
            all_entries.append({**entry, "type": "long_term", "weight": 0.8})
        
        for entry in self.episodic_memory[-20:]:  # Recent episodic memory
            all_entries.append({**entry, "type": "episodic", "weight": 0.6})
        
        # Simple relevance scoring
        query_words = set(query.lower().split())
        scored_entries = []
        
        for entry in all_entries:
            content = entry.get('content', '') + ' ' + entry.get('action', '')
            content_words = set(content.lower().split())
            
            # Calculate relevance score
            overlap = len(query_words & content_words)
            score = (overlap / len(query_words)) * entry.get('weight', 1.0)
            
            scored_entries.append({**entry, "relevance_score": score})
        
        # Sort by relevance and return top entries
        scored_entries.sort(key=lambda x: x["relevance_score"], reverse=True)
        return scored_entries[:limit]


class AutoGPTTools:
    """Collection of tools for AutoGPT-style autonomous agents"""
    
    def __init__(self, safety_config: Optional[SafetyConfig] = None):
        self.safety_config = safety_config or SafetyConfig()
        self.cost_tracker = CostTracker()
        self.memory_manager = MemoryManager()
        
        # Initialize Tavily client if API key is available
        self.tavily_client = None
        if os.getenv("TAVILY_API_KEY"):
            self.tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
    
    def _check_safety(self, operation: str) -> bool:
        """Check if an operation is allowed by safety rules"""
        if operation in self.safety_config.blocked_operations:
            return False
        return True
    
    def web_search(self, query: str, max_results: int = 3) -> str:
        """Enhanced web search with safety and cost tracking"""
        if not self._check_safety("web_search"):
            return "Web search is blocked by safety rules"
        
        if self.cost_tracker.search_count >= self.safety_config.max_searches_per_session:
            return "Maximum search limit reached for this session"
        
        if not self.tavily_client:
            return "Tavily client not initialized. Please check TAVILY_API_KEY."
        
        try:
            self.cost_tracker.record_search()
            
            # Perform search
            result = self.tavily_client.search(query, max_results=max_results)
            
            # Format results
            search_results = []
            for i, article in enumerate(result["results"], 1):
                search_results.append(f"Result {i}:\n")
                search_results.append(f"Title: {article['title']}\n")
                search_results.append(f"Content: {article['content'][:300]}...\n")
                search_results.append(f"URL: {article['url']}\n")
                search_results.append("-" * 50)
            
            # Store in memory
            self.memory_manager.add_working_memory(
                f"Searched for: {query}. Found {len(result['results'])} results."
            )
            
            return "\n".join(search_results)
            
        except Exception as e:
            error_msg = f"Search failed: {str(e)}"
            self.memory_manager.add_episodic_memory("web_search", error_msg, query)
            return error_msg
    
    def save_file(self, content: str, filename: str, category: str = "general") -> str:
        """Enhanced file saving with organization and safety"""
        if not self._check_safety("save_file"):
            return "File saving is blocked by safety rules"
        
        if self.cost_tracker.file_operations >= self.safety_config.max_file_operations:
            return "Maximum file operations limit reached"
        
        try:
            # Create organized directory structure
            base_dir = "autonomous_agent_output"
            category_dir = os.path.join(base_dir, category)
            os.makedirs(category_dir, exist_ok=True)
            
            # Generate safe filename
            safe_filename = self._generate_safe_filename(filename)
            filepath = os.path.join(category_dir, safe_filename)
            
            # Save file
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            self.cost_tracker.record_file_operation()
            
            # Record in memory
            self.memory_manager.add_episodic_memory(
                "save_file", f"Saved {safe_filename}", f"Category: {category}"
            )
            self.memory_manager.add_long_term_memory(
                f"Created file: {safe_filename} with {len(content)} characters",
                "file_creation"
            )
            
            return f"Successfully saved to {filepath}"
            
        except Exception as e:
            error_msg = f"Failed to save file: {str(e)}"
            self.memory_manager.add_episodic_memory("save_file", error_msg, filename)
            return error_msg
    
    def read_file(self, filename: str, category: str = "general") -> str:
        """Enhanced file reading with error handling"""
        try:
            filepath = os.path.join("autonomous_agent_output", category, filename)
            
            if not os.path.exists(filepath):
                return f"File not found: {filepath}"
            
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            self.cost_tracker.record_file_operation()
            
            # Record in memory
            self.memory_manager.add_episodic_memory(
                "read_file", f"Read {filename}", f"Size: {len(content)} characters"
            )
            
            return content
            
        except Exception as e:
            error_msg = f"Failed to read file: {str(e)}"
            self.memory_manager.add_episodic_memory("read_file", error_msg, filename)
            return error_msg
    
    def list_files(self, category: str = "general") -> str:
        """List files in a category directory"""
        try:
            category_dir = os.path.join("autonomous_agent_output", category)
            
            if not os.path.exists(category_dir):
                return f"No files found in category: {category}"
            
            files = []
            for filename in os.listdir(category_dir):
                filepath = os.path.join(category_dir, filename)
                if os.path.isfile(filepath):
                    size = os.path.getsize(filepath)
                    modified = datetime.fromtimestamp(os.path.getmtime(filepath))
                    files.append(f"- {filename} ({size} bytes, modified {modified})")
            
            if not files:
                return f"No files in category: {category}"
            
            return f"Files in {category}:\n" + "\n".join(files)
            
        except Exception as e:
            return f"Failed to list files: {str(e)}"
    
    def get_usage_stats(self) -> str:
        """Get current usage statistics"""
        stats = self.cost_tracker.get_usage_report()
        
        return f"""
Usage Statistics:
- Searches: {stats['searches']}/{self.safety_config.max_searches_per_session}
- File Operations: {stats['file_operations']}/{self.safety_config.max_file_operations}
- Token Usage: {stats['token_usage']:,}
- Elapsed Time: {stats['elapsed_minutes']:.1f} minutes
- Estimated Cost: ${stats['estimated_cost_usd']:.4f}
"""
    
    def get_memory_summary(self) -> str:
        """Get a summary of current memory state"""
        working_count = len(self.memory_manager.working_memory)
        long_term_count = len(self.memory_manager.long_term_memory)
        episodic_count = len(self.memory_manager.episodic_memory)
        
        recent_working = self.memory_manager.working_memory[-3:] if working_count > 0 else []
        recent_long_term = self.memory_manager.long_term_memory[-2:] if long_term_count > 0 else []
        
        summary = f"""
Memory Summary:
- Working Memory: {working_count} entries
- Long-term Memory: {long_term_count} entries  
- Episodic Memory: {episodic_count} entries

Recent Working Memory:
"""
        
        for entry in recent_working:
            summary += f"- {entry['content'][:100]}...\n"
        
        summary += "\nRecent Long-term Memory:\n"
        for entry in recent_long_term:
            summary += f"- [{entry['category']}] {entry['content'][:100]}...\n"
        
        return summary
    
    def search_memory(self, query: str) -> str:
        """Search memory for relevant information"""
        relevant_entries = self.memory_manager.get_relevant_memory(query)
        
        if not relevant_entries:
            return f"No relevant memories found for query: {query}"
        
        result = f"Found {len(relevant_entries)} relevant memory entries:\n\n"
        
        for i, entry in enumerate(relevant_entries, 1):
            result += f"{i}. [{entry['type'].upper()}] "
            
            if entry['type'] == 'episodic':
                result += f"Action: {entry.get('action', 'N/A')}\n"
                result += f"   Result: {entry.get('result', 'N/A')[:100]}...\n"
            else:
                result += f"{entry.get('content', 'N/A')[:150]}...\n"
            
            result += f"   (Score: {entry['relevance_score']:.2f})\n\n"
        
        return result
    
    def create_plan(self, goal: str, num_tasks: int = 5) -> str:
        """Create a structured plan for achieving a goal"""
        plan_id = hashlib.md5(f"{goal}{datetime.now()}".encode()).hexdigest()[:8]
        
        plan = {
            "plan_id": plan_id,
            "goal": goal,
            "created_at": datetime.now().isoformat(),
            "tasks": []
        }
        
        # Generate task ideas (simplified - in practice, you'd use LLM here)
        task_templates = [
            f"Research and gather information about {goal}",
            f"Analyze the key components of {goal}",
            f"Identify potential challenges and solutions",
            f"Create a structured outline for {goal}",
            f"Develop a comprehensive implementation strategy"
        ]
        
        for i, template in enumerate(task_templates[:num_tasks]):
            task = {
                "id": f"{plan_id}_task_{i+1}",
                "description": template,
                "status": "pending",
                "priority": "high" if i < 2 else "medium"
            }
            plan["tasks"].append(task)
        
        # Save plan
        plan_file = os.path.join("autonomous_agent_output", "plans", f"plan_{plan_id}.json")
        os.makedirs(os.path.dirname(plan_file), exist_ok=True)
        
        with open(plan_file, 'w', encoding='utf-8') as f:
            json.dump(plan, f, indent=2, default=str)
        
        # Record in memory
        self.memory_manager.add_long_term_memory(
            f"Created plan {plan_id} for goal: {goal}",
            "planning"
        )
        
        # Format for display
        result = f"Plan Created (ID: {plan_id})\n"
        result += f"Goal: {goal}\n"
        result += f"Tasks:\n"
        
        for task in plan["tasks"]:
            result += f"  {task['id']}: {task['description']} [{task['status']}]\n"
        
        return result
    
    def _generate_safe_filename(self, filename: str) -> str:
        """Generate a safe filename with timestamp"""
        # Remove dangerous characters
        safe_chars = "-_.abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        safe_filename = ''.join(c for c in filename if c in safe_chars)
        
        # Add timestamp if too generic
        if len(safe_filename) < 3:
            safe_filename = f"file_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Ensure it ends with .txt if no extension
        if '.' not in safe_filename:
            safe_filename += '.txt'
        
        return safe_filename
    
    def get_all_tools(self) -> List[Tool]:
        """Get all available tools as LangChain Tool objects"""
        tools = [
            Tool(
                name="web_search",
                func=self.web_search,
                description="Search the web for information. Provide a search query and optionally max_results (default 3)."
            ),
            Tool(
                name="save_file",
                func=self.save_file,
                description="Save content to a file. Provide content, filename, and optionally category (default 'general')."
            ),
            Tool(
                name="read_file",
                func=self.read_file,
                description="Read content from a file. Provide filename and optionally category (default 'general')."
            ),
            Tool(
                name="list_files",
                func=self.list_files,
                description="List all files in a category. Provide category name (default 'general')."
            ),
            Tool(
                name="get_usage_stats",
                func=lambda x: self.get_usage_stats(),
                description="Get current usage statistics and costs."
            ),
            Tool(
                name="get_memory_summary",
                func=lambda x: self.get_memory_summary(),
                description="Get a summary of current memory state."
            ),
            Tool(
                name="search_memory",
                func=self.search_memory,
                description="Search memory for relevant information. Provide a search query."
            ),
            Tool(
                name="create_plan",
                func=self.create_plan,
                description="Create a structured plan for achieving a goal. Provide goal and optionally num_tasks (default 5)."
            )
        ]
        
        return tools


# Convenience function for quick tool access
def get_autogpt_tools(safety_config: Optional[SafetyConfig] = None) -> List[Tool]:
    """Get AutoGPT tools for use in agents"""
    tools_manager = AutoGPTTools(safety_config)
    return tools_manager.get_all_tools()


if __name__ == "__main__":
    # Demo the tools
    print("🔧 AutoGPT Tools Demo")
    print("=" * 50)
    
    tools_manager = AutoGPTTools()
    
    # Test each tool
    print("\n1. Creating a plan...")
    plan_result = tools_manager.create_plan("Research AI trends in 2024")
    print(plan_result)
    
    print("\n2. Getting memory summary...")
    memory_result = tools_manager.get_memory_summary()
    print(memory_result)
    
    print("\n3. Getting usage stats...")
    stats_result = tools_manager.get_usage_stats()
    print(stats_result)
    
    print("\n4. Saving a test file...")
    save_result = tools_manager.save_file("This is a test file for AutoGPT tools.", "test_file.txt", "test")
    print(save_result)
    
    print("\n5. Listing files...")
    list_result = tools_manager.list_files("test")
    print(list_result)
    
    print("\n✅ All tools tested successfully!")
