"""
SESSION 1 - Task 5: Chains vs. Direct API Calls (Zomato Food Chatbot Case Study)
Objective: List three ways using chains in LangChain improves an AI-powered app
like Zomato's food recommendation chatbot compared to making direct LLM API calls.
"""

def print_zomato_comparison():
    title = "THREE WAYS LANGCHAIN CHAINS IMPROVE ZOMATO'S RECOMMENDATION CHATBOT"
    print("=" * len(title))
    print(title)
    print("=" * len(title))
    
    points = [
        (
            "1. Multi-Step Orchestration & Real-Time Data Pipeline",
            "Chains allow Zomato to connect distinct processing steps sequentially—such as extracting a user's craving ('spicy biryani'), querying live restaurant APIs for nearby availability and discounts, and passing structured results into an LLM for conversational suggestions.\nDirect API calls would require hundreds of lines of fragile manual glue code to combine external database queries with LLM completions."
        ),
        (
            "2. Statefulness & Dynamic Session Memory Management",
            "LangChain chains seamlessly integrate memory components (like ConversationBufferMemory), allowing the bot to remember past constraints (e.g., 'pure vegetarian', 'budget under ₹300', or previously selected restaurant) throughout the user's order journey.\nDirect API calls are inherently stateless, requiring developers to manually serialize, truncate, and reinject the entire chat history on every single request."
        ),
        (
            "3. Structured Output Parsing & Input Validation Guardrails",
            "Chains enforce strict output schemas (like Pydantic/JSON parsers) so that the LLM reliably produces parseable dish IDs, prices, and cart actions that directly trigger Zomato's checkout flow without hallucinations.\nDirect API calls often produce unstructured conversational text that easily breaks frontend checkout buttons and downstream order microservices."
        )
    ]
    
    for heading, explanation in points:
        print(f"\n{heading}")
        print("-" * len(heading))
        print(explanation)
        
    print("\n" + "=" * len(title))

def main():
    print_zomato_comparison()

if __name__ == "__main__":
    main()
