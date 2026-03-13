from deep_researcher.graph.builder import build_graph
import click
import asyncio
from rich.console import Console
from rich.markdown import Markdown
import uuid
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver
from deep_researcher.config import settings



async def run_graph(question: str):
    async with AsyncSqliteSaver.from_conn_string(settings.DB_PATH) as checkpointer:
        graph = build_graph(checkpointer=checkpointer)
        result = await graph.ainvoke(
            {"question": question, "session_id": str(uuid.uuid4())},
            config={"configurable": {"thread_id": str(uuid.uuid4())}}
        )
        print_report(result["report"])

def print_report(report):
    console = Console()
    console.print(f"\n[bold cyan]Question:[/bold cyan] {report.question}\n")
    # console.print(f"[bold green]Answer:[/bold green]\n{report.answer}\n")
    console.print("[bold green]Answer:[/bold green]")
    console.print(Markdown(report.answer))
    console.print(f"[bold yellow]Confidence:[/bold yellow] {report.confidence}")
    if report.knowledge_gaps:
        console.print(f"\n[bold red]Knowledge Gaps:[/bold red]")
        for gap in report.knowledge_gaps:
            console.print(f"  • {gap}")
    if report.contradictions:
        console.print(f"\n[bold red]Contradictions:[/bold red]")
        for c in report.contradictions:
            console.print(f"  • {c.explanation} (severity: {c.severity})")

@click.command()
@click.argument("question")
def main(question):
    asyncio.run(run_graph(question))

if __name__ == "__main__":
    main()