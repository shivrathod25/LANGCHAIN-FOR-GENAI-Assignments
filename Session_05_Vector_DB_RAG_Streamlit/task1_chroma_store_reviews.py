"""
SESSION 5 - Task 1: Store Restaurant Reviews in Chroma Vector Database
Objective: Initialize ChromaDB locally and store embeddings for 5 different 
restaurant reviews (as plain text strings).
"""

import os
import sys
import chromadb
from chromadb.utils import embedding_functions

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Define 5 diverse restaurant reviews
REVIEWS_DATA = [
    {
        "id": "review_1",
        "restaurant": "Napoli Delights",
        "cuisine": "Italian",
        "text": "The wood-fired sourdough Margherita pizza at Napoli Delights has the crispiest crust, melted buffalo mozzarella, and freshest basil in town."
    },
    {
        "id": "review_2",
        "restaurant": "Punjab Grill",
        "cuisine": "North Indian",
        "text": "Punjab Grill serves heavenly slow-cooked Dal Makhani, tender Paneer Tikka, and warm butter garlic naan that completely melts in your mouth."
    },
    {
        "id": "review_3",
        "restaurant": "Golden Dragon",
        "cuisine": "Chinese / Pan-Asian",
        "text": "Golden Dragon offers outstanding Cantonese dim sums, fiery Szechuan chilli noodles, and steamed dumplings bursting with savory umami."
    },
    {
        "id": "review_4",
        "restaurant": "Café Mocha Haven",
        "cuisine": "Café / Desserts",
        "text": "A cozy, ambient spot with velvety iced hazelnut caramel coffee, freshly brewed espresso, and warm Belgian dark chocolate fudge brownies."
    },
    {
        "id": "review_5",
        "restaurant": "Taco Fiesta",
        "cuisine": "Mexican",
        "text": "Taco Fiesta delivers crunchy authentic street tacos loaded with grilled fillings, zesty lime guacamole, and spicy roasted chipotle salsa."
    }
]

def initialize_and_populate_chroma(persist_dir: str = "./chroma_reviews_db"):
    print("=" * 65)
    print("   SESSION 5 - TASK 1: CHROMA VECTOR DATABASE SETUP")
    print("=" * 65)
    print(f"[+] Initializing Persistent Chroma Client at: '{persist_dir}'")
    
    # Initialize persistent Chroma client
    client = chromadb.PersistentClient(path=persist_dir)
    
    # Use default all-MiniLM-L6-v2 embedding function
    embed_fn = embedding_functions.DefaultEmbeddingFunction()
    
    # Create or get collection
    collection = client.get_or_create_collection(
        name="restaurant_reviews",
        embedding_function=embed_fn,
        metadata={"description": "Food & Restaurant Reviews Collection"}
    )
    
    # Prepare documents, metadatas, and ids
    ids = [item["id"] for item in REVIEWS_DATA]
    documents = [item["text"] for item in REVIEWS_DATA]
    metadatas = [{"restaurant": item["restaurant"], "cuisine": item["cuisine"]} for item in REVIEWS_DATA]
    
    print(f"[+] Upserting {len(documents)} restaurant reviews into ChromaDB...")
    collection.upsert(
        ids=ids,
        documents=documents,
        metadatas=metadatas
    )
    
    total_count = collection.count()
    print(f"[SUCCESS] Total documents indexed in vector collection: {total_count}")
    print("-" * 65)
    print("Stored Reviews in Vector Database:")
    for i, doc in enumerate(documents, 1):
        print(f"  {i}. [{metadatas[i-1]['restaurant']} - {metadatas[i-1]['cuisine']}]")
        print(f"     \"{doc}\"")
        
    print("=" * 65)
    return client, collection

if __name__ == "__main__":
    db_path = os.path.join(os.path.dirname(__file__), "chroma_reviews_db")
    initialize_and_populate_chroma(persist_dir=db_path)
