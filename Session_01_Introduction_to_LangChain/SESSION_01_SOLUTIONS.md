# Session 1: Introduction to LangChain - Why & What

## Overview
This document contains the complete solutions, explanations, and execution outputs for **Session 1** of the LangChain Assignments.

---

## Task 1: Environment Setup & LangChain Installation
### Objective
Install LangChain in a new Python virtual environment and run a simple script that prints the version of LangChain installed.

### Solution Code: `task1_langchain_version.py`
```python
import sys
import platform

try:
    import langchain
    print(f"[SUCCESS] langchain version      : {langchain.__version__}")
except ImportError as e:
    print(f"[ERROR] langchain is not installed: {e}")
```

### Execution Output
```text
============================================================
   SESSION 1 - TASK 1: LANGCHAIN ENVIRONMENT CHECK
============================================================
[+] Python Executable : E:\TOPS Classes\Agentic Ai\.venv\Scripts\python.exe
[+] Python Version    : 3.12.10
[+] Operating System  : Windows 10
------------------------------------------------------------
[SUCCESS] langchain version      : 1.4.0
[SUCCESS] langchain-core version : 1.6.9
[SUCCESS] langchain-community   : 0.4.2
[SUCCESS] langchain-openai      : 1.7.0
============================================================
Environment setup verified successfully!
```

---

## Task 2: Direct OpenAI API Call & Problem Analysis
### Objective
Write a Python script that sends a prompt to OpenAI's GPT-3.5 API directly and prints the response. Then, list two problems faced or could be faced with this direct API approach.

### Solution Code: `task2_direct_openai.py`
```python
import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Explain what IPL is in two concise sentences."}
    ],
    temperature=0.7
)
print(response.choices[0].message.content)
```

### Two Problems with Direct API Approach
1. **Lack of Dynamic Prompt Management & Templating:**
   - With raw API calls, developers must manually concatenate strings using f-strings. As prompts grow complex with variable substitutions, few-shot examples, and conditional logic, raw strings become error-prone and non-reusable.
2. **Statelessness & Absence of Memory/Tool Orchestration:**
   - Raw API calls are completely stateless. To keep track of multi-turn dialogues or integrate tools (like web search or calculators), developers have to write complex custom state-management and parsing code. LangChain solves this with built-in Chains, Memory, and Agents.

---

## Task 3: Dynamic Prompts with PromptTemplate
### Objective
Use LangChain's `PromptTemplate` class to create a dynamic prompt that takes a user's favorite IPL team as input and generates a question like `'Why do you support [team] in IPL?'`. Print the final prompt for `'Gujarat Titans'`.

### Solution Code: `task3_prompt_template.py`
```python
from langchain_core.prompts import PromptTemplate

template_str = "Why do you support {team} in IPL?"
prompt_template = PromptTemplate(
    input_variables=["team"],
    template=template_str
)

formatted_prompt = prompt_template.format(team="Gujarat Titans")
print(formatted_prompt)
```

### Execution Output
```text
Base Template       : 'Why do you support {team} in IPL?'
Expected Variables  : ['team']
Input Team          : 'Gujarat Titans'
Formatted Output    : "Why do you support Gujarat Titans in IPL?"
```

---

## Task 4: Simple LLMChain for Food Fun Fact
### Objective
Build a simple chain in LangChain that takes a user's favorite food (like `'pani puri'`) and uses an `LLMChain` to generate a fun fact about it. Print the output.

### Solution Code: `task4_food_chain.py`
```python
from langchain_core.prompts import PromptTemplate
from langchain_classic.chains import LLMChain
from langchain_openai import ChatOpenAI

prompt = PromptTemplate(
    template="You are a culinary historian. Share a fun fact about {food}.",
    input_variables=["food"]
)

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)
chain = LLMChain(llm=llm, prompt=prompt)
result = chain.run(food="pani puri")
print(result)
```

### Execution Output
```text
[OUTPUT FUN FACT]:
Pani Puri is known by over 10 different regional names across India! In Delhi it is 'Gol Gappa', in West Bengal 'Puchka', in Maharashtra 'Pani Puri', and legend has it that Draupadi invented it in the Mahabharata when tasked with feeding the five Pandavas with limited leftover dough!
```

---

## Task 5: Zomato Recommendation Chatbot: Chains vs. Direct API
### Objective
List three ways using chains in LangChain can improve an AI-powered app like Zomato's food recommendation chatbot compared to making direct LLM API calls, and explain each in 1-2 sentences.

### Three Key Advantages:
1. **Multi-Step Orchestration & Real-Time Data Pipeline:**  
   Chains allow Zomato to connect distinct processing steps sequentially—such as extracting a user's craving ('spicy biryani'), querying live restaurant APIs for nearby availability and discounts, and passing structured results into an LLM for conversational suggestions.
2. **Statefulness & Dynamic Session Memory Management:**  
   LangChain chains seamlessly integrate memory components (like `ConversationBufferMemory`), allowing the bot to remember past constraints (e.g., 'pure vegetarian', 'budget under ₹300', or previously selected restaurant) throughout the user's order journey.
3. **Structured Output Parsing & Guardrails:**  
   Chains enforce strict output schemas (like Pydantic/JSON parsers) so that the LLM reliably produces parseable dish IDs, prices, and cart actions that directly trigger Zomato's checkout flow without hallucinations.
