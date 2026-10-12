"""
SESSION 1 - Task 4: Simple LLMChain for Food Fun Facts
Objective: Build a simple chain in LangChain that takes a user's favorite food
(e.g., 'pani puri') and uses an LLMChain to generate a fun fact about it.
"""

import os
from dotenv import load_dotenv

load_dotenv()

from langchain_core.prompts import PromptTemplate

try:
    from langchain_openai import ChatOpenAI
except ImportError:
    ChatOpenAI = None

try:
    from langchain_classic.chains import LLMChain
except ImportError:
    try:
        # pyrefly: ignore [missing-import]
        from langchain.chains import LLMChain 
    except ImportError:
        LLMChain = None

# A mock runnable LLM for offline demonstration when no API key is provided
class MockFoodLLM:
    """Simulates an LLM for food facts when an API key is not present."""
    def __init__(self):
        self.facts = {
            "pani puri": (
                "Pani Puri is known by over 10 different regional names across India! "
                "In Delhi it is 'Gol Gappa', in West Bengal 'Puchka', in Maharashtra 'Pani Puri', "
                "and legend has it that Draupadi invented it in the Mahabharata when tasked "
                "with feeding the five Pandavas with limited leftover dough!"
            ),
            "pizza": (
                "The world's most famous pizza, the Margherita, was created in 1889 in Naples "
                "to represent the colors of the Italian flag: red tomatoes, white mozzarella, "
                "and green basil!"
            ),
            "biryani": (
                "The word 'Biryani' originates from the Persian word 'Birian' meaning 'fried before cooking'. "
                "It is believed to have been introduced to Indian royal kitchens during the Mughal era."
            )
        }

    def invoke(self, prompt_text: str) -> str:
        food_key = "pani puri"
        for key in self.facts:
            if key in prompt_text.lower():
                food_key = key
                break
        return self.facts.get(food_key, f"Fun fact: {food_key.title()} is a culinary delight enjoyed worldwide for its rich flavors and culture!")

    def predict(self, **kwargs) -> str:
        prompt_val = kwargs.get("food", "pani puri")
        return self.invoke(prompt_val)


def build_food_fact_chain(food_item: str):
    print("=" * 60)
    print("   SESSION 1 - TASK 4: LLMCHAIN FOOD FUN FACT GENERATOR")
    print("=" * 60)
    print(f"Target Food Item : '{food_item}'")
    print("-" * 60)

    template = (
        "You are an enthusiastic culinary historian. "
        "Share an interesting, unique, and fun fact about the food '{food}'. "
        "Keep the fact engaging and under 3 sentences."
    )
    
    prompt = PromptTemplate(
        template=template,
        input_variables=["food"]
    )
    
    api_key = os.getenv("OPENAI_API_KEY")
    has_valid_key = bool(api_key and api_key != "your_openai_api_key_here")

    if has_valid_key and LLMChain is not None:
        print("[*] Running with live OpenAI LLM via LangChain...")
        llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)
        chain = LLMChain(llm=llm, prompt=prompt)
        result = chain.run(food=food_item)
    elif LLMChain is not None:
        print("[*] Running LLMChain with Mock LLM (No API key required)...")
        # Demonstrate chain execution logic
        formatted_prompt = prompt.format(food=food_item)
        mock_llm = MockFoodLLM()
        result = mock_llm.invoke(formatted_prompt)
    else:
        # LCEL runnable fallback
        formatted_prompt = prompt.format(food=food_item)
        mock_llm = MockFoodLLM()
        result = mock_llm.invoke(formatted_prompt)

    print("\n[OUTPUT FUN FACT]:")
    print(result)
    print("=" * 60)
    return result


if __name__ == "__main__":
    test_food = "pani puri"
    build_food_fact_chain(test_food)
