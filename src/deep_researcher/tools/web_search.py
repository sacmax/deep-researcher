import asyncio
from deep_researcher.models.research import Source
from deep_researcher.config import settings
from duckduckgo_search import DDGS

ddgs = DDGS()

async def web_search(query: str, max_results: int) -> list[Source]:
    try:
        if settings.SEARCH_PROVIDER == "tavily":
            from tavily import TavilyClient
            tavily_client = TavilyClient(api_key=settings.TAVILY_API_KEY)
            response = await asyncio.to_thread(tavily_client.search, query, max_results=max_results)
            return [Source(url=r["url"], title=r["title"], snippet=r["content"]) for r in response]
        elif settings.SEARCH_PROVIDER == "duckduckgo":
            response = await asyncio.to_thread(ddgs.text, query, max_results=max_results)
            return [Source(url=r["href"], title=r["title"], snippet=r["body"]) for r in response]
        else:
            raise ValueError(f"Invalid search provider: {settings.SEARCH_PROVIDER}")
    except Exception:
        return []




