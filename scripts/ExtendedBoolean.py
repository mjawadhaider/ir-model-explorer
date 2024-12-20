import os
from math import log

# Directory for text files containing documents
DOCUMENTS_DIR = "data/documents"

def loadDocuments():
    """Load all text files from the DOCUMENTS_DIR as a dictionary."""
    documents = {}
    for filename in os.listdir(DOCUMENTS_DIR):
        if filename.endswith('.txt'):
            filepath = os.path.join(DOCUMENTS_DIR, filename)
            with open(filepath, 'r', encoding='utf-8') as file:
                documents[filename] = file.read()
    return documents

DOCUMENTS = loadDocuments()

def search(query):
    """
    Perform a Boolean search over the DOCUMENTS.
    Supports AND, OR, and NOT operations (case-insensitive).
    """
    query = query.upper()
    results = set(DOCUMENTS.keys())

    if ' AND ' in query:
        terms = query.split(' AND ')
        results = set.intersection(*[searchTerm(term) for term in terms])
    elif ' OR ' in query:
        terms = query.split(' OR ')
        results = set.union(*[searchTerm(term) for term in terms])
    elif ' NOT ' in query:
        term, excluded = query.split(' NOT ')
        results = searchTerm(term) - searchTerm(excluded)
    else:
        results = searchTerm(query)

    return [(highlightTerms(fileName, query), highlightTerms(DOCUMENTS[fileName], query)) for fileName in results]

def searchTerm(term):
    """Search for a single term in the documents."""
    term = term.strip()
    return {docId for docId, text in DOCUMENTS.items() if term in text.replace(',', '').replace('.', '').upper()}

def highlightTerms(content, query):
    """Highlight search terms in the content."""
    terms = query.replace('AND', '').replace('OR', '').replace('NOT', '').split()
    for term in terms:
        term = term.strip().lower()
        for word in content.strip().split(' '):
            if word.lower().replace(',', '').replace('.', '') == term:
                content = content.replace(word, f'<span class="highlight">{word}</span>')
    return content