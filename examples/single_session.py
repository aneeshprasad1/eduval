#!/usr/bin/env python3
"""Run and inspect a single tutoring session in detail."""

import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from harness.evaluator import run_session, RuleBasedTutor, load_tasks
from harness.raters import run_all_raters

def main():
    tasks = load_tasks()
    # Pick a mid-difficulty task
    task = next(t for t in tasks if t["id"] == "math-calc-003")
    
    tutor = RuleBasedTutor(style="socratic")
    session = run_session(task, tutor, persona_name="priya", max_turns=8, verbose=True)
    
    print("\n" + "=" * 60)
    print("AUTO-RATER SCORES")
    print("=" * 60)
    
    scores = run_all_raters(session)
    for rater_name, result in scores.items():
        if rater_name == "overall":
            print(f"\n  OVERALL: {result['score']:.3f}")
        else:
            print(f"\n  {rater_name}:")
            print(f"    Score: {result['score']:.3f}")
            for k, v in result.get("details", {}).items():
                print(f"    {k}: {v}")
    
    print(f"\nPersona state: {json.dumps(session['persona_state'], indent=2)}")

if __name__ == "__main__":
    main()
