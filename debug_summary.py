"""
Debug script to test summary extraction
"""

from main_api import extract_summary_from_output, extract_alternative_summary

# Test sample output that might come from main.py
sample_output = """
🔍 Checking available LLM providers...
⚡ Trying Groq Llama...
✅ Using Groq Llama: groq/llama-3.3-70b-versatile

==================================================
FINAL RESULT:
==================================================

The ReWAAO pattern (Retrieval-Augmented Generation with Write-Ahead-and-Observe) is an advanced AI architecture pattern that combines retrieval-augmented generation with observational learning mechanisms. This pattern enhances traditional RAG systems by implementing a write-ahead logging mechanism that captures and observes the reasoning process.

Key Components:
1. Retrieval System: Fetches relevant information from knowledge bases
2. Write-Ahead Module: Logs reasoning steps before execution
3. Observation Component: Monitors and learns from the reasoning process
4. Generation Engine: Produces final outputs based on retrieved and observed data

Benefits:
- Improved reasoning transparency
- Better error detection and correction
- Enhanced learning from previous interactions
- More reliable and consistent outputs

The ReWAAO pattern is particularly useful in complex AI applications where transparency and reliability are crucial, such as medical diagnosis, legal analysis, and scientific research.

(crewai_mcp) C:\Users\PLNAYAK\Documents\crewai_mcp>
"""

def test_summary_extraction():
    print("Testing summary extraction...")
    print("="*50)
    
    summary = extract_summary_from_output(sample_output)
    print("Extracted Summary:")
    print("-" * 30)
    print(summary)
    print("-" * 30)
    print(f"Summary length: {len(summary)} characters")
    
    print("\nTesting alternative extraction...")
    alt_summary = extract_alternative_summary(sample_output)
    print("Alternative Summary:")
    print("-" * 30)
    print(alt_summary)
    print("-" * 30)
    print(f"Alternative summary length: {len(alt_summary)} characters")

if __name__ == "__main__":
    test_summary_extraction() 