import os
import re

indexMap = {}

def addInIndexMap(key, value):
    if key not in indexMap:
        indexMap[key] = [value]
    elif indexMap[key].count(value) == 0:
        indexMap[key].append(value)

def addHyperlinksToContent(content, currentFilePath, fileStructure):
    """
    Modify the content to add hyperlinks to other documents
    based on keywords found in the text.
    """
    # print(fileStructure['Chapter 1 - Monuments']['The Eiffel Tower'], 'fileStructure')

    # Extract words or terms that are used as document names in the structure
    def extractTitles(structure, prefix = ''):
        for name, substructure in structure.items():
            if isinstance(substructure, dict):
                splittedContent = filterImportantWords(name)
                for word in splittedContent:
                    addInIndexMap(word, '#' + prefix + name)

                extractTitles(substructure, prefix + name + '/')
            elif isinstance(substructure, str):
                splittedAndFilteredList = filterImportantWords(substructure)
                for word in splittedAndFilteredList:
                    addInIndexMap(word, prefix + name)
    
    extractTitles(fileStructure)

    # for key, value in indexMap.items():
    #     print(key, ' => ', value)

    # Create hyperlinks for the titles in the content
    for word in filterImportantWords(content):
        if word in indexMap:
            docs = indexMap[word][:]
            docs.remove(currentFilePath)
            if len(docs):
                hyperLink = f'/document/{docs[0]}' if docs[0].count('#') == 0 else f'/{docs[0]}'
                content = re.sub(r'\b' + re.escape(word) + r'\b', f'<a href="{hyperLink}">{word}</a>', content)
    
    return content

def readDirectoryStructure(rootDir):
    """
    Reads the directory structure and returns a dictionary
    representing the hierarchy and content of the .txt files.
    """
    hierarchy = {}
    
    # Traverse the directory structure
    for root, dirs, files in os.walk(rootDir):
        # Skip the root directory itself, focus on files
        if root == rootDir:
            continue
        
        # Build the path relative to the root directory
        pathParts = os.path.relpath(root, rootDir).split(os.sep)
        # Find the parent node
        parent = hierarchy
        for part in pathParts:
            parent = parent.setdefault(part, {})

        # Add content for each text file
        for file in files:
            if file.endswith('.txt'):
                # Read file content
                with open(os.path.join(root, file), 'r') as f:
                    content = f.read()
                
                # Store content with the filename as the key
                parent[file.replace('.txt', '')] = content
    
    return hierarchy

def filterImportantWords(text):
    """
    Filter out unimportant words (stop words, verb suffixes) and return a list of important words.
    """
    stopWords = {'the', 'is', 'and', 'in', 'to', 'of', 'a', 'with', 'for', 'on', 'by', 'are', 'an', 'as', 'that', 'was', 'it'}
    verbSuffixes = {'ing', 'ed', 'ate', 'ify', 'ize', 'en', 'fy'}
    wordsList = []
    for word in text.split():
        word = word.lower().strip(',.')

        if word in stopWords or len(word) <= 4:
            continue 

        if any(word.endswith(suffix) for suffix in verbSuffixes):
            continue

        wordsList.append(word)

    return wordsList


rootDirectory = 'data/Famous Landmarks Around the World'
browsingStructure = readDirectoryStructure(rootDirectory)
