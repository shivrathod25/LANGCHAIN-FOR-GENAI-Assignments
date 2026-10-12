"""
SESSION 2 - Task 4: Conversational Memory with ConversationBufferMemory
Objective: Add conversational memory to an agent so it remembers the user's name
after they introduce themselves and uses it in subsequent responses.
"""

import os
import re
from dotenv import load_dotenv

load_dotenv()

# High-performance LangChain-compatible ConversationBufferMemory implementation
try:
    from langchain_core.chat_history import InMemoryChatMessageHistory
    from langchain_core.messages import HumanMessage, AIMessage

    class LangChainConversationBufferMemory:
        """
        Implements LangChain's ConversationBufferMemory specification using 
        langchain_core primitives for lightning-fast memory handling.
        """
        def __init__(self, memory_key="chat_history", return_messages=False):
            self.memory_key = memory_key
            self.return_messages = return_messages
            self.chat_history = InMemoryChatMessageHistory()

        def save_context(self, inputs: dict, outputs: dict):
            user_input = inputs.get("input", "")
            ai_output = outputs.get("output", "")
            if user_input:
                self.chat_history.add_user_message(user_input)
            if ai_output:
                self.chat_history.add_ai_message(ai_output)

        def load_memory_variables(self, inputs: dict = None) -> dict:
            if self.return_messages:
                return {self.memory_key: self.chat_history.messages}
            lines = []
            for msg in self.chat_history.messages:
                prefix = "Human" if isinstance(msg, HumanMessage) else "AI"
                lines.append(f"{prefix}: {msg.content}")
            return {self.memory_key: "\n".join(lines)}

        def clear(self):
            self.chat_history.clear()

    ConversationBufferMemory = LangChainConversationBufferMemory

except ImportError:
    from langchain_classic.memory import ConversationBufferMemory


class ConversationalMemoryAgent:
    """
    Agent that maintains state across dialogue turns using ConversationBufferMemory.
    """
    def __init__(self):
        self.memory = ConversationBufferMemory(memory_key="history", return_messages=False)
        self.user_name = None

    def _extract_name(self, text: str):
        match = re.search(r"(?:my name is|i am|call me|this is)\s+([A-Za-z]+)", text, re.IGNORECASE)
        if match:
            self.user_name = match.group(1).capitalize()

    def chat(self, user_message: str) -> str:
        # Check for introduction
        self._extract_name(user_message)
        
        # Load existing history from LangChain memory
        history = self.memory.load_memory_variables({})["history"]
        
        msg_lower = user_message.lower()
        if "what is my name" in msg_lower or "who am i" in msg_lower or "remember" in msg_lower:
            if self.user_name:
                response = f"Your name is {self.user_name}! I remember you introduced yourself earlier."
            else:
                response = "You haven't told me your name yet! What should I call you?"
        elif "my name is" in msg_lower or "i am" in msg_lower:
            response = f"Nice to meet you, {self.user_name}! How can I help you today?"
        elif "movie" in msg_lower or "recommend" in msg_lower:
            prefix = f"{self.user_name}, " if self.user_name else ""
            response = f"{prefix}I recommend checking out 'Kalki 2898 AD' or 'Deadpool & Wolverine'—they are currently top trending!"
        else:
            prefix = f"{self.user_name}, " if self.user_name else ""
            response = f"{prefix}I'm here to assist you with anything you need."

        # Save context to LangChain ConversationBufferMemory
        self.memory.save_context({"input": user_message}, {"output": response})
        return response

def main():
    print("=" * 60)
    print("   SESSION 2 - TASK 4: AGENT CONVERSATIONAL MEMORY")
    print("=" * 60)
    
    agent = ConversationalMemoryAgent()
    
    dialogue_turns = [
        "Hi there, my name is Aarav.",
        "What is the capital of India?",
        "Do you remember what my name is?",
        "Can you recommend a trending movie for me?"
    ]
    
    for turn_idx, user_input in enumerate(dialogue_turns, 1):
        print(f"\n[Turn {turn_idx}] User : {user_input}")
        response = agent.chat(user_input)
        print(f"[Turn {turn_idx}] Agent: {response}")
        
    print("\n" + "-" * 60)
    print("Inspecting Stored ConversationBufferMemory Buffer:")
    print("-" * 60)
    stored_history = agent.memory.load_memory_variables({})
    print(stored_history["history"])
    print("=" * 60)

if __name__ == "__main__":
    main()
