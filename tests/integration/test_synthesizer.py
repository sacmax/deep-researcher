import pytest
from datetime import datetime
from deep_researcher.agents.synthesizer import SynthesizerAgent
from deep_researcher.models.research import BranchResult, Claim, Source, ResearchReport


class MockLLMClient:
    async def synthesize(self, state: dict) -> dict:
        return {
            "report": ResearchReport(
                question=state["question"],
                answer="test answer",
                claims=[claim for br in state["branch_results"] for claim in br.claims],
                contradictions=state["contradictions"],
                knowledge_gaps=["test gap"],
                confidence=0.9,
                sources=[source for br in state["branch_results"] for source in br.sources],
                generated_at=datetime.now(),
            )
        }


def make_branch_result(sub_question_id: str) -> BranchResult:
    return BranchResult(
        sub_question_id=sub_question_id,
        claims=[
            Claim(text="test claim", source_url="http://test.com", confidence=0.9, sub_question_id=sub_question_id),
            Claim(text="another claim", source_url="http://test2.com", confidence=0.8, sub_question_id=sub_question_id),
        ],
        search_queries_used=["test query"],
        sources=[Source(url="http://test.com", title="test", snippet="test")],
    )


async def test_synthesizer_with_mock():
    synthesizer = SynthesizerAgent(llm_client=MockLLMClient())
    state = {
        "question": "test question",
        "branch_results": [make_branch_result("1"), make_branch_result("2")],
        "contradictions": [],
    }
    result = await synthesizer.run(state)

    assert "report" in result
    report = result["report"]
    assert isinstance(report, ResearchReport)
    assert report.question == state["question"]
    assert report.answer == "test answer"
    assert report.confidence == 0.9
    assert len(report.claims) == 4   # 2 branches × 2 claims each
    assert len(report.knowledge_gaps) == 1


async def test_synthesizer_fallback():
    class FailingLLMClient:
        async def synthesize(self, state: dict) -> dict:
            raise Exception("LLM failed")

    synthesizer = SynthesizerAgent(llm_client=FailingLLMClient())
    state = {
        "question": "test question",
        "branch_results": [make_branch_result("1")],
        "contradictions": [],
    }
    result = await synthesizer.run(state)

    assert "report" in result
    report = result["report"]
    assert isinstance(report, ResearchReport)
    assert report.answer == ""
    assert report.confidence == 0.0
    assert report.claims == []
    assert report.knowledge_gaps == []