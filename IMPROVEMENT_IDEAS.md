# Improvement Ideas

## 1. Faster and More Capable LLMs

### 1.1 Drop-in model upgrades

This project is built on free Qwen models. As new LLMs continue to emerge, router, analyzer and generator can be seamlessly upgraded to more advanced alternatives, such as Qwen3.5 series and MiniMax M2.5 - specifically designed for agent-based applications. Additional LLM options can also be made available.

### 1.2 Streaming responses

Streaming in the generate node will reduce perceived latency from ~30s to first-token in <1s.

### 1.3 Async Tool Execution

Run multiple tool calls in parallel using asyncio.gather instead of sequentially. This distributed parallel approach significantly reduces latency by executing independent tool calls concurrently, rather than waiting for each to complete one after another.


## 2. Better Prompts

### 2.1 Query Rewriting

Before hybrid search, the analyze node rewrites the user query into a retrieval-optimized form. This helps bridge the gap between natural language questions and the structure of indexed documents, improving retrieval relevance.

### 2.2 Structured Output Instructions

Using explicit JSON schema instructions in prompts ensures consistent, parseable outputs from the router and analyzer nodes.

### 2.3 Prompt Caching

For system prompts and static financial context — such as fixed glossaries, tool descriptions, and domain-specific instructions — prompt caching can be used to reduce costs by approximately 90% on repeated calls. This is particularly effective in financial RAG systems where the same context is reused across multiple user interactions.


## 3. Re-ranking

To enhance the quality of retrieved context without modifying the underlying LLM, a cross-encoder re-ranker (e.g., `bge-reranker`) can be inserted between the retrieval and generation stages. Unlike bi-encoder retrievers used in vector search, cross-encoders jointly process the query and each candidate document, producing more accurate relevance scores. This re-ranking step ensures that only the most semantically relevant documents are passed to the LLM for final answer generation, improving both accuracy and faithfulness of responses.


## 4. Metadata Filtering for Permission Layering

To prevent lower-privilege users from accessing restricted research reports or internal risk data, Weaviate's `where` filter on metadata fields can enforce access control at the vector database layer, rather than relying on post-retrieval filtering.

This approach is essential in the financial industry, where customer information is highly sensitive and access permissions for different departments must be isolated in accordance with relevant laws and regulations.

**Concept:**

```
User Role → Permission Level → Metadata Filter → Filtered Retrieval Results
```


## 5. Source Citations in Generated Answers

Surface the retrieved document metadata (title, date, source) alongside the generated answer so users can verify claims.


## 6. Evaluation Pipeline

To ensure consistent system quality as models or configurations evolve, an offline evaluation harness (e.g., RAGAs or a custom framework) should be implemented. This pipeline enables systematic measurement of key metrics such as retrieval recall and answer faithfulness, providing objective feedback for iterative improvements.



# Industrial Improvement Ideas

## 1. Faster and More Capable LLMs

### 1.1 Drop-in model upgrades

This project is built on free Qwen models. As new LLMs continue to emerge, router, analyzer and generator can be seamlessly upgraded to more advanced alternatives, such as Qwen3.5 series and MiniMax M2.5 - specifically designed for agent-based applications. Additional LLM options can also be made available.

### 1.2 Streaming responses

Streaming in the generate node will reduce perceived latency from ~30s to first-token in <1s.

### 1.3 Async Tool Execution

Run multiple tool calls in parallel using asyncio.gather instead of sequentially. This distributed parallel approach significantly reduces latency by executing independent tool calls concurrently, rather than waiting for each to complete one after another.


## 2. Better Prompts

### 2.1 Query Rewriting

Before hybrid search, the analyze node rewrites the user query into a retrieval-optimized form. This helps bridge the gap between natural language questions and the structure of indexed documents, improving retrieval relevance.

### 2.2 Structured Output Instructions

Using explicit JSON schema instructions in prompts ensures consistent, parseable outputs from the router and analyzer nodes.

### 2.3 Prompt Caching

For system prompts and static financial context — such as fixed glossaries, tool descriptions, and domain-specific instructions — prompt caching can be used to reduce costs by approximately 90% on repeated calls. This is particularly effective in financial RAG systems where the same context is reused across multiple user interactions.


## 3. Re-ranking

To enhance the quality of retrieved context without modifying the underlying LLM, a cross-encoder re-ranker (e.g., `bge-reranker`) can be inserted between the retrieval and generation stages. Unlike bi-encoder retrievers used in vector search, cross-encoders jointly process the query and each candidate document, producing more accurate relevance scores. This re-ranking step ensures that only the most semantically relevant documents are passed to the LLM for final answer generation, improving both accuracy and faithfulness of responses.


## 4. Graph RAG

Current RAG implementation uses vector similarity search (Weaviate) to retrieve relevant documents. While effective for point‑fact retrieval, it struggles with questions requiring multi‑hop reasoning or understanding entity relationships - for example, "How does Tesla's supply chain affect its competitors?"

Graph RAG replaces or augments vector retrieval with a knowledge graph, where entities (e.g., companies, people, financial metrics) are nodes and relationships (e.g., "supplier_of", "competitor_of", "acquired_by") are edges. Retrieval navigates the graph to find connected entities and extract contextual subgraphs.

### Integration Options

- **Option A: Replace Weaviate** — Use a graph database (e.g., Neo4j) as the primary retrieval engine
- **Option B: Hybrid** — Keep Weaviate for semantic search, augment with graph retrieval for relationship‑heavy queries
- **Option C: Entity‑linked retrieval** — Extract entities from query, retrieve relevant subgraphs, combine with vector results

## 5. Metadata Filtering for Permission Layering

To prevent lower-privilege users from accessing restricted research reports or internal risk data, Weaviate's `where` filter on metadata fields can enforce access control at the vector database layer, rather than relying on post-retrieval filtering.

This approach is essential in the financial industry, where customer information is highly sensitive and access permissions for different departments must be isolated in accordance with relevant laws and regulations.

**Concept:**

```
User Role → Permission Level → Metadata Filter → Filtered Retrieval Results
```


## 6. Source Citations in Generated Answers

Surface the retrieved document metadata (title, date, source) alongside the generated answer so users can verify claims.


## 7. Evaluation Pipeline

To ensure consistent system quality as models or configurations evolve, an offline evaluation harness (e.g., RAGAs or a custom framework) should be implemented. This pipeline enables systematic measurement of key metrics such as retrieval recall and answer faithfulness, providing objective feedback for iterative improvements.
