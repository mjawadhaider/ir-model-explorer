import os
import re
# import math
from collections import defaultdict


class FuzzyInformationRetrieval:
    def __init__(self):
        """
        Initializes the Fuzzy IR system by reading and indexing all .txt files in the current folder.
        """
        self.documents = {}  # {doc_id: content}
        self.term_frequencies = defaultdict(lambda: defaultdict(int))  # {doc_id: {term: frequency}}
        self.fuzzy_memberships = defaultdict(lambda: defaultdict(float))  # {doc_id: {term: membership}} 
        self._read_documents()
        self._calculate_fuzzy_memberships()
    
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
    
    def _calculate_fuzzy_memberships(self):
        """Calculates fuzzy membership degrees for each term in each document."""
        for doc_id, term_freqs in self.term_frequencies.items():
            max_freq = max(term_freqs.values())  # Maximum frequency of any term in the document
            for term, freq in term_freqs.items():
                self.fuzzy_memberships[doc_id][term] = freq / max_freq  # Membership degree between 0 and 1
    
    def query(self, query_text):
        """
        Processes the query and returns a ranked list of documents based on fuzzy membership.
        
        Args:
            query_text (str): The user's search query.
        
        Returns:
            list of tuples: List of (doc_id, score) sorted by descending score.
        """
        query_terms = re.findall(r'\w+', query_text.lower())  # Tokenize the query into terms
        document_scores = defaultdict(float)  # {doc_id: fuzzy score}
        
        for doc_id, memberships in self.fuzzy_memberships.items():
            scores = [memberships.get(term, 0) for term in query_terms]  # Get membership for each query term
            document_scores[doc_id] = max(scores)  # Fuzzy logic: Use max of membership degrees
        
        # Rank documents by score in descending order
        ranked_results = sorted(document_scores.items(), key=lambda x: x[1], reverse=True)
        return ranked_results
    
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
    ir_system = FuzzyInformationRetrieval()
    return ir_system.display_results(query, top_n)


if __name__ == "__main__":
    # Example usage
    ir_system = FuzzyInformationRetrieval()
    
    # Interactive query session
    while True:
        query = input("Enter your search query (or type 'exit' to quit): ")
        if query.lower() == 'exit':
            break
        ir_system.display_results(query)

