import os
import string

# Preprocessing: Tokenization, Stop Word Removal, and Stemming
def preprocess_text(text, stop_words):
    # Lowercase the text
    text = text.lower()
    # Remove punctuation
    text = text.translate(str.maketrans("", "", string.punctuation))
    # Tokenize the text
    tokens = text.split()
    # Remove stop words
    tokens = [token for token in tokens if token not in stop_words]
    return tokens

# Read documents and preprocess them
def read_and_preprocess_documents(directory, stop_words):
    documents = {}
    for file_name in os.listdir(directory):
        if file_name.endswith(".txt"):
            with open(os.path.join(directory, file_name), 'r', encoding='utf-8') as file:
                text = file.read()
                documents[file_name] = preprocess_text(text, stop_words)
    return documents

# Represent terms as a binary vector
def build_term_vectors(documents, query_terms):
    unique_terms = set()
    for terms in documents.values():
        unique_terms.update(terms)
    unique_terms.update(query_terms)

    term_index = {term: i for i, term in enumerate(sorted(unique_terms))}

    # Create binary vectors for documents
    doc_vectors = {}
    for doc_name, terms in documents.items():
        vector = [1 if term in terms else 0 for term in term_index]
        doc_vectors[doc_name] = vector

    # Create binary vector for query
    query_vector = [1 if term in query_terms else 0 for term in term_index]

    return term_index, doc_vectors, query_vector

# Compute Jaccard coefficient
def compute_jaccard_coefficient(vec1, vec2):
    intersection = sum(1 for a, b in zip(vec1, vec2) if a == b == 1)
    union = sum(1 for a, b in zip(vec1, vec2) if a == 1 or b == 1)
    return intersection / union if union > 0 else 0

# Rank documents based on scores
def rank_documents(doc_vectors, query_vector):
    scores = {}
    for doc_name, vector in doc_vectors.items():
        scores[doc_name] = compute_jaccard_coefficient(vector, query_vector)
    return sorted(scores.items(), key=lambda x: x[1], reverse=True)

# Main Function
def main():
    # Directory containing the text files
    directory = "../data/documents"
    
    # List of stop words (can be expanded or replaced with a stop word file)
    stop_words = {"the", "is", "at", "on", "in", "and", "a", "of", "to", "for"}

    # Preprocess documents
    documents = read_and_preprocess_documents(directory, stop_words)

    # Input the user's query
    query = input("Enter your query: ")
    query_terms = preprocess_text(query, stop_words)

    # Build term vectors
    term_index, doc_vectors, query_vector = build_term_vectors(documents, query_terms)

    # Rank documents
    ranked_docs = rank_documents(doc_vectors, query_vector)

    # Display results
    print("\nRanked Documents:")
    for doc, score in ranked_docs:
        print(f"{doc}: {score:.4f}")

def search(query):
     # Directory containing the text files
    directory = "data/documents"
    
    # List of stop words (can be expanded or replaced with a stop word file)
    stop_words = {"the", "is", "at", "on", "in", "and", "a", "of", "to", "for"}

    # Preprocess documents
    documents = read_and_preprocess_documents(directory, stop_words)

    # Input the user's query
    query_terms = preprocess_text(query, stop_words)

    # Build term vectors
    term_index, doc_vectors, query_vector = build_term_vectors(documents, query_terms)

    # Rank documents
    ranked_docs = rank_documents(doc_vectors, query_vector)
    return [(item[0], f"{item[1]:.4f}") for item in ranked_docs if item[1] > 0]

if __name__ == "__main__":
    main()

