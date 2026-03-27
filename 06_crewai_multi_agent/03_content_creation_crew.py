#!/usr/bin/env python3
"""
03_content_creation_crew.py - 4-Agent Content Creation Pipeline

This script demonstrates a complete content creation pipeline with four agents
working together to produce high-quality content. The workflow includes planning,
research, writing, and quality review stages.

Learning Objectives:
- Understand complex multi-agent workflows
- Learn quality assurance with reviewer agents
- See hierarchical task dependencies
- Observe complete content production pipeline

Prerequisites:
- Complete 02_research_crew.py
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
from utils.crew_tools import get_research_tools, get_writing_tools

# Load environment variables
load_dotenv()

def create_llm():
    """Create and return the LLM instance"""
    return ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0.7,  # Balanced temperature for creative but structured content
        api_key=os.getenv("OPENAI_API_KEY")
    )

def create_content_agents(llm):
    """Create the four content creation agents"""
    
    # Content Planner - Outlines content structure
    content_planner = Agent(
        role='Content Strategist',
        goal='Create comprehensive content plans and outlines for high-quality articles',
        backstory="""You are an experienced content strategist with expertise in 
        creating engaging, well-structured content plans. You understand audience 
        needs, SEO best practices, and how to structure content for maximum impact. 
        You excel at breaking down complex topics into logical, digestible sections.""",
        tools=[],  # Planner works with topic requirements
        verbose=True,
        allow_delegation=False,
        llm=llm
    )
    
    # Content Researcher - Gathers supporting information
    content_researcher = Agent(
        role='Content Researcher',
        goal='Find accurate, up-to-date information and data to support content creation',
        backstory="""You are a skilled content researcher with expertise in finding 
        credible sources, statistics, and examples that enhance content quality. 
        You have a talent for identifying the most relevant and interesting information 
        that makes content more valuable and engaging for readers.""",
        tools=get_research_tools(),
        verbose=True,
        allow_delegation=False,
        llm=llm
    )
    
    # Content Writer - Creates the actual content
    content_writer = Agent(
        role='Content Writer',
        goal='Transform plans and research into engaging, well-written articles',
        backstory="""You are a talented content writer with expertise in creating 
        compelling, informative articles that engage and educate readers. You have 
        a knack for making complex topics accessible while maintaining depth and 
        accuracy. Your writing is clear, engaging, and well-structured.""",
        tools=get_writing_tools(),
        verbose=True,
        allow_delegation=False,
        llm=llm
    )
    
    # Content Reviewer - Quality control and improvements
    content_reviewer = Agent(
        role='Content Editor',
        goal='Review and improve content for quality, accuracy, and engagement',
        backstory="""You are an experienced content editor with a keen eye for 
        detail and quality. You excel at identifying areas for improvement, ensuring 
        factual accuracy, maintaining consistent tone, and enhancing overall content 
        quality. You provide constructive feedback and specific improvement suggestions.""",
        tools=get_writing_tools(),
        verbose=True,
        allow_delegation=False,
        llm=llm
    )
    
    return content_planner, content_researcher, content_writer, content_reviewer

def create_content_tasks(planner, researcher, writer, reviewer):
    """Create sequential content creation tasks"""
    
    # Task 1: Content Planning
    planning_task = Task(
        description="""Create a comprehensive content plan for an article titled 
        'The Future of Sustainable Technology: Innovations Shaping Our World'.
        
        The content plan should include:
        1. Target audience analysis
        2. Key learning objectives
        3. Detailed outline with section headings
        4. Key points to cover in each section
        5. Call-to-action recommendations
        6. SEO considerations and target keywords
        
        Focus on creating a structure that flows logically and covers the topic 
        comprehensively while keeping readers engaged. The article should be 
        informative but accessible to general audiences interested in technology 
        and sustainability.""",
        expected_output="""A detailed content plan document with audience analysis, 
        learning objectives, comprehensive outline, key points for each section, 
        call-to-action recommendations, and SEO considerations. The plan should 
        provide clear guidance for research and writing phases.""",
        agent=planner
    )
    
    # Task 2: Content Research
    research_task = Task(
        description="""Based on the content plan, conduct thorough research on 
        sustainable technology innovations. Focus on finding:
        
        1. Recent breakthrough technologies and innovations
        2. Real-world applications and case studies
        3. Statistics and data on sustainability impact
        4. Expert opinions and predictions
        5. Challenges and limitations
        6. Future trends and developments
        
        Use web search to find current, credible sources. Prioritize information 
        from the last 2 years and include specific examples and data points that 
        will make the article more compelling and informative.""",
        expected_output="""A comprehensive research document with current information 
        on sustainable technology innovations, including specific examples, statistics, 
        expert opinions, challenges, and future trends. All information should be 
        well-sourced and relevant to the content plan.""",
        agent=researcher
    )
    
    # Task 3: Content Writing
    writing_task = Task(
        description="""Using the content plan and research findings, write a 
        comprehensive article on 'The Future of Sustainable Technology: 
        Innovations Shaping Our World'.
        
        The article should:
        1. Follow the structure outlined in the content plan
        2. Incorporate research findings naturally
        3. Be engaging and informative
        4. Target approximately 1200-1500 words
        5. Include a compelling introduction and conclusion
        6. Use clear headings and subheadings
        7. Maintain a professional yet accessible tone
        
        Focus on creating content that educates and inspires readers while 
        maintaining factual accuracy and depth. Make complex concepts understandable 
        without oversimplifying them.""",
        expected_output="""A well-written article of 1200-1500 words that follows 
        the content plan structure, incorporates research findings effectively, 
        and engages readers with clear, informative content. The article should 
        have proper structure, tone, and depth suitable for the target audience.""",
        agent=writer
    )
    
    # Task 4: Content Review
    review_task = Task(
        description="""Review the written article for quality and provide 
        improvement suggestions. Focus on:
        
        1. Content accuracy and factual correctness
        2. Structure and flow
        3. Clarity and readability
        4. Engagement and interest level
        5. Tone consistency
        6. Grammar and style
        7. SEO optimization
        8. Overall impact on target audience
        
        Provide specific, actionable feedback for improvements. If the content 
        meets quality standards, approve it with minor suggestions. If significant 
        improvements are needed, provide detailed guidance for revision.""",
        expected_output="""A comprehensive review with specific feedback on content 
        accuracy, structure, clarity, engagement, tone, grammar, SEO, and overall 
        quality. Include actionable improvement suggestions and a final recommendation 
        (approved, needs minor revisions, or needs major revisions).""",
        agent=reviewer
    )
    
    return planning_task, research_task, writing_task, review_task

def main():
    """Main function to run the content creation crew demo"""
    print("📝 Starting CrewAI Content Creation Demo - 4 Agent Pipeline")
    print("=" * 70)
    
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
        print("👥 Creating content creation agents...")
        planner, researcher, writer, reviewer = create_content_agents(llm)
        
        # Create tasks
        print("📋 Defining content creation tasks...")
        planning_task, research_task, writing_task, review_task = create_content_tasks(
            planner, researcher, writer, reviewer
        )
        
        # Create crew
        print("🔗 Forming content creation crew...")
        crew = Crew(
            agents=[planner, researcher, writer, reviewer],
            tasks=[planning_task, research_task, writing_task, review_task],
            process=Process.sequential,
            verbose=True,
            memory=True
        )
        
        # Execute crew
        print("⚡ Executing content creation pipeline...")
        print("-" * 70)
        
        result = crew.kickoff()
        
        print("-" * 70)
        print("✅ Content creation crew execution completed!")
        
        # Display result with markdown formatting
        display_markdown_options(
            content=str(result),
            filename="content_creation_output.md",
            title="CrewAI Content Creation Crew - Final Result",
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
