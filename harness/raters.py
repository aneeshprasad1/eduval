"""
EduVal v0 - Auto-Rater System

Five raters:
1. PrePostScorer - measures learning gain from pre to post test
2. ZPDEfficiencyCalculator - learning_gain / scaffolding_intensity
3. FlowFrictionDetector - conversation quality analysis
4. FactualAccuracyChecker - checks against reference solutions
5. RubricEvaluator - multi-dimension rubric scoring
"""

import re
import json
from dataclasses import dataclass
from typing import Optional


@dataclass
class RaterResult:
    rater_name: str
    score: float  # 0-1 normalized
    raw_score: float
    max_score: float
    details: dict
    

class PrePostScorer:
    """
    Measures learning gain by comparing student's understanding
    before and after the tutoring interaction.
    
    Pre-test: student's initial response quality
    Post-test: student's final response quality
    """
    
    def score(self, session: dict) -> RaterResult:
        turns = session.get("turns", [])
        task = session.get("task", {})
        correct_answer = task.get("correct_answer", "")
        
        if not turns:
            return RaterResult("pre_post", 0, 0, 1, {"error": "no turns"})
        
        # Pre-test: score the student's first response
        student_turns = [t for t in turns if t["role"] == "student"]
        if not student_turns:
            return RaterResult("pre_post", 0, 0, 1, {"error": "no student turns"})
        
        pre_score = self._score_response(student_turns[0]["content"], correct_answer, task)
        
        # Post-test: score the student's last response
        post_score = self._score_response(student_turns[-1]["content"], correct_answer, task)
        
        # Learning gain: normalized gain (Hake's gain)
        # g = (post - pre) / (1 - pre) if pre < 1
        if pre_score >= 1.0:
            gain = 1.0  # Already knew it
        else:
            gain = max(0, (post_score - pre_score) / (1.0 - pre_score))
        
        return RaterResult(
            rater_name="pre_post",
            score=gain,
            raw_score=gain,
            max_score=1.0,
            details={
                "pre_score": round(pre_score, 3),
                "post_score": round(post_score, 3),
                "normalized_gain": round(gain, 3),
                "first_response": student_turns[0]["content"][:100],
                "last_response": student_turns[-1]["content"][:100],
            }
        )
    
    def _score_response(self, response: str, correct_answer: str, task: dict) -> float:
        """Score a student response 0-1 based on correctness."""
        response_lower = response.lower().strip()
        correct_lower = correct_answer.lower().strip()
        
        # Exact match
        if correct_lower in response_lower:
            return 1.0
        
        # Check for numeric answer extraction
        correct_nums = re.findall(r'-?\d+\.?\d*', correct_lower)
        response_nums = re.findall(r'-?\d+\.?\d*', response_lower)
        
        if correct_nums and response_nums:
            # Check if any response number matches any correct number
            for cn in correct_nums:
                for rn in response_nums:
                    try:
                        if abs(float(cn) - float(rn)) < 0.01:
                            return 0.9  # Close numeric match
                    except ValueError:
                        pass
        
        # Check for misconception answers
        misconceptions = task.get("common_misconceptions", [])
        for m in misconceptions:
            if str(m.get("error", "")).lower() in response_lower:
                return 0.2  # Has a known misconception
        
        # Partial credit: mentions relevant terms
        steps = task.get("solution_steps", [])
        if steps:
            step_terms = " ".join(steps).lower()
            overlap = sum(1 for word in response_lower.split() 
                        if word in step_terms and len(word) > 3)
            return min(0.5, overlap * 0.1)
        
        return 0.1  # At least attempted


class ZPDEfficiencyCalculator:
    """
    Zone of Proximal Development efficiency.
    
    ZPD Efficiency = learning_gain / scaffolding_intensity
    
    High efficiency = student learned a lot with minimal scaffolding
    (tutor hit the ZPD sweet spot)
    """
    
    def score(self, session: dict) -> RaterResult:
        turns = session.get("turns", [])
        task = session.get("task", {})
        
        tutor_turns = [t for t in turns if t["role"] == "tutor"]
        student_turns = [t for t in turns if t["role"] == "student"]
        
        if not tutor_turns or not student_turns:
            return RaterResult("zpd_efficiency", 0, 0, 1, {"error": "insufficient turns"})
        
        # Scaffolding intensity: how much help was given
        scaffolding_intensity = self._measure_scaffolding(tutor_turns)
        
        # Learning gain: did the student improve?
        pre_post = PrePostScorer()
        learning_result = pre_post.score(session)
        learning_gain = learning_result.score
        
        # ZPD efficiency
        if scaffolding_intensity == 0:
            efficiency = 0.0
        else:
            efficiency = min(1.0, learning_gain / scaffolding_intensity)
        
        return RaterResult(
            rater_name="zpd_efficiency",
            score=efficiency,
            raw_score=efficiency,
            max_score=1.0,
            details={
                "learning_gain": round(learning_gain, 3),
                "scaffolding_intensity": round(scaffolding_intensity, 3),
                "efficiency": round(efficiency, 3),
                "tutor_turns": len(tutor_turns),
                "interpretation": self._interpret(efficiency, scaffolding_intensity, learning_gain)
            }
        )
    
    def _measure_scaffolding(self, tutor_turns: list) -> float:
        """
        Measure scaffolding intensity 0-1.
        Higher = more scaffolding provided.
        """
        total_words = sum(len(t["content"].split()) for t in tutor_turns)
        num_turns = len(tutor_turns)
        
        # Count scaffolding indicators
        scaffolding_phrases = [
            "think about", "what if", "try", "consider", "hint",
            "remember", "notice", "what happens", "can you",
            "let's break", "step by step", "first"
        ]
        direct_answer_phrases = [
            "the answer is", "it equals", "you get", "the result is",
            "the solution is", "that gives us"
        ]
        
        scaffolding_count = 0
        direct_count = 0
        
        for t in tutor_turns:
            content_lower = t["content"].lower()
            scaffolding_count += sum(1 for p in scaffolding_phrases if p in content_lower)
            direct_count += sum(1 for p in direct_answer_phrases if p in content_lower)
        
        # Intensity based on volume and scaffolding type
        volume_factor = min(1.0, total_words / (num_turns * 100))
        scaffolding_ratio = scaffolding_count / max(1, scaffolding_count + direct_count)
        
        # High scaffolding = lots of guided questions (intensity is amount of help)
        intensity = volume_factor * 0.5 + (1 - scaffolding_ratio) * 0.3 + (num_turns / 10) * 0.2
        return min(1.0, intensity)
    
    def _interpret(self, efficiency: float, scaffolding: float, gain: float) -> str:
        if gain < 0.2:
            return "Low learning gain - student didn't improve much"
        if efficiency > 0.7:
            return "Excellent ZPD targeting - high learning with efficient scaffolding"
        if efficiency > 0.4:
            return "Good ZPD targeting - reasonable learning-to-scaffolding ratio"
        if scaffolding > 0.7:
            return "Over-scaffolded - too much help for the learning achieved"
        return "Under-scaffolded - student needed more targeted support"


class FlowFrictionDetector:
    """
    Analyzes conversation flow for signs of productive struggle vs. unproductive friction.
    
    Flow indicators: progressive understanding, engagement, building on hints
    Friction indicators: frustration, repetition, confusion spirals, giving up
    """
    
    def score(self, session: dict) -> RaterResult:
        turns = session.get("turns", [])
        
        if len(turns) < 2:
            return RaterResult("flow_friction", 0.5, 0.5, 1, {"error": "too few turns"})
        
        flow_signals = 0
        friction_signals = 0
        details = {"flow_markers": [], "friction_markers": []}
        
        student_turns = [t for t in turns if t["role"] == "student"]
        
        for i, turn in enumerate(student_turns):
            content = turn["content"].lower()
            
            # Flow signals
            if any(w in content for w in ["oh i see", "aha", "makes sense", "got it", "right"]):
                flow_signals += 1
                details["flow_markers"].append(f"Turn {i}: understanding signal")
            
            if any(w in content for w in ["so then", "that means", "because", "therefore"]):
                flow_signals += 1
                details["flow_markers"].append(f"Turn {i}: reasoning chain")
            
            if "?" in content and any(w in content for w in ["why", "how", "what if", "is this"]):
                flow_signals += 0.5
                details["flow_markers"].append(f"Turn {i}: productive question")
            
            # Friction signals
            if any(w in content for w in ["don't get", "confused", "lost", "don't understand"]):
                friction_signals += 1
                details["friction_markers"].append(f"Turn {i}: confusion")
            
            if any(w in content for w in ["give up", "too hard", "just tell me", "show me the answer"]):
                friction_signals += 2
                details["friction_markers"].append(f"Turn {i}: giving up")
            
            # Repetition detection
            if i > 0 and self._is_repetitive(student_turns[i-1]["content"], content):
                friction_signals += 1
                details["friction_markers"].append(f"Turn {i}: repetition")
        
        # Engagement: longer sessions with flow are good
        total = flow_signals + friction_signals
        if total == 0:
            score = 0.5  # Neutral
        else:
            score = flow_signals / total
        
        return RaterResult(
            rater_name="flow_friction",
            score=round(score, 3),
            raw_score=round(score, 3),
            max_score=1.0,
            details={
                "flow_signals": flow_signals,
                "friction_signals": friction_signals,
                "flow_ratio": round(score, 3),
                **details
            }
        )
    
    def _is_repetitive(self, prev: str, curr: str) -> bool:
        prev_words = set(prev.lower().split())
        curr_words = set(curr.lower().split())
        if not prev_words or not curr_words:
            return False
        overlap = len(prev_words & curr_words) / max(len(prev_words), len(curr_words))
        return overlap > 0.7


class FactualAccuracyChecker:
    """
    Checks tutor responses against reference solutions for factual accuracy.
    
    Catches:
    - Wrong formulas
    - Incorrect calculations
    - Misleading explanations
    """
    
    def score(self, session: dict) -> RaterResult:
        turns = session.get("turns", [])
        task = session.get("task", {})
        
        tutor_turns = [t for t in turns if t["role"] == "tutor"]
        if not tutor_turns:
            return RaterResult("factual_accuracy", 0, 0, 1, {"error": "no tutor turns"})
        
        correct_answer = task.get("correct_answer", "")
        solution_steps = task.get("solution_steps", [])
        misconceptions = task.get("common_misconceptions", [])
        
        errors_found = []
        correct_elements = []
        
        for i, turn in enumerate(tutor_turns):
            content = turn["content"]
            
            # Check: does tutor ever state a misconception as fact?
            for m in misconceptions:
                error_val = str(m.get("error", "")).lower()
                if error_val and error_val in content.lower():
                    # Check if it's being corrected or stated as true
                    if not any(w in content.lower() for w in ["incorrect", "wrong", "not", "careful", "mistake", "actually"]):
                        errors_found.append(f"Turn {i}: States misconception '{error_val}' without correction")
            
            # Check: does tutor mention correct answer/steps?
            if correct_answer.lower() in content.lower():
                correct_elements.append(f"Turn {i}: Mentions correct answer")
            
            for step in solution_steps:
                if step.lower() in content.lower():
                    correct_elements.append(f"Turn {i}: References correct step")
        
        total_checks = len(errors_found) + max(1, len(correct_elements))
        accuracy = len(correct_elements) / total_checks if total_checks > 0 else 0.5
        
        # Penalize for errors
        if errors_found:
            accuracy = max(0, accuracy - 0.3 * len(errors_found))
        
        return RaterResult(
            rater_name="factual_accuracy",
            score=round(min(1.0, accuracy), 3),
            raw_score=round(accuracy, 3),
            max_score=1.0,
            details={
                "errors_found": errors_found,
                "correct_elements": correct_elements[:5],
                "error_count": len(errors_found),
            }
        )


class RubricEvaluator:
    """
    Multi-dimensional rubric scoring for tutoring quality.
    
    Dimensions:
    1. Scaffolding quality (does tutor guide rather than tell?)
    2. Misconception handling (does tutor detect and address misconceptions?)
    3. Encouragement/affect (does tutor support student motivation?)
    4. Explanation clarity (are explanations clear and appropriate level?)
    5. Adaptive teaching (does tutor adjust based on student responses?)
    """
    
    DIMENSIONS = [
        "scaffolding_quality",
        "misconception_handling", 
        "encouragement",
        "explanation_clarity",
        "adaptive_teaching"
    ]
    
    def score(self, session: dict) -> RaterResult:
        turns = session.get("turns", [])
        task = session.get("task", {})
        
        tutor_turns = [t for t in turns if t["role"] == "tutor"]
        student_turns = [t for t in turns if t["role"] == "student"]
        
        scores = {}
        
        # 1. Scaffolding quality
        scores["scaffolding_quality"] = self._score_scaffolding(tutor_turns)
        
        # 2. Misconception handling
        scores["misconception_handling"] = self._score_misconception_handling(
            tutor_turns, student_turns, task
        )
        
        # 3. Encouragement
        scores["encouragement"] = self._score_encouragement(tutor_turns)
        
        # 4. Explanation clarity
        scores["explanation_clarity"] = self._score_clarity(tutor_turns)
        
        # 5. Adaptive teaching
        scores["adaptive_teaching"] = self._score_adaptiveness(tutor_turns, student_turns)
        
        avg_score = sum(scores.values()) / len(scores) if scores else 0
        
        return RaterResult(
            rater_name="rubric",
            score=round(avg_score, 3),
            raw_score=round(avg_score * 5, 3),
            max_score=5.0,
            details={
                "dimension_scores": {k: round(v, 3) for k, v in scores.items()},
                "overall": round(avg_score, 3),
            }
        )
    
    def _score_scaffolding(self, tutor_turns: list) -> float:
        """Does the tutor guide rather than directly give answers?"""
        if not tutor_turns:
            return 0
        
        question_count = 0
        direct_answer_count = 0
        
        for t in tutor_turns:
            c = t["content"].lower()
            if "?" in c:
                question_count += 1
            if any(p in c for p in ["the answer is", "it equals", "you get", "the solution is"]):
                direct_answer_count += 1
            if any(p in c for p in ["think about", "what if", "try", "can you"]):
                question_count += 0.5
        
        total = question_count + direct_answer_count
        if total == 0:
            return 0.5
        return min(1.0, question_count / total)
    
    def _score_misconception_handling(self, tutor_turns, student_turns, task) -> float:
        """Does the tutor detect and address student misconceptions?"""
        misconceptions = task.get("common_misconceptions", [])
        if not misconceptions or not student_turns:
            return 0.5  # N/A
        
        # Check if student expressed a misconception
        student_had_misconception = False
        for st in student_turns:
            for m in misconceptions:
                if str(m.get("error", "")).lower() in st["content"].lower():
                    student_had_misconception = True
                    break
        
        if not student_had_misconception:
            return 0.7  # No misconception to handle, neutral-good
        
        # Check if tutor addressed it
        addressed = False
        for tt in tutor_turns:
            c = tt["content"].lower()
            if any(w in c for w in ["actually", "careful", "not quite", "common mistake",
                                     "watch out", "that's a", "misconception"]):
                addressed = True
                break
        
        return 0.9 if addressed else 0.2
    
    def _score_encouragement(self, tutor_turns: list) -> float:
        """Does the tutor support student motivation?"""
        if not tutor_turns:
            return 0
        
        encouraging_phrases = [
            "good", "great", "nice", "well done", "excellent", "right",
            "you're on the right track", "keep going", "almost",
            "that's a good", "interesting", "close"
        ]
        
        count = 0
        for t in tutor_turns:
            c = t["content"].lower()
            count += sum(1 for p in encouraging_phrases if p in c)
        
        # Normalize: expect ~1 encouragement per 2 turns
        expected = len(tutor_turns) / 2
        return min(1.0, count / max(1, expected))
    
    def _score_clarity(self, tutor_turns: list) -> float:
        """Are explanations clear and at appropriate level?"""
        if not tutor_turns:
            return 0
        
        scores = []
        for t in tutor_turns:
            content = t["content"]
            words = content.split()
            
            # Sentence length: shorter is often clearer for tutoring
            avg_word_len = sum(len(w) for w in words) / max(1, len(words))
            
            # Penalize very long responses (walls of text)
            length_score = 1.0 if len(words) < 80 else max(0.3, 1.0 - (len(words) - 80) / 200)
            
            # Reward structured explanations (numbered steps, etc.)
            has_structure = bool(re.search(r'\d[\.\)]\s', content)) or "step" in content.lower()
            structure_bonus = 0.1 if has_structure else 0
            
            scores.append(min(1.0, length_score + structure_bonus))
        
        return sum(scores) / len(scores) if scores else 0
    
    def _score_adaptiveness(self, tutor_turns: list, student_turns: list) -> float:
        """Does the tutor adjust based on student responses?"""
        if len(tutor_turns) < 2 or not student_turns:
            return 0.5  # Not enough data
        
        # Check if later tutor responses reference student's words
        adaptation_signals = 0
        for i, tt in enumerate(tutor_turns[1:], 1):
            c = tt["content"].lower()
            # Referencing what student said
            if any(w in c for w in ["you said", "you mentioned", "your answer", "you wrote",
                                     "i see that", "based on your"]):
                adaptation_signals += 1
            # Changing approach
            if any(w in c for w in ["let me try", "another way", "different approach",
                                     "let's think about it differently", "simpler"]):
                adaptation_signals += 1
        
        expected = max(1, len(tutor_turns) - 1)
        return min(1.0, adaptation_signals / expected)


def run_all_raters(session: dict) -> dict:
    """Run all raters on a session and return combined results."""
    raters = [
        PrePostScorer(),
        ZPDEfficiencyCalculator(),
        FlowFrictionDetector(),
        FactualAccuracyChecker(),
        RubricEvaluator(),
    ]
    
    results = {}
    for rater in raters:
        result = rater.score(session)
        results[result.rater_name] = {
            "score": result.score,
            "raw_score": result.raw_score,
            "max_score": result.max_score,
            "details": result.details,
        }
    
    # Overall score: weighted average
    weights = {
        "pre_post": 0.25,
        "zpd_efficiency": 0.20,
        "flow_friction": 0.15,
        "factual_accuracy": 0.25,
        "rubric": 0.15,
    }
    
    overall = sum(
        results[name]["score"] * weight 
        for name, weight in weights.items() 
        if name in results
    )
    
    results["overall"] = {
        "score": round(overall, 3),
        "weights": weights,
    }
    
    return results
