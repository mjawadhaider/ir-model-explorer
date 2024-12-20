import glob
import os
import string

indexes = {}

def loadDocuments(folderPath):
    """
    Load all text documents from the given folder, process their content, 
    and build an inverted index for efficient searching.
    """
    try:
        for fileName in os.listdir(folderPath):
            if fileName.endswith('.txt'):  # Only process .txt files
                filePath = os.path.join(folderPath, fileName)
                with open(filePath, 'r', encoding='utf-8') as file:
                    content = file.read()
                    
                    # Remove file extension to use as document name
                    if 'txt' in fileName:
                        fileName = fileName.split('.')[0]

                    # Filter important words from the document name and content
                    filteredFileNamesList = filterImportantWords(fileName)
                    filteredContentWordsList = filterImportantWords(content)

                    # Build inverted index: for each word, store the documents and their frequency
                    for indexWord in filteredFileNamesList + filteredContentWordsList:
                        if indexWord not in indexes:
                            indexes[indexWord] = [[fileName, 1]]
                        else:
                            not_inserted = True
                            indexValue = indexes[indexWord]

                            # Check if the word already exists in the document, update count if it does
                            for i in range(0, len(indexValue)):
                                if indexValue[i][0] == fileName:
                                    indexValue[i][1] += 1
                                    not_inserted = False
                            if not_inserted:
                                indexValue.append([fileName, 1])
    except FileNotFoundError:
        print(f'The Directory {folderPath} does not exist.')

def filterImportantWords(text):
    """
    Filter out unimportant words (stop words, verb suffixes) and return a list of important words.
    """
    wordsList = []
    stopWords = {'the', 'is', 'and', 'in', 'to', 'of', 'a', 'with', 'for', 'on', 'by', 'are', 'an', 'as', 'that'}
    verbSuffixes = {'ing', 'ed', 'ate', 'ify', 'ize', 'en', 'fy'}
    for word in text.split():
        word = word.lower().strip(',.')

        if word in stopWords:
            continue 

        if any(word.endswith(suffix) for suffix in verbSuffixes):
            continue

        wordsList.append(word)

    return wordsList

def search(query):
    """
    Process the query to find documents that contain the queried terms, 
    combining results without overlapping.
    """
    folderPath = "data/documents"
    loadDocuments(folderPath)

    queries = {}
    # Prepare the query list by initializing a dictionary for each query
    queryList = query.split(',')
    for query in queryList:
        query = query.lower().strip()  # Clean the query
        queries[query] = []

    # Process each query, checking the inverted index for matching documents
    for query, files in queries.items():
        for word in query.split(' '):
            if word in indexes:
                for fileName, count in indexes[word]:
                    if fileName not in files:
                        files.append(fileName)

    # Combine the results and avoid overlapping documents
    nonOverLappedList = []
    for _, files in queries.items():
        for file in files:
            if file not in nonOverLappedList:
                nonOverLappedList.append(file)
    
    # Display the final result of non-overlapping documents
    return nonOverLappedList
