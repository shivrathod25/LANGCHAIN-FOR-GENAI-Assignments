"""
SESSION 3 - Task 4: Follow-up Question Handler IPL Chatbot
Objective: Modify the chatbot to maintain context across turns and resolve follow-up 
questions like 'Who is the captain?' after the user mentions an IPL team.
"""

import os
import sys
import re
from dotenv import load_dotenv

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

load_dotenv()

try:
    from langchain_core.chat_history import InMemoryChatMessageHistory
    from langchain_core.messages import HumanMessage, AIMessage

    class ConversationBufferMemory:
        def __init__(self, memory_key="history"):
            self.memory_key = memory_key
            self.history = InMemoryChatMessageHistory()

        def save_context(self, inputs: dict, outputs: dict):
            self.history.add_user_message(inputs.get("input", ""))
            self.history.add_ai_message(outputs.get("output", ""))

        def load_memory_variables(self, inputs=None):
            lines = [f"{'Human' if isinstance(m, HumanMessage) else 'AI'}: {m.content}" for m in self.history.messages]
            return {self.memory_key: "\n".join(lines)}
except ImportError:
    from langchain_classic.memory import ConversationBufferMemory

# Team details lookup
IPL_TEAMS = {
    "gujarat titans": {"name": "Gujarat Titans", "captain": "Shubman Gill", "home": "Narendra Modi Stadium, Ahmedabad"},
    "gt": {"name": "Gujarat Titans", "captain": "Shubman Gill", "home": "Narendra Modi Stadium, Ahmedabad"},
    "chennai super kings": {"name": "Chennai Super Kings", "captain": "Ruturaj Gaikwad", "home": "MA Chidambaram Stadium, Chennai"},
    "csk": {"name": "Chennai Super Kings", "captain": "Ruturaj Gaikwad", "home": "MA Chidambaram Stadium, Chennai"},
    "mumbai indians": {"name": "Mumbai Indians", "captain": "Hardik Pandya", "home": "Wankhede Stadium, Mumbai"},
    "mi": {"name": "Mumbai Indians", "captain": "Hardik Pandya", "home": "Wankhede Stadium, Mumbai"},
    "royal challengers bengaluru": {"name": "Royal Challengers Bengaluru", "captain": "Faf du Plessis", "home": "M. Chinnaswamy Stadium, Bengaluru"},
    "rcb": {"name": "Royal Challengers Bengaluru", "captain": "Faf du Plessis", "home": "M. Chinnaswamy Stadium, Bengaluru"},
    "kolkata knight riders": {"name": "Kolkata Knight Riders", "captain": "Shreyas Iyer", "home": "Eden Gardens, Kolkata"},
    "kkr": {"name": "Kolkata Knight Riders", "captain": "Shreyas Iyer", "home": "Eden Gardens, Kolkata"}
}

class ContextualIPLChatbot:
    """Chatbot capable of remembering active topic and handling follow-up queries."""
    def __init__(self):
        self.memory = ConversationBufferMemory(memory_key="history")
        self.active_team = None

    def _detect_team_mention(self, text: str):
        t_lower = text.lower()
        for key, data in IPL_TEAMS.items():
            if key in t_lower:
                self.active_team = data
                return data
        return None

    def respond(self, user_msg: str) -> str:
        new_team = self._detect_team_mention(user_msg)
        msg_lower = user_msg.lower()

        # Follow-up: Captain inquiry
        if "captain" in msg_lower or "who leads" in msg_lower or "skipper" in msg_lower:
            if self.active_team:
                reply = (
                    f"The captain of {self.active_team['name']} is {self.active_team['captain']}! "
                    f"He leads their batting order and on-field tactical strategy."
                )
            else:
                reply = "Which IPL team are you asking about? Tell me the team name first!"

        # Follow-up: Stadium inquiry
        elif "stadium" in msg_lower or "home ground" in msg_lower or "where do they play" in msg_lower:
            if self.active_team:
                reply = f"{self.active_team['name']}'s home ground is the iconic {self.active_team['home']}."
            else:
                reply = "Which team's stadium are you curious about?"

        # Team statement / introduction
        elif new_team:
            reply = (
                f"Awesome! {new_team['name']} is a fantastic squad. "
                f"They play their home matches at {new_team['home']}. What would you like to know about them?"
            )
        else:
            if self.active_team:
                reply = f"Talking about {self.active_team['name']}—feel free to ask about their captain, squad, or home ground!"
            else:
                reply = "Hello! Which IPL cricket team would you like to discuss today?"

        self.memory.save_context({"input": user_msg}, {"output": reply})
        return reply

def main():
    print("=" * 60)
    print("   SESSION 3 - TASK 4: CONTEXTUAL FOLLOW-UP IPL CHATBOT")
    print("=" * 60)
    
    bot = ContextualIPLChatbot()
    
    conversation_steps = [
        "I really love watching Gujarat Titans play!",
        "Who is the captain?",
        "Where is their home stadium?",
        "What about CSK?",
        "Who is the captain?"
    ]
    
    for idx, user_input in enumerate(conversation_steps, 1):
        print(f"\n[Step {idx}] User : {user_input}")
        bot_response = bot.respond(user_input)
        print(f"[Step {idx}] Bot  : {bot_response}")
        
    print("\n" + "-" * 60)
    print("Stored Multi-Turn Conversation History in Memory:")
    print("-" * 60)
    print(bot.memory.load_memory_variables()["history"])
    print("=" * 60)

if __name__ == "__main__":
    main()
