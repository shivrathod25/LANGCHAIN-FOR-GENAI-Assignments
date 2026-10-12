"""
SESSION 4 - Task 4: Chatbot Connected with Custom Calculator Tool
Objective: Connect the custom calculator tool to the chatbot so that when a user 
types a calculation request (like 'What is 15*3?'), the chatbot uses the tool to answer.
"""

import sys
import os
import re
from dotenv import load_dotenv

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

load_dotenv()

# Import the custom calculator tool from Task 3
from task3_custom_calculator_tool import get_custom_calculator_tool

class ConversationalToolChatbot:
    """A chatbot equipped with the custom calculator tool."""
    def __init__(self):
        self.calc_tool = get_custom_calculator_tool()

    def is_calculation_query(self, query: str) -> bool:
        """Determines if the user query is asking for mathematical calculation."""
        math_indicators = [
            r'\bwhat is\s+[0-9]+',
            r'\bcalculate\b',
            r'\bcompute\b',
            r'\badd\b',
            r'\bsubtract\b',
            r'\bmultiply\b',
            r'\bdivide\b',
            r'\b[0-9]+\s*[\+\-\*\/\^]\s*[0-9]+',
            r'\b[0-9]+\s*(?:times|plus|minus|divided by)\s*[0-9]+'
        ]
        return any(re.search(pattern, query.lower()) for pattern in math_indicators)

    def process_message(self, user_query: str) -> str:
        print(f"\nUser Query: \"{user_query}\"")
        
        if self.is_calculation_query(user_query):
            print(f"  [Intent Detected] -> Math calculation required")
            print(f"  [Tool Invocation] -> Calling {self.calc_tool.name}...")
            tool_output = self.calc_tool.run(user_query)
            print(f"  [Tool Result]     -> {tool_output}")
            response = f"Using my calculator tool, the answer is: {tool_output}"
        else:
            print(f"  [Intent Detected] -> Conversational inquiry")
            response = (
                f"I am an AI assistant with arithmetic tool capabilities! "
                f"You can ask me questions or send me math calculations like 'What is 15*3?'."
            )
            
        print(f"Bot Response: {response}")
        return response


def main():
    print("=" * 65)
    print("   SESSION 4 - TASK 4: CHATBOT WITH CUSTOM CALCULATOR TOOL")
    print("=" * 65)
    
    bot = ConversationalToolChatbot()
    
    test_queries = [
        "What is 15*3?",
        "Can you calculate 450 plus 150 divided by 2?",
        "What is 99 * 11?",
        "Hello! What kind of tasks can you help me with?"
    ]
    
    for q in test_queries:
        bot.process_message(q)
        print("-" * 65)

if __name__ == "__main__":
    main()
