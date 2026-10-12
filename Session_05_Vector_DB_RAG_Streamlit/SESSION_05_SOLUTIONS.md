# Session 5: Vector DB, RAG Intro & Streamlit Chatbot

## Overview
This document contains the complete solutions, explanations, and execution outputs for **Session 5** of the LangChain Assignments.

---

## Task 1: Store Restaurant Reviews in Chroma Vector DB
### Objective
Install Chroma vector database locally and create a Python script that stores embeddings for 5 different restaurant reviews (as plain text strings).

### Solution Code: `task1_chroma_store_reviews.py`
```python
import chromadb
from chromadb.utils import embedding_functions

client = chromadb.PersistentClient(path="./chroma_reviews_db")
embed_fn = embedding_functions.DefaultEmbeddingFunction()

collection = client.get_or_create_collection(
    name="restaurant_reviews",
    embedding_function=embed_fn
)

REVIEWS_DATA = [
    {"id": "review_1", "restaurant": "Napoli Delights", "cuisine": "Italian", "text": "The wood-fired sourdough Margherita pizza..."},
    {"id": "review_2", "restaurant": "Punjab Grill", "cuisine": "North Indian", "text": "Punjab Grill serves heavenly slow-cooked Dal Makhani..."},
    {"id": "review_3", "restaurant": "Golden Dragon", "cuisine": "Chinese / Pan-Asian", "text": "Golden Dragon offers outstanding Cantonese dim sums..."},
    {"id": "review_4", "restaurant": "Café Mocha Haven", "cuisine": "Café / Desserts", "text": "A cozy, ambient spot with velvety iced hazelnut caramel coffee..."},
    {"id": "review_5", "restaurant": "Taco Fiesta", "cuisine": "Mexican", "text": "Taco Fiesta delivers crunchy authentic street tacos..."}
]

collection.upsert(
    ids=[r["id"] for r in REVIEWS_DATA],
    documents=[r["text"] for r in REVIEWS_DATA],
    metadatas=[{"restaurant": r["restaurant"], "cuisine": r["cuisine"]} for r in REVIEWS_DATA]
)
```

### Execution Output:
```text
[+] Initializing Persistent Chroma Client at: './chroma_reviews_db'
[+] Upserting 5 restaurant reviews into ChromaDB...
[SUCCESS] Total documents indexed in vector collection: 5
```

---

## Task 2: Cosine Similarity Review Search
### Objective
Write a Python function that takes a user's search query (like `'best pizza'`) and finds the most similar review from your stored embeddings using cosine similarity.

### Solution Code: `task2_cosine_similarity_search.py`
```python
def find_most_similar_review(query: str, persist_dir: str = "./chroma_reviews_db", top_k: int = 1) -> dict:
    collection = get_chroma_collection(persist_dir)
    results = collection.query(
        query_texts=[query],
        n_results=top_k,
        include=["documents", "metadatas", "distances"]
    )
    # Cosine Similarity = 1 - Cosine Distance
    ...
```

### Execution Output:
```text
User Query: "best pizza"
  Restaurant : Napoli Delights
  Cuisine    : Italian
  Cosine Sim : 0.2094 (Distance: 0.7906)
  Review     : "The wood-fired sourdough Margherita pizza at Napoli Delights has the crispiest crust, melted buffalo mozzarella, and freshest basil in town."

User Query: "rich coffee and sweet desserts"
  Restaurant : Café Mocha Haven
  Cuisine    : Café / Desserts
  Review     : "A cozy, ambient spot with velvety iced hazelnut caramel coffee, freshly brewed espresso, and warm Belgian dark chocolate fudge brownies."

User Query: "spicy noodles and dumplings"
  Restaurant : Golden Dragon
  Cuisine    : Chinese / Pan-Asian
  Review     : "Golden Dragon offers outstanding Cantonese dim sums, fiery Szechuan chilli noodles, and steamed dumplings bursting with savory umami."
```

---

## Task 3: Streamlit Chatbot UI with Vector DB
### Objective
Build a basic Streamlit chatbot UI where users can type a question about food recommendations and see a bot response fetching the most relevant review from ChromaDB.

### Run Command:
```bash
streamlit run Session_05_Vector_DB_RAG_Streamlit/task3_streamlit_chatbot.py
```

### Features:
- Clean responsive UI with `st.chat_message` and `st.chat_input`.
- Automatically connects to `./chroma_reviews_db`.
- Retrieves verified reviews and displays restaurant name, cuisine type, and match confidence score.

---

## Task 4: How RAG Improves Chatbot Quality Over Plain LLMs
### Objective
Explain in your own words how Retrieval-Augmented Generation (RAG) improves the quality of answers compared to using a plain language model without document retrieval.

### Detailed Analysis (`task4_rag_explanation.py`):
1. **Elimination of Hallucinations via Factual Grounding:**  
   Plain LLMs generate responses purely from compressed statistical weights, frequently inventing fake restaurants, nonexistent prices, or wrong opening hours. RAG strictly constrains the model's output to verified retrieved facts from the database.
2. **Access to Private, Real-Time & Domain-Specific Data:**  
   Foundation models have fixed training cutoffs and cannot know a company's internal menu changes, real-time inventory, or daily chef specials. RAG enables instant knowledge updates by simply upserting new vectors into ChromaDB in milliseconds.
3. **Transparent Source Attribution & Explainability:**  
   RAG allows the system to cite the exact source document or user review behind an answer (e.g., *"According to review #1 from Napoli Delights..."*), creating transparency and trust.
4. **Massive Cost and Compute Efficiency:**  
   Fine-tuning large language models requires expensive GPU infrastructure and carries the risk of catastrophic forgetting. RAG achieves domain accuracy at near-zero marginal cost using lightweight vector embeddings.

---

## Task 5: Streamlit RAG Chatbot with Local File (`food_facts.txt`)
### Objective
Modify your Streamlit chatbot so that it connects to a local text file containing 10 food facts (one per line) and uses that file as its knowledge source for answering user questions.

### Knowledge File: `food_facts.txt` (10 Indexed Facts)
1. *Pani Puri is known by over 10 distinct names across India including Gol Gappa, Puchka, and Gupchup.*
2. *Saffron is the world's most expensive spice by weight, requiring over 75,000 crocus flowers to produce a single pound.*
3. *The Margherita pizza was invented in 1889 in Naples, representing the Italian flag with tomatoes, mozzarella, and basil.*
4. *Dark chocolate containing 70% or higher cocoa is rich in flavanols, antioxidants, and compounds that boost serotonin and dopamine.*
5. *Biryani originated from the Persian word 'Birian' meaning fried before cooking, brought to royal kitchens during the Mughal era.*
6. *Honey is the only known natural food that never spoils, with edible pots of honey discovered in ancient Egyptian tombs.*
7. *Apples float in water because roughly 25% of their total volume consists of trapped air pockets.*
8. *Wasabi served in most commercial restaurants is actually dyed horseradish and mustard, as real Japanese Wasabi is exceptionally rare.*
9. *Pistachios were considered a royal delicacy in ancient Persia, with the Queen of Sheba decreeing them an exclusively royal food.*
10. *Coffee beans are not actually beans, but rather the harvested seeds from bright red fruits known as coffee cherries.*

### Run Command:
```bash
streamlit run Session_05_Vector_DB_RAG_Streamlit/task5_streamlit_rag_food_facts.py
```

### Retrieval Verification:
- **Query:** *"Why does honey never spoil?"*  
  -> **Matched Fact #6:** *"Honey is the only known natural food that never spoils, with edible pots of honey discovered in ancient Egyptian tombs."*
- **Query:** *"Is wasabi real?"*  
  -> **Matched Fact #8:** *"Wasabi served in most commercial restaurants is actually dyed horseradish and mustard, as real Japanese Wasabi is exceptionally rare."*
