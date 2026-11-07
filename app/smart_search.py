
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class SmartSearch:

    def __init__(self, records):
        self.records = records

        self.documents = [
            " ".join([
                str(record.get("city", "")),
                str(record.get("aqi_value", "")),
                str(record.get("aqi_category", "")),
                str(record.get("prominent_pollutant", "")),
                str(record.get("stations_reporting", ""))
            ])
            for record in records
        ]

        self.vectorizer = TfidfVectorizer(
            lowercase=True,
            ngram_range=(1, 2)
        )

        self.matrix = (
            self.vectorizer.fit_transform(self.documents)
            if self.documents else None
        )

    def search(self, query, limit=10):

        if not query.strip() or self.matrix is None:
            return []

        query_vector = self.vectorizer.transform([query])

        scores = cosine_similarity(
            query_vector,
            self.matrix
        ).flatten()

        ranked_indices = scores.argsort()[::-1]

        results = []

        for index in ranked_indices:
            score = float(scores[index])

            if score <= 0:
                continue

            result = self.records[index].copy()
            result["similarity_score"] = round(score, 4)

            results.append(result)

            if len(results) >= limit:
                break

        return results
