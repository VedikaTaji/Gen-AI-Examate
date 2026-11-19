import json
from pathlib import Path

from app.vectorstore import build_index, search_chunks

BASE_DIR = Path(__file__).resolve().parent.parent
EVAL_FILE = BASE_DIR / "eval" / "eval_set.json"
RESULTS_JSON = BASE_DIR / "eval" / "results.json"
RESULTS_MD = BASE_DIR / "eval" / "results.md"


CONFIGURATIONS = [
    {
        "name": "Configuration A",
        "chunk_size": 900,
        "overlap": 150,
        "top_k": 3,
        "collection_name": "aqi_eval_a",
    },
    {
        "name": "Configuration B",
        "chunk_size": 500,
        "overlap": 100,
        "top_k": 5,
        "collection_name": "aqi_eval_b",
    },
]


def load_questions():
    """Load the 15 evaluation questions."""
    with EVAL_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


def evaluate_configuration(config, questions):
    """Build an index and evaluate semantic retrieval."""
    print("\n" + "=" * 55)
    print("Running:", config["name"])
    print("=" * 55)

    # Build a separate ChromaDB collection.
    build_index(
        chunk_size=config["chunk_size"],
        overlap=config["overlap"],
        collection_name=config["collection_name"],
    )

    question_results = []
    total_hits = 0
    total_answerable = 0
    similarity_scores = []

    for question_data in questions:
        question_id = question_data["id"]
        question = question_data["question"]
        expected_keywords = question_data["expected_keywords"]
        answerable = question_data["answerable"]

        print(f"\nEvaluating {question_id}: {question}")

        # Retrieve relevant document chunks.
        hits = search_chunks(
            question=question,
            top_k=config["top_k"],
            collection_name=config["collection_name"],
        )

        retrieved_text = " ".join(hit["text"].lower() for hit in hits)

        # Unanswerable questions are not included in retrieval hit rate.
        if answerable:
            total_answerable += 1

            keyword_hit = any(
                keyword.lower() in retrieved_text for keyword in expected_keywords
            )

            if keyword_hit:
                total_hits += 1

            for hit in hits:
                similarity_scores.append(hit["similarity"])

            status = "HIT" if keyword_hit else "MISS"
        else:
            keyword_hit = None
            status = "UNANSWERABLE - verify abstention separately"

        print("Retrieved chunks:", len(hits))
        print("Evaluation:", status)

        question_results.append(
            {
                "id": question_id,
                "question": question,
                "answerable": answerable,
                "retrieved_chunks": len(hits),
                "keyword_hit": keyword_hit,
                "status": status,
                "sources": [hit["source"] for hit in hits],
            }
        )

    hit_rate = total_hits / total_answerable * 100 if total_answerable else 0

    mean_similarity = (
        sum(similarity_scores) / len(similarity_scores) if similarity_scores else 0
    )

    summary = {
        "name": config["name"],
        "chunk_size": config["chunk_size"],
        "overlap": config["overlap"],
        "top_k": config["top_k"],
        "collection_name": config["collection_name"],
        "total_questions": len(questions),
        "answerable_questions": total_answerable,
        "keyword_hits": total_hits,
        "hit_rate_percent": round(hit_rate, 2),
        "mean_similarity": round(mean_similarity, 4),
        "question_results": question_results,
    }

    print("\nConfiguration summary:")
    print("Keyword hits:", total_hits, "/", total_answerable)
    print("Retrieval hit rate:", round(hit_rate, 2), "%")
    print("Mean similarity:", round(mean_similarity, 4))

    return summary


def save_results(results):
    """Save evaluation results as JSON and Markdown."""
    RESULTS_JSON.write_text(json.dumps(results, indent=4), encoding="utf-8")

    lines = [
        "# AQIExplainer Retrieval Evaluation",
        "",
        "## Configuration Comparison",
        "",
        "| Configuration | Chunk Size | Overlap | Top-k | Keyword Hits | Hit Rate | Mean Similarity |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]

    for result in results["configurations"]:
        lines.append(
            f"| {result['name']} "
            f"| {result['chunk_size']} "
            f"| {result['overlap']} "
            f"| {result['top_k']} "
            f"| {result['keyword_hits']}/{result['answerable_questions']} "
            f"| {result['hit_rate_percent']}% "
            f"| {result['mean_similarity']} |"
        )

    lines.extend(
        [
            "",
            "## Winner",
            "",
            f"**{results['winner']}**",
            "",
            "Winner selected by retrieval hit rate, with mean similarity as a tie-breaker.",
            "",
            "## Q6 Abstention Check",
            "",
            "Q6 is an unanswerable historical-data question. It is excluded from retrieval hit-rate calculations.",
            "Verify that POST /ask returns exactly `I don't know`, with no citations and low confidence.",
            "",
            "## Evaluation Method",
            "",
            "Keyword hit rate measures whether at least one expected keyword appears in the retrieved chunks.",
            "It is a simple retrieval relevance proxy, not a measure of answer correctness.",
            "Mean similarity is the average similarity score of retrieved chunks for answerable questions.",
        ]
    )

    RESULTS_MD.write_text("\n".join(lines), encoding="utf-8")

    print("\nEvaluation reports saved:")
    print(RESULTS_JSON)
    print(RESULTS_MD)


def main():
    questions = load_questions()

    print("Total evaluation questions:", len(questions))

    if len(questions) != 15:
        raise ValueError(f"Expected exactly 15 questions, found {len(questions)}.")

    results = []

    for config in CONFIGURATIONS:
        summary = evaluate_configuration(config, questions)
        results.append(summary)

    # Select winner by hit rate, then mean similarity.
    winner = max(
        results, key=lambda item: (item["hit_rate_percent"], item["mean_similarity"])
    )

    final_results = {"winner": winner["name"], "configurations": results}

    save_results(final_results)

    print("\n" + "=" * 55)
    print("FINAL WINNER:", winner["name"])
    print("=" * 55)


if __name__ == "__main__":
    main()
