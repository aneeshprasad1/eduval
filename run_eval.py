#!/usr/bin/env python3
"""
EduVal v0 - Run evaluation harness

Usage:
    python run_eval.py                          # Run all tasks, all personas, rule-based tutor
    python run_eval.py --verbose                # Show conversation details
    python run_eval.py --subject math           # Math tasks only
    python run_eval.py --persona diego priya    # Specific personas
    python run_eval.py --style direct           # Direct-answer tutor (baseline comparison)
    python run_eval.py --output results.json    # Save results to file
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from harness.evaluator import EduvalEvaluator, RuleBasedTutor, print_report


def main():
    parser = argparse.ArgumentParser(description="EduVal v0 Evaluation Harness")
    parser.add_argument("--subject", choices=["math", "physics"], help="Filter by subject")
    parser.add_argument("--topic", help="Filter by topic (e.g., algebra, mechanics)")
    parser.add_argument("--difficulty", type=int, help="Filter by difficulty level")
    parser.add_argument("--persona", nargs="+", help="Persona names to test")
    parser.add_argument("--style", choices=["socratic", "direct", "minimal"], 
                       default="socratic", help="Tutor style")
    parser.add_argument("--max-turns", type=int, default=8, help="Max conversation turns")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show conversations")
    parser.add_argument("--output", "-o", help="Save results to JSON file")
    parser.add_argument("--tasks-dir", help="Custom tasks directory")
    
    args = parser.parse_args()
    
    # Build task filter
    task_filter = {}
    if args.subject:
        task_filter["subject"] = args.subject
    if args.topic:
        task_filter["topic"] = args.topic
    if args.difficulty:
        task_filter["difficulty"] = args.difficulty
    
    # Create tutor
    tutor = RuleBasedTutor(style=args.style)
    
    # Run evaluation
    evaluator = EduvalEvaluator(tasks_dir=args.tasks_dir)
    results = evaluator.evaluate(
        tutor=tutor,
        persona_names=args.persona,
        task_filter=task_filter or None,
        max_turns=args.max_turns,
        verbose=args.verbose,
    )
    
    # Print report
    print_report(results)
    
    # Save if requested
    if args.output:
        # Remove non-serializable task data from results
        for r in results["results"]:
            if "task" in r.get("scores", {}).get("factual_accuracy", {}).get("details", {}):
                pass  # already clean
        
        output_path = Path(args.output)
        with open(output_path, "w") as f:
            json.dump(results, f, indent=2, default=str)
        print(f"\nResults saved to {output_path}")


if __name__ == "__main__":
    main()
