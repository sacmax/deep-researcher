import pytest
from unittest.mock import patch, AsyncMock
from deep_researcher.agents.researcher import ResearcherAgent
from deep_researcher.models.research import BranchResult, Claim, Source, SubQuestion

class MockLLMClient:
      async def research(self, state: dict) -> dict:
          return {"branch_results": [
              BranchResult(
                  sub_question_id="1",
                  claims=[Claim(text="test claim", source_url="http://test.com", confidence=0.9, sub_question_id="1")],
                  search_queries_used=["test query"],
                  sources=[Source(url="http://test.com", title="test", snippet="test")]
              )
          ]}

@patch("deep_researcher.agents.researcher.web_search", new_callable=AsyncMock)
@patch("deep_researcher.agents.researcher.extract_page", new_callable=AsyncMock)
async def test_researcher_with_mock(mock_extract, mock_search):
    mock_search.return_value = [
        Source(url="http://test.com", title="test", snippet="test")
    ]
    mock_extract.return_value = "extracted page text"

    researcher = ResearcherAgent(llm_client=MockLLMClient())
    state = {"sub_question": SubQuestion(id="1", question="test?", rationale="test", priority=5)}
    result = await researcher.run(state)

    assert "branch_results" in result
    assert len(result["branch_results"]) == 1
    assert result["branch_results"][0].sub_question_id == "1"


@patch("deep_researcher.agents.researcher.web_search", new_callable=AsyncMock)
@patch("deep_researcher.agents.researcher.extract_page", new_callable=AsyncMock)
async def test_researcher_fallback(mock_extract, mock_search):
    mock_search.side_effect = Exception("search failed")

    researcher = ResearcherAgent()
    state = {"sub_question": SubQuestion(id="1", question="test?", rationale="test", priority=5)}
    result = await researcher.run(state)

    assert "branch_results" in result
    assert len(result["branch_results"]) == 1
    assert result["branch_results"][0].claims == []
    assert result["branch_results"][0].sources == []