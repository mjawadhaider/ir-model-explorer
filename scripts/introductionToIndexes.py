import os

class searchEngine:
    def __init__(self):
        self.indexes = {}
        # common Stop words and verb's suffixes to be filtered from text
        self.stopWords = {'the', 'is', 'and', 'in', 'to', 'of', 'a', 'with', 'for', 'on', 'by', 'are', 'an', 'as', 'that'}
        self.verbSuffixes = {'ing', 'ed', 'ate', 'ify', 'ize', 'en', 'fy'}

    # Add fileName in the dict against its indexedWord 
    def addIndexInDict(self, indexWord, value):
        if indexWord not in self.indexes:
            self.indexes[indexWord] = [value]
        elif value not in self.indexes[indexWord]:
            self.indexes[indexWord].append(value)

    # Take filePath as parameter and returns it's content
    def readFile(self, filePath):
        try:
            with open(filePath, 'r') as file:
                content = file.read()
                return content
        except FileNotFoundError:
            displayMsg(f'The file {filePath} does not exist.')
        
        return None

    # This method read's the documentsFolderPath, reads the files content and creates title and content's indexes
    def createIndexes(self, documentsFolderPath):
        try:
            for filename in os.listdir(documentsFolderPath):
                if filename.endswith('.txt'):
                    filePath = os.path.join(documentsFolderPath, filename)
                    fileContent = self.readFile(filePath)

                    if not fileContent:
                        continue

                    self.createTitleAndContentsIndex(filename, fileContent)
            return True
        except FileNotFoundError:
            displayMsg(f'The Directory {documentsFolderPath} does not exist.')
            return False

    # Take fileName and it's content as parameters and creates its index in the dictionary
    def createTitleAndContentsIndex(self, fileName, contentWords):
        # Remove .txt if any fileName has
        if 'txt' in fileName:
            fileName = fileName.split('.')[0]

        filteredFileNamesList = self.filterImportantWords(fileName)
        filteredContentWordsList = self.filterImportantWords(contentWords)

        for indexWord in filteredFileNamesList + filteredContentWordsList:
            self.addIndexInDict(indexWord, fileName)

    # This method take text as parameter and remove stop words and words with verb suffixes
    def filterImportantWords(self, text):
        wordsList = []
        for word in text.split():
            word = word.lower().strip(',.')

            # Check if the word is a stop word
            if word in self.stopWords:
                continue 

            # Check if the word ends with a verb suffix
            if any(word.endswith(suffix) for suffix in self.verbSuffixes):
                continue

            wordsList.append(word)

        return wordsList

    # This method take query as parameter and returns a list of related file names
    def searchDocuments(self, query):
        if query == "" or not query:
            displayMsg('Enter a valid query!')
            return None

        if len(self.indexes) == 0:
            displayMsg('Create Indexes to search a document!')
            return None
        
        results = []
        for subQuery in query.split():
            subQuery = subQuery.lower()
            if subQuery in self.indexes:
                results.extend(self.indexes[subQuery])

        if len(results) == 0:
            displayMsg('No Document found against the query!')
        
        return results

    # Display Index and its values
    def lookupIndexes(self):
        if len(self.indexes) == 0:
            return displayMsg('Create indexes to look up!')

        print('\n-------------------------------------')
        for index in self.indexes:
            print(index, '=>', end=' ')
            for file in self.indexes[index]:
                print('\t', file, end=', ')
            print()
        print('-------------------------------------')

    # Display results of the searched query
    def displayResult(self, query, result):
        print('\n-------------------------------------')
        print('Searched Query: ', query)
        if len(result) == 0:
            print('No Documents found!')
        else:
            print('Results:')
            for index, file in enumerate(result):
                print('\t', index + 1, file)
        print('-------------------------------------')

# Helper function to display messages
def displayMsg(msg):
    print('\n-------------------------------------')
    print(msg)
    print('-------------------------------------')

if __name__ == '__main__':
    documentsFolderPath = './documents'
    searchEngineInstance = searchEngine()

    while True:
        print('\nMenu:')
        print('1. Change Documents Directory Path (default: ./documents)')
        print('2. Create Indexes')
        print('3. Lookup Indexes')
        print('4. Search FileName')
        print('5. Exit')

        choice = input('Enter your choice (1-5): ')

        if choice == '1':
            documentsFolderPath = input('\nEnter Documents Directory: ')
            displayMsg('Documents Directory Path updated successfully!')
        elif choice == '2':
            indexCreated = searchEngineInstance.createIndexes(documentsFolderPath)
            if indexCreated:
                displayMsg('Indexes created successfully!')
        elif choice == '3':
            searchEngineInstance.lookupIndexes()
        elif choice == '4':
            query = input('\nEnter Query: ')
            results = searchEngineInstance.searchDocuments(query)
            if results:
                searchEngineInstance.displayResult(query, results)
        elif choice == '5':
            print('Exiting program.')
            break
        else:
            displayMsg('Invalid choice. Please enter a number between 1 and 5.')