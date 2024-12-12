from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import os
from collections import defaultdict

class PodcastSearchEngine:
    def __init__(self, corpus, metadata):
        self.vectorizer = TfidfVectorizer()
        self.corpus = corpus
        self.metadata = metadata
        self.tfidf_matrix = self.vectorizer.fit_transform(corpus)

        # Precompute file-wise concatenated text
        self.filewise_text = defaultdict(str)
        for i, meta in enumerate(metadata):
            self.filewise_text[meta["file"]] += " " + corpus[i]

    def search(self, query, top_n=5):
        query_vec = self.vectorizer.transform([query])
        similarities = cosine_similarity(query_vec, self.tfidf_matrix).flatten()

        # Filter results to exclude similarity score of 0
        filtered_indices = [i for i, score in enumerate(similarities) if score > 0]

        # Sort by similarity score in descending order
        sorted_indices = sorted(filtered_indices, key=lambda i: similarities[i], reverse=True)

        # Debug: Check the content of filewise_text for validation
        print("Filewise concatenated text:", self.filewise_text)

        # Count occurrences of the query (case insensitive) in each file
        query_count_per_file = {}
        for file, text in self.filewise_text.items():
            count = text.lower().count(query.lower())
            query_count_per_file[file] = count
            # Debug: Check the count for each file
            print(f"Query '{query}' found {count} times in file {file}")

        # Return top N results
        results = [
            {
                "file": os.path.splitext(self.metadata[i]["file"])[0] + ".mp3",  # Convert JSON to MP3
                "start": self.metadata[i]["start"],
                "end": self.metadata[i]["end"],
                "text": self.corpus[i],
                "score": similarities[i],
                "query_count": query_count_per_file[self.metadata[i]["file"]]  # Query count for the entire file
            }
            for i in sorted_indices[:top_n]
        ]

        return results
