import httpx
from app.config import settings

class TMDBService:
    """Handles all communication with the external TMDB API."""
    
    def __init__(self):
        self.base_url = "https://api.themoviedb.org/3"
        # Set up bearer token authorization headers using our config settings
        self.headers = {
            "Authorization": f"Bearer {settings.TMDB_API_KEY}",
            "accept": "application/json"
        }

    async def get_popular_movies(self, page: int = 1) -> dict:
        """
        Fetches a list of currently popular movies from TMDB for a specific page.
        Accepts an optional page integer parameter to scale seed collections.
        """
        # Dynamic template literal string embedding the specific page argument
        url = f"{self.base_url}/movie/popular?language=en-US&page={page}"
        
        # Use an async client to keep operations non-blocking
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=self.headers)
            response.raise_for_status() 
            return response.json()

# Instantiate a singleton to be imported in our routes
tmdb_service = TMDBService()