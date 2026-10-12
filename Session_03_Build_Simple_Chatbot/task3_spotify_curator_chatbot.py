"""
SESSION 3 - Task 3: Spotify Playlist Curator Prompt Template
Objective: Add a prompt template to your chatbot so that when a user asks for a song 
recommendation, the chatbot responds in the style of an official Spotify playlist curator.
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

from langchain_core.prompts import PromptTemplate

SPOTIFY_CURATOR_TEMPLATE = """
You are 'Alex', an elite Senior Editorial Curator at Spotify.
When a user asks for a music recommendation based on their vibe, genre, or mood: '{query}',
respond with the stylish, immersive swagger of a Spotify playlist curator.

Follow this exact curation format:
--------------------------------------------------
🎧 CURATED PLAYLIST: [Catchy Playlist Title]
🎶 FEATURED TRACK : [Song Title] - [Artist Name]
✨ VIBE CHECK     : [2-3 words describing aesthetic, e.g., 'Late Night Drive / Melancholic Lo-fi']
📝 CURATOR'S NOTE : [A chic 2-sentence breakdown of why this track hits different]
--------------------------------------------------
"""

def curate_music(query: str) -> str:
    prompt = PromptTemplate(
        input_variables=["query"],
        template=SPOTIFY_CURATOR_TEMPLATE
    )
    
    api_key = os.getenv("OPENAI_API_KEY")
    has_valid_key = bool(api_key and api_key != "your_openai_api_key_here")

    if has_valid_key:
        try:
            from langchain_openai import ChatOpenAI
            llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)
            chain = prompt | llm
            return chain.invoke({"query": query}).content
        except Exception as e:
            print(f"[!] API Notice: {e}. Using simulated curation response.")

    # Simulated curator response
    q_lower = query.lower()
    if "workout" in q_lower or "gym" in q_lower:
        return (
            "--------------------------------------------------\n"
            "🎧 CURATED PLAYLIST: 'BEAST MODE: ADRENALINE RUSH'\n"
            "🎶 FEATURED TRACK : 'Till I Collapse' - Eminem ft. Nate Dogg\n"
            "✨ VIBE CHECK     : High-Octane / Heavy Reps / Pure Focus\n"
            "📝 CURATOR'S NOTE : Built for pushing past failure on your final set. "
            "That relentless kick-drum and Nate Dogg's hook will turn fatigue into fuel.\n"
            "--------------------------------------------------"
        )
    elif "rain" in q_lower or "sad" in q_lower or "calm" in q_lower:
        return (
            "--------------------------------------------------\n"
            "🎧 CURATED PLAYLIST: 'RAIN DANCE & MONSOON MELLOW'\n"
            "🎶 FEATURED TRACK : 'Kun Faya Kun' - A.R. Rahman, Mohit Chauhan, Javed Ali\n"
            "✨ VIBE CHECK     : Ethereal Peace / Soulful Rainy Afternoons\n"
            "📝 CURATOR'S NOTE : A transcendent sonic journey that washes away mental clutter. "
            "Rahman's acoustic tapestry paired with soulful vocals feels like an embrace.\n"
            "--------------------------------------------------"
        )
    else:
        return (
            "--------------------------------------------------\n"
            "🎧 CURATED PLAYLIST: 'INDIE SUNSET VIBES'\n"
            "🎶 FEATURED TRACK : 'Kasoor' - Prateek Kuhad\n"
            "✨ VIBE CHECK     : Golden Hour / Nostalgic Warmth\n"
            "📝 CURATOR'S NOTE : Raw, acoustic vulnerability wrapped in gentle melodies. "
            "Drop this on your sunset commute when you want to feel deeply present.\n"
            "--------------------------------------------------"
        )

def main():
    print("=" * 60)
    print("   SESSION 3 - TASK 3: SPOTIFY CURATOR CHATBOT")
    print("=" * 60)
    
    test_queries = [
        "Give me a track for a high energy gym workout",
        "I want something calming while it rains outside",
        "Recommend a cool acoustic song for sunset"
    ]
    
    for q in test_queries:
        print(f"\nUser: \"{q}\"")
        curation = curate_music(q)
        print(curation)

if __name__ == "__main__":
    main()
