
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
        "collection_name": "aqi_eval_a"
    },
    {
        "name": "Configuration B",
        "chunk_size": 500,
        "overlap": 100,
        "top_k": 5,
        "collection_name": "aqi_eval_b"
    }
]


def load_questions():
    with EVAL_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


def get_keyword_groups(question_data):
    """
    Each group represents one required evidence concept.
    A group can contain alternative terms with the same meaning.

    Example:
    [
        ["CPCB", "Central Pollution Control Board"],
        ["AQI"]
    ]
    """
    groups = question_data.get("expected_keyword_groups")

    if groups:
        return groups

    # Backward compatibility with the original Day 8 dataset.
    # Each old keyword is temporarily treated as its own group.
    return [[keyword] for keyword in question_data["expected_keywords"]]


def group_matches(text, group):
    text = text.lower()
    return any(term.lower() in text for term in group)


def calculate_question_metrics(hits, keyword_groups, top_k):
    """
    These are keyword-based evidence metrics.
    They are proxies, not human-verified relevance judgments.
    """
    if not keyword_groups:
        return {
            "precision_at_k": 0,
            "recall_at_k": 0,
            "mrr": 0,
            "matched_groups": 0,
            "total_groups": 0
        }

    matched_groups = set()
    relevant_chunks = 0
    reciprocal_rank = 0

    for rank, hit in enumerate(hits, start=1):
        text = hit["text"]

        matched_in_chunk = [
            index
            for index, group in enumerate(keyword_groups)
            if group_matches(text, group)
        ]

        if matched_in_chunk:
            relevant_chunks += 1

            if reciprocal_rank == 0:
                reciprocal_rank = 1 / rank

            matched_groups.update(matched_in_chunk)

    precision = relevant_chunks / top_k if top_k else 0
    recall = len(matched_groups) / len(keyword_groups)

    return {
        "precision_at_k": round(precision, 4),
        "recall_at_k": round(recall, 4),
        "mrr": round(reciprocal_rank, 4),
        "matched_groups": len(matched_groups),
        "total_groups": len(keyword_groups)
    }


def evaluate_configuration(config, questions):
    print("\n" + "=" * 60)
    print("Running:", config["name"])
    print("=" * 60)

    build_index(
        chunk_size=config["chunk_size"],
        overlap=config["overlap"],
        collection_name=config["collection_name"]
    )

    question_results = []
    answerable_results = []
    similarity_scores = []

    for question_data in questions:
        question_id = question_data["id"]
        question = question_data["question"]
        answerable = question_data["answerable"]
        keyword_groups = get_keyword_groups(question_data)

        print(f"\nEvaluating {question_id}: {question}")

        hits = search_chunks(
            question=question,
            top_k=config["top_k"],
            collection_name=config["collection_name"]
        )

        retrieved_text = " ".join(
            hit["text"].lower() for hit in hits
        )

        if answerable:
            metrics = calculate_question_metrics(
                hits,
                keyword_groups,
                config["top_k"]
            )

            keyword_hit = any(
                group_matches(retrieved_text, group)
                for group in keyword_groups
            )

            for hit in hits:
                similarity_scores.append(hit["similarity"])

            answerable_results.append(metrics)

            status = "HIT" if keyword_hit else "MISS"

            print("Evaluation:", status)
            print("Precision@K:", metrics["precision_at_k"])
            print("Recall@K:", metrics["recall_at_k"])
            print("MRR:", metrics["mrr"])

        else:
            metrics = {
                "precision_at_k": None,
                "recall_at_k": None,
                "mrr": None,
                "matched_groups": 0,
                "total_groups": len(keyword_groups)
            }
            keyword_hit = None
            status = "UNANSWERABLE - abstention evaluated separately"

            print("Evaluation:", status)

        question_results.append({
            "id": question_id,
            "question": question,
            "answerable": answerable,
            "retrieved_chunks": len(hits),
            "keyword_hit": keyword_hit,
            **metrics,
            "status": status,
            "sources": [hit["source"] for hit in hits],
            "similarities": [
                hit["similarity"] for hit in hits
            ]
        })

    total_answerable = len(answerable_results)

    keyword_hits = sum(
        1 for result in question_results
        if result["answerable"] and result["keyword_hit"]
    )

    def average(metric):
        if not answerable_results:
            return 0

        return round(
            sum(item[metric] for item in answerable_results)
            / total_answerable,
            4
        )

    hit_rate = (
        keyword_hits / total_answerable * 100
        if total_answerable else 0
    )

    mean_similarity = (
        sum(similarity_scores) / len(similarity_scores)
        if similarity_scores else 0
    )

    summary = {
        "name": config["name"],
        "chunk_size": config["chunk_size"],
        "overlap": config["overlap"],
        "top_k": config["top_k"],
        "collection_name": config["collection_name"],
        "total_questions": len(questions),
        "answerable_questions": total_answerable,
        "keyword_hits": keyword_hits,
        "hit_rate_percent": round(hit_rate, 2),
        "precision_at_k": average("precision_at_k"),
        "recall_at_k": average("recall_at_k"),
        "mrr": average("mrr"),
        "mean_similarity": round(mean_similarity, 4),
        "question_results": question_results
    }

    print("\nConfiguration summary:")
    print("Keyword hit rate:", summary["hit_rate_percent"], "%")
    print("Precision@K:", summary["precision_at_k"])
    print("Recall@K:", summary["recall_at_k"])
    print("MRR:", summary["mrr"])
    print("Mean similarity:", summary["mean_similarity"])

    return summary


def save_results(results):
    RESULTS_JSON.write_text(
        json.dumps(results, indent=4),
        encoding="utf-8"
    )

    lines = [
        "# AQIExplainer Advanced Retrieval Evaluation",
        "",
        "## Configuration Comparison",
        "",
        "| Configuration | Chunk | Overlap | Top-k | Keyword Hit Rate | Precision@K | Recall@K | MRR | Mean Similarity |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|"
    ]

    for result in results["configurations"]:
        lines.append(
            f"| {result['name']} "
            f"| {result['chunk_size']} "
            f"| {result['overlap']} "
            f"| {result['top_k']} "
            f"| {result['hit_rate_percent']}% "
            f"| {result['precision_at_k']} "
            f"| {result['recall_at_k']} "
            f"| {result['mrr']} "
            f"| {result['mean_similarity']} |"
        )

    lines.extend([
        "",
        "## Winner",
        "",
        f"**{results['winner']}**",
        "",
        "Winner selected using Recall@K, Precision@K, and MRR.",
        "",
        "## Evaluation Method and Limitations",
        "",
        "- Keyword hit rate checks whether at least one expected evidence group appears in retrieved text.",
        "- Precision@K measures the proportion of retrieved chunks matching at least one expected evidence group.",
        "- Recall@K measures the proportion of expected evidence groups found in retrieved chunks.",
        "- MRR measures the reciprocal rank of the first chunk matching an expected evidence group.",
        "- Mean similarity is a retrieval-distance diagnostic, not proof of relevance.",
        "- These metrics use keyword matching as a relevance proxy. They are not human-verified semantic relevance or answer correctness.",
        "",
        "## Unanswerable Questions",
        "",
        "Unanswerable questions are excluded from retrieval quality averages.",
        "Their answer refusal behavior must be evaluated separately.",
        "",
        "## Detailed Results",
        ""
    ])

    for config in results["configurations"]:
        lines.extend([
            f"### {config['name']}",
            "",
            "| ID | Keyword Hit | Precision@K | Recall@K | MRR |",
            "|---|---|---:|---:|---:|"
        ])

        for item in config["question_results"]:
            lines.append(
                f"| {item['id']} "
                f"| {item['keyword_hit']} "
                f"| {item['precision_at_k']} "
                f"| {item['recall_at_k']} "
                f"| {item['mrr']} |"
            )

        lines.append("")

    RESULTS_MD.write_text(
        "\n".join(lines),
        encoding="utf-8"
    )

    print("\nEvaluation reports saved:")
    print(RESULTS_JSON)
    print(RESULTS_MD)


def main():
    questions = load_questions()

    print("Total evaluation questions:", len(questions))

    if len(questions) != 15:
        raise ValueError(
            f"Expected exactly 15 questions, found {len(questions)}."
        )

    results = []

    for config in CONFIGURATIONS:
        results.append(
            evaluate_configuration(config, questions)
        )

    # Prioritize recall, then precision, then MRR.
    winner = max(
        results,
        key=lambda item: (
            item["recall_at_k"],
            item["precision_at_k"],
            item["mrr"]
        )
    )

    final_results = {
        "winner": winner["name"],
        "winner_selection": (
            "Recall@K, then Precision@K, then MRR"
        ),
        "configurations": results
    }

    save_results(final_results)

    print("\n" + "=" * 60)
    print("FINAL WINNER:", winner["name"])
    print("=" * 60)


if __name__ == "__main__":
    main()
