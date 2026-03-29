#!/usr/bin/env python3
"""
utils/crew_tools.py - Shared Tools for CrewAI Agents

This module contains reusable tools that can be used by different agents
across various CrewAI crews. Tools extend agent capabilities by providing
access to external services, APIs, and specialized functions.

Available Tools:
- WebSearchTool: Search the web using Tavily
- CalculatorTool: Perform mathematical calculations
- DateTimeTool: Get current date and time information
- TextAnalysisTool: Basic text analysis functions
"""

import os
import re
from datetime import datetime
from typing import Dict, Any, List
from dotenv import load_dotenv
try:
    from langchain_tavily import TavilySearch as TavilySearchResults
except ImportError:
    from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field

# Load environment variables
load_dotenv()

class WebSearchTool(BaseTool):
    """Web search tool using Tavily API"""
    name: str = "web_search"
    description: str = "Search the web for current information on any topic"
    search_tool: Any = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not os.getenv("TAVILY_API_KEY"):
            print("⚠️ Warning: TAVILY_API_KEY not found. Web search may not work.")

        self.search_tool = TavilySearchResults(
            max_results=5,
            search_depth="basic",
            include_answer=True,
            include_raw_content=False
        )
    
    def _run(self, query: str) -> str:
        """Execute web search and return results"""
        try:
            results = self.search_tool.invoke(query)
            
            if not results:
                return "No results found for the query."
            
            formatted_results = []
            for i, result in enumerate(results, 1):
                title = result.get('title', 'No title')
                url = result.get('url', 'No URL')
                snippet = result.get('content', 'No content available')
                
                formatted_results.append(
                    f"{i}. {title}\n"
                    f"   URL: {url}\n"
                    f"   Content: {snippet[:200]}...\n"
                )
            
            return "\n".join(formatted_results)
            
        except Exception as e:
            return f"Error performing search: {str(e)}"
    
    async def _arun(self, query: str) -> str:
        """Async version of web search"""
        return self._run(query)

class CalculatorTool(BaseTool):
    """Simple calculator tool for basic mathematical operations"""
    name: str = "calculator"
    description: str = "Perform basic mathematical calculations"
    
    def _run(self, expression: str) -> str:
        """Evaluate mathematical expression safely"""
        try:
            # Remove any potentially harmful characters
            safe_expression = re.sub(r'[^0-9+\-*/().\s]', '', expression)
            
            if not safe_expression:
                return "Invalid expression"
            
            # Evaluate the expression
            result = eval(safe_expression)
            
            return f"Result: {result}"
            
        except Exception as e:
            return f"Calculation error: {str(e)}"
    
    async def _arun(self, expression: str) -> str:
        """Async version of calculator"""
        return self._run(expression)

class DateTimeTool(BaseTool):
    """Tool for date and time information"""
    name: str = "datetime"
    description: str = "Get current date, time, and perform date calculations"
    
    def _run(self, query: str) -> str:
        """Handle date/time queries"""
        try:
            query_lower = query.lower()
            
            if "current" in query_lower or "now" in query_lower:
                now = datetime.now()
                return f"Current date and time: {now.strftime('%Y-%m-%d %H:%M:%S')}"
            
            elif "date" in query_lower and "time" not in query_lower:
                today = datetime.now().date()
                return f"Today's date: {today.strftime('%Y-%m-%d')}"
            
            elif "time" in query_lower and "date" not in query_lower:
                now = datetime.now()
                return f"Current time: {now.strftime('%H:%M:%S')}"
            
            else:
                return "Available commands: 'current time', 'current date', 'current date and time'"
                
        except Exception as e:
            return f"Date/time error: {str(e)}"
    
    async def _arun(self, query: str) -> str:
        """Async version of datetime tool"""
        return self._run(query)

class TextAnalysisTool(BaseTool):
    """Basic text analysis tool"""
    name: str = "text_analysis"
    description: str = "Analyze text for word count, character count, and basic statistics"
    
    def _run(self, text: str) -> str:
        """Analyze text and return statistics"""
        try:
            if not text or not text.strip():
                return "No text provided for analysis"
            
            # Basic statistics
            char_count = len(text)
            char_count_no_spaces = len(text.replace(' ', ''))
            word_count = len(text.split())
            sentence_count = len(re.split(r'[.!?]+', text)) - 1
            paragraph_count = len([p for p in text.split('\n\n') if p.strip()])
            
            # Reading time estimation (average 200 words per minute)
            reading_time_minutes = max(1, round(word_count / 200))
            
            analysis = f"""
Text Analysis Results:
- Characters: {char_count}
- Characters (no spaces): {char_count_no_spaces}
- Words: {word_count}
- Sentences: {sentence_count}
- Paragraphs: {paragraph_count}
- Estimated reading time: {reading_time_minutes} minutes

Text Preview:
{text[:200]}{'...' if len(text) > 200 else ''}
"""
            return analysis.strip()
            
        except Exception as e:
            return f"Text analysis error: {str(e)}"
    
    async def _arun(self, text: str) -> str:
        """Async version of text analysis"""
        return self._run(text)

def get_default_tools() -> List[BaseTool]:
    """Return list of default tools for agents"""
    return [
        WebSearchTool(),
        CalculatorTool(),
        DateTimeTool(),
        TextAnalysisTool()
    ]

def get_research_tools() -> List[BaseTool]:
    """Return tools specifically useful for research agents"""
    return [
        WebSearchTool(),
        TextAnalysisTool(),
        DateTimeTool()
    ]

def get_writing_tools() -> List[BaseTool]:
    """Return tools specifically useful for writing agents"""
    return [
        TextAnalysisTool(),
        CalculatorTool(),
        DateTimeTool()
    ]

# Tool usage examples for documentation
if __name__ == "__main__":
    print("🛠️ Testing CrewAI Tools")
    print("=" * 40)
    
    # Test Web Search
    web_tool = WebSearchTool()
    print("\n🔍 Testing Web Search:")
    result = web_tool._run("artificial intelligence in education")
    print(result[:300] + "..." if len(result) > 300 else result)
    
    # Test Calculator
    calc_tool = CalculatorTool()
    print("\n🧮 Testing Calculator:")
    print(calc_tool._run("15 * 8 + 12"))
    
    # Test DateTime
    dt_tool = DateTimeTool()
    print("\n📅 Testing DateTime:")
    print(dt_tool._run("current date and time"))
    
    # Test Text Analysis
    text_tool = TextAnalysisTool()
    print("\n📊 Testing Text Analysis:")
    sample_text = "This is a sample text for testing the text analysis tool. It contains multiple sentences and should provide meaningful statistics."
    print(text_tool._run(sample_text))
