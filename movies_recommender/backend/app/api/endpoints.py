from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
import asyncio
from app.services.tmdb import tmdb_service
from app.services.recommender import recommender_service

router = APIRouter()

# A simple Pydantic schema to validate the incoming search data payload
class SearchRequest(BaseModel):
    query: str
    limit: int = 5

# --- BACKGROUND WORKER TASK ---
async def sync_large_movie_pool(total_pages: int):
    """
    Quietly fetches a massive number of pages from TMDB in the background,
    preventing timeouts while significantly scaling up ChromaDB.
    """
    print(f"--- Starting background sync for {total_pages} pages ---")
    total_seeded = 0
    
    for page in range(1, total_pages + 1):
        try:
            # Reusing your project's tmdb_service
            data = await tmdb_service.get_popular_movies(page=page)
            movies_list = data.get("results", [])
            
            if movies_list:
                # Reusing your project's recommender_service
                await recommender_service.seed_movies(movies_list)
                total_seeded += len(movies_list)
                print(f"[Background Sync] Successfully processed page {page}/{total_pages} (+{len(movies_list)} movies)")
            
            # Pause for 200ms to be a good citizen and respect TMDB rate limits
            await asyncio.sleep(0.2)
            
        except Exception as e:
            print(f"[Background Sync Error] Failed on page {page}: {str(e)}")
            continue
            
    print(f"--- Background movie sync complete! Total seeded in this run: {total_seeded} ---")


# --- ENDPOINTS ---

@router.get("/health", tags=["Health"])
async def health_check():
    """Verifies that the backend API layer is live and responsive."""
    return {"status": "healthy", "message": "Movie Recommender API is operational"}

@router.get("/movies/popular", tags=["Movies"])
async def get_popular_movies():
    """
    Fetches 5 pages of popular movies from TMDB (100 movies total) 
    and systematically seeds them all into ChromaDB.
    """
    try:
        total_seeded = 0
        
        # Sequentially loop through pages 1 to 5 to pull a diverse, robust movie library
        for page in range(1, 6):
            data = await tmdb_service.get_popular_movies(page=page)
            movies_list = data.get("results", [])
            
            if movies_list:
                # Upsert this page's chunk into the local vector space
                await recommender_service.seed_movies(movies_list)
                total_seeded += len(movies_list)
        
        return {
            "status": "success",
            "message": f"Successfully fetched and seeded {total_seeded} movies into ChromaDB!"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch and seed movies: {str(e)}")

@router.get("/movies/seed-vast-pool", tags=["Movies"])
async def seed_vast_pool(background_tasks: BackgroundTasks):
    """
    Triggers a background worker to ingest 50 pages (~1,000 movies) into ChromaDB
    without freezing the server or timing out the client request.
    """
    try:
        # Pass the background worker function to FastAPI's manager
        background_tasks.add_task(sync_large_movie_pool, total_pages=50)
        
        return {
            "status": "processing",
            "message": "Database expansion has started in the background. Check your VS Code terminal to watch it pull pages live!"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start background synchronization: {str(e)}")

@router.post("/movies/recommend", tags=["Recommendations"])
async def recommend_movies(payload: SearchRequest):
    """Accepts a natural language query, vectorizes it, and maps semantic results from ChromaDB."""
    try:
        results = await recommender_service.search_similar_movies(
            query=payload.query, 
            limit=payload.limit
        )
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Semantic lookup failed: {str(e)}")