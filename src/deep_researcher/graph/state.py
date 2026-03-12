from typing import TypedDict, Annotated
import operator
from deep_researcher.models.research import SubQuestion, BranchResult, Contradiction, ResearchReport

class DeepResearcherState(TypedDict):
    question: str
    sub_questions: list[SubQuestion] 
    branch_results: Annotated[list[BranchResult], operator.add]
    contradictions: list[Contradiction]
    report: ResearchReport | None
    errors: Annotated[list[str], operator.add]
    session_id: str
