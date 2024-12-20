import os
import re
import random

class InterferenceModel:
    def __init__(self, document_folder):
        """Initialize the Interference Model with documents and relevance probabilities."""
        self.documents = self.load_documents(document_folder)
        self.relevance_probs = self.initialize_relevance_probabilities()

    def load_documents(self, folder_path):
        """Load documents from the folder and return a dictionary with filenames and content."""
        documents = {}
        for filename in os.listdir(folder_path):
            if filename.endswith('.txt'):
                with open(os.path.join(folder_path, filename), 'r', encoding='utf-8') as file:
                    documents[filename] = file.read()
        return documents

    def initialize_relevance_probabilities(self):
        """Randomly initialize relevance probabilities for each document."""
        relevance_probs = {}
        for doc_name in self.documents:
            relevance_probs[doc_name] = random.uniform(0.1, 0.9)  # Random initial relevance probability
        return relevance_probs

    def calculate_query_document_similarity(self, query, document):
        """Calculate similarity between query and document using term frequency."""
        query_terms = re.findall(r'\w+', query.lower())
        document_terms = re.findall(r'\w+', self.documents[document].lower())
        
        term_frequencies = {term: document_terms.count(term) for term in query_terms}
        total_terms = len(document_terms)
        
        similarity = sum(freq / total_terms for freq in term_frequencies.values())
        return similarity

    def calculate_relevance(self, query, document):
        """Calculate the relevance of a document given a query using the Interference Model."""
        query_similarity = self.calculate_query_document_similarity(query, document)
        document_relevance = self.relevance_probs[document]
        return query_similarity * document_relevance

    def rank_documents(self, query):
        """Rank documents by their relevance score for the given query."""
        relevance_scores = {doc: self.calculate_relevance(query, doc) for doc in self.documents}
        ranked_docs = sorted(relevance_scores.items(), key=lambda x: x[1], reverse=True)
        return ranked_docs

    def display_ranked_documents(self, query):
        """Display the ranked documents with their relevance scores."""
        print(f"\nRanked documents for query: '{query}'\n")
        ranked_docs = self.rank_documents(query)
        results = []
        for rank, (doc, score) in enumerate(ranked_docs, start=1):
            print(f"{rank}. {doc} - Relevance Score = {score:.4f}")
            if score > 0:
                results.append(f"{rank}. {doc} - Relevance Score = {score:.4f}")

        return results

def search(query):
    model = InterferenceModel('data/documents')
    return model.display_ranked_documents(query)


if __name__ == "__main__":
    model = InterferenceModel('documents')

    while(True):
        os.system('cls')
        # Example query
        query = input("Enter your Query:")
        # Rank and display documents based on the query
        model.display_ranked_documents(query)
        query = input("\nPress Enter to continue:")
