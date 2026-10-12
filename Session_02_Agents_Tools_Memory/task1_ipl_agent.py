"""
SESSION 2 - Task 1: IPL Cricket Team Agent
Objective: Create a simple LangChain Agent that can answer basic questions about 
IPL cricket teams using a predefined list of teams and their captains.
"""

import os
from dotenv import load_dotenv

load_dotenv()

# Predefined database of IPL teams and their captains & details
IPL_DATABASE = {
    "chennai super kings": {"captain": "Ruturaj Gaikwad", "trophies": 5, "home": "MA Chidambaram Stadium, Chennai"},
    "csk": {"captain": "Ruturaj Gaikwad", "trophies": 5, "home": "MA Chidambaram Stadium, Chennai"},
    "mumbai indians": {"captain": "Hardik Pandya", "trophies": 5, "home": "Wankhede Stadium, Mumbai"},
    "mi": {"captain": "Hardik Pandya", "trophies": 5, "home": "Wankhede Stadium, Mumbai"},
    "gujarat titans": {"captain": "Shubman Gill", "trophies": 1, "home": "Narendra Modi Stadium, Ahmedabad"},
    "gt": {"captain": "Shubman Gill", "trophies": 1, "home": "Narendra Modi Stadium, Ahmedabad"},
    "royal challengers bengaluru": {"captain": "Faf du Plessis", "trophies": 0, "home": "M. Chinnaswamy Stadium, Bengaluru"},
    "rcb": {"captain": "Faf du Plessis", "trophies": 0, "home": "M. Chinnaswamy Stadium, Bengaluru"},
    "kolkata knight riders": {"captain": "Shreyas Iyer", "trophies": 3, "home": "Eden Gardens, Kolkata"},
    "kkr": {"captain": "Shreyas Iyer", "trophies": 3, "home": "Eden Gardens, Kolkata"},
    "rajasthan royals": {"captain": "Sanju Samson", "trophies": 1, "home": "Sawai Mansingh Stadium, Jaipur"},
    "rr": {"captain": "Sanju Samson", "trophies": 1, "home": "Sawai Mansingh Stadium, Jaipur"},
    "sunrisers hyderabad": {"captain": "Pat Cummins", "trophies": 1, "home": "Rajiv Gandhi Intl Stadium, Hyderabad"},
    "srh": {"captain": "Pat Cummins", "trophies": 1, "home": "Rajiv Gandhi Intl Stadium, Hyderabad"},
    "delhi capitals": {"captain": "Rishabh Pant", "trophies": 0, "home": "Arun Jaitley Stadium, Delhi"},
    "dc": {"captain": "Rishabh Pant", "trophies": 0, "home": "Arun Jaitley Stadium, Delhi"},
    "punjab kings": {"captain": "Sam Curran", "trophies": 0, "home": "PCA Stadium, Mullanpur"},
    "pbks": {"captain": "Sam Curran", "trophies": 0, "home": "PCA Stadium, Mullanpur"},
    "lucknow super giants": {"captain": "KL Rahul", "trophies": 0, "home": "BRSABV Ekana Cricket Stadium, Lucknow"},
    "lsg": {"captain": "KL Rahul", "trophies": 0, "home": "BRSABV Ekana Cricket Stadium, Lucknow"}
}

def lookup_ipl_info(query: str) -> str:
    """Finds IPL team captain and stats from the predefined database."""
    query_lower = query.lower().strip()
    for team, info in IPL_DATABASE.items():
        if team in query_lower:
            return (
                f"Team: {team.upper()}\n"
                f"Captain: {info['captain']}\n"
                f"IPL Titles Won: {info['trophies']}\n"
                f"Home Stadium: {info['home']}"
            )
    return (
        "Team not found in database. Available teams: CSK, MI, GT, RCB, KKR, "
        "RR, SRH, DC, PBKS, LSG."
    )

def create_ipl_tool():
    """Initializes and returns the LangChain Tool for IPL Lookup."""
    from langchain_core.tools import Tool
    return Tool(
        name="IPL_Lookup_Tool",
        func=lookup_ipl_info,
        description="Useful for answering questions about IPL teams, captains, trophies, and stadiums. Input should be the team name."
    )

def run_agent_query(user_query: str):
    print(f"\nUser Query: \"{user_query}\"")
    ipl_tool = create_ipl_tool()
    
    api_key = os.getenv("OPENAI_API_KEY")
    has_valid_key = bool(api_key and api_key != "your_openai_api_key_here")

    if has_valid_key:
        try:
            from langchain_openai import ChatOpenAI
            from langchain.agents import initialize_agent, AgentType
            llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
            agent = initialize_agent([ipl_tool], llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)
            print("[*] Running Live LangChain ReAct Agent...")
            response = agent.run(user_query)
            print(f"Agent Final Answer: {response}")
            return
        except Exception as e:
            print(f"[!] Falling back to local agent execution: {e}")

    # ReAct Simulation Framework (Agent Thought -> Action -> Observation -> Final Answer)
    print("-" * 50)
    print("Agent Reasoning Flow (ReAct Pattern):")
    print(f"Thought: The user is asking about an IPL team. I need to look up details in the IPL database.")
    print(f"Action: {ipl_tool.name}")
    print(f"Action Input: '{user_query}'")
    obs = ipl_tool.run(user_query)
    print(f"Observation:\n{obs}")
    print(f"Thought: I now have the team details. I can provide the final answer to the user.")
    print(f"Final Answer: {obs.replace(chr(10), ', ')}")
    print("-" * 50)

def main():
    print("=" * 60)
    print("   SESSION 2 - TASK 1: IPL CRICKET TEAMS AGENT")
    print("=" * 60)
    
    run_agent_query("Who is the captain of Gujarat Titans and where is their home stadium?")
    run_agent_query("Tell me about CSK captain and their trophies")

if __name__ == "__main__":
    main()
