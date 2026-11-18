
import json
import re
import time
from pathlib import Path
from statistics import mean

from app.rag import answer_with_rag

BASE_DIR = Path(__file__).resolve().parent.parent
EVAL_FILE = BASE_DIR / "eval" / "eval_set.json"
RESULT_FILE = BASE_DIR / "eval" / "answer_eval_results.json"
REPORT_FILE = BASE_DIR / "eval" / "answer_eval_report.md"


def normalize(text):
    return re.sub(r"\s+", " ", text.lower()).strip()


def evaluate_question(item):
    question = item["question"]
    expected_answerable = item["answerable"]

    start = time.perf_counter()

    try:
        result = answer_with_rag(question, top_k=5)
        latency = round(time.perf_counter() - start, 3)

        answer = result.get("answer", "")
        citations = result.get("citations", [])
        confidence = result.get("confidence", "low")

        normalized_answer = normalize(answer)
        refused = normalized_answer == "i don't know"

        if expected_answerable:
            expected_facts = item.get("expected_facts", [])
            if expected_facts:
                matched_facts = [
                    fact for fact in expected_facts
                    if normalize(fact) in normalized_answer
                ]
                answer_score = len(matched_facts) / len(expected_facts)
                answer_correct = answer_score >= 0.5
            else:
                answer_score = None
                answer_correct = None

            refusal_correct = not refused

        else:
            answer_score = None
            answer_correct = None
            refusal_correct = refused

        references = [
            int(number)
            for number in re.findall(r"\[(\d+)\]", answer)
        ]

        retrieved_count = result.get("retrieved_chunks", 0)

        citation_valid = all(
            1 <= reference <= retrieved_count
            for reference in references
        )

        citation_coverage = (
            len(set(references)) / retrieved_count
            if retrieved_count else 0
        )

        return {
            "id": item["id"],
            "question": question,
            "answerable": expected_answerable,
            "answer": answer,
            "answer_score": answer_score,
            "answer_correct": answer_correct,
            "refused": refused,
            "refusal_correct": refusal_correct,
            "citations": citations,
            "citation_references": references,
            "citation_valid": citation_valid,
            "citation_coverage": round(citation_coverage, 4),
            "retrieved_chunks": retrieved_count,
            "confidence": confidence,
            "latency_seconds": latency,
            "api_success": True,
            "error": None
        }

    except Exception as error:
        latency = round(time.perf_counter() - start, 3)

        return {
            "id": item["id"],
            "question": question,
            "answerable": expected_answerable,
            "answer": None,
            "answer_score": None,
            "answer_correct": None,
            "refused": None,
            "refusal_correct": False,
            "citations": [],
            "citation_references": [],
            "citation_valid": False,
            "citation_coverage": 0,
            "retrieved_chunks": 0,
            "confidence": "low",
            "latency_seconds": latency,
            "api_success": False,
            "error": str(error)
        }


def main():
    with EVAL_FILE.open("r", encoding="utf-8") as file:
        questions = json.load(file)

    results = []

    print("\nAQIExplainer Answer Evaluation")
    print("=" * 55)

    for item in questions:
        print(f"\nRunning {item['id']}: {item['question']}")

        result = evaluate_question(item)
        results.append(result)

        print("API success:", result["api_success"])
        print("Answer:", result["answer"])
        print("Refusal correct:", result["refusal_correct"])
        print("Citation valid:", result["citation_valid"])
        print("Latency:", result["latency_seconds"], "seconds")

    successful = [r for r in results if r["api_success"]]
    answerable = [r for r in successful if r["answerable"]]
    unanswerable = [r for r in successful if not r["answerable"]]

    refusal_accuracy = (
        mean([r["refusal_correct"] for r in successful]) * 100
        if successful else 0
    )

    answer_scores = [
        r["answer_score"] for r in answerable
        if r["answer_score"] is not None
    ]

    answer_accuracy = (
        mean([r["answer_correct"] for r in answerable
              if r["answer_correct"] is not None]) * 100
        if any(r["answer_correct"] is not None for r in answerable)
        else None
    )

    citation_validity = (
        mean([r["citation_valid"] for r in successful]) * 100
        if successful else 0
    )

    avg_latency = (
        mean([r["latency_seconds"] for r in successful])
        if successful else 0
    )

    summary = {
        "total_questions": len(questions),
        "successful_api_calls": len(successful),
        "failed_api_calls": len(questions) - len(successful),
        "api_success_rate": round(
            len(successful) / len(questions) * 100, 2
        ) if questions else 0,
        "answerable_questions": len(answerable),
        "unanswerable_questions": len(unanswerable),
        "answer_fact_coverage": round(mean(answer_scores) * 100, 2)
        if answer_scores else None,
        "answer_accuracy_proxy": round(answer_accuracy, 2)
        if answer_accuracy is not None else None,
        "refusal_accuracy": round(refusal_accuracy, 2),
        "citation_reference_validity": round(citation_validity, 2),
        "average_latency_seconds": round(avg_latency, 3),
        "results": results
    }

    RESULT_FILE.write_text(
        json.dumps(summary, indent=4),
        encoding="utf-8"
    )

    report = [
        "# AQIExplainer Answer Evaluation",
        "",
        "## Summary",
        "",
        f"- Total questions: {summary['total_questions']}",
        f"- Successful API calls: {summary['successful_api_calls']}",
        f"- Failed API calls: {summary['failed_api_calls']}",
        f"- API success rate: {summary['api_success_rate']}%",
        f"- Answer fact coverage: {summary['answer_fact_coverage']}",
        f"- Answer accuracy proxy: {summary['answer_accuracy_proxy']}",
        f"- Refusal accuracy: {summary['refusal_accuracy']}%",
        f"- Citation reference validity: {summary['citation_reference_validity']}%",
        f"- Average latency: {summary['average_latency_seconds']} seconds",
        "",
        "## Question-level results",
        "",
        "| ID | API | Answer correct | Refusal correct | Citations valid | Latency (s) |",
        "|---|---|---|---|---|---:|"
    ]

    for r in results:
        report.append(
            f"| {r['id']} | {r['api_success']} "
            f"| {r['answer_correct']} "
            f"| {r['refusal_correct']} "
            f"| {r['citation_valid']} "
            f"| {r['latency_seconds']} |"
        )

    report.extend([
        "",
        "## Methodology and limitations",
        "",
        "- Answer fact coverage is only calculated when expected_facts are provided.",
        "- Exact phrase matching is a baseline, not semantic answer evaluation.",
        "- Answer accuracy proxy uses a 50% expected-fact threshold.",
        "- Refusal accuracy checks whether answerable questions receive an answer and unanswerable questions receive exactly 'I don't know'.",
        "- Citation reference validity checks numbering against retrieved chunk count, not factual support.",
        "- Citation coverage is the fraction of retrieved chunks referenced by the answer.",
        "- API errors are counted separately from answer quality.",
        "- Latency measures the complete answer_with_rag call."
    ])

    REPORT_FILE.write_text("\n".join(report), encoding="utf-8")

    print("\n" + "=" * 55)
    print("EVALUATION SUMMARY")
    print("=" * 55)

    for key, value in summary.items():
        if key != "results":
            print(f"{key}: {value}")

    print("\nReports saved:")
    print(RESULT_FILE)
    print(REPORT_FILE)


if __name__ == "__main__":
    main()
