# EduVal v0 - Educational AI Tutoring Benchmark

A working prototype for evaluating AI tutoring quality. Measures pedagogical effectiveness, not just answer correctness.

## Quick Start

```bash
# Run full evaluation (50 tasks × 5 personas = 250 sessions)
python run_eval.py

# Verbose single-subject run
python run_eval.py --subject math --persona diego priya --verbose

# Compare tutor styles
python examples/compare_styles.py

# Inspect a single session
python examples/single_session.py

# Save results to JSON
python run_eval.py --output results.json
```

No dependencies beyond Python 3.10+ standard library.

## Architecture

```
eduval/
├── tasks/v0/              # 50 task definitions (JSON)
│   ├── math_tasks.json    # 25 math tasks (algebra, geometry, calculus)
│   └── physics_tasks.json # 25 physics tasks (mechanics, EM)
├── personas/              # Student persona engine
│   └── personas.py        # 5 personas with knowledge states & response rules
├── harness/               # Evaluation system
│   ├── evaluator.py       # Session runner, task loader, report generator
│   └── raters.py          # 5 auto-raters
├── examples/              # Example scripts and outputs
├── run_eval.py            # Main entry point
└── README_V0.md           # This file
```

## Components

### 1. Task Definitions (50 tasks)
Each task has: problem statement, correct answer, solution steps, common misconceptions, scaffolding hints, difficulty level (1-4), prerequisite knowledge.

### 2. Student Personas (5)
| Persona | Grade | Motivation | Style | Key Trait |
|---------|-------|------------|-------|-----------|
| **Diego** | 9 | 0.7 | Normal | Persistent, needs examples |
| **Priya** | 11 | 0.9 | Verbose | Analytical, asks "why" |
| **Aiden** | 8 | 0.4 | Terse | Easily frustrated, visual learner |
| **Alex** | 10 | 0.6 | Normal | Rushes ahead, skips steps |
| **Maya** | 12 | 0.85 | Verbose | Methodical, connects concepts |

Each persona has misconceptions, learning rules, and frustration thresholds that drive realistic simulated student behavior.

### 3. Auto-Raters (5)
| Rater | What it measures | Weight |
|-------|-----------------|--------|
| **Pre/Post Scorer** | Learning gain (Hake's normalized gain) | 25% |
| **ZPD Efficiency** | learning_gain / scaffolding_intensity | 20% |
| **Flow/Friction Detector** | Conversation quality (engagement vs frustration) | 15% |
| **Factual Accuracy** | Tutor correctness against reference solutions | 25% |
| **Rubric Evaluator** | 5-dimension rubric (scaffolding, misconception handling, encouragement, clarity, adaptiveness) | 15% |

### 4. Tutor Models
- **RuleBasedTutor**: 3 styles (socratic, direct, minimal) for baseline testing
- **LLMTutor**: Plug in any LLM via a callable `llm_fn(prompt) -> str`

## Results (Baseline)

Socratic vs Direct vs Minimal tutor comparison on math tasks:

| Style | Overall | Pre/Post | ZPD | Flow | Accuracy | Rubric |
|-------|---------|----------|-----|------|----------|--------|
| Socratic | **0.710** | 0.620 | 0.627 | 0.643 | 0.903 | 0.717 |
| Direct | 0.522 | 0.411 | 0.413 | 0.407 | 0.905 | 0.327 |
| Minimal | 0.517 | 0.653 | 0.667 | 0.692 | 0.168 | 0.501 |

Key finding: Socratic tutoring scores 36% higher overall than direct answer-giving.

## Using with an LLM

```python
from harness.evaluator import EduvalEvaluator, LLMTutor

# Your LLM function
def my_llm(prompt: str) -> str:
    # Call OpenAI, Anthropic, Gemini, local model, etc.
    return response

tutor = LLMTutor(llm_fn=my_llm)
evaluator = EduvalEvaluator()
results = evaluator.evaluate(tutor=tutor, persona_names=["diego", "priya"])
```

## Next Steps (v1)
- Expand to 500+ tasks across more subjects
- Add LLM-as-judge rater for deeper evaluation
- Human annotation pipeline for ground truth
- Multi-turn conversation quality metrics
- Leaderboard and CI/CD integration
