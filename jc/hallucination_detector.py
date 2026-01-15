"""
JC-Agent Hallucination Detector

This module provides a utility to compare a user's answer with an expert answer for factual consistency, using an LLM-based classifier.
"""

from typing import Dict

PROMPT = """\
You are comparing a submitted answer to an expert answer on a given question. Here is the data:
[BEGIN DATA]
************
[Question]: {{input}}
************
[Expert]: {{expected}}
************
[Submission]: {{output}}
************
[END DATA]
 
Compare the factual content of the submitted answer with the expert answer. Ignore any differences in style, grammar, or punctuation.
The submitted answer may either be a subset or superset of the expert answer, or it may conflict with it. Determine which case applies. Answer the question by selecting one of the following options:
(A) The submitted answer is a subset of the expert answer and is fully consistent with it.
(B) The submitted answer is a superset of the expert answer and is fully consistent with it.
(C) The submitted answer contains all the same details as the expert answer.
(D) There is a disagreement between the submitted answer and the expert answer.
(E) The answers differ, but these differences don't matter from the perspective of factuality.
 
Answer the question by calling `select_choice` with your reasoning in a step-by-step matter to be
sure that your conclusion is correct. Avoid simply stating the correct answer at the outset. Select a
single choice by setting the `choice` parameter to a single choice from A, B, C, D, or E.
"""

class HallucinationDetector:
    def __init__(self, llm_classifier):
        self.classifier = llm_classifier

    def evaluate(self, question: str, expert: str, submission: str) -> Dict:
        data = {
            "input": question,
            "expected": expert,
            "output": submission
        }
        return self.classifier.classify(data)

# Example usage (requires an LLMClassifier implementation):
# from autoevals import LLMClassifier
# detector = HallucinationDetector(LLMClassifier(
#     name="JC Hallucination Detector",
#     prompt_template=PROMPT,
#     choice_scores={"A": 0.5, "B": 0, "C": 1, "D": 0, "E": 1},
#     use_cot=True,
# ))
# result = detector.evaluate("What is AI?", "AI is artificial intelligence.", "AI is intelligence by machines.")
# print(result)
