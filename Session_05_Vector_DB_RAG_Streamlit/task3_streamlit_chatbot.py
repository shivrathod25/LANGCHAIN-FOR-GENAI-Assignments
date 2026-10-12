"""
SESSION 5 - Task 3: Streamlit Vector DB Food Recommendation Chatbot
Objective: Build a basic Streamlit chatbot UI where users type questions about 
food recommendations and the bot fetches and displays the most relevant review from ChromaDB.

Run Command: streamlit run Session_05_Vector_DB_RAG_Streamlit/task3_streamlit_chatbot.py
"""

import os
import streamlit as st
import chromadb
from chromadb.utils import embedding_functions

# Set page configuration
st.set_page_config(
    page_title="Zomato AI - Food Review Recommender",
    page_icon="🍕",
    layout="centered"
)

# Custom header styling
st.title("🍕 FoodieBot: Vector DB Recommender")
st.caption("Powered by ChromaDB Vector Search & Local Embeddings")
st.markdown("---")

@st.cache_resource
def get_vector_db():
    """Initializes or connects to the local ChromaDB vector store."""
    db_path = os.path.join(os.path.dirname(__file__), "chroma_reviews_db")
    
    # If not populated, seed it with initial reviews
    from task1_chroma_store_reviews import initialize_and_populate_chroma
    if not os.path.exists(db_path):
        initialize_and_populate_chroma(persist_dir=db_path)
        
    client = chromadb.PersistentClient(path=db_path)
    embed_fn = embedding_functions.DefaultEmbeddingFunction()
    collection = client.get_collection(name="restaurant_reviews", embedding_function=embed_fn)
    return collection

collection = get_vector_db()

# Initialize chat session history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "👋 Hi there! I'm your food recommendation concierge. Ask me for recommendations like 'Where can I find the best pizza?' or 'Recommend spicy noodles'!"
        }
    ]

# Display existing chat messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User prompt input
if prompt := st.chat_input("Ask for food recommendations..."):
    # Append user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Perform Vector DB similarity retrieval
    with st.chat_message("assistant"):
        with st.spinner("Searching restaurant reviews in Vector DB..."):
            results = collection.query(
                query_texts=[prompt],
                n_results=1,
                include=["documents", "metadatas", "distances"]
            )
            
            if results and results["documents"] and results["documents"][0]:
                top_doc = results["documents"][0][0]
                meta = results["metadatas"][0][0]
                distance = results["distances"][0][0]
                similarity_score = max(0.0, 1.0 - distance)
                
                bot_reply = (
                    f"### 🍽️ Top Recommendation: **{meta['restaurant']}**\n"
                    f"- **Cuisine**: {meta['cuisine']}\n"
                    f"- **Match Score**: {similarity_score:.1%}\n\n"
                    f"**Verified Review:**\n"
                    f"> \"{top_doc}\"\n\n"
                    f"*Would you like directions, menu details, or another cuisine suggestion?*"
                )
            else:
                bot_reply = "I couldn't find a review closely matching that craving in our database. Try asking for pizza, biryani, dim sums, or café desserts!"

            st.markdown(bot_reply)
            st.session_state.messages.append({"role": "assistant", "content": bot_reply})
