import pytest
from deep_researcher.agents.planner import PlannerAgent
from deep_researcher.models.research import SubQuestion

class MockLLMClient:
    async def plan(self, state: dict) -> dict:
        return {"sub_questions": [
            SubQuestion(id="1", question="test?", rationale="test", priority=5)
        ]}

async def test_planner_with_mock():
    planner = PlannerAgent(llm_client=MockLLMClient())
    result = await planner.run({"question": "test question"})
    
    assert "sub_questions" in result
    assert len(result["sub_questions"]) == 1
    assert result["sub_questions"][0].question == "test?"

async def test_planner_fallback():
    class FailingLLMClient:
        async def plan(self, state: dict) -> dict:
            raise Exception("LLM failed")
    
    planner = PlannerAgent(llm_client=FailingLLMClient())
    result = await planner.run({"question": "test question"})

    assert "sub_questions" in result
    assert len(result["sub_questions"]) == 1
    assert result["sub_questions"][0].question == "test question"
    assert result["sub_questions"][0].rationale == "fallback"