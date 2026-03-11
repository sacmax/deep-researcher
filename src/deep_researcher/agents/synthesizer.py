from pydantic import BaseModel
import litellm
from deep_researcher.config import settings
from deep_researcher.models.research import ResearchReport
from datetime import datetime


class SynthesisResult(BaseModel):
    answer: str
    knowledge_gaps: list[str]
    overall_confidence: float

class SynthesizerAgent:
    def __init__(self, llm_client=None):
        self._llm_client = llm_client
    
    async def run(self, state: dict) -> dict:
        question = state["question"]
        claims = [claim for br in state["branch_results"] for claim in br.claims]
        contradictions = state["contradictions"]
        sources = [source for br in state["branch_results"] for source in br.sources]

        try:
            if self._llm_client is not None:
                        return await self._llm_client.synthesize(state)
            else:
                SYSTEM_PROMPT = """You are a research synthesizer. You have a question and multiple claims, contradictions and sources, your task is to produce a cohesive answer for the question, identify knowledge gaps and overall confidence score for the answer ."""
                USER_PROMPT = f"Question: {question}\n\nClaims: {claims}\n\nContradictions: {contradictions}\n\nSources: {sources}"
                response = await litellm.acompletion(
                    model=settings.LLM_MODEL,
                    messages=[{"role": "system", "content": SYSTEM_PROMPT},{"role": "user", "content": USER_PROMPT}],
                    response_format=SynthesisResult
                )
                sythesis_results = response.choices[0].message.content
                return {"report": ResearchReport(question=question, answer=sythesis_results.answer, claims=claims, contradictions=contradictions, knowledge_gaps=sythesis_results.knowledge_gaps, confidence=sythesis_results.overall_confidence, sources=sources, generated_at=datetime.now())}
        except Exception:
             return {"report": ResearchReport(question=question, answer="", claims=[], contradictions=[], knowledge_gaps=[], confidence=0.0, sources=[], generated_at=datetime.now())}
             