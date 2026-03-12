from deep_researcher.agents.planner import PlannerAgent
from deep_researcher.agents.researcher import ResearcherAgent
from deep_researcher.agents.fact_checker import FactCheckerAgent
from deep_researcher.agents.synthesizer import SynthesizerAgent
from deep_researcher.graph.state import DeepResearcherState

planner = PlannerAgent()
researcher = ResearcherAgent()
factchecker = FactCheckerAgent()
synthesizer = SynthesizerAgent()

async def planner_node(state: DeepResearcherState) -> dict:
    return await planner.run(state)

async def researcher_node(state: DeepResearcherState) -> dict:
    return await researcher.run(state)

async def factchecker_node(state: DeepResearcherState) -> dict:
    return await factchecker.run(state)

async def synthesizer_node(state: DeepResearcherState) -> dict:
    return await synthesizer.run(state)