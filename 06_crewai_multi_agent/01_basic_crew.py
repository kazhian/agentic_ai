#!/usr/bin/env python3
"""
01_basic_crew.py - Simple 2-Agent CrewAI Demo

This script demonstrates the fundamental concepts of CrewAI by creating
a simple 2-agent system where a Researcher gathers information and a 
Writer creates content based on that research.

Learning Objectives:
- Understand basic CrewAI setup
- Learn how to define agents with roles and goals
- See task delegation between agents
- Observe sequential task execution

Prerequisites:
- Complete modules 01-05
- Have OPENAI_API_KEY in .env file
"""

import os
import sys
from datetime import datetime
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI

# Add utils directory to path for importing display utilities
sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))
from utils.markdown_display import display_markdown_options

# Load environment variables
load_dotenv()

def create_llm():
    """Create and return the LLM instance"""
    return ChatOpenAI(
        model="gpt-3.5-turbo",  # Using cost-effective model for demo
        temperature=0.7,
        api_key=os.getenv("OPENAI_API_KEY")
    )

def create_agents(llm_for_agents):
    """Create the two agents for our basic crew"""
    
    # Researcher Agent
    researcher = Agent(
        role='Senior Research Analyst',
        goal='Find comprehensive and accurate information on given topics',
        backstory="""You are a senior research analyst with 10 years of experience 
        in academic and industry research. You have a talent for finding relevant 
        information quickly and organizing it in a clear, structured manner. 
        You always verify facts and provide multiple perspectives on complex topics.""",
        verbose=True,
        allow_delegation=False,
        llm=llm_for_agents
    )
    
    # Writer Agent
    writer = Agent(
        role='Content Writer',
        goal='Transform research findings into engaging, well-structured content',
        backstory="""You are a skilled content writer who specializes in making 
        complex topics accessible to general audiences. You have a knack for 
        creating compelling narratives while maintaining accuracy and clarity. 
        You always structure your content with clear headings, bullet points, 
        and logical flow.""",
        verbose=True,
        allow_delegation=False,
        llm=llm_for_agents
    )
    
    return researcher, writer

def create_tasks(researcher, writer):
    """Create tasks for the agents to complete"""
    
    # Research Task
    research_task = Task(
        description="""Research the topic of 'Artificial Intelligence in Education' 
        and provide a comprehensive overview including:
        1. Current applications of AI in educational settings
        2. Benefits and advantages for students and teachers
        3. Challenges and limitations
        4. Future trends and predictions
        
        Focus on providing factual, well-sourced information that would be useful 
        for someone writing an educational article on this topic.""",
        expected_output="""A detailed research report with clear sections covering 
        current applications, benefits, challenges, and future trends of AI in education. 
        Include specific examples and data points where possible.""",
        agent=researcher
    )
    
    # Writing Task
    writing_task = Task(
        description="""Based on the research provided, write an engaging article 
        titled 'How AI is Transforming Education: Opportunities and Challenges' 
        that is suitable for a general audience including educators, students, 
        and parents.
        
        The article should:
        1. Start with a compelling introduction
        2. Cover the key findings from the research
        3. Use clear, accessible language
        4. Include practical examples
        5. End with a thoughtful conclusion
        
        Aim for approximately 800-1000 words with proper structure and flow.""",
        expected_output="""A well-structured article of 800-1000 words with engaging 
        introduction, informative body sections covering key research findings, 
        practical examples, and a thoughtful conclusion. The writing should be clear 
        and accessible to general audiences.""",
        agent=writer
    )
    
    return research_task, writing_task

def main():
    """Main function to run the basic crew demo"""
    print("🚀 Starting CrewAI Basic Demo - 2 Agent System")
    print("=" * 50)
    
    # Verify API key
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Error: OPENAI_API_KEY not found in .env file")
        print("Please set up your API key in the .env file")
        return
    
    try:
        # Create LLM
        print("🤖 Initializing LLM...")
        llm = create_llm()
        
        # Create agents
        print("👥 Creating agents...")
        researcher, writer = create_agents(llm)
        
        # Create tasks
        print("📋 Defining tasks...")
        research_task, writing_task = create_tasks(researcher, writer)
        
        # Create crew
        print("🔗 Forming crew...")
        crew = Crew(
            agents=[researcher, writer],
            tasks=[research_task, writing_task],
            process=Process.sequential,  # Tasks execute one after another
            verbose=True  # Show detailed execution logs
        )
        
        # Execute crew
        print("⚡ Executing crew tasks...")
        print("-" * 50)
        
        result = crew.kickoff()
        
        print("-" * 50)
        print("✅ Crew execution completed!")
        
        # Display result with markdown formatting
        display_markdown_options(
            content=str(result),
            filename="basic_crew_output.md",
            title="CrewAI Basic Crew - Final Result",
            show_console=True
        )
        
    except Exception as e:
        print(f"❌ Error during execution: {str(e)}")
        print("\n🔧 Troubleshooting Tips:")
        print("1. Check your internet connection")
        print("2. Verify your OpenAI API key is valid")
        print("3. Ensure you have sufficient API credits")
        print("4. Try running with verbose=True for more details")

if __name__ == "__main__":
    main()
