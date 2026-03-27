"""
EduVal v0 - Student Persona Engine

Each persona has:
- prior_knowledge: topics they understand well
- misconceptions: specific wrong beliefs they hold
- motivation: 0-1 scale affecting engagement
- learning_rate: how quickly they absorb new info
- personality_traits: affect conversation style
- response_rules: deterministic rules for how they respond
"""

import json
import random
from dataclasses import dataclass, field
from typing import Optional
from pathlib import Path


@dataclass
class Persona:
    name: str
    grade_level: int
    prior_knowledge: list[str]
    weak_topics: list[str]
    misconceptions: dict[str, str]  # topic -> wrong belief
    motivation: float  # 0-1
    learning_rate: float  # 0-1, how quickly they update beliefs
    personality_traits: list[str]
    verbosity: str  # "terse", "normal", "verbose"
    asks_questions: float  # 0-1 probability of asking follow-up
    gives_up_threshold: int  # number of failed attempts before frustration
    
    def should_ask_followup(self) -> bool:
        return random.random() < self.asks_questions
    
    def has_misconception(self, topic: str) -> Optional[str]:
        """Return the misconception if persona has one for this topic."""
        for key, val in self.misconceptions.items():
            if key in topic:
                return val
        return None
    
    def knows_topic(self, topic: str) -> bool:
        return any(t in topic for t in self.prior_knowledge)
    
    def is_weak_at(self, topic: str) -> bool:
        return any(t in topic for t in self.weak_topics)


# === The Five Personas ===

DIEGO = Persona(
    name="Diego",
    grade_level=9,
    prior_knowledge=[
        "arithmetic", "basic_algebra", "linear_equations",
        "kinematics", "basic_forces"
    ],
    weak_topics=[
        "quadratic_equations", "trigonometry", "calculus",
        "electromagnetism", "energy_conservation"
    ],
    misconceptions={
        "inequality": "You don't need to flip the sign when dividing by negative",
        "newtons_third_law": "Action-reaction forces act on the same object",
        "friction": "Friction always opposes motion, even for stationary objects being pushed",
        "derivative": "The derivative of x² is x",
        "energy": "Heavier objects fall faster because they have more energy"
    },
    motivation=0.7,
    learning_rate=0.6,
    personality_traits=["persistent", "concrete_thinker", "needs_examples"],
    verbosity="normal",
    asks_questions=0.4,
    gives_up_threshold=4
)

PRIYA = Persona(
    name="Priya",
    grade_level=11,
    prior_knowledge=[
        "algebra", "geometry", "trigonometry", "linear_equations",
        "quadratic_equations", "kinematics", "newtons_laws",
        "energy", "momentum"
    ],
    weak_topics=[
        "calculus", "integration", "electromagnetism",
        "magnetic_force", "induction"
    ],
    misconceptions={
        "chain_rule": "Just differentiate the outer function, ignore the inner",
        "integral_constant": "Definite integrals also need +C",
        "electric_field": "Electric field points toward positive charges",
        "parallel_circuits": "Current is the same through all branches of a parallel circuit",
        "limit": "If you get 0/0, the limit doesn't exist"
    },
    motivation=0.9,
    learning_rate=0.8,
    personality_traits=["analytical", "asks_why", "self_correcting"],
    verbosity="verbose",
    asks_questions=0.7,
    gives_up_threshold=6
)

AIDEN = Persona(
    name="Aiden",
    grade_level=8,
    prior_knowledge=[
        "arithmetic", "basic_fractions", "simple_equations"
    ],
    weak_topics=[
        "algebra", "geometry", "quadratic_equations", "functions",
        "physics_all", "newtons_laws", "energy"
    ],
    misconceptions={
        "equation": "You can move terms to the other side without changing the sign",
        "exponent": "x² + x² = x⁴",
        "fraction": "You can add fractions by adding numerators and denominators separately",
        "force": "Objects need a constant force to keep moving",
        "gravity": "Gravity only works when things are falling"
    },
    motivation=0.4,
    learning_rate=0.4,
    personality_traits=["easily_frustrated", "needs_encouragement", "visual_learner"],
    verbosity="terse",
    asks_questions=0.2,
    gives_up_threshold=2
)

ALEX = Persona(
    name="Alex",
    grade_level=10,
    prior_knowledge=[
        "arithmetic", "algebra", "linear_equations",
        "basic_geometry", "kinematics"
    ],
    weak_topics=[
        "calculus", "trigonometry", "electromagnetism",
        "torque", "circular_motion"
    ],
    misconceptions={
        "quadratic": "The quadratic formula has a minus sign before the square root, not ±",
        "vector": "You can add vector magnitudes to get the resultant magnitude",
        "centripetal": "Centripetal force is a separate force (like gravity or friction)",
        "circuit": "A battery supplies current, not voltage",
        "similar_triangles": "Similar means same size"
    },
    motivation=0.6,
    learning_rate=0.5,
    personality_traits=["rushes_ahead", "skips_steps", "competitive"],
    verbosity="normal",
    asks_questions=0.3,
    gives_up_threshold=3
)

MAYA = Persona(
    name="Maya",
    grade_level=12,
    prior_knowledge=[
        "algebra", "geometry", "trigonometry", "calculus_basics",
        "derivatives", "kinematics", "newtons_laws", "energy",
        "momentum", "circuits", "electric_field"
    ],
    weak_topics=[
        "integration_techniques", "optimization",
        "gauss_law", "induction", "RC_circuits"
    ],
    misconceptions={
        "optimization": "Just set f(x) = 0, not f'(x) = 0, to find extrema",
        "gauss": "Gauss's law uses total charge, not enclosed charge",
        "induction": "EMF depends on the magnetic field, not its rate of change",
        "integral_substitution": "u-substitution changes only the integrand, not the limits"
    },
    motivation=0.85,
    learning_rate=0.75,
    personality_traits=["methodical", "checks_work", "connects_concepts"],
    verbosity="verbose",
    asks_questions=0.6,
    gives_up_threshold=5
)

ALL_PERSONAS = {
    "diego": DIEGO,
    "priya": PRIYA,
    "aiden": AIDEN,
    "alex": ALEX,
    "maya": MAYA,
}


class PersonaEngine:
    """Generates student responses based on persona rules and task context."""
    
    def __init__(self, persona: Persona):
        self.persona = persona
        self.attempt_count = 0
        self.learned_this_session: list[str] = []
        self.frustration = 0.0
    
    def generate_initial_response(self, task: dict) -> str:
        """Generate the student's first attempt at the problem."""
        p = self.persona
        topic = task.get("subtopic", task.get("topic", ""))
        difficulty = task.get("difficulty", 2)
        
        # Check if they know the topic
        if p.knows_topic(topic) and difficulty <= p.grade_level - 7:
            return self._confident_attempt(task)
        
        # Check for misconception
        misconception = p.has_misconception(topic)
        if misconception:
            return self._misconception_attempt(task, misconception)
        
        # Weak topic
        if p.is_weak_at(topic):
            return self._struggling_attempt(task)
        
        # Default: partial attempt
        return self._partial_attempt(task)
    
    def generate_followup(self, task: dict, tutor_message: str, turn_number: int) -> str:
        """Generate student response after tutor provides feedback/hint."""
        p = self.persona
        self.attempt_count += 1
        
        # Check frustration
        if self.attempt_count >= p.gives_up_threshold:
            self.frustration = min(1.0, self.frustration + 0.3)
            if self.frustration > 0.7 and p.motivation < 0.6:
                return self._frustrated_response()
        
        # Learning check: did the tutor address a misconception?
        topic = task.get("subtopic", "")
        misconception = p.has_misconception(topic)
        
        if misconception and self._tutor_addresses_misconception(tutor_message, misconception):
            if random.random() < p.learning_rate:
                self.learned_this_session.append(topic)
                return self._aha_moment(task, tutor_message)
            else:
                return self._still_confused(task, misconception)
        
        # If tutor gave a hint, try to use it
        if self._contains_hint(tutor_message):
            if random.random() < (p.learning_rate + 0.2):
                return self._uses_hint(task, tutor_message)
            else:
                return self._misapplies_hint(task)
        
        # Ask a question?
        if p.should_ask_followup():
            return self._asks_question(task, tutor_message)
        
        # Default progression
        return self._incremental_progress(task, turn_number)
    
    def _confident_attempt(self, task: dict) -> str:
        p = self.persona
        answer = task["correct_answer"]
        if p.verbosity == "verbose":
            steps = task.get("solution_steps", [])
            return f"I think I know this one! {steps[0] if steps else ''} ... so the answer is {answer}"
        return f"I got {answer}"
    
    def _misconception_attempt(self, task: dict, misconception: str) -> str:
        p = self.persona
        errors = task.get("common_misconceptions", [])
        wrong_answer = errors[0]["error"] if errors else "I'm not sure"
        
        if p.verbosity == "terse":
            return f"Is it {wrong_answer}?"
        elif p.verbosity == "verbose":
            return f"I think the answer is {wrong_answer}. My reasoning: {misconception}"
        return f"I got {wrong_answer}. I used the rule that {misconception}"
    
    def _struggling_attempt(self, task: dict) -> str:
        p = self.persona
        if p.motivation < 0.5:
            return "I don't really know how to start this. Can you help?"
        if "prerequisite_knowledge" in task:
            prereq = task["prerequisite_knowledge"][0]
            return f"I think this involves {prereq}? But I'm not sure what to do."
        return "I'm not sure where to begin. What formula should I use?"
    
    def _partial_attempt(self, task: dict) -> str:
        steps = task.get("solution_steps", [])
        if steps:
            return f"OK so I started with {steps[0]}, but then I got stuck."
        return "I started working on it but I'm not sure if I'm on the right track."
    
    def _frustrated_response(self) -> str:
        p = self.persona
        responses = [
            "I don't get it. Can you just show me the answer?",
            "This is too hard. I keep getting it wrong.",
            "I've been trying but nothing works.",
        ]
        if "needs_encouragement" in p.personality_traits:
            responses.append("Am I even close? I feel like I'm doing everything wrong.")
        return random.choice(responses)
    
    def _aha_moment(self, task: dict, tutor_msg: str) -> str:
        p = self.persona
        answer = task["correct_answer"]
        if p.verbosity == "verbose":
            return f"Oh wait, I see! So that means... the answer should be {answer}? That makes so much more sense now!"
        return f"Ohh I see! So it's {answer}?"
    
    def _still_confused(self, task: dict, misconception: str) -> str:
        return f"Hmm, I hear you but I'm still confused. I thought {misconception}. Why is that wrong?"
    
    def _uses_hint(self, task: dict, tutor_msg: str) -> str:
        steps = task.get("solution_steps", [])
        # Simulate making progress
        step_idx = min(self.attempt_count, len(steps) - 1) if steps else 0
        if steps:
            return f"OK so using your hint... {steps[step_idx]}. Is that right?"
        return "Let me try again with your suggestion..."
    
    def _misapplies_hint(self, task: dict) -> str:
        errors = task.get("common_misconceptions", [])
        if errors and len(errors) > 1:
            return f"So using what you said... I get {errors[-1]['error']}? That doesn't seem right."
        return "I tried using your hint but I'm getting a weird answer. Where did I go wrong?"
    
    def _asks_question(self, task: dict, tutor_msg: str) -> str:
        p = self.persona
        questions = []
        if "asks_why" in p.personality_traits:
            questions.append("But why does that work? What's the intuition?")
        if "connects_concepts" in p.personality_traits:
            questions.append("Is this related to what we learned about " + 
                           task.get("prerequisite_knowledge", ["other topics"])[0] + "?")
        if "visual_learner" in p.personality_traits:
            questions.append("Can you draw it out or give me a picture?")
        if "needs_examples" in p.personality_traits:
            questions.append("Can you show me another example like this?")
        
        if questions:
            return random.choice(questions)
        return "Can you explain that part again?"
    
    def _incremental_progress(self, task: dict, turn: int) -> str:
        steps = task.get("solution_steps", [])
        if steps and turn < len(steps):
            return f"OK so next step: {steps[turn]}. Am I on track?"
        return "Let me try once more..." 
    
    def _tutor_addresses_misconception(self, tutor_msg: str, misconception: str) -> bool:
        """Heuristic: does the tutor message address the student's misconception?"""
        keywords = misconception.lower().split()
        msg_lower = tutor_msg.lower()
        # Check if tutor mentions key terms from the misconception
        matches = sum(1 for kw in keywords if kw in msg_lower and len(kw) > 3)
        return matches >= 2 or "actually" in msg_lower or "careful" in msg_lower or "not quite" in msg_lower
    
    def _contains_hint(self, tutor_msg: str) -> bool:
        hint_phrases = ["try", "think about", "what if", "consider", "hint", 
                       "remember", "notice", "look at", "what happens"]
        msg_lower = tutor_msg.lower()
        return any(phrase in msg_lower for phrase in hint_phrases)
    
    def get_state(self) -> dict:
        """Return current persona state for logging."""
        return {
            "name": self.persona.name,
            "attempt_count": self.attempt_count,
            "frustration": round(self.frustration, 2),
            "learned": self.learned_this_session,
            "motivation": self.persona.motivation,
        }


def load_persona(name: str) -> Persona:
    """Load a persona by name."""
    name_lower = name.lower()
    if name_lower not in ALL_PERSONAS:
        raise ValueError(f"Unknown persona: {name}. Available: {list(ALL_PERSONAS.keys())}")
    return ALL_PERSONAS[name_lower]


def get_all_personas() -> dict[str, Persona]:
    return ALL_PERSONAS
