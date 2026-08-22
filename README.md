# PolicyGuard AI — Compliance Auditor & Chat Assistant

PolicyGuard AI is an automated privacy policy auditor and regulatory chatbot platform. The application scans organization privacy agreements, identifies compliance violations, recommends specific clause modifications, and classifies the organisation's industry sector to provide tailored legal recommendations.

---

## 🎯 Core Capabilities
* **Multi-Framework Evaluation**: Audit policy documents against multiple regulatory frameworks simultaneously (*GDPR, HIPAA, CCPA, PCI DSS, UK GDPR*).
* **Industry Sector Classifier**: Automatically detects the organization's business sector (*Healthcare, Finance, E-commerce, Tech/SaaS, or Education*) from the text and suggests sector-specific privacy clauses.
* **AI Suggested Rewrite Tool**: Suggests direct compliance rewrites for violated clauses using LLM intelligence with customizable provider selections (*Groq Llama 3.3, OpenAI GPT-4o, or local template fallbacks*).
* **Grounded RAG Chatbot**: Chat directly with legal regulations powered by a high-performance semantic search database indexed against official article contents.
* **Auditing Dashboard & Executive Reports**: Interactive charts tracking framework scores, recent critical violations, and print-ready PDF executive summaries.
* **Polyglot Persistence Database**: Relational schema safety via PostgreSQL alongside flexible document storage via MongoDB.

---

## 🛠️ Technology Stack & Tooling

* **Frontend**:
  * **Framework**: React 19 + TypeScript + Vite.
  * **Styling**: Tailwind CSS v4 (native variables, utility optimizations).
  * **Icons & Charts**: `lucide-react` & `recharts`.
  * **State & Routing**: `react-router-dom`.

* **Backend**:
  * **Framework**: Python 3.12 + FastAPI (Async ASGI with Lifespan management).
  * **Relational DB**: PostgreSQL (SQLAlchemy ORM) with automatic local SQLite fallback (`policyguard.db`).
  * **Document DB**: MongoDB (Motor async driver & PyMongo) for raw texts, analysis reports, and chat transcripts.
  * **Testing**: Pytest (Automated unit validation suites).

* **Machine Learning & RAG**:
  * **Embedding Model**: Sentence-Transformers `all-MiniLM-L6-v2` (SBERT).
  * **Classification**: Bi-Directional LSTM neural network for sentence classification.
  * **Vector Database**: SQLite + NumPy vector store with cosine similarity calculation (or Qdrant container).
  * **NLP Tokenization**: NLTK sentence tokenize framework.
  * **LLM Clients**: Groq API (Llama 3.3) and OpenAI SDK.

---

## 📐 Architecture & System Design

```mermaid
graph TD
    subgraph ClientLayer [Frontend & Clients]
        UI[React 19 + Vite Frontend]
    end

    subgraph FastAPILayer [FastAPI Backend Engine]
        AUTH[Auth Router]
        PROJ[Projects Router]
        DOCS[Documents Router]
        ANALYZE[Analysis Router]
        CHAT[Chat Router]
        ADMIN[Admin Router]
    end

    subgraph RelationalDB [PostgreSQL / SQLite Fallback]
        U[(Users, Auth, Roles)]
        P[(Projects & Workspaces)]
        DM[(Document Metadata & Paths)]
        AM[(Analysis Runs & Status)]
        AL[(Audit Logs)]
    end

    subgraph DocumentDB [MongoDB]
        DT[(Document Raw Text & Chunks)]
        AF[(Detailed Findings & Scores JSON)]
        CS[(Chat Sessions & Transcripts)]
    end

    subgraph VectorEngine [Vector Store]
        VS[(Regulatory Articles Embeddings)]
    end

    UI --> FastAPILayer
    AUTH --> RelationalDB
    PROJ --> RelationalDB
    DOCS --> RelationalDB
    DOCS --> DocumentDB
    ANALYZE --> RelationalDB
    ANALYZE --> DocumentDB
    CHAT --> DocumentDB
    CHAT --> VectorEngine
    ADMIN --> RelationalDB
```

---

## 🗄️ Polyglot Persistence Split

| Data Domain | Database Engine | Collection / Table | Why? |
| :--- | :--- | :--- | :--- |
| **Users, Auth, Roles** | **PostgreSQL** | `user` | Strict schema, ACID transactional integrity, password hashing. |
| **Projects & Ownership** | **PostgreSQL** | `project` | Relational constraints and cascading rules. |
| **Document Metadata** | **PostgreSQL** | `document` | Storage paths, hashes, upload tracking. |
| **Analysis Metadata** | **PostgreSQL** | `analysis`, `score` | Summary metrics, statuses, and relational linking. |
| **Extracted Raw Policy Text** | **MongoDB** | `document_contents` | Large text payloads, parsed page chunks. |
| **Complete Audit Findings** | **MongoDB** | `analysis_reports` | Dynamic, deeply nested finding structures per regulation. |
| **Chat Message History** | **MongoDB** | `chat_sessions` | Conversational message arrays with rapid retrieval. |
| **RAG Embeddings** | **SQLite / Qdrant** | `vector_chunks` | Cosine similarity nearest-neighbor lookup for legal articles. |

---

## ⚡ Setup & Development

### 1. Environment Configuration
Create a `backend/.env` file:
```env
# Database Settings
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/policyguard
MONGO_URI=mongodb://localhost:27017
MONGO_DB_NAME=policyguard

# JWT Security
JWT_SECRET=your_jwt_secret_key
ACCESS_TOKEN_EXPIRE_MINUTES=60

# Upload Settings
UPLOAD_DIR=uploads
MAX_UPLOAD_SIZE_MB=10

# LLM Settings — Groq / OpenAI
GROQ_API_KEY=gsk_your_groq_api_key_here
GROQ_MODEL=llama-3.3-70b-versatile
```

### 2. Option A: Run via Docker Compose (Recommended)
Spins up PostgreSQL, MongoDB, Qdrant, FastAPI Backend, and React Frontend in isolated containers:
```powershell
docker compose up -d
```
* **Frontend**: [http://localhost:8080](http://localhost:8080)
* **Backend API**: [http://localhost:8000](http://localhost:8000)
* **API Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)

---

### 3. Option B: Run Locally

#### Start Backend:
```powershell
# Activate virtual environment
.\.venv\Scripts\activate

# Install dependencies
pip install -r backend/requirements.txt

# Start FastAPI server
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
```

#### Start Frontend:
```powershell
cd frontend
npm install
npm run dev
```

---

### 4. Run Automated Test Suite
To verify code changes and check endpoints across all frameworks:
```powershell
.\.venv\Scripts\pytest backend/tests/ -v
```

---

## ☁️ Deployment (Render Blueprint)

PolicyGuard is configured for one-click deployment using **`render.yaml`**:
1. **PostgreSQL**: Managed database (`policyguard-db`) provisioned automatically on Render.
2. **MongoDB**: Connect to a free [MongoDB Atlas Cluster](https://www.mongodb.com/cloud/atlas) by supplying your `MONGO_URI` in the Render dashboard.
3. **Backend & Frontend**: Dockerized web services built and served with HTTPS.

---

## 🛠️ Admin & Operations CLI

A command-line administration tool [`backend/admin_cli.py`](file:///c:/Users/ayush/Document/V_Sem/SI_2/PolicyGuard/backend/admin_cli.py) is available for system management:

```powershell
# Show system summary & database metrics
python backend/admin_cli.py summary

# List all registered users
python backend/admin_cli.py list-users

# Rebuild vector embeddings for regulatory frameworks
python backend/admin_cli.py reindex
```

### Default Seeded Credentials:
* **Admin**: `admin` / `admin`
* **User**: `test1` / `test1`
