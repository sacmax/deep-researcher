import httpx
from trafilatura import extract
from deep_researcher.config import settings


async def extract_page(url: str) -> str:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
        text = extract(response.text)
        if text:
            result = text[:settings.PAGE_EXTRACT_CHARS]
            return result
        else: 
            return ""
    except Exception as e:
        print(e)
        return ""

