---
name: rag-eval-observability
description: Evaluate and observe RAG pipelines — faithfulness, answer relevance, context precision/recall with Ragas, TruLens, and LangSmith tracing. Use when the user needs to measure RAG quality, debug retrieval failures, or add observability to LLM applications. Triggers on: rag evaluation, ragas, trulens, langsmith, faithfulness, context precision, context recall, answer relevance, rag observability, llm evaluation, retrieval evaluation, rag tracing.
---

# RAG Evaluation & Observability

Measure, debug, and observe RAG pipeline quality. Covers automated evaluation metrics (Ragas), tracing (LangSmith/TruLens), retrieval debugging, and production observability for LLM applications grounded in document retrieval.

## When to trigger

- User wants to measure RAG quality (is the answer grounded? are retrieved chunks relevant?)
- User needs to debug why a RAG system gave a wrong or hallucinated answer
- User wants tracing/observability on LLM application traces
- User is evaluating chunking, embedding, or retrieval strategy changes

## Evaluation metrics (Ragas)

Install: `pip install ragas`

| Metric | What it measures | Scale |
|---|---|---|
| Faithfulness | Is the answer supported by retrieved context? | 0–1 |
| Answer Relevance | Does the answer address the question? | 0–1 |
| Context Precision | Are retrieved chunks relevant to the question? | 0–1 |
| Context Recall | Were all needed chunks retrieved? | 0–1 |

### Ragas evaluation example

```python
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy, context_precision, context_recall
from datasets import Dataset

eval_data = Dataset.from_list([
    {
        "question": "What is the refund policy?",
        "answer": "You can request a refund within 30 days of purchase.",
        "contexts": ["Customers may request refunds within 30 days of the original purchase date."],
        "ground_truth": "Refunds are available within 30 days."
    }
])

result = evaluate(
    eval_data,
    metrics=[faithfulness, answer_relevancy, context_precision, context_recall]
)
print(result.to_pandas())
```

## Tracing with LangSmith

Install: `pip install langsmith`

```bash
export LANGCHAIN_TRACING_V2=true
export LANGCHAIN_API_KEY="ls__..."
export LANGCHAIN_PROJECT="rag-eval"
```

```python
from langsmith import Client
from langchain.callbacks.tracers.langsmith import LangSmithTracer

client = Client()
tracer = LangSmithTracer(project_name="rag-eval")

# Traces are automatically captured when using LangChain components
# View traces at https://smith.langchain.com
```

### What to trace

- Retrieval: which chunks were fetched, similarity scores, latency
- Generation: prompt, model, tokens, response, latency
- Full chain: end-to-end RAG latency, success/failure

## TruLens evaluation

Install: `pip install trulens`

```python
from trulens.core import Tru
from trulens.providers.langchain import Langchain

tru = Tru()
provider = Langchain()

# Wrap your RAG chain
from trulens.core import TruChain

tru_rag = TruChain(rag_chain, app_name="RAG Pipeline")

with tru_rag as recording:
    response = rag_chain.invoke("What is the refund policy?")

# View dashboard
tru.get_dashboard_url()
```

## Retrieval debugging

When answers are wrong, diagnose at each stage:

1. **Query** — Was the question clear and specific?
2. **Retrieval** — Were relevant chunks retrieved? Check similarity scores.
3. **Context** — Was enough context provided? Too much noise?
4. **Generation** — Did the model hallucinate or ignore context?

Debug queries:
```python
# Inspect raw retrieval results
docs = vectorstore.similarity_search_with_score("query", k=10)
for doc, score in docs:
    print(f"Score: {score:.3f} | {doc.page_content[:100]}")
```

## Production observability

Key metrics to monitor:

- Retrieval latency (p50, p95, p99)
- Generation latency (time to first token, total)
- Token usage per request (prompt + completion)
- Failure rate (empty retrieval, model errors, timeouts)
- User feedback (thumbs up/down, corrections)

## Decision checklist

- [ ] Evaluation dataset created (questions + answers + contexts + ground truths)
- [ ] Ragas metrics configured (faithfulness, relevance, precision, recall)
- [ ] LangSmith or TruLens tracing enabled
- [ ] Retrieval scores logged for debugging
- [ ] Production metrics defined (latency, tokens, failure rate)
- [ ] Evaluation cadence established (per deploy, weekly, on demand)

## Related Workshop skills

- `rag-pipeline-builder` — build the RAG pipeline being evaluated
- `ollama-local-ai` — local LLMs for fully offline RAG evaluation
- `observability-and-instrumentation` — broader application observability
- `mcp-builder` — expose evaluation results as MCP tools
