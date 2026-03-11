from pydantic import BaseModel, Field
from deep_researcher.models.research import SubQuestion
from deep_researcher.config import settings
import litellm
import asyncio

class SubQuestionList(BaseModel):
    sub_questions: list[SubQuestion]

SYSTEM_PROMPT = f"You are a helpful research assistant. Break the given question into {settings.MAX_SUB_QUESTIONS} sub-questions. Each sub-question must have an id, question, rationale, and priority (1-10)." 

class PlannerAgent:
    def __init__(self, llm_client=None):
        self._llm_client = llm_client

    async def run(self, state: dict) -> dict:
        try:

            if self._llm_client is not None:
                return await self._llm_client.plan(state)
            else:
                response  = await litellm.acompletion(
                    model=settings.LLM_MODEL,
                    messages=[{"role":"system", "content":SYSTEM_PROMPT},
                            {"role": "user", "content":state["question"]}],
                    response_format=SubQuestionList
                )
                result = response.choices[0].message.content
            return {"sub_questions": result.sub_questions}
        except Exception:
            return {"sub_questions": [SubQuestion(id="1", question=state["question"], rationale="fallback", priority=5)]}
