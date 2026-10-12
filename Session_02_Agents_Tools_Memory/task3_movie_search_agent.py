"""
SESSION 2 - Task 3: Movie Search Tool for LangChain Agent
Objective: Build a Search tool using LangChain that lets an agent fetch latest
trending movies from a mock list (e.g., 'Show me trending movies on BookMyShow').
"""

import os
from dotenv import load_dotenv

load_dotenv()

# Simulated database of trending movies on BookMyShow
MOCK_BOOKMYSHOW_MOVIES = [
    {
        "title": "Kalki 2898 AD",
        "genre": "Sci-Fi / Action",
        "language": "Hindi / Telugu",
        "rating": "9.1/10",
        "trending_rank": 1,
        "synopsis": "A modern avatar of Vishnu descends to Earth in a dystopian future to protect the world."
    },
    {
        "title": "Stree 2: Sarkate Ka Aatank",
        "genre": "Horror / Comedy",
        "language": "Hindi",
        "rating": "8.8/10",
        "trending_rank": 2,
        "synopsis": "The town of Chanderi is haunted once again, this time by a headless entity known as Sarkata."
    },
    {
        "title": "Deadpool & Wolverine",
        "genre": "Superhero / Action / Comedy",
        "language": "English / Hindi",
        "rating": "8.9/10",
        "trending_rank": 3,
        "synopsis": "Wolverine is recovering from his injuries when he crosses paths with the loudmouth Deadpool."
    },
    {
        "title": "Fighter",
        "genre": "Action / Aerial Drama",
        "language": "Hindi",
        "rating": "8.2/10",
        "trending_rank": 4,
        "synopsis": "Top Indian Air Force aviators come together to form Air Dragons in the face of imminent danger."
    },
    {
        "title": "Pushpa 2: The Rule",
        "genre": "Action / Drama",
        "language": "Telugu / Hindi",
        "rating": "9.3/10",
        "trending_rank": 5,
        "synopsis": "Pushpa Raj continues to reign over the red sandalwood smuggling empire while confronting law enforcement."
    }
]

def search_trending_movies(query: str) -> str:
    """
    Searches the mock BookMyShow movie catalog by title, genre, language, or general trending request.
    """
    q_words = set(query.lower().replace('/', ' ').replace('&', ' ').split())
    results = []
    
    # Generic request check
    is_general_trending = any(word in q_words for word in ["trending", "bookmyshow", "all", "show", "movies", "latest"])
    
    for m in MOCK_BOOKMYSHOW_MOVIES:
        genre_words = set(m["genre"].lower().replace('/', ' ').split())
        title_words = set(m["title"].lower().split())
        
        # Match if genre or title intersects with search query keywords
        if (q_words & genre_words) or (q_words & title_words) or is_general_trending:
            results.append(
                f"#{m['trending_rank']} {m['title']} | Genre: {m['genre']} | "
                f"Lang: {m['language']} | Rating: {m['rating']}\n"
                f"   Synopsis: {m['synopsis']}"
            )
            
    if results:
        header = f"Found {len(results)} trending movie(s) on BookMyShow:\n"
        return header + "\n" + "\n\n".join(results)
    
    return "No matching movies found. Try searching for 'action', 'horror', or 'trending'."

def create_movie_search_tool():
    """Wraps movie search into a LangChain Tool."""
    from langchain_core.tools import Tool
    return Tool(
        name="BookMyShow_Movie_Search",
        func=search_trending_movies,
        description="Useful for fetching current trending movies, ratings, genres, and synopses on BookMyShow."
    )

def run_agent_movie_query(query: str):
    print(f"\nUser Query: \"{query}\"")
    movie_tool = create_movie_search_tool()

    api_key = os.getenv("OPENAI_API_KEY")
    has_valid_key = bool(api_key and api_key != "your_openai_api_key_here")

    if has_valid_key:
        try:
            from langchain_openai import ChatOpenAI
            from langchain.agents import initialize_agent, AgentType
            llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
            agent = initialize_agent([movie_tool], llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)
            print("[*] Running Live LangChain Agent with Movie Search...")
            response = agent.run(query)
            print(f"Agent Final Answer:\n{response}")
            return
        except Exception as e:
            print(f"[!] Falling back to local agent reasoning: {e}")

    # ReAct Simulation Framework
    print("-" * 50)
    print("Agent Reasoning Flow (ReAct Pattern):")
    print(f"Thought: The user wants to know about movies matching '{query}'. I will query the BookMyShow tool.")
    print(f"Action: {movie_tool.name}")
    print(f"Action Input: '{query}'")
    results = movie_tool.run(query)
    print(f"Observation:\n{results}")
    print("Thought: I have retrieved the movie records. Ready to present the answer.")
    print(f"\n[Agent Final Answer]:\n{results}")
    print("-" * 50)

def main():
    print("=" * 60)
    print("   SESSION 2 - TASK 3: BOOKMYSHOW MOVIE SEARCH AGENT")
    print("=" * 60)
    
    run_agent_movie_query("Show me trending movies on BookMyShow")
    run_agent_movie_query("Find horror comedy movies")

if __name__ == "__main__":
    main()
