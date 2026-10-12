"""
SESSION 1 - Task 2: Direct OpenAI API Call & Problem Analysis
Objective: Send a prompt to OpenAI GPT-3.5 directly, print the response, 
and analyze problems faced with direct API calls without a framework like LangChain.
"""

import os
from openai import OpenAI

def direct_openai_call(prompt: str) -> str:
    """
    Sends a direct request to OpenAI's API using the official SDK.
    Includes graceful handling for missing or unconfigured API keys.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key or api_key.strip() == "" or api_key == "your_openai_api_key_here":
        print("\n[!] NOTICE: OPENAI_API_KEY not detected or placeholder used.")
        print("[!] Running in Demonstration / Simulated Response Mode.\n")
        return (
            "[Simulated GPT-3.5 Response]\n"
            f"Query received: '{prompt}'\n"
            "Response: The Indian Premier League (IPL) is a premier men's T20 cricket "
            "league established in 2008 by the BCCI. It features ten franchise teams "
            "representing different Indian cities and is renowned for fast-paced, high-octane cricket."
        )
    
    try:
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful and knowledgeable AI assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=150
        )
        return response.choices[0].message.content.strip() 
    except Exception as e:
        return f"[API Error Encountered]: {str(e)}"

def print_problems_analysis():
    """
    Prints the two major challenges faced when using direct LLM API calls.
    """
    analysis = """
================================================================================
  TWO MAJOR PROBLEMS FACED WITH THE DIRECT LLM API APPROACH
================================================================================

1. LACK OF PROMPT MANAGEMENT & DYNAMIC REUSABILITY:
   - When calling the raw OpenAI API directly, developers must manually construct,
     interpolate, and sanitize prompt strings (e.g. using f-strings or manual concatenations).
   - There is no native version control, validation of required input variables, or
     support for few-shot examples and partial prompt templates.
   - As an application grows with multiple dynamic inputs, managing raw strings leads
     to fragile, duplicate, and hard-to-maintain code.

2. ABSENCE OF BUILT-IN ORCHESTRATION, MEMORY & TOOL EXTENSIBILITY:
   - Direct API calls are completely stateless; there is no built-in conversation history,
     window buffer, or token management across multiple turns.
   - Chaining multiple steps (e.g. fetching database records, doing calculations, and then
     generating a response) requires writing hundreds of lines of glue code manually.
   - Integrating external tools (calculators, web search, vector databases) requires
     custom parsing logic and manual state machines, which frameworks like LangChain solve
     out of the box with Chains, Runnables, and Agents.
================================================================================
"""
    print(analysis)

def main():
    print("=" * 60)
    print("   SESSION 1 - TASK 2: DIRECT OPENAI API INVOCATION")
    print("=" * 60)
    
    test_prompt = "Explain what IPL is in two concise sentences."
    print(f"Prompt Sent: \"{test_prompt}\"")
    print("-" * 60)
    
    response = direct_openai_call(test_prompt)
    print("Response Received:")
    print(response)
    print("-" * 60)
    
    # Print the analysis of problems
    print_problems_analysis()

if __name__ == "__main__":
    main()
