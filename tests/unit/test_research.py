from deep_researcher.models.research import Source, Claim, SubQuestion, BranchResult, Contradiction
from pydantic import ValidationError
import pytest

# Source tests
def test_valid_source():
    source = Source(url="http://test.com", title="test", snippet="test" )
    assert source.url == "http://test.com"
    assert source.title == "test"
    assert source.snippet == "test"

def test_invalid_source():
    with pytest.raises(ValidationError):
        Source(url=123, title=None, snippet="test")

# Claim tests
def test_valid_claim():
    claim = Claim(text="test", source_url="http://test.com", confidence=0.5, sub_question_id="1")
    assert claim.text == "test"
    assert claim.source_url == "http://test.com"
    assert claim.confidence == 0.5
    assert claim.sub_question_id == "1"

def test_confidence_below_zero():
    with pytest.raises(ValidationError):
        Claim(text="test", source_url="http://test.com", confidence=-0.5, sub_question_id="1")

def test_confidence_above_one():
    with pytest.raises(ValidationError):
        Claim(text="test", source_url="http://test.com", confidence=1.5, sub_question_id="1")


# Sub-question tests
def test_valid_sub_question():
    sq = SubQuestion(id="1", question="test?", rationale="test", priority=5)
    assert sq.id == "1"
    assert sq.priority == 5

def test_priority_above_ten():
     with pytest.raises(ValidationError):
         SubQuestion(id="1", question="test?", rationale="test", priority=11)

def test_priority_below_one():
     with pytest.raises(ValidationError):
         SubQuestion(id="1", question="test?", rationale="test", priority=0)

# Branch Result tests
def test_valid_branch_result():
    source = Source(url="http://test.com", title="test", snippet="test")
    claim = Claim(text="test", source_url="http://test.com", confidence=0.5, sub_question_id="1")
    br = BranchResult(sub_question_id="1", claims=[claim], search_queries_used=["test query"], sources=[source])
    assert br.sub_question_id == "1"
    assert len(br.claims) == 1
    assert len(br.sources) == 1

# Contradiction tests
def test_valid_contradiction():
    claim_a = Claim(text="A", source_url="http://a.com", confidence=0.9, sub_question_id="1")
    claim_b = Claim(text="B", source_url="http://b.com", confidence=0.8, sub_question_id="2")
    c = Contradiction(claim_a=claim_a, claim_b=claim_b, explanation="they contradict", severity="high")
    assert c.severity == "high"

def test_invalid_severity():
      claim_a = Claim(text="A", source_url="http://a.com", confidence=0.9, sub_question_id="1")
      claim_b = Claim(text="B", source_url="http://b.com", confidence=0.8, sub_question_id="2")
      with pytest.raises(ValidationError):
          Contradiction(claim_a=claim_a, claim_b=claim_b, explanation="they conflict", severity="critical")