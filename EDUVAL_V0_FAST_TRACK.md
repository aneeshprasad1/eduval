# EDUVAL v0: Fast Track Plan

**Goal**: Deliver working v0 in 4 weeks with ~500 high-quality eval examples that demonstrates learning impact.

**Philosophy**: Ruthless scope reduction. Perfect is enemy of shipped. Learn fast, expand later.

---

## v0 Scope (The "500 Challenge")

### What We're Building
A focused benchmark that proves the core hypothesis: **pedagogical quality can be measured and improved**.

| Component | v0 Target | Full Vision |
|-----------|-----------|-------------|
| **Examples** | 500 | 50,000 |
| **Subjects** | 2 (Math + Physics) | All K-12 + College |
| **Modalities** | Text + LaTeX equations | Full multimodal (diagrams, images) |
| **Languages** | English only | Multilingual |
| **Turn Length** | 1-5 turns | Up to 30 turns |
| **Evaluation** | Expert annotated + automated metrics | Full dashboard + CI/CD |

---

## Week-by-Week Breakdown

### Week 1: Data & Scope Lock
**Goal**: Secure data access and finalize 500-example composition

**Day 1-2: Data Access Sprint**
- [ ] Confirm Gemini educational logs access (anonymization pipeline)
- [ ] Get 100-200 real tutoring dialogues from logs
- [ ] If blocked: pivot to Khan Academy + synthetic data

**Day 3-4: The "500 Mix" Design**
Target composition (adjust based on data availability):

| Source | Count | Rationale |
|--------|-------|-----------|
| Gemini logs | 200 | Real user interactions, authentic misconceptions |
| Khan Academy transcripts | 150 | High-quality tutoring, diverse topics |
| Expert-crafted | 100 | Edge cases, specific pedagogical scenarios |
| Synthetic (LLM + human review) | 50 | Fill gaps, stress-test metrics |

**Day 5: Annotation Protocol**
- [ ] Recruit 3-5 expert annotators (teachers, tutors)
- [ ] Design lightweight rubric (5-point scale, 3 dimensions)
- [ ] Run pilot on 10 examples, calibrate

**Week 1 Deliverable**: Data pipeline confirmed, 500 examples sourced, annotation team ready

---

### Week 2: Evaluation Harness MVP
**Goal**: Working evaluation system that can score any model

**Day 1-2: Core Infrastructure**
```python
# Minimal viable harness
class EduvalEvaluator:
    def __init__(self, examples_path):
        self.examples = load_examples(examples_path)
    
    def evaluate(self, model_fn) -> dict:
        results = []
        for ex in self.examples:
            response = model_fn(ex.student_input)
            score = self.score(response, ex.gold_standard)
            results.append(score)
        return aggregate(results)
```

**Day 3-4: Automated Metrics (Fast Feedback)**
Implement 3 core metrics:
1. **Accuracy**: Did it get the answer right?
2. **Process Score**: LLM-as-judge (1-5) on pedagogical quality
3. **Safety Check**: Red flags (giving answer immediately, unsafe content)

**Day 5: Human Annotation Pipeline**
- [ ] Build simple annotation UI (Google Sheets or lightweight web)
- [ ] Start annotating first 100 examples
- [ ] Calculate inter-annotator agreement

**Week 2 Deliverable**: Evaluation harness working, can run models and get scores

---

### Week 3: The "Hill Climbing" Demo
**Goal**: Show that models can improve on this benchmark

**Day 1-2: Baseline Models**
- [ ] Evaluate GPT-4 baseline
- [ ] Evaluate Gemini baseline (current production)
- [ ] Evaluate smaller model (e.g., Gemini Flash) for comparison

**Day 3-4: Targeted Improvements**
Pick ONE pedagogical technique to improve:
- **Option A**: Socratic questioning (don't give answer, guide to it)
- **Option B**: Misconception detection (catch and correct specific errors)
- **Option C**: Step-by-step scaffolding (break problems into hints)

Implementation:
- [ ] Create prompt engineering variation
- [ ] Fine-tune small model (if data permits)
- [ ] Evaluate both approaches

**Day 5: Results Analysis**
- [ ] Show improvement on specific dimension
- [ ] Document what worked / what didn't
- [ ] Prepare 5-slide summary

**Week 3 Deliverable**: Demonstrated measurable improvement on at least one pedagogical dimension

---

### Week 4: Polish & Stakeholder Demo
**Goal**: Presentable v0 with clear next steps

**Day 1-2: The "500" Finalized**
- [ ] Complete annotation of all 500 examples
- [ ] Quality check (remove edge cases that don't work)
- [ ] Lock gold standard labels

**Day 3-4: Demo Preparation**
- [ ] Live demo: model responding to 3-5 example prompts
- [ ] Side-by-side comparison: baseline vs improved model
- [ ] Metrics dashboard (even if simple)
- [ ] 10-minute presentation deck

**Day 5: Stakeholder Review**
- [ ] Present to 2-3 modeling teams
- [ ] Gather feedback on utility
- [ ] Document feature requests for v1

**Week 4 Deliverable**: Working v0 benchmark, stakeholder buy-in, clear v1 roadmap

---

## The "500" Composition (Detailed)

### Subject: Mathematics (250 examples)

**Algebra (100)**
- Solving linear equations
- Quadratic factoring
- Common misconceptions: sign errors, distribution errors

**Calculus (50)**
- Derivatives basics
- Integration concepts
- Limit intuition

**Statistics/Probability (50)**
- Mean vs median
- Conditional probability misconceptions
- Correlation vs causation

**Geometry (50)**
- Proof structure
- Similar triangles
- Area/volume formulas

### Subject: Physics (250 examples)

**Mechanics (150)**
- Newton's laws
- Free body diagrams
- Energy conservation
- Common misconceptions: force=motion, action-reaction confusion

**Electricity & Magnetism (50)**
- Ohm's law
- Circuit basics
- Field concepts

**Waves & Optics (50)**
- Wave properties
- Reflection/refraction

---

## The Three Metrics That Matter (v0)

Forget complex dashboards. Three numbers:

### 1. Accuracy ( correctness )
Did the model arrive at the right answer?
- **Target**: 80%+ on L1-L2, 60%+ on L4
- **Automated**: Yes (exact match or LLM judge)

### 2. Pedagogy Score ( quality )
How well did it teach?
- **Scale**: 1-5
- **Criteria**: 
  - 5: Socratic, guides discovery, checks understanding
  - 3: Explains clearly but gives answer
  - 1: Wrong, unsafe, or unhelpful
- **Evaluated by**: Human experts (gold), LLM judge (approximation)

### 3. Misconception Detection Rate ( awareness )
Did it catch and address student errors?
- **Formula**: (# detected misconceptions) / (# total misconceptions in set)
- **Target**: 70%+
- **Requires**: Curated examples with known misconceptions

---

## Risk Mitigation (v0)

| Risk | Likelihood | Mitigation | Contingency |
|------|------------|------------|-------------|
| **Can't access Gemini logs** | Medium | Start paperwork immediately | Use Khan Academy + synthetic |
| **Annotators unavailable** | Medium | Recruit backup teachers | Use LLM-as-judge only for v0 |
| **Metrics don't correlate with quality** | Low | Validate on 10 examples first | Simplify to binary good/bad |
| **Models don't show improvement** | Medium | Focus on single technique | Pivot to error analysis value |
| **Scope creep** | High | Daily check-ins on 500 target | Cut subjects to 1 if needed |

---

## The "Derisk" Checklist

By end of v0, we should have proven:

- [ ] **Data availability**: We can get real educational interactions
- [ ] **Annotation feasibility**: Experts can agree on quality (κ > 0.6)
- [ ] **Metric validity**: Automated scores correlate with human judgment
- [ ] **Improvement possible**: Models can get measurably better with iteration
- [ ] **Stakeholder interest**: Modeling teams want this for hill-climbing

---

## Success Criteria for v0

**Minimum viable success (ship v0)**:
- 500 examples across Math + Physics
- 3 metrics that measure different aspects
- Demonstrated improvement on at least 1 metric
- 2+ modeling teams express interest in using it

**Stretch goals**:
- Add third subject (Chemistry or CS)
- Build simple leaderboard/web UI
- Identify specific model weaknesses that lead to feature work

---

## Immediate Actions (This Week)

### Today
- [ ] Email/calendar: Schedule 30min with data access person for Gemini logs
- [ ] Reach out to 3 teachers/tutors for annotation
- [ ] Create shared folder for v0 work

### This Week
- [ ] Confirm data access timeline
- [ ] Lock in 2 annotators minimum
- [ ] Draft the 500-example spreadsheet (titles only)
- [ ] Set up simple evaluation harness repo

---

## v0 → v1 Transition

After v0 ships, the path to full EDUVAL:

| v0 (4 weeks) | v1 (3 months) | v2 (6 months) |
|--------------|---------------|---------------|
| 500 examples | 5,000 examples | 50,000 examples |
| 2 subjects | 6 subjects | All subjects |
| Text + equations | Basic diagrams | Full multimodal |
| Python harness | Web dashboard | CI/CD integration |
| Manual annotation | Semi-automated | Active learning |
| Expert panel | Expanded panel | Crowdsourced validation |

---

## The Pitch (30 seconds)

"EDUVAL v0 is a 500-example benchmark proving we can measure and improve pedagogical AI quality. In 4 weeks, we'll have real evals on Math and Physics, showing whether models can Socratically tutor, catch misconceptions, and actually improve student understanding — not just get answers right."

---

**Document Version**: v0 Fast Track  
**Target Delivery**: 4 weeks from start  
**Success**: Shipped benchmark + stakeholder buy-in

---

*Ready to execute? Pick the first action and go.*
