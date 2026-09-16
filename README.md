# Governed Clinical Trial Patient Screening & Regulatory Audit Agent

An enterprise-grade AI-powered system for clinical trial patient screening and regulatory compliance auditing, built for the HiDevs AI Quest 2026.

## Problem Statement

Clinical trial patient screening is a complex, time-intensive process that requires:
- Meticulous matching of patient eligibility criteria against trial protocols
- Strict adherence to regulatory compliance (FDA, EMA, ICH-GCP)
- Protection of Protected Health Information (PHI) under HIPAA/GDPR
- Comprehensive audit trails for regulatory inspections

Current manual processes are prone to errors, delays, and inconsistencies, leading to:
- Prolonged trial timelines
- Increased operational costs
- Regulatory non-compliance risks
- Suboptimal patient recruitment

## Objectives

This project aims to:
1. Automate patient screening against clinical trial protocols using AI agents
2. Ensure regulatory compliance through governed AI workflows
3. Protect patient privacy with PHI scrubbing capabilities
4. Provide comprehensive audit trails for regulatory inspections
5. Enable real-time eligibility assessment with medical safety validation
6. Streamline the clinical trial recruitment process

## Architecture Overview

The system employs a multi-agent architecture with specialized AI agents:

```
┌─────────────────────────────────────────────────────────────┐
│                     Orchestrator Agent                        │
│              (Workflow Coordination & Routing)                 │
└──────────────────────┬────────────────────────────────────────┘
                       │
       ┌───────────────┼───────────────┐
       │               │               │
       ▼               ▼               ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│ Ingestion    │ │ Protocol     │ │ PHI Scrubber │
│ Agent        │ │ Agent        │ │ Agent        │
└──────────────┘ └──────────────┘ └──────────────┘
       │               │               │
       └───────────────┼───────────────┘
                       │
       ┌───────────────┼───────────────┐
       │               │               │
       ▼               ▼               ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│ Eligibility  │ │ Medical      │ │ Audit        │
│ Agent        │ │ Safety Agent │ │ Agent        │
└──────────────┘ └──────────────┘ └──────────────┘
```

## Repository Structure

```
lyzr-b2b-negotiation-agent/
├── agents/                    # AI Agent implementations
│   ├── orchestrator/          # Workflow orchestration
│   ├── ingestion_agent/       # Data ingestion & parsing
│   ├── protocol_agent/        # Protocol analysis
│   ├── phi_scrubber/          # PHI detection & redaction
│   ├── eligibility_agent/     # Eligibility assessment
│   ├── medical_safety_agent/  # Safety validation
│   ├── audit_agent/           # Compliance auditing
│   └── configs/               # Agent configurations
├── backend/                   # FastAPI backend
│   ├── api/                   # API endpoints
│   ├── core/                  # Core configuration
│   ├── models/                # Database models
│   ├── schemas/               # Pydantic schemas
│   ├── services/              # Business logic
│   ├── routers/               # Route handlers
│   ├── utils/                 # Utility functions
│   ├── middleware/            # Custom middleware
│   ├── dependencies/          # Dependency injection
│   └── tests/                 # Backend tests
├── frontend/                  # Next.js frontend
│   ├── app/                   # Next.js app directory
│   ├── components/            # React components
│   ├── hooks/                 # Custom hooks
│   ├── lib/                   # Utility libraries
│   ├── public/                # Static assets
│   └── styles/                # Global styles
├── docs/                      # Documentation
│   ├── architecture/          # Architecture docs
│   ├── api/                   # API documentation
│   └── diagrams/              # Architecture diagrams
├── data/                      # Data storage
│   ├── protocols/             # Clinical trial protocols
│   ├── synthetic_ehrs/        # Synthetic EHR data
│   ├── outputs/              # Agent outputs
│   └── samples/              # Sample data
├── scripts/                   # Utility scripts
├── .github/                   # GitHub workflows
│   └── workflows/            # CI/CD pipelines
├── backend/main.py           # FastAPI entry point
├── requirements.txt          # Python dependencies
├── pyproject.toml            # Project configuration
├── Dockerfile                # Docker configuration
├── docker-compose.yml        # Docker Compose setup
├── .env.example              # Environment variables template
├── .gitignore               # Git ignore rules
└── LICENSE                  # MIT License
```

## Technology Stack

### Backend
- **Python 3.14**: Core programming language
- **FastAPI**: Modern, fast web framework for building APIs
- **Pydantic**: Data validation using Python type annotations
- **Uvicorn**: ASGI server for running FastAPI applications

### AI & ML
- **Lyzr SDK**: AI agent framework for building intelligent systems
- **Lyzr Agent API**: Agent orchestration and management
- **Google AI Studio (Gemini)**: Large language model for natural language processing

### Frontend
- **Next.js**: React framework for production-ready applications
- **React**: UI library for building user interfaces
- **TypeScript**: Type-safe JavaScript superset
- **Tailwind CSS**: Utility-first CSS framework

### Testing
- **Pytest**: Testing framework for Python applications
- **pytest-asyncio**: Async support for pytest
- **httpx**: HTTP client for testing FastAPI endpoints

### Code Quality
- **Ruff**: Fast Python linter and formatter
- **Black**: Code formatter for Python
- **isort**: Import sorting utility

### Deployment
- **Docker**: Containerization platform
- **Docker Compose**: Multi-container Docker applications
- **Render**: Cloud deployment platform

## Agent Responsibilities

### Orchestrator Agent
- Coordinates workflow execution across all agents
- Manages agent communication and data flow
- Handles error recovery and retry logic
- Maintains execution state and context

### Ingestion Agent
- Parses and validates input data (EHRs, protocols)
- Standardizes data formats for downstream processing
- Performs initial data quality checks
- Extracts structured information from unstructured documents

### Protocol Agent
- Analyzes clinical trial protocols
- Extracts inclusion/exclusion criteria
- Identifies regulatory requirements
- Maps protocol constraints to screening rules

### PHI Scrubber Agent
- Detects Protected Health Information in patient data
- Applies HIPAA/GDPR compliant redaction
- Maintains audit trail of PHI handling
- Ensures data privacy compliance

### Eligibility Agent
- Matches patient profiles against protocol criteria
- Generates eligibility scores and recommendations
- Provides detailed rationale for eligibility decisions
- Flags borderline cases for manual review

### Medical Safety Agent
- Validates medical safety considerations
- Checks for contraindications and drug interactions
- Assesses risk factors based on medical history
- Ensures patient safety in trial participation

### Audit Agent
- Generates comprehensive audit trails
- Validates regulatory compliance at each step
- Produces compliance reports for inspections
- Maintains immutable logs of all decisions

## Getting Started

### Prerequisites

- Python 3.14 or higher
- Node.js 18 or higher (for frontend)
- Docker and Docker Compose (optional)
- Git

### Environment Variables

Copy `.env.example` to `.env` and configure:

```bash
cp .env.example .env
```

Required environment variables:
- `LYZR_API_KEY`: Your Lyzr API key
- `GOOGLE_AI_API_KEY`: Your Google AI Studio API key

### Running Locally

#### Backend Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set environment variables in `.env`

4. Run the FastAPI server:
```bash
python -m backend.main
```

The API will be available at `http://localhost:8000`

API documentation: `http://localhost:8000/docs`

#### Frontend Setup (Future Implementation)

```bash
cd frontend
npm install
npm run dev
```

The frontend will be available at `http://localhost:3000`

### Running with Docker

1. Build and start all services:
```bash
docker-compose up --build
```

2. Access the application:
- Backend API: `http://localhost:8000`
- Frontend: `http://localhost:3000`

3. Stop services:
```bash
docker-compose down
```

### Deployment on Render

#### Backend Deployment

1. Create a new Render service
2. Connect your GitHub repository
3. Configure build settings:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
4. Add environment variables in Render dashboard
5. Deploy

#### Frontend Deployment (Future Implementation)

1. Create a new Render web service
2. Configure as Next.js application
3. Set environment variables
4. Deploy

## Testing

Run backend tests:
```bash
pytest backend/tests/
```

Run with coverage:
```bash
pytest --cov=backend backend/tests/
```

## Code Quality

Format code with Black:
```bash
black backend/
```

Sort imports with isort:
```bash
isort backend/
```

Lint with Ruff:
```bash
ruff check backend/
```

## Future Roadmap

### Phase 1: Core Agent Implementation
- [ ] Implement Orchestrator Agent
- [ ] Implement Ingestion Agent
- [ ] Implement Protocol Agent
- [ ] Implement PHI Scrubber Agent

### Phase 2: Screening & Safety
- [ ] Implement Eligibility Agent
- [ ] Implement Medical Safety Agent
- [ ] Implement Audit Agent
- [ ] Integrate agent workflows

### Phase 3: Frontend Development
- [ ] Set up Next.js application
- [ ] Build patient screening interface
- [ ] Build protocol management interface
- [ ] Build audit dashboard

### Phase 4: Advanced Features
- [ ] Real-time screening
- [ ] Batch processing
- [ ] Advanced analytics
- [ ] Multi-protocol support

### Phase 5: Production Readiness
- [ ] Performance optimization
- [ ] Security hardening
- [ ] Comprehensive monitoring
- [ ] Disaster recovery

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Competition

This project is developed for the **HiDevs AI Quest 2026** powered by Lyzr.

## Contact

For questions or collaboration opportunities, please open an issue in the GitHub repository.
