#!/usr/bin/env python3
"""
Script to demonstrate how to simulate a critical review node
that suggests improvements in the content creator agent.
"""

from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage

# Load environment variables
from pathlib import Path
from dotenv import load_dotenv
import os

# Try multiple possible locations for .env file
possible_paths = [
    Path.cwd().parent / '.env',  # Parent directory
    Path.cwd() / '.env',         # Current directory
    Path('.env')                 # Relative path
]

for path in possible_paths:
    if path.exists():
        load_dotenv(dotenv_path=path)
        print(f"Loaded .env from: {path}")
        break
else:
    print("No .env file found in expected locations")

print("Environment variables loaded:")
print("OPENAI_API_KEY:", "[LOADED]" if os.getenv("OPENAI_API_KEY") else "Not found")
print("TAVILY_API_KEY:", "[LOADED]" if os.getenv("TAVILY_API_KEY") else "Not found")

# Initialize LLM
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

@tool
def critical_review_content(draft: str) -> str:
    """Critical review function that's more likely to suggest revisions."""
    review_prompt = f"""
    You are a CRITICAL content reviewer. Be thorough and demanding in your evaluation.
    
    Review the following article draft:
    
    {draft}
    
    CRITICAL EVALUATION CRITERIA:
    1. Content Depth: Is it superficial or does it provide real insights?
    2. Structure Quality: Are transitions smooth? Is the flow logical?
    3. Engagement: Is it boring or compelling to read?
    4. Completeness: Are there gaps in information or reasoning?
    5. Originality: Is it generic or does it offer unique perspectives?
    6. Technical Quality: Grammar, spelling, and formatting issues
    7. Word Count: Should be 800-1200 words for proper depth
    
    BE CRITICAL: Find at least 3-5 specific issues that need improvement.
    Only say "READY_TO_PUBLISH" if the draft is truly exceptional.
    
    If you find ANY significant issues, say "NEEDS_REVISION" and provide detailed feedback.
    
    Example issues to look for:
    - Introduction doesn't grab attention
    - Missing statistics or evidence
    - Sections are too brief or undeveloped
    - Conclusion is weak or missing call-to-action
    - Generic statements without specific examples
    - Poor paragraph structure
    """
    
    response = llm.invoke([HumanMessage(content=review_prompt)])
    return response.content

# Test with a sample draft
sample_draft = """
AI in Healthcare

Artificial intelligence is changing healthcare. Doctors use AI to help patients. 
It makes things better. AI can look at medical images and find problems. 
This helps doctors make better decisions.

AI also helps with drug discovery. It can analyze lots of data quickly. 
This saves time and money. Many hospitals are using AI now.

In conclusion, AI is good for healthcare.
"""

print("🔍 Testing Critical Review Function")
print("=" * 50)
print("Sample Draft:")
print(sample_draft)
print("=" * 50)

# Run critical review
review_result = critical_review_content.invoke({"draft": sample_draft})

print("📝 Critical Review Result:")
print(review_result)
print("=" * 50)

# Test with a better draft
better_draft = """
The Revolutionary Impact of Artificial Intelligence on Modern Healthcare

Introduction
Artificial Intelligence (AI) is fundamentally transforming healthcare delivery, diagnosis, and treatment methodologies across the globe. According to a 2023 McKinsey report, AI applications in healthcare could potentially create $150 billion in annual value for the U.S. healthcare system by 2026. This technological revolution is not merely theoretical—it's actively reshaping how medical professionals diagnose diseases, develop treatments, and deliver patient care.

Enhanced Diagnostic Capabilities
AI-powered diagnostic tools are demonstrating remarkable accuracy in medical imaging analysis. For instance, Google's DeepMind algorithm can detect over 50 eye diseases with 94% accuracy, matching or exceeding human expert performance. Similarly, Stanford's AI system for skin cancer detection achieves 91% accuracy, significantly reducing false positives compared to traditional methods. These systems analyze thousands of medical images in seconds, enabling early detection that was previously impossible.

Accelerated Drug Discovery and Development
The pharmaceutical industry is leveraging AI to dramatically reduce drug development timelines, which traditionally span 10-15 years and cost billions of dollars. Insilico Medicine's AI platform can identify potential drug candidates in just 46 days, a process that previously took years. This acceleration not only reduces costs but also brings life-saving treatments to market faster, potentially saving millions of lives annually.

Personalized Treatment Protocols
AI enables unprecedented personalization in medical treatment. IBM's Watson for Oncology analyzes patient data, medical literature, and clinical trial results to recommend personalized cancer treatment plans. Studies show that AI-assisted treatment planning improves patient outcomes by 30% compared to traditional methods. This level of personalization was impossible before AI's analytical capabilities.

Challenges and Ethical Considerations
Despite these advances, AI implementation in healthcare faces significant challenges. Data privacy concerns, algorithmic bias, and the need for regulatory frameworks must be addressed. A 2023 study found that 23% of AI diagnostic tools showed bias against minority populations, highlighting the critical need for diverse training data and ethical oversight.

Future Outlook
The integration of AI in healthcare is accelerating, with projected market growth from $11 billion in 2023 to $187 billion by 2030. However, success will require collaboration between technologists, medical professionals, and policymakers to ensure AI benefits all patient populations equitably.

Conclusion
AI is not replacing healthcare professionals but augmenting their capabilities, enabling more accurate diagnoses, faster drug development, and personalized treatments. As we move forward, the focus must remain on ethical implementation and equitable access to ensure AI's benefits transform healthcare for everyone, everywhere.
"""

print("\n🎯 Testing with Better Draft:")
print("=" * 50)
print("Better Draft:")
print(better_draft[:500] + "...")
print("=" * 50)

# Run critical review on better draft
better_review_result = critical_review_content.invoke({"draft": better_draft})

print("📝 Review of Better Draft:")
print(better_review_result)
print("=" * 50)

print("💡 Key Takeaways:")
print("1. The critical review function is more likely to find issues")
print("2. It provides specific, actionable feedback")
print("3. It has higher standards for 'READY_TO_PUBLISH'")
print("4. This creates more revision loops for quality improvement")
