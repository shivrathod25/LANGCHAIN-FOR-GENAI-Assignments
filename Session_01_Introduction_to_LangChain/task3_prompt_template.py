"""
SESSION 1 - Task 3: Dynamic Prompts using PromptTemplate
Objective: Use LangChain's PromptTemplate class to generate dynamic prompts 
with variable placeholders and format for 'Gujarat Titans'.
"""

from langchain_core.prompts import PromptTemplate

def main():
    print("=" * 60)
    print("   SESSION 1 - TASK 3: LANGCHAIN PROMPTTEMPLATE")
    print("=" * 60)
    
    # Define the PromptTemplate with an input variable
    template_str = "Why do you support {team} in IPL?"
    prompt_template = PromptTemplate(
        input_variables=["team"],
        template=template_str
    )
    
    print(f"Base Template       : '{template_str}'")
    print(f"Expected Variables  : {prompt_template.input_variables}")
    print("-" * 60)
    
    # Format with 'Gujarat Titans' as requested
    target_team = "Gujarat Titans"
    formatted_prompt = prompt_template.format(team=target_team)
    
    print(f"Input Team          : '{target_team}'")
    print(f"Formatted Output    : \"{formatted_prompt}\"")
    print("-" * 60)
    
    # Additional demonstration with other teams to show reusability
    sample_teams = ["Chennai Super Kings", "Mumbai Indians", "Royal Challengers Bengaluru"]
    print("Demonstrating Template Reusability:")
    for team in sample_teams:
        print(f"  -> {prompt_template.format(team=team)}")
        
    print("=" * 60)

if __name__ == "__main__":
    main()
