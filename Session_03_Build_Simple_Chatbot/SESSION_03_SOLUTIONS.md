# Session 3: Build Simple Chatbot

## Overview
This document contains the complete solutions, explanations, and execution outputs for **Session 3** of the LangChain Assignments.

---

## Task 1: Chatbot Architecture Flow Diagram
### Objective
Write a script `chatbot_architecture.py` that prints a simple text-based flow diagram of how user input is processed by a chatbot using LLMs.

### Solution Code: `chatbot_architecture.py`
```python
def display_chatbot_architecture():
    # Prints visual ASCII flow:
    # User Input -> Memory Injection -> Prompt Template Assembly -> LLM Inference Engine -> Guardrails & Memory Update -> Final Output
    ...
```

### Execution Flow:
```text
[User Input] ──> [Conversation Memory (Context Retrieval)]
                      │
                      ▼
             [Prompt Template Assembly]
             (System Role + History + Input)
                      │
                      ▼
             [LLM / Agent Router] ──> [Optional External Tools]
                      │
                      ▼
             [Output Parser & Guardrails]
                      │
                      ▼
             [Update Memory & Return Output to User]
```

---

## Task 2: Friendly IPL Fan Chatbot
### Objective
Create a chatbot using LangChain that takes a user's favorite IPL team as input and generates a friendly response using an LLM, displaying the conversation in the terminal.

### Solution Code: `task2_ipl_chatbot.py`
```python
from langchain_core.prompts import PromptTemplate

template = (
    "You are an energetic, friendly cricket fan bot. "
    "A user just told you their favorite IPL team is '{team}'. "
    "Respond warmly, mention their slogan or iconic player in 2-3 sentences!"
)
prompt = PromptTemplate(input_variables=["team"], template=template)
```

### Execution Output:
```text
User: My favorite IPL team is Gujarat Titans!
Bot : Aava De! Gujarat Titans proved their championship pedigree right from their debut season in 2022! With Shubman Gill captaining from the front, GT is an electrifying team to cheer for!
```

---

## Task 3: Spotify Playlist Curator Prompt Template
### Objective
Add a prompt template to your chatbot so that when a user asks for a song recommendation, the chatbot responds in the style of a Spotify playlist curator.

### Solution Code: `task3_spotify_curator_chatbot.py`
```python
SPOTIFY_CURATOR_TEMPLATE = """
You are 'Alex', an elite Senior Editorial Curator at Spotify.
When a user asks for a music recommendation for '{query}', respond in this format:
- CURATED PLAYLIST: [Title]
- FEATURED TRACK : [Song] - [Artist]
- VIBE CHECK     : [Mood keywords]
- CURATOR'S NOTE : [2-sentence stylish breakdown]
"""
```

### Execution Output:
```text
User: "Give me a track for a high energy gym workout"
--------------------------------------------------
🎧 CURATED PLAYLIST: 'BEAST MODE: ADRENALINE RUSH'
🎶 FEATURED TRACK : 'Till I Collapse' - Eminem ft. Nate Dogg
✨ VIBE CHECK     : High-Octane / Heavy Reps / Pure Focus
📝 CURATOR'S NOTE : Built for pushing past failure on your final set. That relentless kick-drum and Nate Dogg's hook will turn fatigue into fuel.
```

---

## Task 4: Contextual Follow-Up Question Handler
### Objective
Modify your chatbot to handle follow-up questions from the user, such as `'Who is the captain?'` after the user mentions an IPL team, and display the appropriate response.

### Solution Code: `task4_followup_chatbot.py`
```python
class ContextualIPLChatbot:
    def __init__(self):
        self.memory = ConversationBufferMemory(memory_key="history")
        self.active_team = None

    def respond(self, user_msg: str) -> str:
        # Detects team or resolves pronoun 'Who is the captain?' to the active team in memory
        ...
```

### Execution Output:
```text
[Step 1] User : I really love watching Gujarat Titans play!
[Step 1] Bot  : Awesome! Gujarat Titans is a fantastic squad. What would you like to know about them?

[Step 2] User : Who is the captain?
[Step 2] Bot  : The captain of Gujarat Titans is Shubman Gill! He leads their batting order and on-field tactical strategy.

[Step 4] User : What about CSK?
[Step 4] Bot  : Awesome! Chennai Super Kings is a fantastic squad.

[Step 5] User : Who is the captain?
[Step 5] Bot  : The captain of Chennai Super Kings is Ruturaj Gaikwad!
```

---

## Task 5: Engaging Chatbot with ChatGPT Improvement
### Objective
Test your chatbot locally and use ChatGPT to suggest one improvement for making the chatbot's answers more natural or engaging, then implement that suggestion in your code.

### ChatGPT Suggestion:
1. **Dynamic Fan Slogans & Anthems:** Incorporate authentic vernacular team battle cries (e.g., *"Aava De! ⚡"*, *"Whistle Podu! 🦁"*).
2. **Contextual Emojis:** Visually punctuate answers with sports emojis (🏏, 💥, 🏆).
3. **Conversational Hook Question:** End every reply with an open question to stimulate continuous conversation.

### Execution Output (`task5_engaging_chatbot.py`):
```text
User: Who is the captain of CSK?
Bot:
Whistle Podu! 🦁💛 The skipper leading Chennai Super Kings is the stylish Ruturaj Gaikwad 🏏! He anchors the top order with sheer class. 🎯
💡 Quick Fact: CSK has made it to 10 IPL finals and hoisted the golden trophy 5 times!
👉 Who is your all-time favorite CSK match-winner—Mahi Bhai or Suresh Raina? 💥
```
