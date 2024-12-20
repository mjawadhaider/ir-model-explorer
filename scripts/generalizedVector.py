import os
import re
import math
from collections import defaultdict

class GeneralizedVectorInformationRetrieval:
    def __init__(self):
        """
        Initializes the Generalized Vector IR system by reading and indexing all .txt files in the current folder.
        """
        self.documents = {}  # {doc_id: content}
        self.term_frequencies = defaultdict(lambda: defaultdict(int))  # {doc_id: {term: frequency}}
        self.document_vectors = defaultdict(lambda: defaultdict(float))  # {doc_id: {term: tf-idf weight}}
        self.document_magnitudes = defaultdict(float)  # {doc_id: magnitude of the document vector}
        self._read_documents()
        self._calculate_tfidf_vectors()
    
    def _read_documents(self):
        """Reads all .txt files in the current folder and stores their content."""
        DOCUMENTS_DIR = "data/documents"
        for filename in os.listdir(DOCUMENTS_DIR):
            if filename.endswith(".txt"):
                doc_id = filename  # Use filename as the document ID
                filename = os.path.join(DOCUMENTS_DIR, filename)
                with open(filename, 'r', encoding='utf-8') as file:
                    content = file.read().lower()  # Convert to lowercase for case-insensitive search
                    self.documents[doc_id] = content
                    self._tokenize_and_count_terms(doc_id, content)
    
    def _tokenize_and_count_terms(self, doc_id, content):
        """Tokenizes the document's content and counts term frequencies."""
        terms = re.findall(r'\w+', content)  # Extract words only
        for term in terms:
            self.term_frequencies[doc_id][term] += 1
    
    def _calculate_tfidf_vectors(self):
        """Calculates TF-IDF weights for each term in each document and computes document magnitudes."""
        total_documents = len(self.documents)
        
        # Calculate document frequencies for each term
        document_frequencies = defaultdict(int)
        for term_freqs in self.term_frequencies.values():
            for term in term_freqs:
                document_frequencies[term] += 1
        
        # Calculate TF-IDF weights and document magnitudes
        for doc_id, term_freqs in self.term_frequencies.items():
            max_freq = max(term_freqs.values())
            for term, freq in term_freqs.items():
                tf = freq / max_freq  # Term frequency (normalized)
                idf = math.log(total_documents / (1 + document_frequencies[term]))  # Inverse document frequency (smoothed)
                tf_idf = tf * idf  # TF-IDF weight
                self.document_vectors[doc_id][term] = tf_idf
            
            # Calculate the magnitude of the document vector
            magnitude = math.sqrt(sum(weight ** 2 for weight in self.document_vectors[doc_id].values()))
            self.document_magnitudes[doc_id] = magnitude
    
    def query(self, query_text):
        """
        Processes the query and returns a ranked list of documents based on cosine similarity.
        
        Args:
            query_text (str): The user's search query.
        
        Returns:
            list of tuples: List of (doc_id, score) sorted by descending score.
        """
        query_terms = re.findall(r'\w+', query_text.lower())  # Tokenize the query into terms
        query_term_frequencies = defaultdict(int)
        for term in query_terms:
            query_term_frequencies[term] += 1
        
        query_vector = {}  # TF-IDF vector for the query
        max_freq = max(query_term_frequencies.values())
        for term, freq in query_term_frequencies.items():
            tf = freq / max_freq  # Term frequency (normalized)
            idf = math.log(len(self.documents) / (1 + self._document_frequency(term)))  # Inverse document frequency
            query_vector[term] = tf * idf
        
        query_magnitude = math.sqrt(sum(weight ** 2 for weight in query_vector.values()))
        
        document_scores = defaultdict(float)  # {doc_id: cosine similarity score}
        for doc_id, doc_vector in self.document_vectors.items():
            dot_product = sum(query_vector.get(term, 0) * doc_vector.get(term, 0) for term in query_vector)
            if self.document_magnitudes[doc_id] * query_magnitude != 0:
                document_scores[doc_id] = dot_product / (self.document_magnitudes[doc_id] * query_magnitude)
            else:
                document_scores[doc_id] = 0.0
        
        # Rank documents by score in descending order
        ranked_results = sorted(document_scores.items(), key=lambda x: x[1], reverse=True)
        return ranked_results
    
    def _document_frequency(self, term):
        """Returns the number of documents that contain the given term."""
        return sum(1 for term_freqs in self.term_frequencies.values() if term in term_freqs)
    
    def display_results(self, query_text, top_n=5):
        """
        Runs a query and displays the top N results.
        
        Args:
            query_text (str): The user's search query.
            top_n (int): Number of top results to display.
        """
        results = self.query(query_text)
        mappedResults = []
        print(f"\nTop {top_n} results for query: '{query_text}'\n{'=' * 40}")
        for rank, (doc_id, score) in enumerate(results[:top_n], start=1):
            print(f"{rank}. {doc_id} (Score: {score:.4f})")
            if score > 0:
                mappedResults.append(f"{rank}. {doc_id} (Score: {score:.4f})")
        
        return mappedResults

def search(query, top_n = 10):
    if not query:
        return []
    ir_system = GeneralizedVectorInformationRetrieval()
    return ir_system.display_results(query, top_n)


if __name__ == "__main__":
    # Example usage
    ir_system = GeneralizedVectorInformationRetrieval()
    
    # Interactive query session
    while True:
        query = input("Enter your search query (or type 'exit' to quit): ")
        if query.lower() == 'exit':
            break
        ir_system.display_results(query)

