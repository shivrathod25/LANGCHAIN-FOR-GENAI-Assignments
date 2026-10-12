# Session 4: Memory + Custom Tool Integration

## Overview
This document contains the complete solutions, explanations, and execution outputs for **Session 4** of the LangChain Assignments.

---

## Task 1: Sliding Window Memory (`k=2`) Chatbot
### Objective
Add conversation memory to a simple chatbot using LangChain so it can remember the last 2 messages from the user and reply accordingly.

### Solution Code: `task1_window_memory_chatbot.py`
```python
class ConversationBufferWindowMemory:
    """
    Implements LangChain's ConversationBufferWindowMemory specification with sliding window k.
    Prunes earlier interactions to prevent token window overflow.
    """
    def __init__(self, k: int = 2):
        self.k = k
        self.buffer = deque(maxlen=k)
```

### Execution Output:
```text
[Turn 1] User : Message 1: My favorite sport is cricket.
[Turn 2] User : Message 2: I live in Ahmedabad, Gujarat.
[Turn 3] User : Message 3: My favorite food is Pani Puri.
[Turn 4] User : What do you remember from our conversation?
Bot: My active window (k=2) currently holds: 'Message 2: I live in Ahmedabad, Gujarat.', 'Message 3: My favorite food is Pani Puri.'.
[Turn 5] User : What did I ask first in your active memory?
Bot: In my active memory window (last 2 interactions), the earliest query I remember is: 'Message 3: My favorite food is Pani Puri.'. Any older messages have been automatically pruned!
```

---

## Task 2: Zomato-Style Food Ordering Chatbot with Memory
### Objective
Implement a Zomato-style food ordering chatbot that remembers the user's chosen restaurant and cuisine in the conversation using `ConversationBufferMemory`.

### Solution Code: `task2_zomato_memory_chatbot.py`
```python
class ZomatoOrderChatbot:
    def __init__(self):
        self.memory = ConversationBufferMemory(memory_key="chat_history")
        self.chosen_restaurant = None
        self.chosen_cuisine = None
        self.cart = []
```

### Multi-Turn Dialogue Output:
```text
[Turn 1] User : Hi, I want to order from Punjab Grill today. Craving North Indian food!
[Turn 1] Zomato: Perfect! I've set your restaurant to Punjab Grill and cuisine preference to North Indian. What delicious dishes can I help you order today?

[Turn 2] User : What appetizers do you recommend here?
[Turn 2] Zomato: Great choice! For North Indian dining at Punjab Grill, I highly recommend: 1. Paneer Tikka (Rs. 240), 2. Dal Makhani (Rs. 260), 3. Garlic Butter Naan (Rs. 50).

[Turn 3] User : Add 1 Paneer Tikka and 2 Butter Naan to my cart.
[Turn 3] Zomato: Added 1x Paneer Tikka (Rs. 240), 2x Butter Naan (Rs. 100) to your cart from Punjab Grill!

[Turn 4] User : Can you review my order summary and confirm which restaurant I am ordering from?
[Turn 4] Zomato: [ZOMATO ORDER SUMMARY]
  - Selected Restaurant: Punjab Grill
  - Preferred Cuisine  : North Indian
  - Items in Cart      : 1x Paneer Tikka (Rs. 240), 2x Butter Naan (Rs. 100)
  - Delivery Status    : Ready to place order
```

---

## Task 3: Custom Calculator Tool Integration with LangChain's Tool Class
### Objective
Create a custom calculator tool in Python (add, subtract, multiply, divide functions) and integrate it with your chatbot using LangChain's `Tool` class.

### Solution Code: `task3_custom_calculator_tool.py`
```python
from langchain_core.tools import Tool

def add(a: float, b: float) -> float: return a + b
def subtract(a: float, b: float) -> float: return a - b
def multiply(a: float, b: float) -> float: return a * b
def divide(a: float, b: float) -> float:
    if b == 0: raise ZeroDivisionError("Cannot divide by zero!")
    return a / b

calc_tool = Tool(
    name="CustomCalculator",
    func=custom_calculator_engine,
    description="Performs arithmetic operations: add, subtract, multiply, divide."
)
```

### Execution Output:
```text
Input : '15*3'               -> Output: 15*3 = 45
Input : 'add 120 and 45'     -> Output: 120 + 45 = 165.0
Input : 'divide 100 by 4'    -> Output: 100 / 4 = 25.0
Input : 'subtract 30 from 100' -> Output: 100 - 30 = 70.0
```

---

## Task 4: Connect Custom Calculator Tool to Chatbot
### Objective
Connect your custom calculator tool to the chatbot so that when a user types a calculation request (like `'What is 15*3?'`), the chatbot uses your tool to answer.

### Solution Code: `task4_chatbot_with_calc_tool.py`
```python
class ConversationalToolChatbot:
    def __init__(self):
        self.calc_tool = get_custom_calculator_tool()

    def process_message(self, user_query: str):
        if self.is_calculation_query(user_query):
            # invokes self.calc_tool.run(user_query)
```

### Execution Output:
```text
User Query: "What is 15*3?"
  [Intent Detected] -> Math calculation required
  [Tool Invocation] -> Calling CustomCalculator...
  [Tool Result]     -> 15*3 = 45
Bot Response: Using my calculator tool, the answer is: 15*3 = 45
```

---

## Task 5: Tool Routing Prompt Template (Calculator vs. Normal Answer)
### Objective
Generate a prompt template that helps your chatbot decide when to use the calculator tool versus when to answer normally. Test with at least two different user queries.

### Decision Prompt Template:
```text
You are an intelligent Intent Router for an AI Assistant system.
Analyze the user query: "{query}"

Available Paths:
1. USE_CALCULATOR: Select this if the user asks for arithmetic, discounts, percentage, bill calculation, or numerical computations.
2. ANSWER_NORMALLY: Select this if the user asks for explanations, trivia, conversation, recommendations, or non-math general knowledge.

Decision Rules:
- If numeric operations (+, -, *, /, %, tax, bill) must be computed -> ACTION: USE_CALCULATOR
- Otherwise -> ACTION: ANSWER_NORMALLY
```

### Execution Output on Distinct Queries:
1. **Query:** `"What is 450 * 0.18 + 25?"`
   - **Router Action:** `USE_CALCULATOR`
   - **Result:** `450 * 0.18 + 25 = 106.0`
2. **Query:** `"What are some popular street food snacks in Mumbai and why?"`
   - **Router Action:** `ANSWER_NORMALLY`
   - **Result:** Conversational response generated by LLM.
3. **Query:** `"Calculate the bill for 3 plates of biryani at 320 each with 5% tax"`
   - **Router Action:** `USE_CALCULATOR`
   - **Result:** `(3.0 * 320.0) + 5.0% tax = 1008.00`
