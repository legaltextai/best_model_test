"""
MBE Sample Questions API Test Script
Sends questions 7, 11, 18 to Gemini 3 Pro, GPT-5.2, and Claude Opus 4.5
Expects structured output: single letter A, B, C, or D
"""

import json
import os
from typing import Literal
from pydantic import BaseModel
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ============================================================================
# Structured Output Schema
# ============================================================================

class MBEAnswer(BaseModel):
    answer: Literal["A", "B", "C", "D"]

# ============================================================================
# Load Questions
# ============================================================================

def load_questions(filepath: str, question_numbers: list[int]) -> list[dict]:
    """Load specific questions from the MBE JSON file."""
    with open(filepath, "r") as f:
        data = json.load(f)

    questions = []
    for q in data["questions"]:
        if q["question_number"] in question_numbers:
            questions.append(q)

    return sorted(questions, key=lambda x: x["question_number"])

def format_question_prompt(question: dict) -> str:
    """Format a question for the API prompt."""
    prompt = f"{question['question_text']}\n\n{question['question_stem']}\n\n"
    for choice in question["choices"]:
        prompt += f"({choice['label']}) {choice['text']}\n"
    return prompt

# ============================================================================
# Google Gemini API (gemini-3-pro-preview)
# ============================================================================

def query_gemini(questions: list[dict]) -> dict:
    """
    Query Google Gemini 3 Pro with structured output.
    Requires: pip install google-genai
    Set env var: GOOGLE_API_KEY
    """
    from google import genai
    from google.genai import types

    client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
    results = {}

    for q in questions:
        prompt = format_question_prompt(q)

        response = client.models.generate_content(
            model="gemini-3-pro-preview",
            contents=f"Answer the following multiple choice question. Respond with ONLY the letter of your answer (A, B, C, or D).\n\n{prompt}",
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=MBEAnswer,
            ),
        )

        # Parse the structured response
        answer_data = json.loads(response.text)
        results[q["question_number"]] = answer_data["answer"]
        print(f"Gemini - Q{q['question_number']}: {answer_data['answer']}")

    return results

# ============================================================================
# OpenAI API (gpt-5.2)
# ============================================================================

def query_openai(questions: list[dict]) -> dict:
    """
    Query OpenAI GPT-5.2 with structured output.
    Requires: pip install openai
    Set env var: OPENAI_API_KEY
    """
    from openai import OpenAI

    client = OpenAI()
    results = {}

    for q in questions:
        prompt = format_question_prompt(q)

        response = client.chat.completions.create(
            model="gpt-5.2",
            messages=[
                {
                    "role": "user",
                    "content": f"Answer the following multiple choice question. Respond with ONLY the letter of your answer (A, B, C, or D).\n\n{prompt}"
                }
            ],
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "mbe_answer",
                    "strict": True,
                    "schema": {
                        "type": "object",
                        "properties": {
                            "answer": {
                                "type": "string",
                                "enum": ["A", "B", "C", "D"]
                            }
                        },
                        "required": ["answer"],
                        "additionalProperties": False
                    }
                }
            }
        )

        # Parse the structured response
        answer_data = json.loads(response.choices[0].message.content)
        results[q["question_number"]] = answer_data["answer"]
        print(f"OpenAI - Q{q['question_number']}: {answer_data['answer']}")

    return results

# ============================================================================
# Anthropic Claude API (claude-opus-4-5-20251101)
# ============================================================================

def query_claude(questions: list[dict]) -> dict:
    """
    Query Anthropic Claude Opus 4.5 with tool-based structured output.
    Requires: pip install anthropic
    Set env var: ANTHROPIC_API_KEY
    """
    from anthropic import Anthropic

    client = Anthropic()
    results = {}

    # Define tool for structured output
    answer_tool = {
        "name": "submit_answer",
        "description": "Submit your answer to the multiple choice question",
        "input_schema": {
            "type": "object",
            "properties": {
                "answer": {
                    "type": "string",
                    "enum": ["A", "B", "C", "D"],
                    "description": "The letter of your answer choice"
                }
            },
            "required": ["answer"]
        }
    }

    for q in questions:
        prompt = format_question_prompt(q)

        response = client.messages.create(
            model="claude-opus-4-5-20251101",
            max_tokens=100,
            tools=[answer_tool],
            tool_choice={"type": "tool", "name": "submit_answer"},
            messages=[
                {
                    "role": "user",
                    "content": f"Answer the following multiple choice question. Use the submit_answer tool to provide your answer (A, B, C, or D).\n\n{prompt}"
                }
            ]
        )

        # Extract answer from tool use
        for block in response.content:
            if block.type == "tool_use" and block.name == "submit_answer":
                results[q["question_number"]] = block.input["answer"]
                print(f"Claude - Q{q['question_number']}: {block.input['answer']}")
                break

    return results

# ============================================================================
# Correct Answers
# ============================================================================

CORRECT_ANSWERS = {
    1: "B",
    2: "C",
    3: "D",
    4: "A",
    5: "B",
    6: "A",
    7: "C",
    8: "D",
    9: "A",
    10: "B",
    11: "C",
    12: "A",
    13: "B",
    14: "B",
    15: "C",
    16: "A",
    17: "D",
    18: "D",
    19: "B",
    20: "C",
    21: "B"
}

# ============================================================================
# Comparison Function
# ============================================================================

def compare_results(all_results: dict, correct_answers: dict) -> dict:
    """Compare model responses against correct answers."""
    comparison = {}

    for provider, results in all_results.items():
        comparison[provider] = {
            "correct": 0,
            "incorrect": 0,
            "missing": 0,
            "details": {}
        }

        for qnum, correct_ans in correct_answers.items():
            model_ans = results.get(qnum)
            if model_ans is None:
                comparison[provider]["missing"] += 1
                comparison[provider]["details"][qnum] = {"model": None, "correct": correct_ans, "result": "MISSING"}
            elif model_ans == correct_ans:
                comparison[provider]["correct"] += 1
                comparison[provider]["details"][qnum] = {"model": model_ans, "correct": correct_ans, "result": "CORRECT"}
            else:
                comparison[provider]["incorrect"] += 1
                comparison[provider]["details"][qnum] = {"model": model_ans, "correct": correct_ans, "result": "INCORRECT"}

        total = len(correct_answers)
        comparison[provider]["accuracy"] = f"{comparison[provider]['correct']}/{total} ({100*comparison[provider]['correct']/total:.1f}%)"

    return comparison

# ============================================================================
# Main Execution
# ============================================================================

def main():
    # Configuration
    questions_file = "/Users/mitch/fine_tune/MBE_sample/mbe_sample_questions.json"
    target_questions = list(range(1, 22))  # All 21 questions

    # Load questions
    questions = load_questions(questions_file, target_questions)
    print(f"Loaded {len(questions)} questions: {[q['question_number'] for q in questions]}\n")

    # Store all results
    all_results = {
        "gemini": {},
        "openai": {},
        "claude": {}
    }

    # Query each provider
    print("=" * 50)
    print("Querying Gemini 3 Pro...")
    print("=" * 50)
    try:
        all_results["gemini"] = query_gemini(questions)
    except Exception as e:
        print(f"Gemini error: {e}")

    print("\n" + "=" * 50)
    print("Querying OpenAI GPT-5.2...")
    print("=" * 50)
    try:
        all_results["openai"] = query_openai(questions)
    except Exception as e:
        print(f"OpenAI error: {e}")

    print("\n" + "=" * 50)
    print("Querying Claude Opus 4.5...")
    print("=" * 50)
    try:
        all_results["claude"] = query_claude(questions)
    except Exception as e:
        print(f"Claude error: {e}")

    # Display summary
    print("\n" + "=" * 60)
    print("RESPONSES")
    print("=" * 60)
    print(f"{'Question':<12} {'Correct':<10} {'Gemini':<10} {'OpenAI':<10} {'Claude':<10}")
    print("-" * 52)
    for qnum in target_questions:
        correct_ans = CORRECT_ANSWERS.get(qnum, "-")
        gemini_ans = all_results["gemini"].get(qnum, "-")
        openai_ans = all_results["openai"].get(qnum, "-")
        claude_ans = all_results["claude"].get(qnum, "-")
        print(f"Q{qnum:<11} {correct_ans:<10} {gemini_ans:<10} {openai_ans:<10} {claude_ans:<10}")

    # Compare results
    comparison = compare_results(all_results, CORRECT_ANSWERS)

    # Display comparison
    print("\n" + "=" * 60)
    print("ACCURACY COMPARISON")
    print("=" * 60)
    print(f"{'Provider':<12} {'Accuracy':<15} {'Correct':<10} {'Incorrect':<10} {'Missing':<10}")
    print("-" * 57)
    for provider in ["gemini", "openai", "claude"]:
        c = comparison[provider]
        print(f"{provider.capitalize():<12} {c['accuracy']:<15} {c['correct']:<10} {c['incorrect']:<10} {c['missing']:<10}")

    # Show detailed results
    print("\n" + "=" * 60)
    print("DETAILED RESULTS")
    print("=" * 60)
    for provider in ["gemini", "openai", "claude"]:
        print(f"\n{provider.upper()}:")
        for qnum, detail in comparison[provider]["details"].items():
            status = "✓" if detail["result"] == "CORRECT" else "✗" if detail["result"] == "INCORRECT" else "?"
            print(f"  Q{qnum}: {status} Model={detail['model']} | Correct={detail['correct']}")

    # Save results with comparison
    output_data = {
        "responses": all_results,
        "correct_answers": CORRECT_ANSWERS,
        "comparison": comparison
    }
    output_file = "/Users/mitch/fine_tune/MBE_sample/mbe_api_results.json"
    with open(output_file, "w") as f:
        json.dump(output_data, f, indent=2)
    print(f"\n\nResults saved to {output_file}")

if __name__ == "__main__":
    main()
