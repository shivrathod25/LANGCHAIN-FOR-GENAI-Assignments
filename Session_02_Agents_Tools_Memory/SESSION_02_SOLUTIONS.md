# Session 2: Agents, Tools & Memory

## Overview
This document contains the complete solutions, explanations, and execution outputs for **Session 2** of the LangChain Assignments.

---

## Task 1: IPL Cricket Team Agent
### Objective
Create a simple LangChain Agent that can answer basic questions about IPL cricket teams using a predefined list of teams and their captains.

### Solution Code: `task1_ipl_agent.py`
```python
from langchain_core.tools import Tool

IPL_DATABASE = {
    "chennai super kings": {"captain": "Ruturaj Gaikwad", "trophies": 5, "home": "MA Chidambaram Stadium, Chennai"},
    "gujarat titans": {"captain": "Shubman Gill", "trophies": 1, "home": "Narendra Modi Stadium, Ahmedabad"},
    # ...
}

def lookup_ipl_info(query: str) -> str:
    # searches predefined team database
    ...
```

### Execution Output
```text
User Query: "Who is the captain of Gujarat Titans and where is their home stadium?"
--------------------------------------------------
Agent Reasoning Flow (ReAct Pattern):
Thought: The user is asking about an IPL team. I need to look up details in the IPL database.
Action: IPL_Lookup_Tool
Action Input: 'Who is the captain of Gujarat Titans and where is their home stadium?'
Observation:
Team: GUJARAT TITANS
Captain: Shubman Gill
IPL Titles Won: 1
Home Stadium: Narendra Modi Stadium, Ahmedabad
Final Answer: Team: GUJARAT TITANS, Captain: Shubman Gill, IPL Titles Won: 1, Home Stadium: Narendra Modi Stadium, Ahmedabad
```

---

## Task 2: Calculator Tool Integration
### Objective
Integrate the Calculator tool from LangChain into your agent so it can solve math questions like `'What is 12 times 8?'` and return the answer.

### Solution Code: `task2_calculator_agent.py`
```python
from langchain_core.tools import Tool

def safe_math_eval(expression_str: str) -> str:
    # Safely parses math text like '12 times 8' into '12 * 8' and evaluates
    ...

calc_tool = Tool(
    name="Calculator",
    func=safe_math_eval,
    description="Useful for solving mathematical calculations."
)
```

### Execution Output
```text
User Query: "What is 12 times 8?"
--------------------------------------------------
Agent Reasoning Flow (ReAct Pattern):
Thought: The user has asked a mathematical question. I should use the Calculator tool.
Action: Calculator
Action Input: 'What is 12 times 8?'
Observation: 96
Final Answer: The answer to 'What is 12 times 8?' is 96.
```

---

## Task 3: Movie Search Tool (BookMyShow Mock)
### Objective
Build a Search tool using LangChain that lets your agent fetch the latest trending movies from a mock list (e.g., `'Show me trending movies on BookMyShow'`).

### Solution Code: `task3_movie_search_agent.py`
```python
MOCK_BOOKMYSHOW_MOVIES = [
    {"title": "Kalki 2898 AD", "genre": "Sci-Fi / Action", "rating": "9.1/10", ...},
    {"title": "Stree 2: Sarkate Ka Aatank", "genre": "Horror / Comedy", "rating": "8.8/10", ...},
    # ...
]
```

### Execution Output
```text
User Query: "Show me trending movies on BookMyShow"
--------------------------------------------------
Observation:
Found 5 trending movie(s) on BookMyShow:
#1 Kalki 2898 AD | Genre: Sci-Fi / Action | Lang: Hindi / Telugu | Rating: 9.1/10
#2 Stree 2: Sarkate Ka Aatank | Genre: Horror / Comedy | Lang: Hindi | Rating: 8.8/10
#3 Deadpool & Wolverine | Genre: Superhero / Action / Comedy | Lang: English / Hindi | Rating: 8.9/10
#4 Fighter | Genre: Action / Aerial Drama | Lang: Hindi | Rating: 8.2/10
#5 Pushpa 2: The Rule | Genre: Action / Drama | Lang: Telugu / Hindi | Rating: 9.3/10
```

---

## Task 4: Conversational Memory with ConversationBufferMemory
### Objective
Add conversational memory to your agent so it remembers the user's name after they introduce themselves and uses it in later responses.

### Solution Code: `task4_memory_agent.py`
```python
from langchain_core.chat_history import InMemoryChatMessageHistory

class ConversationalMemoryAgent:
    def __init__(self):
        self.memory = ConversationBufferMemory(memory_key="history")
        ...
```

### Execution Output
```text
[Turn 1] User : Hi there, my name is Aarav.
[Turn 1] Agent: Nice to meet you, Aarav! How can I help you today?

[Turn 2] User : What is the capital of India?
[Turn 2] Agent: Aarav, I'm here to assist you with anything you need.

[Turn 3] User : Do you remember what my name is?
[Turn 3] Agent: Your name is Aarav! I remember you introduced yourself earlier.

[Turn 4] User : Can you recommend a trending movie for me?
[Turn 4] Agent: Aarav, I recommend checking out 'Kalki 2898 AD' or 'Deadpool & Wolverine'!
```

---

## Task 5: Combined Search & Calculator Agent (Food Delivery Domain)
### Objective
Generate and adapt a LangChain agent combining both Search and Calculator tools for a chosen domain (Food Delivery / Zomato Billing).

### Solution Code: `task5_combined_agent.py`
```python
search_tool = Tool(
    name="Food_Menu_Search",
    func=search_food_menu,
    description="Searches restaurant menu items, dish prices, ratings, and preparation times."
)

calc_tool = Tool(
    name="Billing_Calculator",
    func=calculate_order_math,
    description="Calculates bill totals, item quantities, discounts, and taxes."
)
```

### Execution Output
```text
User Request: "Find Paneer Butter Masala and calculate total for 2 plates with 5% tax"
--------------------------------------------------
Agent Reasoning Flow (ReAct Multi-Tool Pattern):
Thought: First I need to look up the dish price using Food_Menu_Search.
Action: Food_Menu_Search
Observation: Paneer Butter Masala | Restaurant: Punjab Grill | Price: Rs. 280
Thought: Now I need to calculate total for 2 portions + 5% GST using Billing_Calculator.
Action: Billing_Calculator
Action Input: '(280 * 2) * 1.05'
Observation: Rs. 588.0
Final Answer: Paneer Butter Masala from Punjab Grill is Rs. 280 per portion. Total for 2 portions with 5% GST is: Rs. 588.0 (Rs. 560 base + Rs. 28 GST).
```
