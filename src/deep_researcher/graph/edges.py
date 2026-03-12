from langgraph.types import Send
from deep_researcher.graph.state import DeepResearcherState

def fan_out(state: DeepResearcherState) -> list[Send]:
    sub_questions = state['sub_questions']
    return [Send("researcher", {"sub_question": sq}) for sq in sub_questions]

