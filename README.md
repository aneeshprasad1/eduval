# EduVal: Educational AI Benchmark

> **Measuring whether AI tutors actually help students learn**

[![Status](https://img.shields.io/badge/status-concept%20%26%20development-orange)](./EDUVAL_V0_FAST_TRACK.md)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)

---

## The Short Version

Current AI benchmarks test whether models *know* things ([MMLU](https://arxiv.org/abs/2009.03300)), *reason* ([GPQA](https://arxiv.org/abs/2311.12022)), or produce *professional work* ([GDPVal](https://openai.com/index/gdpval/)). **None rigorously measure whether AI tutors actually help students learn.**

EduVal is a benchmark grounded in learning science that evaluates AI on pedagogical effectiveness: scaffolding, misconception remediation, zone of proximal development calibration, flow state maintenance, and **measurable learning outcomes**.

We evaluate both sides of the classroom:
- 🎓 **Student-facing**: Multi-turn tutoring with pre/post learning gain measurement
- 📝 **Teacher-facing**: Tool generation (quizzes, lesson plans, rubrics) evaluated by practicing educators  
- 🖼️ **Multimodal**: Diagrams, handwriting interpretation, slide creation, visual explanations

---

## Why This Matters Now

1. **ARC AGI 3** just dropped (March 2026) — humans solve 100%, frontier models score <1%. It tests interactive reasoning and skill acquisition. Educational AI needs similar rigor.

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

**Subject Coverage:** Mathematics, Sciences, ELA, History, World Languages, Computer Science, Arts

**Grade Bands:** K-2, 3-5, 6-8, 9-12, University

### Pillar 2: Teacher Tools (Educator-Facing)

Single-turn and short multi-turn generation tasks for educator workflows.

**Task Types:**
- Quiz and exam generation
- Lesson plan creation
- Rubric design
- Differentiated materials (same content, three reading levels)
- Grading with feedback
- Report card comments
- IEP accommodation suggestions

**Key Evaluation Question** (from GDPVal):
> *"Would you use this in your classroom tomorrow, as-is?"*

### Pillar 3: Multimodal Capabilities

- Diagram generation and interpretation
- Handwriting analysis (student work feedback)
- Slide deck creation
- Visual explanations
- Graph/chart generation from data

---

## Evaluation Framework: Three Layers

```
┌─────────────────────────────────────────────────────────┐
│              LAYER 3: COMPOSITE SCORE                  │
│     Weighted combination → Leaderboard + Profile       │
├─────────────────────────────────────────────────────────┤
│          LAYER 2: HUMAN EXPERT EVAL                    │
│   Pedagogical quality, classroom readiness             │
├─────────────────────────────────────────────────────────┤
│          LAYER 1: AUTOMATED EVAL                       │
│   Learning gain, ZPD tracking, flow metrics            │
└─────────────────────────────────────────────────────────┘
```

### Layer 1: Verifiable Metrics

**Learning Gain**: Pre/post test measurement using normalized gain formula: `(post - pre) / (max - pre)`

**ZPD Efficiency**: `learning_gain / scaffolding_intensity` — measures whether the model provides just enough support

**Flow/Friction Detection**: Automated analysis of conversation dynamics to identify productive struggle vs. unproductive frustration

### Layer 2: Human Expert Evaluation

- **Blind Preference** (Arena-style): Head-to-head model comparison
- **Rubric Scoring** (10 dimensions): Scaffolding, misconception handling, Socratic method, motivational tone, etc.
- **Classroom Readiness**: "Would you use this as-is?"

### Layer 3: Composite Scoring

Weighted combination producing both a **ranking** (who's best?) and a **profile** (best at what?).

---

## Student Personas: Controlled Variation

A model that tutors a motivated honors student might fail with a frustrated student who has learning gaps. We test adaptation via **20+ defined personas**:

| Persona | Grade | Profile |
|---------|-------|---------|
| **Diego** | 5th | Struggling, math-anxious, shuts down when confused |
| **Priya** | 8th | Overachiever, perfectionist, needs extension |
| **Aiden** | 7th | ADHD, gaming-obsessed, needs engagement hooks |
| **Alex** | University | First-gen, overwhelmed, needs metacognitive support |

Each persona has **defined learning rules** — explicit conditions for what causes learning vs. confusion vs. withdrawal.

---

## Comparison to Related Benchmarks

| Benchmark | Scope | What EduVal Adds |
|-----------|-------|------------------|
| **MMLU** | Knowledge recall | Pedagogical process, learning outcomes |
| **MRBench** | Math tutoring | Scale, all subjects, learning gain measurement |
| **EducationQ** | Teaching effectiveness | Multimodal, teacher tools, ZPD tracking |
| **GDPVal** | Professional tasks | Education-specific, learning science grounding |
| **ARC AGI 3** | Interactive reasoning | Human learning, pedagogical scaffolding |
| **Chatbot Arena** | General preference | Education-specific dimensions |

---

## Project Status

- 📄 **Full Proposal**: See [`EDUVAL_PROPOSAL.md`](./EDUVAL_PROPOSAL.md)
- 🚀 **v0 Fast Track Plan**: See [`EDUVAL_V0_FAST_TRACK.md`](./EDUVAL_V0_FAST_TRACK.md)
- 📊 **Specs**: See [`spec/`](./spec/) directory

### v0 Target (4 weeks)
- 500 high-quality eval examples
- 2 subjects (Math + Physics)
- Text + LaTeX equations
- Expert annotation + automated metrics

### v1.0 Target
- 500 tasks across 8 subjects
- 20 personas
- 50-teacher evaluator pool
- Public leaderboard

---

## Design Principles

1. **Learning outcomes over answer quality** — Pre/post testing measures whether students actually learned
2. **All subjects, all levels** — K-5 through university, STEM to humanities
3. **Both sides of the classroom** — Student tutoring AND teacher tools
4. **Multimodal from day one** — Diagrams, slides, handwriting interpretation
5. **Human-graded with automated tier** — Expert evaluation for official scores, auto-grader for iteration
6. **Open and adoptable** — Open-source dataset, eval harness, methodology
7. **Grounded in learning science** — Vygotsky, Csikszentmihalyi, Bloom, IRT

---

## Call for Collaboration

We're looking for:

- 🍎 **Practicing teachers** (all subjects, all levels)
- 🎓 **Learning scientists** & education researchers
- 🤖 **AI researchers** (benchmark design, LLM evaluation)
- 💻 **Engineers** (harness development, dataset pipelines)
- 🏫 **School districts** & edtech companies for pilot studies

---

## References

- **EducationQ**: Wang et al. (2024) — Measuring teaching effectiveness with pre/post tests
- **MRBench**: Lee et al. (2024) — Math tutoring rubrics
- **GDPVal**: OpenAI (2025) — Professional task evaluation
- **ARC AGI 3**: Chollet et al. (2026) — Interactive reasoning benchmark
- **Vygotsky** (1978): Zone of Proximal Development
- **Csikszentmihalyi** (1990): Flow: The Psychology of Optimal Experience
- **Wood, Bruner, Ross** (1976): The Role of Tutoring in Problem Solving

---

*"The goal of education is not to increase the amount of knowledge but to create the possibilities for a child to invent and discover."* — Jean Piaget

**EduVal: Measuring if AI can actually teach.**
