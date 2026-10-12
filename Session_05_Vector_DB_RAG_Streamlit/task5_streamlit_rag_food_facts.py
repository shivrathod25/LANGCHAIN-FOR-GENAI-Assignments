"""
SESSION 5 - Task 5: Streamlit RAG Chatbot using Local Knowledge File (food_facts.txt)
Objective: Connect Streamlit chatbot to a local text file containing 10 food facts 
(one per line), generate embeddings for each line, and use similarity search to pick 
the best answer for user questions.

Run Command: streamlit run Session_05_Vector_DB_RAG_Streamlit/task5_streamlit_rag_food_facts.py
"""

import os
import sys
import streamlit as st
import chromadb
from chromadb.utils import embedding_functions

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Page configuration
st.set_page_config(
    page_title="Food Facts RAG Assistant",
    page_icon="🥑",
    layout="centered"
)

st.title("🥑 FoodFacts: Retrieval-Augmented Chatbot")
st.caption("Grounded Knowledge from 'food_facts.txt' using ChromaDB & Vector Search")
st.markdown("---")

FACTS_FILE_PATH = os.path.join(os.path.dirname(__file__), "food_facts.txt")
CHROMA_FACTS_DIR = os.path.join(os.path.dirname(__file__), "chroma_facts_db")

@st.cache_resource
def index_food_facts():
    """
    Reads food_facts.txt line by line, generates embeddings, 
    and stores them in a local ChromaDB collection.
    """
    if not os.path.exists(FACTS_FILE_PATH):
        st.error(f"File not found: {FACTS_FILE_PATH}")
        return None

    with open(FACTS_FILE_PATH, "r", encoding="utf-8") as f:
        facts = [line.strip() for line in f if line.strip()]

    client = chromadb.PersistentClient(path=CHROMA_FACTS_DIR)
    embed_fn = embedding_functions.DefaultEmbeddingFunction()
    
    collection = client.get_or_create_collection(
        name="food_facts_knowledge_base",
        embedding_function=embed_fn,
        metadata={"description": "10 Verified Food Facts"}
    )
    
    # Upsert lines
    ids = [f"fact_{i+1}" for i in range(len(facts))]
    metadatas = [{"fact_number": i+1, "source": "food_facts.txt"} for i in range(len(facts))]
    
    collection.upsert(
        ids=ids,
        documents=facts,
        metadatas=metadatas
    )
    return collection

facts_collection = index_food_facts()

# Sidebar: View Loaded Knowledge Source
with st.sidebar:
    st.header("📚 Knowledge Base")
    st.markdown(f"**Source:** `food_facts.txt` ({len(open(FACTS_FILE_PATH, 'r', encoding='utf-8').readlines())} facts)")
    with st.expander("View All 10 Indexed Facts"):
        with open(FACTS_FILE_PATH, "r", encoding="utf-8") as f:
            for i, line in enumerate(f, 1):
                if line.strip():
                    st.markdown(f"**{i}.** {line.strip()}")

# Chat history initialization
if "rag_messages" not in st.session_state:
    st.session_state.rag_messages = [
        {
            "role": "assistant",
            "content": "👋 Hello! I am your Food Facts Knowledge Assistant. Ask me anything like:\n- *'Why does honey never spoil?'*\n- *'Tell me a fact about wasabi'* \n- *'Why do apples float?'*"
        }
    ]

# Render conversation history
for msg in st.session_state.rag_messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User query input
if user_input := st.chat_input("Ask a question about food facts..."):
    # Append and render user query
    st.session_state.rag_messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Retrieving verified facts from Vector Database..."):
            # Step 1: Vector similarity retrieval
            results = facts_collection.query(
                query_texts=[user_input],
                n_results=1,
                include=["documents", "metadatas", "distances"]
            )

            if results and results["documents"] and results["documents"][0]:
                retrieved_fact = results["documents"][0][0]
                meta = results["metadatas"][0][0]
                dist = results["distances"][0][0]
                confidence = max(0.0, 1.0 - dist)
                
                # Check for OpenAI API key to run generative synthesis
                api_key = os.getenv("OPENAI_API_KEY")
                has_key = bool(api_key and api_key != "your_openai_api_key_here")

                if has_key:
                    try:
                        from openai import OpenAI
                        client = OpenAI(api_key=api_key)
                        prompt_system = (
                            "You are a helpful culinary AI assistant. "
                            f"Answer the user's question using ONLY the retrieved fact provided below.\n\n"
                            f"Retrieved Fact: {retrieved_fact}"
                        )
                        completion = client.chat.completions.create(
                            model="gpt-3.5-turbo",
                            messages=[
                                {"role": "system", "content": prompt_system},
                                {"role": "user", "content": user_input}
                            ],
                            temperature=0.5
                        )
                        synthesis = completion.choices[0].message.content.strip()
                    except Exception as e:
                        synthesis = retrieved_fact
                else:
                    synthesis = (
                        f"Based on our verified knowledge base: **{retrieved_fact}**"
                    )

                response_markdown = (
                    f"### 💡 Answer:\n{synthesis}\n\n"
                    f"---\n"
                    f"📖 **Retrieved Knowledge Source:**\n"
                    f"> *Fact #{meta['fact_number']} from `food_facts.txt`*  \n"
                    f"> \"{retrieved_fact}\"\n\n"
                    f"🎯 **Vector Match Confidence**: `{confidence:.1%}`"
                )
            else:
                response_markdown = "I couldn't find a relevant fact in the knowledge base. Please ask about honey, wasabi, pizza, coffee, or apples!"

            st.markdown(response_markdown)
            st.session_state.rag_messages.append({"role": "assistant", "content": response_markdown})
