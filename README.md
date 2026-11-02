# AIBA --- AI Business Analyst Agent

> Turn business documents into searchable knowledge and evidence-backed
> business insights.

AIBA (AI Business Analyst Agent) is an AI-powered document intelligence
application. Users can upload business documents, ask questions about
their contents, and request structured business analysis. The backend
combines document parsing, semantic chunking, hybrid retrieval,
reranking, and an LLM-powered response pipeline.

The current application is designed as an **open-access website without
user authentication**. It is being developed as a single shared
workspace; it is not yet a multi-tenant production service.

------------------------------------------------------------------------

## Table of Contents

-   [Overview](#overview)
-   [Core Features](#core-features)
-   [How AIBA Works](#how-aiba-works)
-   [Technology Stack](#technology-stack)
-   [Architecture](#architecture)
-   [Project Structure](#project-structure)
-   [Prerequisites](#prerequisites)
-   [Getting Started](#getting-started)
-   [Environment Configuration](#environment-configuration)
-   [Running the Application](#running-the-application)
-   [Backend API](#backend-api)
-   [Frontend Pages](#frontend-pages)
-   [Document Processing and
    Retrieval](#document-processing-and-retrieval)
-   [Business Analysis Capabilities](#business-analysis-capabilities)
-   [Current Limitations](#current-limitations)
-   [Security and Public Deployment
    Considerations](#security-and-public-deployment-considerations)
-   [Development Workflow](#development-workflow)
-   [Roadmap](#roadmap)
-   [Contributing](#contributing)

------------------------------------------------------------------------

## Overview

Business documents often contain valuable information spread across
reports, financial statements, operational documents, and other PDFs.
Manually searching these documents and turning their contents into
useful conclusions can be time-consuming.

AIBA aims to simplify this process through a document-grounded AI
workflow:

1.  Upload a PDF document.
2.  Parse and structure its content.
3.  Divide the content into meaningful chunks.
4.  Index the chunks for semantic and keyword retrieval.
5.  Ask questions in natural language.
6.  Retrieve and rerank relevant evidence.
7.  Generate answers or structured business analysis using the retrieved
    context.

AIBA is intended to support business understanding and decision-making.
Its generated output should be treated as analytical assistance and
checked against the underlying source documents before important
decisions are made.

## Core Features

### 1. Document Knowledge Base

-   Upload PDF documents.
-   Parse document content through the ingestion pipeline.
-   Build structured document representations.
-   Create semantic chunks for retrieval.
-   View uploaded documents and their metadata.
-   Delete documents from the knowledge base.

### 2. AI Chat

-   Ask natural-language questions about indexed documents.
-   Retrieve relevant document chunks.
-   Generate answers using retrieved context.
-   Inspect supporting retrieval results.
-   View retrieval/reranking scores when returned by the backend.
-   View LLM token usage metadata when available.

The current chat interface keeps conversation messages in frontend React
state. It does not currently send the complete conversation history to
the backend or provide durable conversation storage.

### 3. Business Analysis

Submit a business question and receive a structured response containing:

-   Analysis type
-   Key findings
-   Conclusions
-   Supporting evidence

The backend analysis layer selects an analysis approach based on the
question and available evidence.

### 4. Open-access experience

The current product direction is an open website with no login or signup
requirement. Authentication and multi-user workspaces are intentionally
outside the current implementation scope.

------------------------------------------------------------------------

## How AIBA Works

``` text
                    USER
                     |
          Upload PDF / Ask a Question
                     |
                     v
             FRONTEND (React)
                     |
                FastAPI API
                     |
          +----------+-----------+
          |                      |
          v                      v
    DOCUMENT INGESTION       USER QUERY
          |                      |
          v                      v
     Docling Parser         Question Analysis
          |                      |
          v                      v
     Document Mapper        Retrieval Planner
          |                      |
          v                      v
   Structured Document      Hybrid Retrieval
          |                /             \
          v             Vector           BM25
    Hierarchy Builder   Search           Search
          |                \             /
          v                 Reciprocal Rank
     Chunk Builder             Fusion
          |                      |
          v                      v
   Embedding + Indexing       Reranking
          |                      |
          v                      v
    FAISS + BM25 Index     Relevant Evidence
          |                      |
          +----------+-----------+
                     |
                     v
               RAG / LLM
                     |
          +----------+-----------+
          |                      |
          v                      v
       Chat Answer         Business Analysis
                                 |
                                 v
                       Structured Findings,
                       Conclusions, Evidence
```

The diagram is a conceptual overview of the implemented pipeline. Exact
orchestration and component boundaries are defined by the backend source
code.

------------------------------------------------------------------------

## Technology Stack

### Frontend

  Technology                Purpose
  ------------------------- -----------------------------------------
  React 19                  Component-based user interface
  Vite                      Development server and production build
  JavaScript (ES modules)   Frontend application logic
  React Router              Client-side routing
  CSS                       Styling and responsive layouts
  Fetch API                 Communication with the backend

### Backend

  Technology / Component     Purpose
  -------------------------- ----------------------------------------
  Python                     Backend implementation
  FastAPI                    REST API
  Docling                    PDF document parsing
  Pydantic                   Request, response, and data validation
  BGE embedding model        Text embeddings
  FAISS                      Vector similarity search
  BM25                       Keyword-based retrieval
  Reciprocal Rank Fusion     Hybrid result fusion
  Cross-encoder reranker     Relevance reranking
  LLM provider integration   Answer and analysis generation

The exact Python package versions and model identifiers should be taken
from the backend dependency/configuration files. They are not duplicated
here to avoid documenting stale versions.

------------------------------------------------------------------------

## Architecture

AIBA is separated into a frontend application and a Python backend.

### Frontend responsibilities

-   Render the public-facing application interface.
-   Provide document upload and management interactions.
-   Collect chat and analysis queries.
-   Call backend API endpoints.
-   Display answers, findings, conclusions, and evidence.
-   Handle loading, success, and error states.

### Backend responsibilities

-   Expose REST API endpoints through FastAPI.
-   Parse and map uploaded documents.
-   Build document hierarchy and semantic chunks.
-   Generate embeddings and maintain retrieval indexes.
-   Retrieve and rerank relevant evidence.
-   Build prompts and invoke the configured LLM.
-   Orchestrate business analysis.
-   Persist knowledge-base artifacts according to the configured storage
    implementation.

### Backend module map

The backend architecture is organized around the following modules:

  -----------------------------------------------------------------------
  Module                              Responsibility
  ----------------------------------- -----------------------------------
  `api`                               FastAPI route handlers

  `analysis`                          Business question analysis and
                                      analysis orchestration

  `core`                              Application settings,
                                      configuration, and bootstrap

  `document`                          Document models, hierarchy,
                                      chunking, indexing, and
                                      relationships

  `exceptions`                        Application-specific exceptions

  `ingestion`                         Document parsing and mapping

  `llm`                               LLM integration and factory

  `models`                            Shared application data models

  `monitoring`                        LLM and service health checks

  `preprocessing`                     Document/text preprocessing

  `prompting`                         Prompt builders and prompt
                                      templates

  `providers`                         External provider abstractions

  `rag`                               Retrieval-augmented generation
                                      orchestration

  `retrieval`                         Vector, keyword, hybrid retrieval,
                                      and reranking

  `services`                          Application service layer

  `storage`                           Artifact and knowledge-base
                                      persistence

  `validators`                        Input and data validation
  -----------------------------------------------------------------------

The backend's bootstrap module wires the application components
together. Refer to the actual backend tree for the current file-level
implementation.

------------------------------------------------------------------------

## Project Structure

The repository is expected to have a layout similar to the following.
The backend tree is summarized at module level; the frontend section
reflects the uploaded frontend source snapshot.

``` text
AIBusinessAnalystAgent/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── analysis/
│   │   ├── core/
│   │   ├── document/
│   │   ├── exceptions/
│   │   ├── ingestion/
│   │   ├── llm/
│   │   ├── models/
│   │   ├── monitoring/
│   │   ├── preprocessing/
│   │   ├── prompting/
│   │   ├── providers/
│   │   ├── rag/
│   │   ├── retrieval/
│   │   ├── services/
│   │   ├── storage/
│   │   ├── validators/
│   │   └── main.py
│   └── ...
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── assets/
│   │   ├── components/
│   │   │   └── layout/
│   │   │       ├── AppLayout.jsx
│   │   │       ├── Header.jsx
│   │   │       └── Sidebar.jsx
│   │   ├── hooks/
│   │   ├── pages/
│   │   │   ├── analysis.jsx
│   │   │   ├── analysis.css
│   │   │   ├── chat.jsx
│   │   │   ├── chat.css
│   │   │   ├── knowledgebase.jsx
│   │   │   └── knowledge-base.css
│   │   ├── services/
│   │   │   └── api.js
│   │   ├── styles/
│   │   │   └── global.css
│   │   ├── app.jsx
│   │   └── main.jsx
│   ├── index.html
│   ├── package.json
│   ├── package-lock.json
│   └── vite.config.js
│
└── README.md
```

The frontend is undergoing a redesign. The planned futuristic landing
page, expanded workspace, reports, and settings should be considered
roadmap items until implemented.

------------------------------------------------------------------------

## Prerequisites

Install the following before running AIBA:

-   Python version supported by the backend dependency files.
-   Node.js and npm versions compatible with the frontend dependencies.
-   Git.
-   A configured LLM provider/model and any required credentials, if the
    selected provider requires them.

Check your installed versions:

``` bash
python --version
node --version
npm --version
```

------------------------------------------------------------------------

## Getting Started

### 1. Clone the repository

``` bash
git clone https://github.com/armaanydv/AIBusinessAnalystAgent.git
cd AIBusinessAnalystAgent
```

### 2. Set up the Python environment

From the repository root on Windows:

``` cmd
python -m venv .venv
.venv\Scripts\activate
```

On macOS/Linux:

``` bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install backend dependencies

Use the dependency manifest committed in the backend directory. For
example, if the project uses `requirements.txt`:

``` bash
pip install -r backend/requirements.txt
```

If the backend dependency file has a different name or location, use the
actual committed manifest instead. Do not install an arbitrary set of
packages in place of the project's dependency lock or requirements file.

### 4. Install frontend dependencies

Open a terminal in the frontend directory:

``` bash
cd frontend
npm install
```

------------------------------------------------------------------------

## Environment Configuration

### Frontend

The frontend supports an optional API base URL through a Vite
environment variable.

Create `frontend/.env`:

``` env
VITE_API_BASE_URL=http://127.0.0.1:8000
```

If this variable is not set, the current frontend falls back to:

``` text
http://127.0.0.1:8000
```

Restart the Vite development server after changing environment
variables.

### Backend

Configure the backend using the environment variables and settings
supported by the current backend implementation. In particular,
configure the selected LLM provider and model credentials where
required.

Do not commit API keys, passwords, tokens, or other secrets. Keep local
environment files out of version control and provide a sanitized example
environment file for collaborators.

------------------------------------------------------------------------

## Running the Application

Run the backend and frontend in separate terminals.

### Terminal 1 --- Backend

From the repository root on Windows:

``` cmd
cd backend
..\.venv\Scripts\activate
uvicorn app.main:app --reload
```

The backend is expected to be available at:

``` text
http://127.0.0.1:8000
```

FastAPI's interactive API documentation:

``` text
http://127.0.0.1:8000/docs
```

### Terminal 2 --- Frontend

``` bash
cd frontend
npm run dev
```

Vite will print the local development URL. With the default
configuration, it is usually:

``` text
http://localhost:5173
```

### Production frontend build

From the frontend directory:

``` bash
npm run build
```

Preview the generated build locally:

``` bash
npm run preview
```

The production build is generated in `frontend/dist/`.

------------------------------------------------------------------------

## Backend API

The current frontend integration uses the following backend endpoints.

  Method     Endpoint                          Purpose
  ---------- --------------------------------- ---------------------------------------
  `GET`      `/`                               Backend root/status
  `GET`      `/health`                         Health check
  `GET`      `/knowledge-base`                 List indexed documents
  `POST`     `/upload`                         Upload and ingest a PDF
  `DELETE`   `/knowledge-base/{document_id}`   Delete a document
  `POST`     `/chat`                           Ask a question using RAG
  `POST`     `/analysis`                       Generate structured business analysis

### Upload a document

`POST /upload`

Request: `multipart/form-data` with a required `file` field.

The current response includes:

-   `message`
-   `document_id`
-   `pages`
-   `chunks_created`

### List documents

`GET /knowledge-base`

The response includes:

-   `documents`
-   `total_documents`

Each document can include its ID, name, title, source file, file type,
page count, and creation timestamp.

### Delete a document

`DELETE /knowledge-base/{document_id}`

The document ID is supplied as a path parameter.

### Chat

`POST /chat`

Example request:

``` json
{
  "query": "What are the key business risks described in the report?",
  "top_k": 5
}
```

The response includes:

-   `answer`
-   `retrieval_results`
-   `llm`

Retrieval result objects can include a chunk ID, title, retrieval score,
reranking score, and text. LLM metadata can include input, output, and
total token counts, plus a finish reason.

### Business analysis

`POST /analysis`

Example request:

``` json
{
  "query": "Compare the performance of the business segments."
}
```

The response includes:

-   `analysis_type`
-   `findings`
-   `conclusions`
-   `supporting_evidence`

For the authoritative request and response schemas, inspect the running
backend's OpenAPI specification at `/openapi.json` or its Swagger UI at
`/docs`.

------------------------------------------------------------------------

## Frontend Pages

### Chat --- `/chat`

The Chat page allows users to submit questions about the indexed
documents. It displays the generated answer, retrieved evidence,
available relevance scores, and LLM token usage metadata.

### Knowledge Base --- `/knowledge-base`

The Knowledge Base page allows users to:

-   Upload PDF files.
-   View indexed documents.
-   Review available document metadata.
-   Refresh the document list.
-   Delete documents.

### Business Analysis --- `/analysis`

The Analysis page accepts a business question and displays the analysis
type, findings, conclusions, and supporting evidence.

### Planned public and workspace pages

The following are part of the redesign roadmap and are not represented
as completed features in the current frontend snapshot:

-   Public landing page
-   Features page
-   About page
-   Workspace dashboard
-   Reports page
-   Settings page

------------------------------------------------------------------------

## Document Processing and Retrieval

The backend document workflow is organized into stages.

### 1. Parsing

Docling is used to parse PDF documents into a structured representation.

### 2. Mapping

The parsed document is mapped into AIBA's structured document models,
preserving relevant document elements and metadata.

### 3. Hierarchy construction

The hierarchy builder uses document headings and structure to organize
content into sections.

### 4. Semantic chunking

The chunk builder creates chunks intended to preserve meaningful
document context for retrieval.

### 5. Indexing

The current retrieval architecture uses:

-   BGE embeddings for semantic representation.
-   FAISS with an inner-product index configured for cosine-similarity
    retrieval.
-   BM25 for keyword-based retrieval.

### 6. Hybrid retrieval

The hybrid retriever combines semantic and BM25 results using Reciprocal
Rank Fusion.

### 7. Reranking

A cross-encoder reranker reorders retrieved chunks to improve relevance
before context is passed to the generation pipeline.

### 8. Answer generation

The RAG service coordinates retrieval, reranking, prompt construction,
LLM invocation, and output parsing.

------------------------------------------------------------------------

## Business Analysis Capabilities

AIBA includes an analysis layer that interprets a business question,
plans retrieval, gathers evidence, selects an analysis approach, and
produces a structured result.

The implemented analysis techniques include:

-   **Comparative Analysis:** compare entities, periods, categories, or
    business segments when the source evidence supports comparison.
-   **Trend Analysis:** identify patterns or changes over time.
-   **Ranking Analysis:** rank entities against supported criteria.
-   **Root Cause Analysis:** investigate possible drivers behind an
    observed outcome.
-   **Contribution Analysis:** examine how components contribute to an
    overall result.
-   **SWOT Analysis:** organize supported evidence into strengths,
    weaknesses, opportunities, and threats.

The availability and quality of each technique depend on the question
and the information present in the uploaded documents. AIBA should not
invent missing metrics or treat unsupported assumptions as facts.

------------------------------------------------------------------------

## Current Limitations

The following limitations are important to understand in the current
development stage:

1.  **No authentication:** there are no login, signup, or user identity
    flows in the current product scope.
2.  **Shared knowledge base:** the current backend architecture is
    shared rather than user-isolated. Documents should not be treated as
    private to individual website visitors.
3.  **Chat history:** the current chat UI stores messages in frontend
    state; durable conversation history is not currently implemented.
4.  **Reports:** persistent report management and export are roadmap
    items, not current capabilities.
5.  **Public deployment hardening:** rate limiting, upload quotas, abuse
    prevention, and tenant/session isolation need to be addressed before
    exposing the backend to unrestricted public traffic.
6.  **LLM dependency:** answer generation depends on the configured LLM
    provider, model availability, quotas, and credentials.
7.  **PDF scope:** the current frontend upload interaction is designed
    for PDF files.

------------------------------------------------------------------------

## Security and Public Deployment Considerations

AIBA is being developed as an open-access application. The current
shared Knowledge Base design is suitable for controlled development and
demonstrations, but it must not be assumed to provide visitor-level data
isolation.

Before deploying the application for unrestricted public use, address at
least the following:

-   Enforce upload size limits and validate file content on the backend.
-   Apply API rate limits and abuse protection.
-   Restrict CORS to the actual deployed frontend origin.
-   Protect document deletion and other destructive operations.
-   Define retention and cleanup policies for uploaded files and
    generated artifacts.
-   Avoid exposing provider API keys or backend secrets in frontend
    code.
-   Add monitoring, structured logs, and operational alerts.
-   Decide whether visitors use isolated temporary workspaces or a
    deliberately shared public dataset.
-   Review privacy, data handling, and acceptable-use notices.

Do not expose a shared document store publicly until its access and
deletion behavior is intentional and adequately protected.

------------------------------------------------------------------------

## Development Workflow

A recommended local workflow:

1.  Pull the latest changes.
2.  Activate the Python virtual environment.
3.  Start the backend.
4.  Start the frontend.
5.  Test the affected feature through the browser and Swagger UI.
6.  Run the frontend production build.
7.  Commit a focused milestone.

### Useful Git commands

``` bash
git status
git add .
git commit -m "Describe the completed milestone"
git push
```

Avoid committing:

-   `.venv/`
-   `node_modules/`
-   `dist/`
-   `.env` files containing secrets
-   Generated caches and temporary files
-   Local document uploads or private datasets unless intentionally
    versioned

------------------------------------------------------------------------

## Roadmap

The roadmap reflects the current product direction. Items marked as
planned should not be interpreted as implemented.

### Completed foundation

-   [x] FastAPI backend foundation
-   [x] PDF ingestion with Docling
-   [x] Structured document mapping
-   [x] Hierarchy-aware chunking
-   [x] Embedding and vector indexing
-   [x] BM25 keyword retrieval
-   [x] Hybrid retrieval with Reciprocal Rank Fusion
-   [x] Cross-encoder reranking
-   [x] RAG chat API
-   [x] Business analysis orchestration and techniques
-   [x] React + Vite frontend foundation
-   [x] Knowledge Base frontend integration
-   [x] AI Chat frontend integration
-   [x] Business Analysis frontend integration

### Planned frontend evolution

-   [ ] Futuristic public landing page
-   [ ] Features and About pages
-   [ ] Redesigned workspace dashboard
-   [ ] Futuristic Chat interface
-   [ ] Redesigned Knowledge Base experience
-   [ ] Redesigned Business Analysis experience
-   [ ] Reports interface and report persistence
-   [ ] Settings and application preferences
-   [ ] Responsive layouts and accessibility improvements

### Planned platform hardening

-   [ ] Upload limits and stronger file validation
-   [ ] API rate limiting and abuse prevention
-   [ ] Public deployment configuration
-   [ ] Document retention and cleanup policies
-   [ ] Monitoring and operational observability
-   [ ] End-to-end and deployment testing

------------------------------------------------------------------------

## Contributing

Contributions and suggestions are welcome.

For a change:

1.  Describe the issue or improvement.
2.  Keep changes focused and consistent with the existing architecture.
3.  Preserve the API contracts unless a backend change is intentional.
4.  Test the affected frontend and backend workflows.
5.  Document any new environment variables or API behavior.
6.  Submit a pull request with a clear summary.

------------------------------------------------------------------------

## Project

**AIBA --- AI Business Analyst Agent**

Repository: https://github.com/armaanydv/AIBusinessAnalystAgent

AIBA is an evolving project. Features, architecture, and deployment
practices may change as development progresses.
