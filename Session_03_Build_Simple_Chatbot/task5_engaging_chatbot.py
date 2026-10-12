"""
SESSION 3 - Task 5: Engaging & Natural Chatbot (ChatGPT Improvement Implemented)
Objective: Test chatbot locally and implement ChatGPT's recommendation for making 
responses more natural, vibrant, and engaging (emojis, fan slogans, and interactive hooks).
"""

import os
import sys
from dotenv import load_dotenv

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

load_dotenv()

# ==============================================================================
# CHATGPT SUGGESTION DOCUMENTATION:
# ------------------------------------------------------------------------------
# Recommendation: "Transform robotic factual replies into dynamic fan-to-fan 
# conversations by applying three psychological engagement principles:
# 1. Authentic Team Anthem / Fan Slogan Hooks (e.g., 'Aava De!', 'Whistle Podu!')
# 2. Contextual Cricket Emojis (🏏, 💥, 🏆, ⚡) to bring visual energy
# 3. Conversational Follow-Up Hooks (asking the user an open-ended question to sustain dialogue)."
# ==============================================================================

ENGAGING_TEAM_DATA = {
    "gujarat titans": {
        "name": "Gujarat Titans",
        "slogan": "Aava De! ⚡⚡",
        "captain": "Shubman Gill 🏏",
        "trivia": "Did you know GT won the championship in their very first season in 2022?",
        "hook": "Do you reckon Gill's captaincy will take GT straight to the qualifiers this year? 🤔"
    },
    "csk": {
        "name": "Chennai Super Kings",
        "slogan": "Whistle Podu! 🦁💛",
        "captain": "Ruturaj Gaikwad 🏏",
        "trivia": "CSK has made it to 10 IPL finals and hoisted the golden trophy 5 times!",
        "hook": "Who is your all-time favorite CSK match-winner—Mahi Bhai or Suresh Raina? 💥"
    },
    "mumbai indians": {
        "name": "Mumbai Indians",
        "slogan": "Duniya Hila Denge! 💙🏆",
        "captain": "Hardik Pandya 🏏",
        "trivia": "MI was the first franchise ever to hit the landmark 5 IPL titles!",
        "hook": "What's your favorite iconic MI moment at the Wankhede? 🏟️"
    }
}

def generate_enhanced_response(user_input: str) -> str:
    user_lower = user_input.lower()
    selected_team = None
    
    for key, data in ENGAGING_TEAM_DATA.items():
        if key in user_lower or data["name"].lower() in user_lower:
            selected_team = data
            break
            
    if not selected_team:
        selected_team = ENGAGING_TEAM_DATA["gujarat titans"]

    if "captain" in user_lower:
        return (
            f"{selected_team['slogan']} The skipper leading {selected_team['name']} is the stylish {selected_team['captain']}! "
            f"He anchors the top order with sheer class. 🎯\n"
            f"💡 Quick Fact: {selected_team['trivia']}\n"
            f"👉 {selected_team['hook']}"
        )
    else:
        return (
            f"{selected_team['slogan']} You've got top-tier taste in cricket! {selected_team['name']} brings pure fireworks whenever they step onto the 22 yards. 🎆\n"
            f"💡 Quick Fact: {selected_team['trivia']}\n"
            f"👉 {selected_team['hook']}"
        )

def main():
    print("=" * 70)
    print("   SESSION 3 - TASK 5: NATURALLY ENGAGING CHATBOT")
    print("   (Enhanced with ChatGPT Emojis, Fan Slogans & Interactive Hooks)")
    print("=" * 70)
    
    test_conversations = [
        "I am a huge Gujarat Titans supporter!",
        "Who is the captain of CSK?"
    ]
    
    for prompt in test_conversations:
        print(f"\nUser: {prompt}")
        print("-" * 50)
        bot_reply = generate_enhanced_response(prompt)
        print(f"Bot:\n{bot_reply}")
        print("-" * 70)

if __name__ == "__main__":
    main()
