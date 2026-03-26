# EDUVAL: Educational Dialogue & Learning Benchmark

## Executive Summary

EDUVAL is the definitive hill-climbing benchmark for educational AI - a comprehensive, pedagogically-grounded evaluation system designed for modeling teams to iteratively improve educational capabilities. Unlike existing benchmarks that measure surface-level accuracy, EDUVAL captures the full complexity of effective teaching: subject mastery, pedagogical reasoning, misconception handling, adaptive scaffolding, and metacognitive support.

## 1. Problem Statement

Current evaluation of educational AI suffers from critical gaps:

- **Fragmentation**: Separate benchmarks for math (GSM8K, MATH), coding (HumanEval), general reasoning (MMLU) - no unified educational measure
- **Surface-level metrics**: Accuracy on multiple-choice ≠ pedagogical quality
- **Missing pedagogy**: No evaluation of Socratic questioning, misconception correction, or adaptive scaffolding
- **Single-turn bias**: Real tutoring is multi-turn; most benchmarks are Q&A pairs
- **No multimodal**: Equations, diagrams, and visual reasoning are central to learning but absent from benchmarks

**Goal**: Create the definitive hill-climbing benchmark for educational AI - granular, pedagogically-grounded, multimodal, and predictive of real tutoring efficacy.

---

## 2. Benchmark Design Principles

### 2.1 Core Dimensions (The "Edu Pentad")

| Dimension | Description | Example Evaluation |
|-----------|-------------|------------------|
| **Subject Mastery** | Accurate domain knowledge | Solving problems, explaining concepts correctly |
| **Pedagogical Reasoning** | How well it teaches, not just knows | Socratic questioning, checking understanding |
| **Misconception Handling** | Detecting and correcting errors | When student says 0.5 > 0.25 because 5 > 25 |
| **Adaptive Scaffolding** | Adjusting to learner's ZPD | Providing hints vs full solutions based on context |
| **Metacognitive Support** | Teaching how to learn | Prompting self-explanation, reflection |

### 2.2 Difficulty Progression (ZPD-Aligned)

Each dimension has 5 levels:
- **L1**: Elementary (explicit instruction)
- **L2**: Middle school (guided practice)
- **L3**: High school (inquiry-based)
- **L4**: College (expert-level reasoning)
- **L5**: Expert tutoring (adaptive, nuanced, multilingual)

---

## 3. Dataset Composition

### 3.1 Sources (50K total interactions)

| Source | Count | Description |
|--------|-------|-------------|
| **Gemini Educational Logs** | 20K | Real tutoring sessions, Q&A, homework help (anonymized) |
| **Human Tutoring Transcripts** | 10K | Khan Academy, school tutoring, verified quality |
| **Expert-Crafted Scenarios** | 10K | Pedagogy experts write multimodal multi-turn dialogues |
| **Synthetic Augmentation** | 7K | LLM-generated with expert validation |
| **Adversarial Examples** | 3K | Common student misconceptions, edge cases |

### 3.2 Subject Coverage

**Core K-12:**
- Mathematics (arithmetic, algebra, geometry, calculus, statistics)
- Sciences (physics, chemistry, biology, earth science)
- Language Arts (reading comprehension, writing, grammar, literature)
- Social Studies (history, civics, economics, geography)
- Computer Science (programming concepts, algorithms, data structures)

**College/Advanced:**
- Higher mathematics (linear algebra, differential equations, abstract algebra)
- Advanced sciences (organic chemistry, quantum mechanics, molecular biology)
- Engineering (mechanics, circuits, thermodynamics)
- Language learning (ESL, foreign languages with cultural context)

**21st Century Skills:**
- Data literacy and visualization
- Scientific reasoning and experimental design
- Critical thinking and argumentation
- Digital citizenship and media literacy

### 3.3 Task Types

1. **Single-turn QA** (25%): Factual recall, procedural solving
2. **Multi-turn Tutoring** (35%): 3-15 turn dialogues, Socratic scaffolding
3. **Multimodal Reasoning** (20%): Diagrams, equations, charts, images
4. **Essay/Explanation Evaluation** (10%): Grade and provide feedback on student work
5. **Problem Generation** (5%): Create problems at specific difficulty levels
6. **Pedagogical Strategy** (5%): Choose best next action given student state

---

## 4. Multimodal Design

### 4.1 Supported Modalities

| Modality | Use Cases | Evaluation Approach |
|----------|-----------|---------------------|
| **Text** | Explanations, Q&A, dialogue | Standard NLP metrics + pedagogy rubrics |
| **Mathematical Expressions** | Equations, proofs, derivations | LaTeX parsing + step verification |
| **Diagrams** | Geometric proofs, physics problems, biology illustrations | Visual understanding + annotation accuracy |
| **Charts/Graphs** | Data interpretation, statistics | Reading values, trends, correlations |
| **Code** | CS tutoring, algorithm explanations | Execution correctness + explanation quality |

### 4.2 Multimodal Tasks

**Example 1: Geometric Proof**
```
[Image: Triangle with angles labeled]
Student: "How do I prove these are similar?"
Model: Must reference specific angles, sides, and geometric principles
```

**Example 2: Physics Problem**
```
[Image: Free body diagram with forces]
[Equation: F = ma]
Student: "Why is the normal force less than mg?"
Model: Must explain both diagram and equation relationship
```

**Example 3: Data Interpretation**
```
[Image: Scatter plot with trend line]
Student: "What does this r² value mean?"
Model: Must read graph values and explain statistical concept
```

---

## 5. Evaluation Methodology

### 5.1 Automatic Metrics (Fast Iteration)

| Metric | Description | Target |
|--------|-------------|--------|
| **Accuracy** | Correctness of final answer | 90%+ on L1-L2, 75%+ on L5 |
| **Process Correctness** | Step-by-step validity (reward hacking resistant) | 85%+ |
| **Pedagogy Score** | LLM-judge rubric (1-5 scale) | 4.0+ avg |
| **Scaffold Efficiency** | Min turns to mastery (lower = better adaptation) | < 4 turns avg |
| **Misconception Detection Rate** | % of errors correctly identified | 80%+ |
| **Multimodal Coherence** | Consistency between text and visual references | 90%+ |

### 5.2 Human Evaluation (Gold Standard)

- **1,000 held-out examples** with expert annotator labels
- **Inter-annotator agreement** > 0.8 (Cohen's kappa)
- **Annotator pool**: Certified teachers, tutors with 5+ years experience
- **Dimensions rated**: Accuracy, Helpfulness, Safety, Engagement, Learning Gain, Multimodal Integration

### 5.3 Model-Based Evaluation (Scale)

- **GPT-4/Claude as judge** (with expert-calibrated rubrics)
- **Reference-based**: Compare to expert tutor responses (BERTScore, embedding similarity)
- **Reference-free**: Rubric-based LLM evaluation
- **Multimodal judges**: Vision-language models for image+text coherence

---

## 6. Unique Differentiators (vs Existing Benchmarks)

### 6.1 Dynamic Difficulty (The "Hill Climbing" Feature)

Unlike static benchmarks, EDUVAL supports **curriculum-style evaluation**:

```python
# Example: Model must progress through difficulty levels
if passes_algebra_l1() and passes_algebra_l2():
    unlock_algebra_l3()
    
# Track "learning curve" slope - steeper = better pedagogy
# Models can "level up" through the benchmark
```

**Outcome**: Models can progress through difficulty levels, enabling granular improvement tracking and preventing saturation.

### 6.2 Misconception Bank

Curated dataset of **500+ common student misconceptions** per subject:
- **Math**: "Multiplication always makes numbers bigger", "0.5 > 0.25 because 5 > 25"
- **Physics**: "Heavier objects fall faster", "Force is required to maintain motion"
- **Biology**: "Evolution is goal-directed", "Humans evolved from monkeys"
- **Chemistry**: "Chemical bonds store energy", "Electrons orbit like planets"
- **Languages**: Literal translations ignoring context, false cognates

Models evaluated on **detection** (do they catch it?) and **correction** (do they fix it gently and effectively?).

### 6.3 Multilingual Learning Evaluation

Given the importance of language learning:
- **ESL scenarios**: Common errors for native speakers of Spanish, Mandarin, Hindi, Arabic
- **Foreign language tutoring**: Cultural context + linguistic accuracy
- **Cross-lingual transfer**: Does understanding in L1 help L2 learning?

### 6.4 Pedagogical Fidelity Score

Multi-dimensional rubric scored by expert tutors:
- **Cognitive Load**: Does explanation match working memory limits?
- **Activation**: Does it elicit prior knowledge?
- **Feedback Quality**: Specific, actionable, timely?
- **Affective Tone**: Encouraging without being condescending?
- **Multimodal Integration**: Do visual and textual explanations cohere?

---

## 7. Infrastructure & Tooling

### 7.1 Evaluation Harness

```python
from eduval import Evaluator

evaluator = Evaluator(
    subjects=["math", "physics", "esl"],
    levels=[1, 2, 3, 4, 5],
    modalities=["text", "image", "equation"]
)

results = evaluator.evaluate(model=my_model)

# Returns comprehensive metrics:
# {
#   "math_l1_accuracy": 0.94,
#   "math_l5_pedagogy": 4.2,
#   "misconception_detection_rate": 0.82,
#   "multimodal_coherence": 0.91,
#   "scaffold_efficiency": 3.1,
#   "learning_curve_slope": 0.78
# }
```

### 7.2 Hill-Climbing Dashboard

- **Leaderboard**: By subject, level, modality, and aggregate
- **Error Analysis**: Cluster failure modes (e.g., "struggles with fractional reasoning", "over-explains simple concepts")
- **A/B Testing**: Compare model versions on specific pedagogical strategies
- **Calibration**: Track if model is well-calibrated (confidence vs accuracy)
- **Multimodal Analysis**: Which visual concepts are hardest?

### 7.3 Integration Points

- **CI/CD**: `pytest-eduval` plugin for regression testing
- **Model Cards**: Auto-generated pedagogy reports
- **Research API**: Access to Gemini educational logs for fine-tuning (internal)
- **External API**: Standardized interface for external researchers

---

## 8. Success Metrics for the Benchmark Itself

| Metric | Target | Measurement |
|--------|--------|-------------|
| **Predictive Validity** | r > 0.75 | Correlation with human tutor ratings and student learning gains |
| **Stability** | < 3% variance | Repeated evaluations of same model |
| **Discriminative Power** | d > 1.0 | Effect size between weak/strong models |
| **Coverage** | 95% | Of common K-12 + early college learning objectives |
| **Multimodal Balance** | 20% | Of tasks involve visual/equation components |
| **Adoption** | 5+ teams | Using for hill-climbing within 6 months |

---

## 9. Roadmap

### Phase 1: Foundation (Months 1-3)
- [ ] Curate 10K Gemini educational logs (anonymization pipeline)
- [ ] Collect 5K human tutoring transcripts (Math + Physics focus)
- [ ] Build evaluation harness v0 with multimodal support
- [ ] Expert annotation of 500 gold examples with pedagogy rubrics
- [ ] Pilot with 2 internal modeling teams
- [ ] Create misconception bank v1 (Math + Physics)

### Phase 2: Expansion (Months 4-6)
- [ ] Expand to Chemistry, Biology, CS (15K additional examples)
- [ ] Add language learning (ESL + 3 foreign languages)
- [ ] Build multimodal pipeline (diagram generation, equation rendering)
- [ ] Add misconception detection tasks
- [ ] Build hill-climbing dashboard with dynamic difficulty
- [ ] Synthetic data pipeline for augmentation

### Phase 3: Maturity (Months 7-9)
- [ ] Cross-subject evaluation (interdisciplinary reasoning)
- [ ] Pedagogical fidelity scoring system
- [ ] External validation (partner with Khan Academy, Coursera, schools)
- [ ] Multilingual expansion (10+ languages)
- [ ] Paper submission + open source release planning

### Phase 4: Advanced (Months 10-12)
- [ ] Long-horizon tutoring (30+ turn sessions)
- [ ] Personalized difficulty adaptation algorithms
- [ ] Real-time tutoring integration (live evaluation)
- [ ] Industry standard adoption
- [ ] Open source release with full documentation

---

## 10. Key Design Decisions

### 10.1 Why Multi-Turn Matters
Single-turn accuracy doesn't predict tutoring efficacy. A model that gives the answer immediately vs one that guides discovery - same accuracy, very different pedagogy. Real learning requires dialogue.

### 10.2 Why Process Over Product
Reward models on **how** they teach, not just correctness. Prevents "expert blind spot" (tutors who know but can't teach) and encourages effective pedagogy.

### 10.3 Why Dynamic Difficulty
Static benchmarks saturate quickly. Dynamic levels enable continuous hill-climbing - there's always a harder pedagogical challenge, preventing ceiling effects.

### 10.4 Why Multimodal From Day 1
Mathematics, physics, biology, and many other subjects are inherently visual. A benchmark without diagrams and equations doesn't capture real educational challenges.

### 10.5 Why Open Source Eventually
Educational AI benefits from broad collaboration. While we'll start internal to leverage Gemini logs, the goal is industry-wide adoption through open sourcing.

---

## 11. Immediate Next Steps

1. **Data Access**: Confirm access protocols for Gemini educational logs
2. **Expert Network**: Recruit 15-20 pedagogy PhDs and certified teachers for annotation
3. **Pilot Team**: Identify 2-3 modeling teams willing to iterate with us
4. **MVP Harness**: Build eval framework for multimodal math + multi-turn Socratic
5. **Misconception Collection**: Start curating from existing tutoring logs and education research
6. **Multimodal Pipeline**: Design rendering system for equations and diagrams
7. **Legal Review**: Ensure anonymization meets privacy standards for student data

---

## 12. Resources & Budget (Initial Estimate)

| Resource | Amount | Purpose |
|----------|--------|---------|
| Expert Annotators | 15-20 people × 3 months | Gold standard labels |
| Infrastructure | GCP credits | Benchmark hosting, multimodal rendering |
| Research Staff | 2-3 FTE | Data curation, evaluation design |
| External Validation | Partnership agreements | Khan Academy, school districts |
| Open Source Prep | Legal review | Licensing, documentation, release |

---

## 13. Risks & Mitigations

| Risk | Mitigation |
|------|------------|
| **Data privacy concerns** | Rigorous anonymization, IRB review, student data agreements |
| **Benchmark saturation** | Dynamic difficulty, continuous curation, adversarial examples |
| **Annotator disagreement** | Training protocols, adjudication process, clear rubrics |
| **Multimodal complexity** | Start simple (equations, basic diagrams), expand incrementally |
| **Adoption challenges** | Close collaboration with pilot teams, intuitive tooling |

---

## Appendix A: Example Evaluation Cases

### Case 1: Mathematical Misconception

**Student**: "Is 0.5 bigger than 0.25? I think so because 5 is bigger than 25."

**Good Response**: "You're thinking about whole numbers, which is a good instinct! But with decimals, we need to think about place value. 0.5 is actually 5 tenths, and 0.25 is 25 hundredths. Let's convert: 0.5 = 0.50. Now compare: 50 hundredths vs 25 hundredths. Which is bigger?"

**Bad Response**: "Yes, 0.5 > 0.25." (Misses misconception entirely)

**Evaluation**: Detection (did model catch error?), Explanation (clear place value explanation?), Scaffolding (did it guide student to self-discovery?)

### Case 2: Multimodal Physics

**Input**: 
- Image: Free body diagram showing block on inclined plane
- Student: "Why is the normal force less than mg?"

**Good Response**: References the angle in the diagram, explains component forces, relates to mg cos(θ) with both text and pointing to diagram features.

**Bad Response**: "The normal force is less because of the angle." (Vague, doesn't use diagram)

### Case 3: Language Learning

**Student** (ESL, Spanish speaker): "I am agree with you."

**Good Response**: "I see what you're saying! In English, we say 'I agree' not 'I am agree.' It's one of those tricky differences from Spanish where 'estar de acuerdo' uses a verb. You can say 'I agree' or 'I'm in agreement.'"

**Bad Response**: "Say 'I agree.'" (Correct but no explanation, no connection to L1)

---

## Appendix B: Comparison to Existing Benchmarks

| Benchmark | Focus | Multimodal | Pedagogy | Multi-turn | Hill-Climbing |
|-----------|-------|------------|----------|------------|---------------|
| **GSM8K** | Math word problems | ❌ | ❌ | ❌ | ❌ |
| **MATH** | Competition math | ❌ | ❌ | ❌ | ❌ |
| **HumanEval** | Code generation | ❌ | ❌ | ❌ | ❌ |
| **MMLU** | General knowledge | ❌ | ❌ | ❌ | ❌ |
| **MT-Bench** | Instruction following | ❌ | ❌ | ✅ | ❌ |
| **AlpacaEval** | Instruction following | ❌ | ❌ | ❌ | ❌ |
| **EDUVAL** | Educational dialogue | ✅ | ✅ | ✅ | ✅ |

---

**Document Version**: 1.0  
**Last Updated**: 2025-02-27  
**Authors**: [Aneesh Prasad + AI assistant]  
**Status**: Draft for review

---

*For questions or comments, please use the GitHub issues or reach out directly.*
