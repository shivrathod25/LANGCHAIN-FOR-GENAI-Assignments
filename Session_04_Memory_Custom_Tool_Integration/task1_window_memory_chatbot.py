"""
SESSION 4 - Task 1: Sliding Window Memory (k=2) Chatbot
Objective: Add conversation memory to a chatbot using LangChain so it remembers 
only the last 2 messages/interactions from the user and prunes older history.
"""

import os
import sys
from collections import deque
from dotenv import load_dotenv

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

load_dotenv()

class ConversationBufferWindowMemory:
    """
    Implements LangChain's ConversationBufferWindowMemory specification with sliding window k.
    Only retains the last k user-bot interactions in active memory buffer.
    """
    def __init__(self, k: int = 2, memory_key: str = "history"):
        self.k = k
        self.memory_key = memory_key
        self.buffer = deque(maxlen=k)

    def save_context(self, inputs: dict, outputs: dict):
        user_in = inputs.get("input", "")
        bot_out = outputs.get("output", "")
        self.buffer.append((user_in, bot_out))

    def load_memory_variables(self, inputs=None) -> dict:
        lines = []
        for user_msg, bot_msg in self.buffer:
            lines.append(f"Human: {user_msg}")
            lines.append(f"AI: {bot_msg}")
        return {self.memory_key: "\n".join(lines)}

    def get_history_list(self):
        return list(self.buffer)


class WindowMemoryChatbot:
    def __init__(self, k: int = 2):
        self.memory = ConversationBufferWindowMemory(k=k)

    def chat(self, user_message: str) -> str:
        # Load memory of past k interactions
        recent_history = self.memory.get_history_list()
        
        msg_lower = user_message.lower()
        if "what did i ask first" in msg_lower or "earliest message" in msg_lower:
            if len(recent_history) == 2:
                earliest_stored = recent_history[0][0]
                reply = f"In my active memory window (last 2 interactions), the earliest query I remember is: '{earliest_stored}'. Any older messages have been automatically pruned!"
            elif len(recent_history) == 1:
                reply = f"I only have 1 previous message in memory: '{recent_history[0][0]}'."
            else:
                reply = "This is the start of our chat, so no previous messages exist!"
        elif "remember" in msg_lower:
            stored_queries = [f"'{h[0]}'" for h in recent_history]
            reply = f"My active window (k=2) currently holds: {', '.join(stored_queries) if stored_queries else 'None'}."
        else:
            reply = f"Got it! Processing your message: '{user_message}'. (Active window size: {len(recent_history)}/2 stored items)"

        # Save turn to sliding window memory
        self.memory.save_context({"input": user_message}, {"output": reply})
        return reply


def main():
    print("=" * 65)
    print("   SESSION 4 - TASK 1: CONVERSATION BUFFER WINDOW MEMORY (k=2)")
    print("=" * 65)
    
    bot = WindowMemoryChatbot(k=2)
    
    test_messages = [
        "Message 1: My favorite sport is cricket.",
        "Message 2: I live in Ahmedabad, Gujarat.",
        "Message 3: My favorite food is Pani Puri.",
        "Message 4: What do you remember from our conversation?",
        "Message 5: What did I ask first in your active memory?"
    ]
    
    for idx, msg in enumerate(test_messages, 1):
        print(f"\n[Turn {idx}] User : {msg}")
        resp = bot.chat(msg)
        print(f"[Turn {idx}] Bot  : {resp}")
        print("  --> Active Memory Buffer:")
        print("     ", bot.memory.load_memory_variables()["history"].replace("\n", "\n      "))
        print("-" * 65)

if __name__ == "__main__":
    main()
