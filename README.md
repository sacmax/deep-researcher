# DeepResearcher

A LangGraph-based research agent that decomposes complex questions into parallel research branches, fact-checks claims across sources, and synthesizes a calibrated answer with confidence scoring.

## How it works

1. **Planner** — decomposes your question into focused sub-questions
2. **Researchers** — run in parallel, each searching and extracting claims from real web sources
3. **Fact Checker** — cross-compares claims across branches to surface contradictions
4. **Synthesizer** — combines everything into a calibrated answer with confidence score and knowledge gaps

## Setup

```bash
git clone https://github.com/YOUR_USERNAME/deep-researcher
cd deep-researcher

uv venv
uv pip install -e .

cp .env.example .env
# add your OPENAI_API_KEY to .env
```

## Usage

```bash
deep-researcher "What are the best optimization techniques for training large neural networks?"
```

```
Question: What are the best optimization techniques for training large neural networks?

Answer:
The best optimization techniques for training large neural networks involve a combination
of effective optimization algorithms, learning rate management, normalization techniques,
and hardware acceleration strategies.

 1 Optimization Algorithms: Common algorithms include Stochastic Gradient Descent (SGD)
   and AdamW, which are widely used to minimize loss and enhance model performance.

 2 Learning Rate Management: Learning rate annealing is important. Initiating training
   with a higher learning rate can enable rapid progress, but it should be gradually
   decreased to ensure precise convergence.

 3 Batch Normalization: This technique reduces internal covariate shift by normalizing
   the outputs of each layer, which helps stabilize training.

 4 Hardware Acceleration: Utilizing GPUs and TPUs dramatically speeds up the training
   process due to their parallel processing capabilities.

Confidence: 0.85

Knowledge Gaps:
  • The effectiveness of lesser-known optimization algorithms compared to AdamW or SGD.
  • Optimal strategies for tuning learning rates across different model types.
  • The impact of alternative normalization techniques like Layer Normalization.
```

## Configuration

All settings can be overridden via environment variables:

| Variable | Default | Description |
|---|---|---|
| `OPENAI_API_KEY` | — | Required |
| `SEARCH_PROVIDER` | `duckduckgo` | Use `tavily` for better results |
| `TAVILY_API_KEY` | — | Required if using Tavily |
| `LLM_MODEL` | `gpt-4o-mini` | Any LiteLLM-supported model |
| `MAX_SUB_QUESTIONS` | `5` | Number of parallel research branches |

## Stack

- [LangGraph](https://github.com/langchain-ai/langgraph) — graph execution and checkpointing
- [LiteLLM](https://github.com/BerriAI/litellm) — model-agnostic LLM calls
- [DuckDuckGo Search](https://github.com/deedy5/ddgs) — free web search
- [Trafilatura](https://github.com/adbar/trafilatura) — web page content extraction
- [Pydantic](https://docs.pydantic.dev/) — data validation and structured outputs
