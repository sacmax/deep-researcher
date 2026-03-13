import pytest
from deep_researcher.agents.fact_checker import FactCheckerAgent
from deep_researcher.models.research import BranchResult, Claim, Source


class MockLLMClient:
    async def fact_check(self, state: dict) -> dict:
        return {"contradictions": []}


def make_branch_result(sub_question_id: str) -> BranchResult:
    return BranchResult(
        sub_question_id=sub_question_id,
        claims=[
            Claim(text="test claim", source_url="http://test.com", confidence=0.9, sub_question_id=sub_question_id),
            Claim(text="another claim", source_url="http://test2.com", confidence=0.8, sub_question_id=sub_question_id),
        ],
        search_queries_used=["test query"],
        sources=[Source(url="http://test.com", title="test", snippet="test")]
    )


async def test_fact_checker_with_mock():
    fact_checker = FactCheckerAgent(llm_client=MockLLMClient())
    state = {
        "branch_results": [
            make_branch_result("1"),
            make_branch_result("2"),
        ]
    }
    result = await fact_checker.run(state)

    assert "contradictions" in result
    assert isinstance(result["contradictions"], list)


async def test_fact_checker_fallback():
    class FailingLLMClient:
        async def fact_check(self, state: dict) -> dict:
            raise Exception("LLM failed")

    fact_checker = FactCheckerAgent(llm_client=FailingLLMClient())
    state = {
        "branch_results": [
            make_branch_result("1"),
            make_branch_result("2"),
        ]
    }
    result = await fact_checker.run(state)

    assert "contradictions" in result
    assert result["contradictions"] == []
