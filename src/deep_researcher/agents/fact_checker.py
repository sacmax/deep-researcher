from pydantic import BaseModel
from deep_researcher.models.research import Contradiction
from deep_researcher.config import settings
import itertools
import litellm


class ContradictionResult(BaseModel):
    is_contradiction: bool
    contradiction: Contradiction | None

class FactCheckerAgent:
    def __init__(self, llm_client=None):
        self._llm_client = llm_client
    
    async def run(self, state: dict) -> dict:
        self._branch_results = state["branch_results"]
        all_branch_pairs = itertools.combinations(self._branch_results, 2)
        contradictions = []
        try:
             
            if self._llm_client is not None:
                        return await self._llm_client.fact_check(state)
            else:
                SYSTEM_PROMPT = """You are a research fact-checker.
                                        Compare two claims and determine if they contradict each other.
                                        A contradiction means the claims make opposing or incompatible assertions.
                                        If they contradict, assess the severity as low, medium, or high."""
                for br1, br2 in all_branch_pairs:
                    top_claims_br1 = sorted(br1.claims, key=lambda c: c.confidence, reverse=True)[:2]
                    top_claims_br2 = sorted(br2.claims, key=lambda c: c.confidence, reverse=True)[:2]
                    for claim_br1, claim_br2 in itertools.product(top_claims_br1,top_claims_br2):
                        
                        USER_PROMPT = f"Claim A: {claim_br1.text}\n\nClaim B: {claim_br2.text}"
                    
                        response  = await litellm.acompletion(
                                    model=settings.LLM_MODEL,
                                    messages=[{"role":"system", "content":SYSTEM_PROMPT}, {"role":"user", "content":USER_PROMPT}],
                                    response_format=ContradictionResult
                                )
                        
                        contradiction_results = response.choices[0].message.content
                        if contradiction_results.is_contradiction:
                            contradictions.append(contradiction_results.contradiction)

            return {"contradictions": contradictions}
        except Exception:
             return {"contradictions": []}
            


