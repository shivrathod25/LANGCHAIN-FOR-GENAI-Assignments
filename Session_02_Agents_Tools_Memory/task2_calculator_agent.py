"""
SESSION 2 - Task 2: Calculator Tool Integration in LangChain Agent
Objective: Integrate a Calculator tool into a LangChain Agent to solve math questions
like 'What is 12 times 8?' and return the accurate numerical answer.
"""

import os
import re
import math
from dotenv import load_dotenv

load_dotenv()

def safe_math_eval(expression_str: str) -> str:
    """
    Safely parses and evaluates mathematical expressions.
    Translates common English words (times, plus, divided by) into math symbols.
    """
    clean_expr = expression_str.lower().strip()
    # Word to operator replacements
    clean_expr = re.sub(r'\btimes\b|\bmultiplied by\b|\bx\b', '*', clean_expr)
    clean_expr = re.sub(r'\bdivided by\b|\bover\b', '/', clean_expr)
    clean_expr = re.sub(r'\bplus\b|\band\b', '+', clean_expr)
    clean_expr = re.sub(r'\bminus\b', '-', clean_expr)
    clean_expr = re.sub(r'\bto the power of\b|\bpower\b', '**', clean_expr)
    
    # Extract only valid mathematical characters: numbers, operators, parens, decimal points
    allowed_chars = re.sub(r'[^0-9+\-*/().^ ]', '', clean_expr)
    allowed_chars = allowed_chars.replace('^', '**').strip()
    
    if not allowed_chars:
        return "Error: Could not parse mathematical expression."
        
    try:
        # Safe eval with restricted builtins
        allowed_globals = {"__builtins__": None, "math": math}
        result = eval(allowed_chars, allowed_globals, {})
        return str(result)
    except Exception as e:
        return f"Calculation error: {e}"

def create_calculator_tool():
    """Creates the LangChain Calculator Tool."""
    from langchain_core.tools import Tool
    return Tool(
        name="Calculator",
        func=safe_math_eval,
        description="Useful for solving mathematical calculations. Input can be an expression or word problem like '12 times 8' or '150 * 4'."
    )

def run_agent_math(query: str):
    print(f"\nUser Query: \"{query}\"")
    calc_tool = create_calculator_tool()

    api_key = os.getenv("OPENAI_API_KEY")
    has_valid_key = bool(api_key and api_key != "your_openai_api_key_here")

    if has_valid_key:
        try:
            from langchain_openai import ChatOpenAI
            from langchain.agents import initialize_agent, AgentType
            llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
            agent = initialize_agent([calc_tool], llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)
            print("[*] Running Live LangChain Agent with Calculator...")
            response = agent.run(query)
            print(f"Agent Final Answer: {response}")
            return
        except Exception as e:
            print(f"[!] Falling back to local agent execution: {e}")

    # ReAct Simulation Framework
    print("-" * 50)
    print("Agent Reasoning Flow (ReAct Pattern):")
    print(f"Thought: The user has asked a mathematical question. I should use the Calculator tool.")
    print(f"Action: {calc_tool.name}")
    print(f"Action Input: '{query}'")
    result = calc_tool.run(query)
    print(f"Observation: {result}")
    print(f"Thought: I have calculated the result ({result}). I will formulate the response.")
    print(f"Final Answer: The answer to '{query}' is {result}.")
    print("-" * 50)

def main():
    print("=" * 60)
    print("   SESSION 2 - TASK 2: CALCULATOR TOOL AGENT")
    print("=" * 60)
    
    run_agent_math("What is 12 times 8?")
    run_agent_math("Calculate 250 plus 450 divided by 2")

if __name__ == "__main__":
    main()
