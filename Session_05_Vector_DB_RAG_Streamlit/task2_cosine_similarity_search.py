"""
SESSION 5 - Task 2: Cosine Similarity Review Search
Objective: Write a Python function that takes a user's search query (like 'best pizza') 
and finds the most similar review from stored embeddings using cosine similarity.
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

def get_chroma_collection(persist_dir: str = "./chroma_reviews_db"):
    """Loads the persisted Chroma collection containing restaurant reviews."""
    client = chromadb.PersistentClient(path=persist_dir)
    embed_fn = embedding_functions.DefaultEmbeddingFunction()
    return client.get_collection(name="restaurant_reviews", embedding_function=embed_fn)

def find_most_similar_review(query: str, persist_dir: str = "./chroma_reviews_db", top_k: int = 1) -> dict:
    """
    Takes a user search query and returns the most similar review based on cosine similarity.
    """
    collection = get_chroma_collection(persist_dir)
    
    # Query collection using Chroma vector search
    # In Chroma, distance is cosine distance; similarity = 1 - distance
    results = collection.query(
        query_texts=[query],
        n_results=top_k,
        include=["documents", "metadatas", "distances"]
    )
    
    doc = results["documents"][0][0]
    meta = results["metadatas"][0][0]
    distance = results["distances"][0][0]
    # Convert cosine distance to cosine similarity percentage
    cosine_similarity = max(0.0, 1.0 - distance)
    
    return {
        "query": query,
        "restaurant": meta["restaurant"],
        "cuisine": meta["cuisine"],
        "review_text": doc,
        "cosine_distance": round(distance, 4),
        "cosine_similarity_score": round(cosine_similarity, 4)
    }

def search_and_display(query: str, db_path: str):
    print(f"\nUser Query: \"{query}\"")
    print("-" * 65)
    result = find_most_similar_review(query, persist_dir=db_path, top_k=1)
    
    print(f"[Top Match Found]")
    print(f"  Restaurant : {result['restaurant']}")
    print(f"  Cuisine    : {result['cuisine']}")
    print(f"  Cosine Sim : {result['cosine_similarity_score']} (Distance: {result['cosine_distance']})")
    print(f"  Review     : \"{result['review_text']}\"")
    print("-" * 65)
    return result

def main():
    print("=" * 65)
    print("   SESSION 5 - TASK 2: COSINE SIMILARITY REVIEW SEARCH")
    print("=" * 65)
    
    db_path = os.path.join(os.path.dirname(__file__), "chroma_reviews_db")
    
    # If DB does not exist yet, initialize it
    if not os.path.exists(db_path):
        from task1_chroma_store_reviews import initialize_and_populate_chroma
        initialize_and_populate_chroma(persist_dir=db_path)

    test_queries = [
        "best pizza",
        "rich coffee and sweet desserts",
        "spicy noodles and dumplings",
        "authentic buttery dal makhani"
    ]
    
    for q in test_queries:
        search_and_display(q, db_path)

if __name__ == "__main__":
    main()
