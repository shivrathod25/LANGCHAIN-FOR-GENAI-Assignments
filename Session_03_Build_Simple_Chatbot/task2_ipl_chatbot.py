"""
SESSION 3 - Task 2: Friendly IPL Chatbot
Objective: Create a chatbot using LangChain that takes a user's favorite IPL team
as input and generates a friendly, enthusiastic response using an LLM.
"""

import os
from dotenv import load_dotenv

load_dotenv()

from langchain_core.prompts import PromptTemplate

# Pre-crafted responses for key teams if running in mock/offline mode
MOCK_RESPONSES = {
    "csk": "Whistle Podu! Chennai Super Kings is one of the most successful and beloved franchises in IPL history, led by Ruturaj Gaikwad and backed by the legendary MS Dhoni!",
    "chennai super kings": "Whistle Podu! Chennai Super Kings is one of the most successful and beloved franchises in IPL history, led by Ruturaj Gaikwad and backed by the legendary MS Dhoni!",
    "mi": "Duniya Hila Denge! Mumbai Indians has an incredible legacy of 5 IPL trophies, boasting elite match-winners like Rohit Sharma, Suryakumar Yadav, and Jasprit Bumrah!",
    "mumbai indians": "Duniya Hila Denge! Mumbai Indians has an incredible legacy of 5 IPL trophies, boasting elite match-winners like Rohit Sharma, Suryakumar Yadav, and Jasprit Bumrah!",
    "gt": "Aava De! Gujarat Titans proved their championship pedigree right from their debut season in 2022! With Shubman Gill captaining from the front, GT is an electrifying team to cheer for!",
    "gujarat titans": "Aava De! Gujarat Titans proved their championship pedigree right from their debut season in 2022! With Shubman Gill captaining from the front, GT is an electrifying team to cheer for!",
    "rcb": "Ee Sala Cup Namde! Royal Challengers Bengaluru has the most passionate fan army in cricket, ignited by the heart and soul of King Virat Kohli!"
}

def generate_friendly_ipl_response(team_name: str) -> str:
    template = (
        "You are an energetic, friendly, and knowledgeable cricket fan chatbot. "
        "A user just told you their favorite IPL team is '{team}'. "
        "Respond warmly, mention their iconic team slogan or key player, "
        "and celebrate their fan spirit in 2-3 enthusiastic sentences!"
    )
    prompt = PromptTemplate(input_variables=["team"], template=template)
    
    api_key = os.getenv("OPENAI_API_KEY")
    has_valid_key = bool(api_key and api_key != "your_openai_api_key_here")

    if has_valid_key:
        try:
            from langchain_openai import ChatOpenAI
            llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.8)
            chain = prompt | llm
            return chain.invoke({"team": team_name}).content
        except Exception as e:
            print(f"[!] OpenAI API notice: {e}. Using simulated response.")

    # Simulated response
    t_key = team_name.lower().strip()
    return MOCK_RESPONSES.get(
        t_key,
        f"Awesome choice! Supporting {team_name} shows true passion for the game! "
        f"Every match is an emotional rollercoaster, and their squad brings thrilling T20 fireworks to the pitch!"
    )

def main():
    print("=" * 60)
    print("   SESSION 3 - TASK 2: FRIENDLY IPL FAN CHATBOT")
    print("=" * 60)
    
    sample_teams = ["Gujarat Titans", "Chennai Super Kings", "Mumbai Indians"]
    
    for team in sample_teams:
        print(f"\nUser: My favorite IPL team is {team}!")
        response = generate_friendly_ipl_response(team)
        print(f"Bot : {response}")
        print("-" * 60)

if __name__ == "__main__":
    main()
