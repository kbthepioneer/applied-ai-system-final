# Applied AI System: VibeFinder Recommender

An applied AI music recommendation engine built with feature matching, input guardrails, single-artist diversity capping, and an automated evaluation harness.

---

## Original Project Context
This system evolves the **AI110 Module 3 Music Recommender Simulation**. The original prototype demonstrated basic CSV loading and primitive score sorting. This extended system turns that prototype into a reliable applied system by adding input validation guardrails, artist diversity controls, structured logging, a system architecture diagram, and an automated evaluation harness.

---

## System Architecture

```mermaid
graph TD
    A[User Profile Input] --> B[Guardrail Validation Layer]
    C[(data/songs.csv)] --> D[Data Loader & Normalizer]

    subgraph Guardrails & Input Processing
        B -->|Valid Prefs| E[Agentic Recommender Engine]
        B -->|Invalid Prefs| F[Fallback / Log Error]
    end

    subgraph Core AI Engine
        D --> E
        E --> G[Scoring Strategy Execution]
        G --> H[Weighted Scoring & Energy Distance Math]
        H --> I[Diversity & Filter-Bubble Guardrail]
    end

    subgraph Output & Verification
        I --> J[Ranked Recommendation Engine]
        J --> K[Terminal Output & Reason Generator]
        J --> L[Automated Test Harness / Confidence Evaluator]
        L --> M[Execution Logs & Metrics]
    end


## Portfolio Artifact: What This Project Says About Me as an AI Engineer

Building VibeFinder demonstrates my ability to transition an AI concept from an unconstrained prototype into a production-ready, reliable software system. It highlights my focus on system architecture, defensive engineering through guardrails, and rigorous automated testing. Rather than treating AI as a black box, I prioritize transparent, explainable decision-making and ethical safeguards against algorithmic bias.