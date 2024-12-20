import os
import re
# import math
import numpy as np
from collections import defaultdict


class LatentSemanticIndexing:
    def __init__(self, num_topics=2):
        """
        Initializes the LSI system by reading and indexing all .txt files in the current folder.
        
        Args:
            num_topics (int): Number of latent topics to reduce the dimensionality to.
        """
        self.documents = {}  # {doc_id: content}
        self.term_frequencies = defaultdict(lambda: defaultdict(int))  # {doc_id: {term: frequency}}
        self.term_index = {}  # {term: index} for term-document matrix
        self.doc_index = {}  # {doc_id: index} for term-document matrix
        self.term_document_matrix = None  # The raw term-document matrix
        self.U = None  # Left singular vectors (terms)
        self.S = None  # Singular values
        self.Vt = None  # Right singular vectors (documents)
        self.num_topics = num_topics
        self._read_documents()
        self._build_term_document_matrix()
        self._perform_svd()
    
    def _read_documents(self):
        """Reads all .txt files in the current folder and stores their content."""
        DOCUMENT_FOLDER = "data/documents"
        for filename in os.listdir(DOCUMENT_FOLDER):
            if filename.endswith(".txt"):
                doc_id = filename  # Use filename as the document ID
                filename = os.path.join(DOCUMENT_FOLDER, filename)
                with open(filename, 'r', encoding='utf-8') as file:
                    content = file.read().lower()  # Convert to lowercase for case-insensitive search
                    self.documents[doc_id] = content
                    self._tokenize_and_count_terms(doc_id, content)
    
    def _tokenize_and_count_terms(self, doc_id, content):
        """Tokenizes the document's content and counts term frequencies."""
        terms = re.findall(r'\w+', content)  # Extract words only
        for term in terms:
            self.term_frequencies[doc_id][term] += 1
    
    def _build_term_document_matrix(self):
        """Builds the term-document matrix where each row represents a term and each column a document."""
        all_terms = sorted(set(term for term_freqs in self.term_frequencies.values() for term in term_freqs))
        all_docs = sorted(self.documents.keys())
        
        self.term_index = {term: i for i, term in enumerate(all_terms)}
        self.doc_index = {doc_id: i for i, doc_id in enumerate(all_docs)}
        
        num_terms = len(all_terms)
        num_docs = len(all_docs)
        self.term_document_matrix = np.zeros((num_terms, num_docs))
        
        for doc_id, term_freqs in self.term_frequencies.items():
            doc_idx = self.doc_index[doc_id]
            for term, freq in term_freqs.items():
                term_idx = self.term_index[term]
                self.term_document_matrix[term_idx][doc_idx] = freq
    
    def _perform_svd(self):
        """Performs Singular Value Decomposition (SVD) on the term-document matrix."""
        U, S, Vt = np.linalg.svd(self.term_document_matrix, full_matrices=False)
        self.U = U[:, :self.num_topics]  # Reduce dimensionality to num_topics
        self.S = np.diag(S[:self.num_topics])
        self.Vt = Vt[:self.num_topics, :]  # Reduced dimensionality
    
    def query(self, query_text):
        """
        Processes the query and returns a ranked list of documents based on cosine similarity in reduced space.
        
        Args:
            query_text (str): The user's search query.
        
        Returns:
            list of tuples: List of (doc_id, score) sorted by descending score.
        """
        query_terms = re.findall(r'\w+', query_text.lower())
        query_vector = np.zeros(len(self.term_index))
        
        for term in query_terms:
            if term in self.term_index:
                term_idx = self.term_index[term]
                query_vector[term_idx] += 1
        
        # Project query into reduced space
        query_in_reduced_space = np.dot(np.dot(query_vector, self.U), np.linalg.inv(self.S))
        
        document_scores = defaultdict(float)
        for doc_id, doc_idx in self.doc_index.items():
            doc_vector = self.Vt[:, doc_idx]  # Document in reduced space
            similarity = np.dot(query_in_reduced_space, doc_vector) / (np.linalg.norm(query_in_reduced_space) * np.linalg.norm(doc_vector))
            document_scores[doc_id] = similarity
        
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
    ir_system = LatentSemanticIndexing(num_topics=2)
    return ir_system.display_results(query, top_n)


if __name__ == "__main__":
    # Example usage
    ir_system = LatentSemanticIndexing(num_topics=2)
    
    # Interactive query session
    while True:
        query = input("Enter your search query (or type 'exit' to quit): ")
        if query.lower() == 'exit':
            break
        ir_system.display_results(query)

