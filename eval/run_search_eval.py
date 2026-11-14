
from app.vectorstore import search_chunks


QUESTIONS = [
    "What is the AQI of Nagpur?",
    "Which city has poor air quality?",
    "What is PM2.5?",
    "What does Severe AQI mean?",
    "Which city has the highest AQI?",
    "How has AQI of Pune changed over the last 30 days?",
    "Which cities have Moderate AQI?",
    "What is the prominent pollutant in Mumbai?",
    "How many monitoring stations reported data for Pune?",
    "Which city has the lowest AQI?"
]


def main():
    output = [
        "# Day 7 - Semantic Search Evaluation",
        "",
        "Retrieval evaluation using the AQIExplainer ChromaDB collection.",
        "",
        "Top 3 results are recorded for each question.",
        ""
    ]

    for number, question in enumerate(QUESTIONS, start=1):
        print(f"\nEvaluating {number}/10: {question}")

        results = search_chunks(question, top_k=3)

        output.extend([
            f"## Question {number}: {question}",
            ""
        ])

        if not results:
            output.extend([
                "No matching chunks were retrieved.",
                ""
            ])
            continue

        for rank, result in enumerate(results, start=1):
            output.extend([
                f"### Result {rank}",
                f"- **Title:** {result['title']}",
                f"- **Source:** `{result['source']}`",
                f"- **Page/row:** {result['page']}",
                f"- **Similarity:** {result['similarity']}",
                f"- **Retrieved text:** {result['text'][:500]}",
                ""
            ])

        output.extend([
            "**Manual relevance assessment:** To be reviewed.",
            ""
        ])

    output_path = "eval/search_results.md"

    with open(output_path, "w", encoding="utf-8") as file:
        file.write("\n".join(output))

    print(f"\nEvaluation saved to {output_path}")


if __name__ == "__main__":
    main()
