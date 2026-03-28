#!/usr/bin/env python3
"""
02_research_crew.py - 3-Agent Research Workflow

This script demonstrates a more complex CrewAI setup with three agents working
together in a sequential research workflow. The agents collaborate to gather,
analyze, and summarize information on complex topics.

Learning Objectives:
- Understand sequential task delegation
- Learn tool integration with web search
- See how agents build upon each other's work
- Observe more complex crew orchestration

Prerequisites:
- Complete 01_basic_crew.py
- Have OPENAI_API_KEY and TAVILY_API_KEY in .env file
"""

import os
import sys
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI

# Add utils directory to path for importing display utilities
sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))
from utils.markdown_display import display_markdown_options
from utils.crew_tools import get_research_tools

# Load environment variables
load_dotenv()

def create_llm():
    """Create and return the LLM instance"""
    return ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0.3,  # Lower temperature for more factual research
        api_key=os.getenv("OPENAI_API_KEY")
    )

def create_research_agents(llm):
    """Create the three research agents"""
    
    # Lead Researcher - Gathers initial information
    lead_researcher = Agent(
        role='Lead Researcher',
        goal='Conduct comprehensive web research and gather accurate, up-to-date information',
        backstory="""You are an experienced lead researcher with expertise in information 
        gathering and source evaluation. You have a keen eye for credible sources and can 
        quickly identify the most relevant information on any topic. You always prioritize 
        accuracy and provide multiple sources when possible.""",
        tools=get_research_tools(),
        verbose=True,
        allow_delegation=False,
        llm=llm
    )
    
    # Research Analyst - Analyzes and organizes findings
    research_analyst = Agent(
        role='Research Analyst',
        goal='Analyze research findings and organize them into structured, actionable insights',
        backstory="""You are a skilled research analyst with expertise in data analysis 
        and information synthesis. You excel at identifying patterns, connections, and 
        key insights from complex information. You have a talent for organizing disparate 
        information into coherent structures that highlight the most important points.""",
        tools=[],  # Analyst works with provided research data
        verbose=True,
        allow_delegation=False,
        llm=llm
    )
    
    # Report Summarizer - Creates final summary
    report_summarizer = Agent(
        role='Report Summarizer',
        goal='Create comprehensive, well-structured summaries that are clear and informative',
        backstory="""You are an expert technical writer and summarizer with extensive 
        experience in creating clear, concise reports. You have a special talent for 
        distilling complex information into accessible formats while maintaining accuracy 
        and depth. Your summaries are always well-organized and easy to understand.""",
        tools=[],  # Summarizer works with analyzed data
        verbose=True,
        allow_delegation=False,
        llm=llm
    )
    
    return lead_researcher, research_analyst, report_summarizer

def create_research_tasks(lead_researcher, research_analyst, report_summarizer):
    """Create sequential research tasks"""
    
    # Task 1: Initial Research
    research_task = Task(
        description="""Conduct comprehensive research on 'The Impact of Remote Work on 
        Urban Development and Real Estate Markets'. Focus on:
        
        1. Current trends in remote work adoption
        2. Effects on major cities and urban centers
        3. Real estate market changes (commercial and residential)
        4. Economic implications for urban economies
        5. Future predictions and expert opinions
        
        Use web search to find recent articles, studies, and reports from credible 
        sources. Prioritize information from the last 2-3 years and include specific 
        data points and statistics where available.""",
        expected_output="""A comprehensive research document with clear sections covering 
        remote work trends, urban impacts, real estate changes, economic implications, 
        and future predictions. Include specific data, statistics, and source references.""",
        agent=lead_researcher
    )
    
    # Task 2: Analysis
    analysis_task = Task(
        description="""Analyze the research findings and create a structured analysis 
        that identifies:
        
        1. Key trends and patterns in the data
        2. Causal relationships between remote work and urban changes
        3. Regional variations and differences
        4. Short-term vs long-term impacts
        5. Opportunities and challenges for different stakeholders
        
        Organize the analysis with clear headings and subheadings. Use bullet points 
        for key findings and include a summary table if appropriate. Focus on providing 
        actionable insights rather than just restating facts.""",
        expected_output="""A detailed analysis document with structured sections covering 
        key trends, causal relationships, regional variations, time-based impacts, and 
        stakeholder implications. Include clear organization and actionable insights.""",
        agent=research_analyst
    )
    
    # Task 3: Final Summary
    summary_task = Task(
        description="""Create a comprehensive executive summary based on the research 
        and analysis. The summary should:
        
        1. Start with a clear overview of the main findings
        2. Highlight the most significant impacts of remote work on urban development
        3. Present key statistics and data points
        4. Discuss implications for different stakeholders (city planners, real estate 
           developers, businesses, residents)
        5. Provide forward-looking insights and recommendations
        
        The summary should be approximately 800-1000 words, well-structured, and 
        suitable for presentation to business leaders and urban planners. Use clear 
        headings and maintain a professional, informative tone.""",
        expected_output="""A professional executive summary of 800-1000 words with 
        clear structure covering main findings, significant impacts, key statistics, 
        stakeholder implications, and future recommendations. Suitable for business 
        and policy audiences.""",
        agent=report_summarizer
    )
    
    return research_task, analysis_task, summary_task

def main():
    """Main function to run the research crew demo"""
    print("🔬 Starting CrewAI Research Demo - 3 Agent Workflow")
    print("=" * 60)
    
    # Verify API keys
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Error: OPENAI_API_KEY not found in .env file")
        return
    
    if not os.getenv("TAVILY_API_KEY"):
        print("⚠️ Warning: TAVILY_API_KEY not found. Web search may not work properly.")
    
    try:
        # Create LLM
        print("🤖 Initializing LLM...")
        llm = create_llm()
        
        # Create agents
        print("👥 Creating research agents...")
        lead_researcher, research_analyst, report_summarizer = create_research_agents(llm)
        
        # Create tasks
        print("📋 Defining research tasks...")
        research_task, analysis_task, summary_task = create_research_tasks(
            lead_researcher, research_analyst, report_summarizer
        )
        
        # Create crew
        print("🔗 Forming research crew...")
        crew = Crew(
            agents=[lead_researcher, research_analyst, report_summarizer],
            tasks=[research_task, analysis_task, summary_task],
            process=Process.sequential,  # Tasks execute in sequence
            verbose=True,
            memory=True  # Enable memory for better context retention
        )
        
        # Execute crew
        print("⚡ Executing research workflow...")
        print("-" * 60)
        
        result = crew.kickoff()
        
        print("-" * 60)
        print("✅ Research crew execution completed!")
        
        # Display result with markdown formatting
        display_markdown_options(
            content=str(result),
            filename="research_crew_output.md",
            title="CrewAI Research Crew - Final Summary",
            show_console=True
        )
        
    except Exception as e:
        print(f"❌ Error during execution: {str(e)}")
        print("\n🔧 Troubleshooting Tips:")
        print("1. Check your internet connection")
        print("2. Verify your API keys are valid")
        print("3. Ensure you have sufficient API credits")
        print("4. Try running with verbose=True for more details")
        print("5. Check if Tavily API key is properly set for web search")

if __name__ == "__main__":
    main()
