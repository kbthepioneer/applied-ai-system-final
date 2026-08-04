# Model Card: VibeFinder AI 1.0

## Model Overview
- **Model Name:** VibeFinder AI Recommender System
- **Task:** Content-based music recommendation and rank ordering based on multi-attribute user preference matching.
- **Base Project Origin:** Extended from the AI110 Module 3 *Music Recommender Simulation* starter project. The original prototype provided baseline CSV loading and simple scoring. This applied version adds input guardrails, artist diversity constraints, structured logging, and an automated evaluation harness.

## System Architecture & Algorithm Summary
VibeFinder uses a weighted similarity scoring algorithm combined with pre-inference guardrails:
1. **Guardrail Layer:** Validates that incoming user profiles contain required fields (`favorite_genre`, `favorite_mood`, `target_energy`) and that `target_energy` falls within $[0.0, 1.0]$. Invalid requests fail gracefully with an error log.
2. **Scoring Formula:**
   - **Genre Match:** $+2.0$ points
   - **Mood Match:** $+1.0$ point
   - **Energy Alignment:** $+1.0 - \vert{}\text{song\_energy} - \text{target\_energy}\vert{}$ (Max $+1.0$ point)
3. **Diversity Guardrail:** Caps top recommendations to a maximum of 2 tracks per artist to mitigate single-artist flooding.

## Intended & Non-Intended Use
- **Intended Use:** Personal music discovery, playlist generation prototyping, and studying content-based recommendation logic.
- **Non-Intended Use:** Commercial licensing, copyright enforcement, or high-stakes behavioral targeting.

## Reliability, Testing & Evaluation Results
The system was evaluated using an automated test harness (`tests/eval_harness.py`) and manual profile stress tests:

| Evaluation Test | Criteria | Result | Notes |
| :--- | :--- | :--- | :--- |
| Dataset Integrity | Non-empty CSV load with required attributes | **Pass** | Loaded 20/20 valid song records |
| Input Guardrails | Intercept out-of-bounds `target_energy` ($2.5$) | **Pass** | Logged warning and returned graceful fallback |
| Scoring Math | Verify $+4.0$ max score on perfect match | **Pass** | Math validated across all features |
| Diversity Cap | Limit max 2 songs per artist in Top K | **Pass** | Prevents single-artist domination |

- **Summary Metric:** 4/4 automated tests passed ($100\%$ Reliability Confidence Score).

## Biases and Limitations
1. **Genre Over-Weighting:** Because genre matches award $+2.0$ points, a matching genre song with poor energy alignment often outranks a non-genre song with perfect mood and energy match.
2. **Catalog Distribution Bias:** If the catalog heavily features specific genres (e.g., Regional Mexican or Pop), niche genre requests will fall back to secondary attributes, producing lower-confidence recommendations.
3. **Static Metadata Limitations:** Does not account for real-time user behavior, skip rates, or collaborative filtering patterns.

## Responsible AI Reflection & Collaboration
- **AI Collaboration:** Used AI coding assistants to design unit test assertions for guardrail edge cases and structure modular logging.
- **Helpful AI Suggestion:** AI suggested using `abs()` distance normalized between $0.0$ and $1.0$ for continuous energy matching instead of simple binary step thresholds.
- **Flawed AI Suggestion:** AI initially suggested using raw `.sort()` on dictionaries without key selectors, which caused `TypeError` exceptions during list comparisons.