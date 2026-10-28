---
name: rag-pipeline-builder
description: Build RAG (Retrieval-Augmented Generation) pipelines — document loading, chunking strategies, embedding models, vector store selection (Chroma, Pinecone, Qdrant, Weaviate, pgvector), retrieval methods, reranking, and evaluation. Use when the user wants to ground an LLM in their own documents, build a knowledge base, or create a semantic search system. Triggers on: RAG, retrieval augmented generation, vector database, semantic search, chunking, embedding, knowledge base, document QA, cite sources, ground LLM, pgvector, Chroma, Pinecone, Qdrant, Weaviate, rerank.
---

# RAG Pipeline Builder

Design and implement Retrieval-Augmented Generation systems that ground LLMs in private documents. Covers the full pipeline: ingestion → chunking → embedding → storage → retrieval → generation → evaluation.

## When to trigger

- User wants to chat with their own documents/PDFs/knowledge base
- User mentions RAG, vector database, semantic search, or document QA
- User needs to ground an LLM in specific source material with citations
- User is building a retrieval system and needs chunking/embedding/retrieval guidance

## Pipeline stages

### Stage 1: Document loading

Load content from files, URLs, or APIs. Common loaders:
- PDF: `pypdf`, `PyMuPDF`, `pdfplumber`
- Markdown/HTML: `BeautifulSoup`, `langchain document loaders`
- Text/CSV/JSON: standard file readers
- Web: `crawl4ai`, `firecrawl`, `just-scrape`

### Stage 2: Chunking

Split documents into retrieval-optimized chunks. Strategies:

| Strategy | Best for | Chunk size | Overlap |
|---|---|---|---|
| Fixed-size | Uniform docs | 512–1000 tokens | 50–100 |
| Recursive | Markdown/code (respects structure) | 500–1000 | 50–100 |
| Semantic | Narrative text (splits by meaning) | variable | adaptive |
| Parent-child | Small retrieval + large context | child 400, parent 2000 | n/a |

**Key rule:** Keep chunks small enough for precise retrieval, large enough to retain context. Overlap prevents cutting sentences across boundaries.

Example (recursive character):
```python
from langchain_text_splitters import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    separators=["\n\n", "\n", ".", " ", ""]
)
chunks = splitter.split_documents(docs)
```

### Stage 3: Embedding

Convert text chunks to vectors. Options:

| Model | Dimensions | Local? | Best for |
|---|---|---|---|
| `nomic-embed-text` (Ollama) | 768 | Yes | General local RAG |
| `mxbai-embed-large` | 1024 | Yes | Multilingual |
| `text-embedding-3-small` (OpenAI) | 1536 | No | Production quality |
| `text-embedding-3-large` (OpenAI) | 3072 | No | Highest accuracy |
| `bge-base-en-v1.5` (HuggingFace) | 768 | Yes | Academic/benchmarks |

### Stage 4: Vector store

Store embeddings for similarity search:

| Store | Local? | Persistent? | Best for |
|---|---|---|---|
| Chroma | Yes | Yes | Prototyping, local-first |
| pgvector (Postgres) | Yes | Yes | Apps already using Postgres |
| Pinecone | No | Yes | Managed production |
| Qdrant | Yes | Yes | Self-hosted, advanced filtering |
| Weaviate | Yes | Yes | Graph + vector hybrid |

Example (Chroma):
```python
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings

embeddings = OllamaEmbeddings(model="nomic-embed-text")
vectorstore = Chroma.from_documents(chunks, embeddings, persist_directory="./chroma_db")
```

### Stage 5: Retrieval

Fetch relevant chunks at query time:

- **Similarity search:** cosine distance between query and chunk vectors
- **MMR (Maximal Marginal Relevance):** diversifies results, reduces redundancy
- **Hybrid search:** vector + keyword (BM25) for best of both
- **Parent-child:** retrieve small chunks, return larger parent context

Example:
```python
retriever = vectorstore.as_retriever(
    search_type="mmr",
    search_kwargs={"k": 5, "fetch_k": 20}
)
docs = retriever.invoke("What is the refund policy?")
```

### Stage 6: Augmented generation

Feed retrieved chunks into the LLM as context, with a citation-aware prompt:

```markdown
Answer the question using ONLY the provided context. If the answer is not in the context, say so.

Context:
{context}

Question: {question}

Cite sources using [Source N] format.
```

### Stage 7: Evaluation

Measure RAG quality:

- **Faithfulness:** Is the answer supported by the retrieved context?
- **Answer relevance:** Does the answer address the question?
- **Context precision:** Are retrieved chunks actually relevant?
- **Context recall:** Were all needed chunks retrieved?

Use `ragas` or `trulens` for automated evaluation.

## Example end-to-end (Ollama + Chroma)

```python
# 1. Load & chunk
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.llms import Ollama
from langchain.chains import RetrievalQA

loader = PyPDFLoader("document.pdf")
docs = loader.load()

splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = splitter.split_documents(docs)

# 2. Embed & store
embeddings = OllamaEmbeddings(model="nomic-embed-text")
vectorstore = Chroma.from_documents(chunks, embeddings, persist_directory="./db")

# 3. Query
qa = RetrievalQA.from_chain_type(
    llm=Ollama(model="llama3.2"),
    retriever=vectorstore.as_retriever(search_type="mmr", search_kwargs={"k": 4})
)
result = qa.invoke({"query": "What are the key findings?"})
print(result["result"])
```

## Decision checklist

- [] Documents identified and loadable
- [ ] Chunking strategy matches document structure
- [ ] Embedding model chosen (local vs cloud)
- [ ] Vector store selected (Chroma for local, pgvector for Postgres apps, Pinecone for managed)
- [ ] Retrieval method chosen (similarity vs MMR vs hybrid)
- [ ] Prompt includes citation instructions
- [ ] Evaluation plan defined (faithfulness, relevance, precision, recall)

## Related Workshop skills

- `ollama-local-ai` — local embeddings and LLMs for fully offline RAG
- `mcp-builder` — expose your RAG pipeline as MCP tools
- `observability-and-instrumentation` — trace retrieval and generation
