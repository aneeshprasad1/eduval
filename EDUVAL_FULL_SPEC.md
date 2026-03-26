# EduVal: A Learning-Science-Informed Benchmark for AI in Education

> **Status**: Concept & Specification Phase  
> **Last Updated**: March 2026  
> **Looking for**: Collaborators, feedback, pilot partners

---

## The Short Version

Current AI benchmarks test whether models *know* things (MMLU), *reason* (GPQA), or produce *professional work* (GDPVal). None rigorously measure whether AI tutors actually help students *learn*.

**EduVal is a benchmark grounded in learning science** that evaluates AI on pedagogical effectiveness: scaffolding, misconception remediation, zone of proximal development calibration, flow state maintenance, and measurable learning outcomes.

We evaluate both sides of the classroom:
- **Student-facing**: Multi-turn tutoring with pre/post learning gain measurement
- **Teacher-facing**: Tool generation (quizzes, lesson plans, rubrics) evaluated by practicing educators
- **Multimodal**: Diagrams, handwriting interpretation, slide creation, visual explanations

---

## Why This Matters Now

1. **ARC AGI 3** just dropped (March 25, 2026) — humans solve 100%, frontier models score <1%. It tests interactive reasoning and skill acquisition. Educational AI needs similar rigor.

2. **GDPVal** proved that expert evaluation on economically valuable tasks is possible at scale. We adapt their methodology for classroom value.

3. **AI tutors are being deployed** in schools without rigorous evaluation of actual learning outcomes. We're flying blind.

---

## Core Insight: Beyond "Correctness"

Most benchmarks treat education as a knowledge-transfer problem. It's not. Learning is a **dynamic, adaptive process** that happens in the interaction between learner, content, and support.

EduVal measures:

| Dimension | What It Captures | Learning Science Foundation |
|-----------|------------------|----------------------------|
| **ZPD Calibration** | Does the model pitch content at the edge of the student's capability? | Vygotsky's Zone of Proximal Development |
| **Scaffolding Efficiency** | How much support is needed for independent success? | Wood, Bruner, Ross (1976) |
| **Flow/Friction Dynamics** | Is the student in productive struggle or unproductive frustration? | Csikszentmihalyi's Flow Theory |
| **Misconception Handling** | Can the model diagnose and remediate wrong mental models? | Conceptual Change Theory |
| **Adaptive Explanation** | Does it reframe when the student is confused? | Cognitive Flexibility Theory |
| **Learning Velocity** | Rate of improvement during the session | Dynamic Assessment |

---

## The Three Pillars

### Pillar 1: Tutoring (Student-Facing)

Multi-turn conversational tutoring evaluated via simulated student interactions with **measurable learning outcomes**.

**Task Types:**
- Concept introduction (teaching new material)
- Misconception remediation (fixing wrong mental models)
- Worked problem guidance (Socratic walkthrough)
- Stuck student recovery (frustration handling)
- Error analysis (identifying where student work went wrong)
- Differentiated explanation (same concept, different levels)

**Subject Coverage:**
- Mathematics (K-12 through university: algebra, calculus, statistics, linear algebra)
- Sciences (biology, chemistry, physics, earth science)
- English Language Arts (reading, writing, grammar, literary analysis)
- History & Social Studies (US/world history, civics, economics)
- World Languages (Spanish, French, Mandarin)
- Computer Science (computational thinking through algorithms)
- Arts & Humanities

**Grade Bands:** K-2, 3-5, 6-8, 9-12, University

### Pillar 2: Teacher Tools (Educator-Facing)

Single-turn and short multi-turn generation tasks for educator workflows.

**Task Types:**
- Quiz and exam generation (with standards alignment)
- Lesson plan creation (objectives, activities, assessment)
- Rubric design (clear criteria, actionable levels)
- Differentiated materials (same content, three reading levels)
- Grading with feedback (rubric-based evaluation)
- Report card comments (personalized, constructive)
- IEP accommodation suggestions
- Parent communication drafts

**Key Evaluation Question** (from GDPVal methodology):
> *"Would you use this in your classroom tomorrow, as-is?"*

### Pillar 3: Multimodal Capabilities

Education is inherently multimodal. Students submit handwritten work. Teachers need diagrams and slides.

**Task Types:**
- Diagram generation (water cycle, cell structure, etc.)
- Visual explanations (fractions with pizza slices)
- Handwriting interpretation (identifying errors in student work)
- Graph/chart creation from data
- Slide deck generation (presentations for class)
- Image-based Q&A (questions about maps, photos, diagrams)
- Annotated feedback (circling errors, margin comments)

---

## Student Personas: Controlled Variation

A model that tutors a motivated honors student might fail completely with a frustrated student who has learning gaps. We test adaptation via **20+ defined personas** across variation axes:

| Dimension | Values | Why It Matters |
|-----------|--------|----------------|
| **Prior Knowledge** | None, Partial, Misconceived, Strong | Starting point for tutoring |
| **Misconceptions** | Specific wrong mental models | Tests misconception detection |
| **Motivation** | High, Medium, Low, Resistant | Engagement strategies |
| **Emotional State** | Curious, Neutral, Frustrated, Anxious | Emotional intelligence |
| **Learning Style** | Examples-first, Theory-first, Visual | Explanation adaptation |
| **Communication** | Verbose, Terse, ESL, Slang | Understanding diversity |
| **Special Needs** | ADHD, Dyslexia, Gifted, IEP | Differentiation & accommodation |

**Example Personas:**
- **Diego** (5th grade, struggling, math-anxious, shuts down when confused)
- **Priya** (8th grade, overachiever, perfectionist, needs extension not remediation)
- **Aiden** (7th grade, ADHD, gaming-obsessed, needs engagement hooks)
- **Alex** (university first-gen, overwhelmed, needs metacognitive support)

Each persona has **defined learning rules** — explicit conditions for what causes learning vs. confusion vs. withdrawal.

---

## Evaluation Framework: Three Layers

```
┌─────────────────────────────────────────────────────────┐
│              LAYER 3: COMPOSITE SCORE                  │
│     Weighted combination → Leaderboard + Profile       │
├─────────────────────────────────────────────────────────┤
│          LAYER 2: HUMAN EXPERT EVAL                    │
│   Pedagogical quality, classroom readiness,            │
│   preference ranking (non-verifiable)                  │
├─────────────────────────────────────────────────────────┤
│          LAYER 1: AUTOMATED EVAL                       │
│   Learning gain, factual accuracy, ZPD tracking,       │
│   flow metrics, curriculum alignment (verifiable)      │
└─────────────────────────────────────────────────────────┘
```

### Layer 1: Verifiable Metrics (Automated)

**Learning Gain Measurement** (adapted from EducationQ):
1. **Pre-test**: 3-5 questions on target topic
2. **Tutoring session**: 10-20 turns
3. **Post-test**: Isomorphic questions (same concepts, different surface)
4. **Score**: Normalized learning gain = (post - pre) / (max - pre)

**ZPD Calibration Tracking:**
- Continuous estimation of student capability vs. task difficulty
- Scaffolding intensity measurement
- ZPD Efficiency Ratio = learning gain / support provided
  - 1.0 = perfect calibration (just enough support)
  - < 1.0 = over-scaffolding (did the work for them)
  - > 1.0 = under-scaffolding (left them struggling)

**Flow/Friction Dynamics:**
- **Productive struggle**: Sustained effort, gradual improvement → optimal
- **Unproductive struggle**: Repeated errors, escalating frustration → needs intervention
- **Boredom**: Minimal responses, rushing → needs challenge
- **Over-scaffolding**: Student stops trying, just agrees → learned helplessness

**Factual Accuracy**: Claims verified against knowledge base
**Curriculum Alignment**: Checked against Common Core, NGSS, AP frameworks
**Task Completion**: Structural requirements met (for teacher tools)

### Layer 2: Human Expert Evaluation

**Evaluator Pool:**
- Practicing K-12 teachers (minimum 3 years experience)
- University instructors
- Curriculum designers
- Special education specialists
- Compensated at professional rates ($75-150/hr)

**Protocols:**

1. **Blind Preference (Arena-Style)**
   - Evaluator sees task + two model outputs (A vs B, randomized)
   - Selects: A better / B better / Tie
   - Aggregated via Bradley-Terry model → Elo ranking

2. **Rubric Scoring (10 dimensions for tutoring):**
   - Scaffolding Quality
   - Misconception Handling
   - Adaptive Explanation
   - Socratic Method
   - Appropriate Challenge (ZPD calibration)
   - Motivational Tone
   - Factual Accuracy
   - Curriculum Alignment
   - Actionability
   - Naturalness

3. **Classroom Readiness (GDPVal-style):**
   - Yes, as-is (3 points)
   - Yes, with minor edits (2 points)
   - Needs significant revision (1 point)
   - Would not use (0 points)

### Layer 3: Composite Scoring

**Per-Pillar Formulas:**

```
TutorScore = 0.35 × LearningGain + 0.25 × PedagogicalRubric + 
             0.20 × ExpertPreference + 0.10 × FactualAccuracy + 
             0.10 × ZPD_Efficiency

ToolScore = 0.30 × ClassroomReadiness + 0.25 × RubricScore + 
            0.20 × ExpertPreference + 0.15 × TaskCompletion + 
            0.10 × ContentAccuracy

MultimodalScore = 0.25 × VisualAccuracy + 0.25 × PedagogicalValue + 
                  0.20 × ExpertPreference + 0.15 × Clarity + 
                  0.15 × ProductionQuality
```

**Overall EduVal Score:**
```
EduVal = 0.40 × TutorScore + 0.35 × ToolScore + 0.25 × MultimodalScore
```

**Diagnostic Profile:**
Each model gets a radar chart across all dimensions, enabling statements like:
- "Model X is best for math tutoring but weak on essay feedback"
- "Model Y produces excellent lesson plans but poor Socratic dialogue"

---

## Learning Science Foundations

### Zone of Proximal Development (Vygotsky)

Learning happens at the edge of current capability with support. EduVal measures:
- **ZPD diagnosis**: Can the model identify where the student's edge is?
- **Scaffolding calibration**: Does it provide the right amount of support?
- **Fade planning**: Does it gradually remove support to build independence?

### Flow Theory (Csikszentmihalyi)

Optimal learning occurs in the channel between anxiety (too hard) and boredom (too easy). We measure:
- **Engagement trajectory**: Is the student staying in flow?
- **Fracture detection**: When does the student exit flow (up or down)?
- **Recovery**: Can the model bring them back to flow?

### Item Response Theory

Not all questions are equal. We weight assessment items by:
- **Difficulty (b)**: How hard is this for the target level?
- **Discrimination (a)**: How well does it separate ability levels?
- **Guessing (c)**: What's the chance of getting it right randomly?

This enables Computerized Adaptive Testing (CAT) for efficient pre/post measurement.

### Bloom's Taxonomy

Models are evaluated on scaffolding across cognitive levels:

| Level | Example | Evaluation Method |
|-------|---------|-------------------|
| Remember | Recall formula | Automated |
| Understand | Explain in own words | Human rubric |
| Apply | Solve similar problem | Pre/post test |
| Analyze | Break down argument | Tutoring scenario |
| Evaluate | Critique two methods | Socratic dialogue |
| Create | Design new approach | Open-ended task |

Each model gets a "cognitive scaffolding profile" showing strengths and gaps.

### Formative Assessment

Assessment *drives* learning, not just measures it. We evaluate:
- **Diagnostic check-ins**: Does the model verify understanding before moving on?
- **Responsiveness**: Does it adapt based on student responses?
- **Feedback quality**: Is feedback specific, actionable, and timely?

---

## Comparison to Related Benchmarks

| Benchmark | Scope | Modality | Key Metric | What EduVal Adds |
|-----------|-------|----------|------------|------------------|
| **MMLU/MMLU-Pro** | Knowledge recall | Text | Accuracy | Pedagogical process, learning outcomes |
| **MRBench** | Math tutoring | Text | Human rubric (8 dims) | Scale, all subjects, learning gain measurement |
| **EducationQ** | Teaching effectiveness | Text | Pre/post test | Multimodal, teacher tools, ZPD tracking |
| **GDPVal** | Professional competence | Multimodal | Expert win-rate | Education-specific, learning science grounding |
| **ARC AGI 3** | Interactive reasoning | Grid world | Skill acquisition | Human learning, pedagogical scaffolding |
| **MLE Bench** | ML engineering | Code | Kaggle medal rate | Educational workflows, classroom value |
| **Chatbot Arena** | General preference | Text | Crowdsourced A/B | Education-specific dimensions, learning outcomes |
| **HELM** | Holistic evaluation | Text | Multi-metric | Pedagogical metrics, multimodal |

**EduVal's unique combination:**
- ✅ Multi-turn tutoring with **measured learning outcomes**
- ✅ **Both sides of the classroom** (student + teacher tools)
- ✅ **Multimodal** input and output
- ✅ **All subjects and grade levels**
- ✅ **Learning science** foundations (ZPD, flow, IRT)
- ✅ **Human expert evaluation** at scale
- ✅ **Open source** with automated grading tier

---

## Target Scale

### Minimum Viable Benchmark (v1.0)

| Pillar | Tasks | Subjects | Grade Bands |
|--------|-------|----------|-------------|
| Tutoring | 200 | 8 core | All 5 |
| Teacher Tools | 200 | 8 core | All 5 |
| Multimodal | 100 | 6 | 3-5, 6-8, 9-12 |
| **Total** | **500** | | |

### Full Benchmark (v2.0)

| Pillar | Tasks | Subjects | Grade Bands |
|--------|-------|----------|-------------|
| Tutoring | 500 | 12+ | All 5 |
| Teacher Tools | 400 | 12+ | All 5 |
| Multimodal | 200 | 10+ | All 5 |
| **Total** | **1,100** | | |

---

## Project Structure

```
eduval/
├── README.md                 # This file
├── spec/                     # Detailed specifications
│   ├── overview.md           # Motivation & positioning
│   ├── taxonomy.md           # Task taxonomy by pillar
│   ├── methodology.md        # Evaluation framework
│   ├── personas.md           # Student persona definitions
│   ├── rubrics.md            # Scoring rubrics per dimension
│   └── construction.md       # Dataset construction plan
├── tasks/                    # Task definitions
│   ├── tutoring/             # Pillar 1 tasks
│   ├── teacher-tools/        # Pillar 2 tasks
│   └── multimodal/           # Pillar 3 tasks
├── harness/                  # Evaluation harness (code)
├── personas/                 # Student agent implementations
├── data/                     # Generated/collected data
└── paper/                    # Research paper drafts
```

---

## Current Status & Roadmap

### Phase 0: Specification (Current)
- [x] Core concept and motivation
- [x] Three-pillar structure
- [x] Student persona framework
- [x] Evaluation methodology
- [ ] Detailed task definitions
- [ ] Learning science integration (ZPD, flow, IRT)
- [ ] Automated grader design

### Phase 1: Pilot (Q2 2026)
- [ ] 50-task pilot across 3 subjects
- [ ] 5 student personas
- [ ] 10-teacher evaluator panel
- [ ] Automated grader calibration
- [ ] Initial model runs (GPT-4, Claude, Gemini)

### Phase 2: v1.0 (Q4 2026)
- [ ] 500 tasks complete
- [ ] 20 personas
- [ ] 50-teacher evaluator pool
- [ ] Public leaderboard
- [ ] Research paper submission

### Phase 3: v2.0 (2027)
- [ ] 1,100 tasks
- [ ] 30+ personas
- [ ] 100+ teacher evaluators
- [ ] Continuous evaluation pipeline
- [ ] API for edtech integration

---

## Call for Collaboration

We're looking for:

**Education Experts**
- Practicing teachers (all subjects, all levels)
- Curriculum designers
- Learning scientists
- Special education specialists

**AI Researchers**
- Benchmark designers
- Evaluation methodology experts
- LLM fine-tuning for education
- Automated grading systems

**Engineers**
- Evaluation harness development
- Dataset construction pipelines
- API design for model integration

**Organizations**
- School districts for pilot studies
- EdTech companies for validation
- AI labs interested in evaluation
- Funders for large-scale annotation

---

## Design Principles

1. **Learning outcomes over answer quality** — Pre/post testing measures whether students actually learned
2. **All subjects, all levels** — K-5 through university, STEM to humanities to arts
3. **Both sides of the classroom** — Student-facing tutoring AND teacher-facing tool generation
4. **Multimodal from day one** — Diagrams, slides, handwriting interpretation, visual explanations
5. **Human-graded with automated tier** — Expert evaluation for official scores, auto-grader for rapid iteration
6. **Open and adoptable** — Open-source dataset, eval harness, and methodology paper
7. **Grounded in learning science** — Not just what seems right, but what research says works

---

## Key Research Questions

EduVal will help answer:

1. **Do AI tutors actually improve learning?** (measured via pre/post gain)
2. **Which models are best for which subjects/levels?** (profiles vs. single ranking)
3. **What pedagogical strategies work in AI tutoring?** (rubric dimension analysis)
4. **How much does multimodality matter?** (comparison to text-only baselines)
5. **Can models adapt to diverse learners?** (persona coverage analysis)
6. **What's the gap between automated and human evaluation?** (calibration studies)

---

## References & Related Work

- **EducationQ**: Wang et al. (2024) — Measuring teaching effectiveness with pre/post tests
- **MRBench**: Lee et al. (2024) — Math tutoring rubrics
- **GDPVal**: OpenAI (2025) — Professional task evaluation
- **ARC AGI 3**: Chollet et al. (2026) — Interactive reasoning benchmark
- **MLE Bench**: OpenAI (2024) — ML engineering evaluation
- **Vygotsky**: Zone of Proximal Development (1978)
- **Csikszentmihalyi**: Flow: The Psychology of Optimal Experience (1990)
- **Wood, Bruner, Ross**: The Role of Tutoring in Problem Solving (1976)

---

## License

TBD — aiming for open-source (likely Apache 2.0 for code, CC-BY for dataset)

---

## Contact

**Project Lead**: [Your name/contact]  
**GitHub**: [repo link when available]  
**Email**: [contact email]  
**Discord/Slack**: [community link]

---

*"The goal of education is not to increase the amount of knowledge but to create the possibilities for a child to invent and discover, to create men who are capable of doing new things."* — Jean Piaget

*EduVal: Measuring if AI can actually teach.*
