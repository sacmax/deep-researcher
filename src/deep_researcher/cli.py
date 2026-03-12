from deep_researcher.graph.builder import build_graph
import click
import asyncio
from rich.console import Console
import uuid

async def run_graph(question: str):
    graph = build_graph()
    result = await graph.ainvoke({"question": question, "session_id": str(uuid.uuid4())})
    report = result["report"]
    print_report(report)

def print_report(report: dict):
    console = Console()
    console.print(f"[bold]Answer:[/bold] {report.answer}")
    console.print(f"[bold]Confidence:[/bold] {report.confidence}")

@click.command()
@click.argument("question")
def main(question):
    asyncio.run(run_graph(question))

if __name__ == "__main__":
    main()