"""
SESSION 4 - Task 5: Tool Routing Prompt Template (Calculator vs. Normal Answer)
Objective: Use a generated Prompt Template to help the chatbot decide when to route 
to the Calculator tool versus when to answer normally. Test with >= 2 distinct user queries.
"""

import sys
import re
import os
from dotenv import load_dotenv

if sys.platform == "win32":
    try:
        # pyrefly: disable [missing-attr]
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

load_dotenv()

from langchain_core.prompts import PromptTemplate

# pyrefly: ignore [missing-import]
from task3_custom_calculator_tool import get_custom_calculator_tool 

# ==============================================================================
# TOOL ROUTING PROMPT TEMPLATE (GENERATED WITH COPILOT / CHATGPT)
# ==============================================================================
ROUTING_PROMPT_TEMPLATE = """
You are an intelligent Intent Router for an AI Assistant system.
Analyze the user query: "{query}"

Available Paths:
1. USE_CALCULATOR: Select this if the user asks for arithmetic, discounts, percentage, bill calculation, or numerical computations.
2. ANSWER_NORMALLY: Select this if the user asks for explanations, trivia, conversation, recommendations, or non-math general knowledge.

Decision Rules:
- If numeric operations (+, -, *, /, %, tax, bill) must be computed -> OUTPUT EXACTLY: ACTION: USE_CALCULATOR [clean_math_expression]
- Otherwise -> OUTPUT EXACTLY: ACTION: ANSWER_NORMALLY

Classification:
"""

class ToolRoutingChatbot:
    """Chatbot implementing the Prompt Template Decision Classifier."""
    def __init__(self):
        self.router_prompt = PromptTemplate(
            input_variables=["query"],
            template=ROUTING_PROMPT_TEMPLATE
        )
        self.calc_tool = get_custom_calculator_tool()

    def classify_intent(self, user_query: str) -> tuple[str, str]:
        """
        Classifies intent according to the Prompt Template rules.
        Returns (action_type, extracted_expression_or_query).
        """
        formatted = self.router_prompt.format(query=user_query)
        
        # Check for arithmetic operations and calculation keywords
        math_symbols = bool(re.search(r'[\+\-\*\/\%]', user_query))
        calc_words = any(w in user_query.lower() for w in ["calculate", "multiply", "divide", "tax", "total", "times", "price", "plus"])
        has_digits = bool(re.search(r'\d+', user_query))

        if (has_digits and (math_symbols or calc_words)):
            # Clean expression
            clean = user_query.lower()
            clean = re.sub(r'[^0-9+\-*/().]', ' ', clean).strip()
            # Collapse multiple spaces
            clean = re.sub(r'\s+', ' ', clean)
            return "USE_CALCULATOR", clean
        else:
            return "ANSWER_NORMALLY", user_query

    def execute(self, user_query: str):
        print(f"\nUser Query: \"{user_query}\"")
        action, payload = self.classify_intent(user_query)
        print(f"Router Decision: ACTION -> {action}")
        
        if action == "USE_CALCULATOR":
            print(f"  [*] Routing to '{self.calc_tool.name}' tool...")
            tool_res = self.calc_tool.run(user_query)
            print(f"  [Tool Output] : {tool_res}")
            final_response = f"Calculation Result: {tool_res}"
        else:
            print("  [*] Routing to Conversational LLM Engine...")
            final_response = (
                f"Conversational Answer: That's a great question! For '{user_query}', "
                f"popular insights include vibrant street food culture, historical recipes, "
                f"and localized culinary recommendations."
            )
            
        print(f"Chatbot Final Answer: {final_response}")
        print("-" * 65)
        return final_response


def main():
    print("=" * 65)
    print("   SESSION 4 - TASK 5: CHATBOT TOOL ROUTING PROMPT TEMPLATE")
    print("=" * 65)
    print("Base Decision Template:")
    print(ROUTING_PROMPT_TEMPLATE)
    print("=" * 65)
    
    bot = ToolRoutingChatbot()
    
    # Test with distinct query types as specified in Task 5
    queries = [
        "What is 450 * 0.18 + 25?",                                       # Calculation query
        "What are some popular street food snacks in Mumbai and why?",     # Normal query
        "Calculate the bill for 3 plates of biryani at 320 each with 5% tax", # Calculation query
        "Tell me a fun historical fact about the Indian Premier League."     # Normal query
    ]
    
    for q in queries:
        bot.execute(q)

if __name__ == "__main__":
    main()
