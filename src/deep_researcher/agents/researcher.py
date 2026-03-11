import asyncio
from deep_researcher.config import settings
from deep_researcher.models.research import SubQuestion, BranchResult, Claim
from deep_researcher.tools.web_search import web_search
from deep_researcher.tools.page_extractor import extract_page
from pydantic import BaseModel, Field
import litellm

class ClaimsList(BaseModel):
    claims_list: list[Claim]

class ResearcherAgent:
    def __init__(self, llm_client=None):
        self._llm_client = llm_client

    
    async def run(self, state: dict) -> dict:
        max_results = settings.MAX_SEARCH_RESULTS
        sub_question_id = state["sub_question"].id
        sub_question = state["sub_question"].question

        try:

            web_result = await web_search(sub_question, max_results=max_results)
            urls = [ws.url for ws in web_result]
            results = await asyncio.gather(*[extract_page(url) for url in urls[:3]],
                return_exceptions=True
                )
            texts = [r for r in results if isinstance(r, str)]
            
            SYSTEM_PROMPT = f"You are a helpful research assistant. Extract all factual claims from this text that are relevant to the sub-question. Every claims must have text, source_url, confidence ans sub_question_id. Show how confident you are of the claims by providing a confidence score between 0.0 - 1.0 \n {texts}" 

            
            if self._llm_client is not None:
                return await self._llm_client.research(state)
            else:
                response  = await litellm.acompletion(
                            model=settings.LLM_MODEL,
                            messages=[{"role":"system", "content":SYSTEM_PROMPT},
                                    {"role": "user", "content":state["sub_question"].question}],
                            response_format=ClaimsList
                        )
                claim_results = response.choices[0].message.content
                return {"branch_results": [BranchResult(sub_question_id=sub_question_id, claims=claim_results.claims_list, search_queries_used=[sub_question], sources=web_result)]}
        except Exception:
            return {"branch_results": [BranchResult(sub_question_id="", claims=[], search_queries_used=[], sources=[])]}