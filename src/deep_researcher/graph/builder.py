from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver
from langgraph.graph import StateGraph, START, END
from deep_researcher.graph.state import DeepResearcherState
from deep_researcher.graph.nodes import planner_node, researcher_node, factchecker_node, synthesizer_node
from deep_researcher.graph.edges import fan_out
from deep_researcher.config import settings

def build_graph()
    graph = StateGraph(DeepResearcherState)
    # add nodes
    graph.add_node("planner", planner_node)
    graph.add_node("researcher", researcher_node)
    graph.add_node("factchecker", factchecker_node)
    graph.add_node("synthesizer", synthesizer_node)

    # add edges
    graph.add_edge(START, "planner")
    graph.add_conditional_edges("planner", fan_out, ["researcher"])
    graph.add_edge("researcher", "factchecker")
    graph.add_edge("factchecker", "synthesizer")
    graph.add_edge("synthesizer", END)

    checkpointer = AsyncSqliteSaver.from_conn_string(settings.DB_PATH)
    return graph.compile(checkpointer=checkpointer)

