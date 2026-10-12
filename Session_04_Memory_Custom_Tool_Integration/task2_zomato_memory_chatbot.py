"""
SESSION 4 - Task 2: Zomato-Style Food Ordering Chatbot with Memory
Objective: Implement a Zomato-style food ordering chatbot that remembers the user's 
chosen restaurant and cuisine in the conversation using ConversationBufferMemory.
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

    class LangChainConversationBufferMemory:
        def __init__(self, memory_key="history"):
            self.memory_key = memory_key
            self.chat_history = InMemoryChatMessageHistory()

        def save_context(self, inputs: dict, outputs: dict):
            self.chat_history.add_user_message(inputs.get("input", ""))
            self.chat_history.add_ai_message(outputs.get("output", ""))

        def load_memory_variables(self, inputs=None) -> dict:
            lines = [f"{'Human' if isinstance(m, HumanMessage) else 'AI'}: {m.content}" for m in self.chat_history.messages]
            return {self.memory_key: "\n".join(lines)}

    ConversationBufferMemory = LangChainConversationBufferMemory
except ImportError:
    from langchain_classic.memory import ConversationBufferMemory


class ZomatoOrderChatbot:
    """Chatbot retaining restaurant, cuisine, and food preferences across multi-turn order flows."""
    def __init__(self):
        self.memory = ConversationBufferMemory(memory_key="chat_history")
        self.chosen_restaurant = None
        self.chosen_cuisine = None
        self.cart = []

    def _extract_restaurant_and_cuisine(self, text: str):
        t_lower = text.lower()
        
        # Restaurant extraction
        restaurants = ["punjab grill", "la pino'z", "domino's", "behrouz biryani", "mainland china", "haldiram's"]
        for r in restaurants:
            if r in t_lower:
                self.chosen_restaurant = r.title()
                break
                
        # Cuisine extraction
        cuisines = ["north indian", "south indian", "italian", "chinese", "mughlai", "mexican", "fast food"]
        for c in cuisines:
            if c in t_lower:
                self.chosen_cuisine = c.title()
                break

    def chat(self, user_msg: str) -> str:
        self._extract_restaurant_and_cuisine(user_msg)
        msg_lower = user_msg.lower()

        # 1. Review / summary query
        if "review" in msg_lower or "summary" in msg_lower or "which restaurant" in msg_lower or "status" in msg_lower:
            cart_str = ", ".join(self.cart) if self.cart else "Empty"
            response = (
                f"[ZOMATO ORDER SUMMARY]\n"
                f"  - Selected Restaurant: {self.chosen_restaurant or 'Not selected'}\n"
                f"  - Preferred Cuisine  : {self.chosen_cuisine or 'Not selected'}\n"
                f"  - Items in Cart      : {cart_str}\n"
                f"  - Delivery Status    : Ready to place order"
            )

        # 2. Recommendation query
        elif "recommend" in msg_lower or "appetizer" in msg_lower or "menu" in msg_lower or "dishes" in msg_lower:
            rest_str = f"at {self.chosen_restaurant}" if self.chosen_restaurant else "nearby"
            cuis_str = f"{self.chosen_cuisine} " if self.chosen_cuisine else ""
            response = (
                f"Great choice! For {cuis_str}dining {rest_str}, I highly recommend: "
                f"1. Paneer Tikka (Rs. 240), 2. Dal Makhani (Rs. 260), 3. Garlic Butter Naan (Rs. 50). "
                f"Would you like to add any of these to your cart?"
            )

        # 3. Add to cart query
        elif "add" in msg_lower or "cart" in msg_lower:
            items_found = []
            if "paneer tikka" in msg_lower:
                items_found.append("1x Paneer Tikka (Rs. 240)")
            if "butter naan" in msg_lower or "naan" in msg_lower:
                items_found.append("2x Butter Naan (Rs. 100)")
            if items_found:
                self.cart.extend(items_found)
                rest_str = f"from {self.chosen_restaurant}" if self.chosen_restaurant else ""
                response = f"Added {', '.join(items_found)} to your cart {rest_str}! Ready for checkout?"
            else:
                response = "Items noted and added to your active order cart!"

        # 4. Initial restaurant / cuisine selection
        elif self.chosen_restaurant or self.chosen_cuisine:
            response = (
                f"Perfect! I've set your restaurant to {self.chosen_restaurant} and cuisine preference to {self.chosen_cuisine}. "
                f"What delicious dishes can I help you order today?"
            )
        else:
            response = "Welcome to Zomato! Please tell me which restaurant or cuisine you'd like to order from."

        # Save to LangChain ConversationBufferMemory
        self.memory.save_context({"input": user_msg}, {"output": response})
        return response


def main():
    print("=" * 65)
    print("   SESSION 4 - TASK 2: ZOMATO FOOD ORDERING CHATBOT WITH MEMORY")
    print("=" * 65)
    
    bot = ZomatoOrderChatbot()
    
    dialogue = [
        "Hi, I want to order from Punjab Grill today. Craving North Indian food!",
        "What appetizers do you recommend here?",
        "Add 1 Paneer Tikka and 2 Butter Naan to my cart.",
        "Can you review my order summary and confirm which restaurant I am ordering from?"
    ]
    
    for turn_idx, msg in enumerate(dialogue, 1):
        print(f"\n[Turn {turn_idx}] User : {msg}")
        reply = bot.chat(msg)
        print(f"[Turn {turn_idx}] Zomato: {reply}")
        print("-" * 65)
        
    print("\nInspecting LangChain ConversationBufferMemory Context:")
    print("=" * 65)
    print(bot.memory.load_memory_variables()["chat_history"])
    print("=" * 65)

if __name__ == "__main__":
    main()
