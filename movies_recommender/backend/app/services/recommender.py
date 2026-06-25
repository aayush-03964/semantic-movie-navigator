import chromadb
from chromadb.utils import embedding_functions

class RecommenderService:
    """Manages the local ChromaDB vector database and text embedding generation."""
    
    def __init__(self):
        # 1. Initialize a persistent database client stored on your local disk
        self.chroma_client = chromadb.PersistentClient(path="./chroma_db")
        
        # 2. Define the AI model we want to use to convert text to vectors.
        # 'all-MiniLM-L6-v2' is highly efficient and runs perfectly locally.
        self.embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="all-MiniLM-L6-v2"
        )
        
        # 3. Create or fetch a 'Collection' (similar to a table in a standard database)
        self.collection = self.chroma_client.get_or_create_collection(
            name="movies_collection",
            embedding_function=self.embedding_function,
            metadata={"hnsw:space": "cosine"} # Use cosine similarity for distance scoring
        )

    async def seed_movies(self, movies_list: list):
        """Takes raw popular movies from TMDB, extracts overviews, and saves them to ChromaDB."""
        ids = []
        documents = []
        metadatas = []
        
        for movie in movies_list:
            if not movie.get("overview"):
                continue
                
            ids.append(str(movie["id"]))
            documents.append(movie["overview"]) # The text description the AI reads and encodes
            metadatas.append({
                "title": movie.get("title", "Unknown"),
                "poster_path": movie.get("poster_path", ""),
                "vote_average": float(movie.get("vote_average", 0.0))
            })
            
        # Add the documents to ChromaDB. 
        if ids:
            self.collection.upsert(
                ids=ids,
                documents=documents,
                metadatas=metadatas
            )

    async def search_similar_movies(self, query: str, limit: int = 5) -> list:
        """Converts a user text query into a vector and finds the top matching movies."""
        results = self.collection.query(
            query_texts=[query],
            n_results=limit
        )
        return results

# Instantiate a single instance to use throughout the application
recommender_service = RecommenderService()