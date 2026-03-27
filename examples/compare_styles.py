#!/usr/bin/env python3
"""Compare tutor styles: socratic vs direct vs minimal."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from harness.evaluator import EduvalEvaluator, RuleBasedTutor, print_report

def main():
    evaluator = EduvalEvaluator()
    
    styles = ["socratic", "direct", "minimal"]
    
    for style in styles:
        print(f"\n{'#' * 70}")
        print(f"  TUTOR STYLE: {style.upper()}")
        print(f"{'#' * 70}")
        
        tutor = RuleBasedTutor(style=style)
        results = evaluator.evaluate(
            tutor=tutor,
            persona_names=["diego", "aiden", "maya"],
            task_filter={"subject": "math"},
            max_turns=6,
        )
        print_report(results)

if __name__ == "__main__":
    main()
