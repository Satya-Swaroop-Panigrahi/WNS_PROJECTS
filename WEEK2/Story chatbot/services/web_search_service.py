import requests
import logging
from typing import List, Dict
from config import Config
from .content_filter import ContentFilter

logger = logging.getLogger(__name__)

class WebSearchService:
    def __init__(self):
        self.api_key = Config.SERPAPI_KEY
        self.content_filter = ContentFilter()
        
    def search(self, query: str, num_results: int = 10) -> List[Dict[str, str]]:
        """Perform web search using SerpAPI"""
        
        # Additional safety check for search queries
        if not self.content_filter.is_safe_search(query):
            raise ValueError("Search query violates safety guidelines")
        
        if not self.api_key:
            logger.warning("SerpAPI key not configured. Using mock results.")
            return self._get_mock_results(query, num_results)
        
        try:
            params = {
                'q': query,
                'api_key': self.api_key,
                'num': num_results,
                'safe': 'active',  # Enable safe search
                'gl': 'us',  # Country
                'hl': 'en'   # Language
            }
            
            response = requests.get('https://serpapi.com/search', params=params)
            response.raise_for_status()
            
            data = response.json()
            results = []
            
            # Extract organic results
            organic_results = data.get('organic_results', [])
            
            for result in organic_results:
                # Additional content filtering for search results
                title = result.get('title', '')
                snippet = result.get('snippet', '')
                
                if self.content_filter.is_safe(f"{title} {snippet}"):
                    results.append({
                        'title': title,
                        'snippet': snippet,
                        'url': result.get('link', ''),
                        'source': result.get('source', '')
                    })
            
            # Filter out any results that don't meet safety standards
            filtered_results = [r for r in results if self.content_filter.is_safe(r['snippet'])]
            
            return filtered_results[:num_results]
            
        except requests.RequestException as e:
            logger.error(f"Search API error: {str(e)}")
            return self._get_mock_results(query, num_results)
        except Exception as e:
            logger.error(f"Search error: {str(e)}")
            return self._get_mock_results(query, num_results)
    
    def _get_mock_results(self, query: str, num_results: int) -> List[Dict[str, str]]:
        """Return mock search results when API is unavailable"""
        mock_results = [
            {
                'title': f'Mock Result for: {query}',
                'snippet': f'This is a mock search result for "{query}". The search functionality requires a valid SerpAPI key to work properly.',
                'url': 'https://example.com/mock-result',
                'source': 'Mock Search Service'
            }
        ]
        
        # Repeat mock results to fill the requested number
        return (mock_results * ((num_results // len(mock_results)) + 1))[:num_results]
    
    def search_news(self, query: str, num_results: int = 5) -> List[Dict[str, str]]:
        """Search for news articles"""
        return self.search(f"{query} news", num_results)
    
    def search_educational(self, query: str, num_results: int = 5) -> List[Dict[str, str]]:
        """Search for educational content"""
        return self.search(f"{query} tutorial guide how to", num_results)
