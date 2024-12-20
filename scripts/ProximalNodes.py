import glob
import os
import string


def createIndex():
    file_names = []
    current_directory = os.getcwd()
    txt_files = glob.glob(current_directory + "/*.txt")

    for file_name in txt_files:
        file_name_only = os.path.basename(file_name)
        file_names.append(file_name_only)

    translator = str.maketrans('', '', string.punctuation)
    index_dict = {}

    for file_name in file_names:

        with open(file_name, 'r') as file:

            content = file.read()
            words = content.split()

            for word in words:
                clean_word = word.translate(translator)
                clean_word = clean_word.lower()
                if clean_word not in index_dict.keys():
                    index_dict[clean_word] = [[file_name, 1]]
                else:
                    not_inserted = True
                    temp = index_dict[clean_word]
                    for i in range(0, len(temp)):
                        if temp[i][0] == file_name:
                            temp[i][1] += 1
                            not_inserted = False
                    if not_inserted:
                        temp.append([file_name, 1])
    return file_names, index_dict


def search(query):
    
    graph = {
    'health': ['pokemon.txt', 'ai.txt', 'plants.txt'],
    'creature': ['pokemon.txt', 'animals.txt', 'plants.txt'],
    'video': ['pokemon.txt'],
    'game': ['pokemon.txt'],
    'entertainment': ['pokemon.txt', 'ai.txt'],
    'ability': ['pokemon.txt'],
    'traits': ['pokemon.txt'],
    'capture': ['pokemon.txt'],
    'train': ['pokemon.txt'],
    'battle': ['pokemon.txt'],
    'strategy': ['pokemon.txt'],
    'decision': ['pokemon.txt', 'ai.txt'],
    'pet': ['pokemon.txt', 'animals.txt'],
    'artificial': ['ai.txt'],
    'intelligence': ['ai.txt'],
    'data': ['ai.txt', 'computer.txt'],
    'machine': ['ai.txt', 'computer.txt'],
    'human': ['ai.txt', 'animals.txt', 'plants.txt'],
    'robot': ['ai.txt'],
    'organism': ['animals.txt'],
    'ecosystem': ['animals.txt', 'plants.txt'],
    'earth': ['animals.txt', 'plants.txt'],
    'plant': ['animals.txt'],
    'species': ['animals.txt'],
    'animal': ['animals.txt'],
    'survive': ['animals.txt'],
    'environment': ['animals.txt'],
    'mammal': ['animals.txt'],
    'insect': ['animals.txt'],
    'food': ['animals.txt', 'plants.txt'],
    'material': ['animals.txt'],
    'essential': ['plants.txt', 'computer.txt'],
    'oxygen': ['plants.txt'],
    'photosynthesis': ['plants.txt'],
    'tree': ['plants.txt'],
    'moss': ['plants.txt'],
    'medicine': ['plants.txt'],
    'carbon dioxide': ['plants.txt'],
    'calculation': ['computer.txt'],
    'software': ['computer.txt'],
    'life': ['computer.txt'],
    'communication': ['computer.txt'],
    'automation': ['computer.txt']
    }

    arr = query.split(' ')

    results = []
    for word in arr:
        if(word in graph.keys()):
            # print(graph[word])
            for file in graph[word]:
                results.append(file)

    return results


def menu():
    """
    Main menu to choose the operation from.
    """

    browserName()
    print('            Menu')
    print('')
    print('1. Refresh Indexer Manually')
    print('2. Search Document by Relevancy')
    print('3. Exit Browser')
    print('')

    while(True):

        option = input('Choose an option from above: ')

        try:
            option = int(option)
            if 0 < option < 4:
                break
            else:
                print("Invalid choice! Choose carefully from the menu.")
                print('')
                continue
        except ValueError:
            print("Invalid input! Please enter a valid number.")
            print('')
            continue

    return option


def browserName():
    print('                 ******************************************')
    print('                 *                                        *')
    print('                 *                My Browser              *')
    print('                 *                                        *')
    print('                 ******************************************')
    print('')


def main():
    browserName()

    # graph = {'pokemon.txt': ['health', 'creature', 'video', 'game', 'entertainment', 'ability', 'traits', 'capture', 'train', 'battle', 'strategy', 'decision', 'pet'],
    #          'ai.txt': ['artificial', 'intelligence', 'data', 'machine', 'human', 'decision', 'health', 'robot', 'entertainment'],
    #          'animals.txt': ['creature', 'organism', 'ecosystem', 'earth', 'plant', 'species', 'animal', 'survive', 'environment', 'mammal', 'insect', 'human', 'pet', 'food', 'material'],
    #          'plants.txt': ['health', 'creature', 'human', 'essential', 'food', 'earth', 'oxygen', 'photosynthesis', 'tree', 'moss', 'medicine', 'ecosystem', 'carbon dioxide'],
    #          'computer.txt': ['machine', 'data', 'calculation', 'software', 'essential', 'life', 'communication', 'automation', ]}


    # file_names, index_dict = createIndex()

    # print(index_dict)
    # return

    # while(True):
    #     os.system('cls')

    #     option = menu()

    #     if option == 1:
    #         file_names, index_dict = createIndex()
    #         print('Indexer Refreshed Successfully!')
    #     elif option == 2:
    #         count = input('How many phrases you wish to search: ')

    #         try:
    #             count = int(count)
    #         except ValueError:
    #             input("Invalid input! Press enter to input a valid number.")
    #             print('')
    #             continue

    #         search(index_dict, count)
    #     else:
    #         break

    #     print('')
    #     input('Press Enter to continue.')

    # os.system('cls')
    # browserName()
    # print('')
    # print('Thank You for using "My Browser"')
    # print('')


if __name__ == "__main__":
    main()
