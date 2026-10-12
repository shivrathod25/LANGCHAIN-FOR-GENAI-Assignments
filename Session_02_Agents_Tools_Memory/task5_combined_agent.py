"""
SESSION 2 - Task 5: Multi-Tool Agent (Food Delivery Domain)
Objective: Combine both Calculator and Search tools in a unified LangChain Agent,
customized for the Food Delivery domain (Zomato/Swiggy-style ordering & billing).
"""

import os
import re
import math
from dotenv import load_dotenv

load_dotenv()

# ==============================================================================
# 1. DOMAIN SEARCH TOOL: Food Delivery Catalog & Prices
# ==============================================================================
FOOD_MENU_DATABASE = {
    "paneer butter masala": {"restaurant": "Punjab Grill", "price": 280, "rating": 4.5, "prep_time": "25 mins"},
    "butter naan": {"restaurant": "Punjab Grill", "price": 45, "rating": 4.6, "prep_time": "15 mins"},
    "margherita pizza": {"restaurant": "La Pino'z Pizza", "price": 249, "rating": 4.2, "prep_time": "30 mins"},
    "farmhouse pizza": {"restaurant": "Domino's Pizza", "price": 399, "rating": 4.4, "prep_time": "30 mins"},
    "chicken dum biryani": {"restaurant": "Behrouz Biryani", "price": 350, "rating": 4.7, "prep_time": "35 mins"},
    "gulab jamun": {"restaurant": "Bikanervala", "price": 60, "rating": 4.8, "prep_time": "10 mins"},
    "cold coffee": {"restaurant": "Café Coffee Day", "price": 120, "rating": 4.1, "prep_time": "10 mins"}
}

def search_food_menu(query: str) -> str:
    """Searches food items, prices, and restaurants in the delivery catalog."""
    q = query.lower().strip()
    matches = []
    for item, details in FOOD_MENU_DATABASE.items():
        if item in q or any(word in item for word in q.split() if len(word) > 3):
            matches.append(
                f"- Dish: {item.title()} | Restaurant: {details['restaurant']} | "
                f"Price: Rs. {details['price']} | Rating: {details['rating']}* | Prep: {details['prep_time']}"
            )
    if matches:
        return "Menu Items Found:\n" + "\n".join(matches)
    return "No exact food match found. Available items: Paneer Butter Masala, Butter Naan, Margherita Pizza, Chicken Dum Biryani, etc."

# ==============================================================================
# 2. DOMAIN CALCULATOR TOOL: Order Total & Tax/Discount Computation
# ==============================================================================
def calculate_order_math(expression: str) -> str:
    """Evaluates mathematical operations for billing, discounts, and taxes."""
    clean_expr = expression.lower().strip()
    clean_expr = re.sub(r'\btimes\b|\bmultiplied by\b|\bx\b', '*', clean_expr)
    clean_expr = re.sub(r'\bplus\b|\band\b', '+', clean_expr)
    clean_expr = re.sub(r'\bminus\b|\boff\b', '-', clean_expr)
    clean_expr = re.sub(r'\bdivided by\b', '/', clean_expr)
    
    # Strip non-math characters
    allowed = re.sub(r'[^0-9+\-*/().^ ]', '', clean_expr).strip()
    if not allowed:
        return "Error: Could not parse calculation expression."
    try:
        result = eval(allowed, {"__builtins__": None, "math": math}, {})
        return str(round(result, 2))
    except Exception as e:
        return f"Calculation error: {e}"

# ==============================================================================
# 3. LANGCHAIN AGENT CREATION
# ==============================================================================
def create_food_delivery_agent():
    from langchain_core.tools import Tool
    
    search_tool = Tool(
        name="Food_Menu_Search",
        func=search_food_menu,
        description="Searches restaurant menu items, dish prices, ratings, and preparation times."
    )
    
    calc_tool = Tool(
        name="Billing_Calculator",
        func=calculate_order_math,
        description="Calculates bill totals, item quantities, discounts, and taxes. Input should be arithmetic expressions like '280 * 2 + 50'."
    )
    
    return [search_tool, calc_tool]

def execute_combined_agent_flow(query: str):
    print(f"\nUser Request: \"{query}\"")
    tools = create_food_delivery_agent()
    search_tool, calc_tool = tools[0], tools[1]

    api_key = os.getenv("OPENAI_API_KEY")
    has_valid_key = bool(api_key and api_key != "your_openai_api_key_here")

    if has_valid_key:
        try:
            from langchain_openai import ChatOpenAI
            from langchain.agents import initialize_agent, AgentType
            llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
            agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)
            print("[*] Running Live LangChain Agent with Combined Tools...")
            res = agent.run(query)
            print(f"Agent Final Output:\n{res}")
            return
        except Exception as e:
            print(f"[!] Falling back to local agent reasoning: {e}")

    # ReAct Multi-Tool Execution Demonstration
    print("-" * 50)
    print("Agent Reasoning Flow (ReAct Multi-Tool Pattern):")
    
    # Step 1: Look up price
    print(f"Thought: First I need to look up the dish price using {search_tool.name}.")
    print(f"Action: {search_tool.name}")
    print(f"Action Input: '{query}'")
    menu_info = search_tool.run(query)
    print(f"Observation:\n{menu_info}")
    
    # Step 2: Extract price and compute bill with 5% GST
    print(f"Thought: Now I need to calculate total for 2 portions + 5% GST using {calc_tool.name}.")
    math_expr = "(280 * 2) * 1.05"
    print(f"Action: {calc_tool.name}")
    print(f"Action Input: '{math_expr}'")
    calc_res = calc_tool.run(math_expr)
    print(f"Observation: Rs. {calc_res}")
    
    # Step 3: Final response
    print(f"Thought: I now have the food details and total bill. Formulating final answer.")
    print(f"\n[Agent Final Answer]:")
    print(f"Paneer Butter Masala from Punjab Grill is Rs. 280 per portion.")
    print(f"Total for 2 portions with 5% GST is: Rs. {calc_res} (Rs. 560 base + Rs. 28 GST).")
    print("-" * 50)

def main():
    print("=" * 60)
    print("   SESSION 2 - TASK 5: COMBINED SEARCH & CALCULATOR AGENT")
    print("   Domain: Food Delivery & Billing (Zomato / Swiggy Style)")
    print("=" * 60)
    
    execute_combined_agent_flow("Find Paneer Butter Masala and calculate total for 2 plates with 5% tax")

if __name__ == "__main__":
    main()
