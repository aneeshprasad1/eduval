"""
EduVal v0 - Evaluation Harness

Orchestrates: task loading → simulated tutoring session → auto-rating → output
"""

import json
import time
import sys
import os
from pathlib import Path
from typing import Callable, Optional

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from personas.personas import PersonaEngine, load_persona, get_all_personas
from harness.raters import run_all_raters


def load_tasks(tasks_dir: str = None) -> list[dict]:
    """Load all task JSON files from the tasks directory."""
    if tasks_dir is None:
        tasks_dir = Path(__file__).parent.parent / "tasks" / "v0"
    else:
        tasks_dir = Path(tasks_dir)
    
    tasks = []
    for f in sorted(tasks_dir.glob("*.json")):
        with open(f) as fh:
            data = json.load(fh)
            if isinstance(data, list):
                tasks.extend(data)
            else:
                tasks.append(data)
    return tasks


class TutorModel:
    """
    Interface for tutor models. Subclass or use the factory.
    
    A tutor model takes the conversation history and returns a response.
    """
    
    def respond(self, conversation: list[dict], task: dict) -> str:
        raise NotImplementedError


class RuleBasedTutor(TutorModel):
    """
    A simple rule-based tutor for testing the harness without an LLM.
    Uses the task's scaffolding hints and solution steps.
    """
    
    def __init__(self, style: str = "socratic"):
        """style: 'socratic' (guided), 'direct' (tells answer), 'minimal' (barely helps)"""
        self.style = style
        self.hint_index = 0
    
    def respond(self, conversation: list[dict], task: dict) -> str:
        student_msgs = [m for m in conversation if m["role"] == "student"]
        hints = task.get("scaffolding_hints", [])
        steps = task.get("solution_steps", [])
        correct = task.get("correct_answer", "")
        
        last_student = student_msgs[-1]["content"] if student_msgs else ""
        turn = len(student_msgs)
        
        if self.style == "direct":
            return self._direct_response(correct, steps, turn)
        elif self.style == "minimal":
            return self._minimal_response(hints, turn)
        else:
            return self._socratic_response(last_student, hints, steps, correct, turn, task)
    
    def _socratic_response(self, student_msg, hints, steps, correct, turn, task):
        # Check if student got it right
        if correct.lower() in student_msg.lower():
            return f"Excellent! That's correct: {correct}. Great work! Can you explain why this approach works?"
        
        # Check for known misconceptions
        misconceptions = task.get("common_misconceptions", [])
        for m in misconceptions:
            if str(m.get("error", "")).lower() in student_msg.lower():
                return (f"Not quite. Be careful - {m['explanation']}. "
                       f"Let me give you a hint: {hints[min(turn, len(hints)-1)] if hints else 'Try again.'}")
        
        # Give progressive hints
        if turn < len(hints):
            encouragement = "Good thinking! " if turn > 0 else "Let's work through this. "
            return f"{encouragement}{hints[turn]}"
        
        # If we've run out of hints, guide through steps
        step_idx = turn - len(hints)
        if step_idx < len(steps):
            return f"You're getting closer! Think about this step: {steps[step_idx]}"
        
        # Final: reveal answer
        return f"The answer is {correct}. Let's make sure you understand why - {steps[-1] if steps else ''}"
    
    def _direct_response(self, correct, steps, turn):
        if turn == 0:
            step_text = " → ".join(steps) if steps else ""
            return f"The answer is {correct}. Here's how: {step_text}"
        return f"As I said, the answer is {correct}."
    
    def _minimal_response(self, hints, turn):
        if turn < len(hints):
            return hints[turn]
        return "Keep trying."


class LLMTutor(TutorModel):
    """
    Uses an LLM API to generate tutor responses.
    Requires a callable that takes a prompt and returns a string.
    """
    
    def __init__(self, llm_fn: Callable[[str], str], system_prompt: str = None):
        self.llm_fn = llm_fn
        self.system_prompt = system_prompt or self._default_system_prompt()
    
    def _default_system_prompt(self):
        return """You are an expert tutor. Your role is to guide students to understanding through:
1. Socratic questioning - ask questions rather than giving answers
2. Scaffolding - break problems into manageable steps
3. Misconception detection - identify and gently correct wrong thinking
4. Encouragement - keep students motivated
5. Adaptive teaching - adjust your approach based on the student's level

Never just give the answer. Guide the student to discover it themselves.
Be warm, patient, and encouraging. Use language appropriate for the student's level."""

    def respond(self, conversation: list[dict], task: dict) -> str:
        # Build prompt
        messages = [{"role": "system", "content": self.system_prompt}]
        
        # Add task context (tutor knows the answer)
        task_context = (f"[TASK CONTEXT - not visible to student]\n"
                       f"Problem: {task['problem']}\n"
                       f"Correct answer: {task['correct_answer']}\n"
                       f"Common misconceptions: {json.dumps(task.get('common_misconceptions', []))}\n"
                       f"Hints to use: {json.dumps(task.get('scaffolding_hints', []))}")
        messages.append({"role": "system", "content": task_context})
        
        # Add conversation history
        for msg in conversation:
            role = "assistant" if msg["role"] == "tutor" else "user"
            messages.append({"role": role, "content": msg["content"]})
        
        # Format as a single prompt string for the LLM function
        prompt = "\n".join(f"[{m['role']}]: {m['content']}" for m in messages)
        
        return self.llm_fn(prompt)


def run_session(
    task: dict,
    tutor: TutorModel,
    persona_name: str = "diego",
    max_turns: int = 8,
    verbose: bool = False,
) -> dict:
    """
    Run a simulated tutoring session.
    
    Returns a session dict with turns, scores, and diagnostic info.
    """
    persona = load_persona(persona_name)
    engine = PersonaEngine(persona)
    conversation = []
    
    # Present the problem
    problem_msg = f"Here's the problem: {task['problem']}"
    conversation.append({"role": "tutor", "content": problem_msg})
    
    if verbose:
        print(f"\n{'='*60}")
        print(f"Task: {task['id']} | Persona: {persona.name} | Difficulty: {task.get('difficulty', '?')}")
        print(f"{'='*60}")
        print(f"[Tutor]: {problem_msg}")
    
    # Student's initial attempt
    student_response = engine.generate_initial_response(task)
    conversation.append({"role": "student", "content": student_response})
    if verbose:
        print(f"[{persona.name}]: {student_response}")
    
    # Tutoring loop
    for turn in range(max_turns):
        # Tutor responds
        tutor_response = tutor.respond(conversation, task)
        conversation.append({"role": "tutor", "content": tutor_response})
        if verbose:
            print(f"[Tutor]: {tutor_response}")
        
        # Check if student got correct answer in last exchange
        if task["correct_answer"].lower() in student_response.lower():
            if verbose:
                print(f"  ✓ Student reached correct answer!")
            break
        
        # Student responds
        student_response = engine.generate_followup(task, tutor_response, turn + 1)
        conversation.append({"role": "student", "content": student_response})
        if verbose:
            print(f"[{persona.name}]: {student_response}")
    
    session = {
        "task": task,
        "persona": persona.name,
        "turns": conversation,
        "persona_state": engine.get_state(),
        "num_turns": len(conversation),
    }
    
    return session


class EduvalEvaluator:
    """Main evaluation harness. Load tasks, run sessions, score results."""
    
    def __init__(self, tasks_dir: str = None):
        self.tasks = load_tasks(tasks_dir)
        print(f"Loaded {len(self.tasks)} tasks")
    
    def evaluate(
        self,
        tutor: TutorModel,
        persona_names: list[str] = None,
        task_filter: dict = None,
        max_turns: int = 8,
        verbose: bool = False,
    ) -> dict:
        """
        Run full evaluation.
        
        Args:
            tutor: TutorModel instance
            persona_names: list of persona names to test (default: all)
            task_filter: dict with keys like 'subject', 'topic', 'difficulty' to filter tasks
            max_turns: max conversation turns per session
            verbose: print conversation to stdout
        
        Returns:
            Complete evaluation results with per-session scores and aggregates.
        """
        if persona_names is None:
            persona_names = list(get_all_personas().keys())
        
        tasks = self._filter_tasks(task_filter)
        print(f"Running {len(tasks)} tasks × {len(persona_names)} personas = {len(tasks) * len(persona_names)} sessions")
        
        all_results = []
        start_time = time.time()
        
        for task in tasks:
            for persona_name in persona_names:
                # Run session
                session = run_session(task, tutor, persona_name, max_turns, verbose)
                
                # Score session
                scores = run_all_raters(session)
                
                result = {
                    "task_id": task["id"],
                    "subject": task.get("subject", ""),
                    "topic": task.get("topic", ""),
                    "difficulty": task.get("difficulty", 0),
                    "persona": persona_name,
                    "num_turns": session["num_turns"],
                    "persona_state": session["persona_state"],
                    "scores": scores,
                }
                all_results.append(result)
        
        elapsed = time.time() - start_time
        
        # Aggregate
        aggregate = self._aggregate(all_results)
        
        return {
            "meta": {
                "num_tasks": len(tasks),
                "num_personas": len(persona_names),
                "total_sessions": len(all_results),
                "elapsed_seconds": round(elapsed, 2),
            },
            "aggregate": aggregate,
            "results": all_results,
        }
    
    def _filter_tasks(self, task_filter: Optional[dict]) -> list[dict]:
        if not task_filter:
            return self.tasks
        
        filtered = self.tasks
        for key, val in task_filter.items():
            if isinstance(val, list):
                filtered = [t for t in filtered if t.get(key) in val]
            else:
                filtered = [t for t in filtered if t.get(key) == val]
        return filtered
    
    def _aggregate(self, results: list) -> dict:
        """Compute aggregate statistics."""
        if not results:
            return {}
        
        # Overall
        overall_scores = [r["scores"]["overall"]["score"] for r in results if "overall" in r["scores"]]
        
        # By subject
        by_subject = {}
        for r in results:
            subj = r["subject"]
            if subj not in by_subject:
                by_subject[subj] = []
            by_subject[subj].append(r["scores"]["overall"]["score"])
        
        # By persona
        by_persona = {}
        for r in results:
            p = r["persona"]
            if p not in by_persona:
                by_persona[p] = []
            by_persona[p].append(r["scores"]["overall"]["score"])
        
        # By difficulty
        by_difficulty = {}
        for r in results:
            d = r["difficulty"]
            if d not in by_difficulty:
                by_difficulty[d] = []
            by_difficulty[d].append(r["scores"]["overall"]["score"])
        
        # By rater
        rater_names = ["pre_post", "zpd_efficiency", "flow_friction", "factual_accuracy", "rubric"]
        by_rater = {}
        for rater in rater_names:
            scores = [r["scores"][rater]["score"] for r in results if rater in r["scores"]]
            if scores:
                by_rater[rater] = {
                    "mean": round(sum(scores) / len(scores), 3),
                    "min": round(min(scores), 3),
                    "max": round(max(scores), 3),
                }
        
        def summarize(scores):
            return {
                "mean": round(sum(scores) / len(scores), 3) if scores else 0,
                "min": round(min(scores), 3) if scores else 0,
                "max": round(max(scores), 3) if scores else 0,
                "count": len(scores),
            }
        
        return {
            "overall": summarize(overall_scores),
            "by_subject": {k: summarize(v) for k, v in by_subject.items()},
            "by_persona": {k: summarize(v) for k, v in by_persona.items()},
            "by_difficulty": {k: summarize(v) for k, v in sorted(by_difficulty.items())},
            "by_rater": by_rater,
        }


def print_report(evaluation: dict):
    """Print a human-readable report of evaluation results."""
    meta = evaluation["meta"]
    agg = evaluation["aggregate"]
    
    print("\n" + "=" * 70)
    print("  EDUVAL v0 - EVALUATION REPORT")
    print("=" * 70)
    print(f"\nSessions: {meta['total_sessions']} ({meta['num_tasks']} tasks × {meta['num_personas']} personas)")
    print(f"Time: {meta['elapsed_seconds']}s")
    
    print(f"\n{'─' * 50}")
    print("OVERALL SCORES")
    print(f"{'─' * 50}")
    o = agg.get("overall", {})
    print(f"  Mean: {o.get('mean', 0):.3f}  |  Min: {o.get('min', 0):.3f}  |  Max: {o.get('max', 0):.3f}")
    
    print(f"\n{'─' * 50}")
    print("BY RATER")
    print(f"{'─' * 50}")
    for rater, stats in agg.get("by_rater", {}).items():
        print(f"  {rater:25s}  mean={stats['mean']:.3f}  min={stats['min']:.3f}  max={stats['max']:.3f}")
    
    print(f"\n{'─' * 50}")
    print("BY SUBJECT")
    print(f"{'─' * 50}")
    for subj, stats in agg.get("by_subject", {}).items():
        print(f"  {subj:15s}  mean={stats['mean']:.3f}  (n={stats['count']})")
    
    print(f"\n{'─' * 50}")
    print("BY PERSONA")
    print(f"{'─' * 50}")
    for persona, stats in agg.get("by_persona", {}).items():
        print(f"  {persona:15s}  mean={stats['mean']:.3f}  (n={stats['count']})")
    
    print(f"\n{'─' * 50}")
    print("BY DIFFICULTY")
    print(f"{'─' * 50}")
    for diff, stats in agg.get("by_difficulty", {}).items():
        print(f"  Level {str(diff):5s}       mean={stats['mean']:.3f}  (n={stats['count']})")
    
    print("\n" + "=" * 70)
