import os
import re
import random

class BeliefNetwork:
    def __init__(self, document_folder):
        """Initialize the belief network with documents and relationships."""
        self.documents = self.load_documents(document_folder)
        self.features = self.extract_features()
        self.relevance_probs = self.initialize_relevance_probabilities()

    def load_documents(self, folder_path):
        """Load documents from the folder and return a dictionary with filenames and content."""
        documents = {}
        for filename in os.listdir(folder_path):
            if filename.endswith('.txt'):
                with open(os.path.join(folder_path, filename), 'r', encoding='utf-8') as file:
                    documents[filename] = file.read()
        return documents

    def extract_features(self):
        """Extract basic features from each document. Here, we use word counts as features."""
        features = {}
        for doc_name, content in self.documents.items():
            words = re.findall(r'\w+', content.lower())
            word_count = len(words)
            unique_word_count = len(set(words))
            avg_word_length = sum(len(word) for word in words) / len(words) if words else 0
            features[doc_name] = {
                'word_count': word_count,
                'unique_word_count': unique_word_count,
                'avg_word_length': avg_word_length
            }
        return features

    def initialize_relevance_probabilities(self):
        """Initialize the probabilities of relevance for each document randomly (for now)."""
        relevance_probs = {}
        for doc_name in self.documents:
            relevance_probs[doc_name] = random.uniform(0.1, 0.9)  # Random initial relevance probability
        return relevance_probs

    def calculate_joint_probability(self, query, document):
        """Calculate the joint probability P(Q, R, F) where Q = query, R = relevance, F = features."""
        relevance = self.relevance_probs[document]
        feature_prob = self.calculate_feature_probability(document)
        query_prob = self.calculate_query_probability(query, document)
        return query_prob * relevance * feature_prob

    def calculate_feature_probability(self, document):
        """Calculate the probability of a feature given the document."""
        # Assume we normalize each feature and combine their values into a single score
        features = self.features[document]
        word_count_score = features['word_count'] / max(1, max(f['word_count'] for f in self.features.values()))
        unique_word_score = features['unique_word_count'] / max(1, max(f['unique_word_count'] for f in self.features.values()))
        avg_word_length_score = features['avg_word_length'] / max(1, max(f['avg_word_length'] for f in self.features.values()))
        return (word_count_score + unique_word_score + avg_word_length_score) / 3  # Combine scores

    def calculate_query_probability(self, query, document):
        """Calculate the probability that a query relates to a document."""
        query_terms = re.findall(r'\w+', query.lower())
        document_terms = re.findall(r'\w+', self.documents[document].lower())
        match_count = sum(1 for term in query_terms if term in document_terms)
        return match_count / len(query_terms) if query_terms else 0

    def calculate_marginal_probability(self, query):
        """Calculate the marginal probability P(Q) by summing over all documents."""
        total_prob = sum(self.calculate_joint_probability(query, doc) for doc in self.documents)
        return total_prob / len(self.documents) if self.documents else 0

    def calculate_conditional_probability(self, query, document):
        """Calculate the conditional probability P(R | Q) using Bayes' theorem."""
        joint_prob = self.calculate_joint_probability(query, document)
        marginal_prob = self.calculate_marginal_probability(query)
        if marginal_prob == 0:
            return 0
        return joint_prob / marginal_prob

    def rank_documents(self, query):
        """Rank documents by P(R | Q) for a given query."""
        relevance_scores = {doc: self.calculate_conditional_probability(query, doc) for doc in self.documents}
        ranked_docs = sorted(relevance_scores.items(), key=lambda x: x[1], reverse=True)
        return ranked_docs

    def display_ranked_documents(self, query):
        """Display the ranked documents with their relevance probabilities."""
        print(f"\n\nRanked documents for query: '{query}'\n\n")
        ranked_docs = self.rank_documents(query)
        results = []
        for rank, (doc, prob) in enumerate(ranked_docs, start=1):
            print(f"{rank}. {doc} - P(R | Q) = {prob:.4f}")
            if prob > 0:
                results.append(f"{rank}. {doc} - P(R | Q) = {prob:.4f}")
        
        return results

def search(query):
    network = BeliefNetwork('data/documents')
    return network.display_ranked_documents(query)


if __name__ == "__main__":
    # Initialize the belief network with documents in the 'documents' folder
    network = BeliefNetwork('documents')
    
    while(True):
        os.system('cls')
        # Example query
        query = input("Enter your Query:")
        # Rank and display documents based on the query
        network.display_ranked_documents(query)
        query = input("\nPress Enter to continue:")
    
