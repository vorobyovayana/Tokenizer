import shelve
import os
from indexation import PositionByLine
from tokenization import ToTokenize
from tokenization import TokenWithType
class SearchEngine:

    def __init__(self, db_name):
        
        self.db = shelve.open(db_name)
        
    def __del__(self):

        self.db.close()
        
    def search(self, query):
        # Raise TypeError if the input type is not string      
        if not isinstance(query, str):
            raise TypeError
        
        # Raise ValueError if the query is an empty string.
        if query == "":
            raise ValueError('Empty query')
        
        # Raise ValueError if the query doesn't match any key in the database.
        if query not in self.db:
            return ValueError("The query doesn't match any key in the database")
        
        # Return dictionary with files that match the query as keys and
        # positions of the query in these files as values.
        else:
            return self.db[query]

    def multi_search(self, query):
        
        # Raise TypeError if the input type is not string 
        if not isinstance(query, str):
            raise TypeError
        
        # Raise ValueError if the query is an empty string.
        if query == "":
            raise ValueError('Empty query')
        
        # Create an object of ToTokenize().
        tokenizer = ToTokenize()
        
        # Chunk the query into tokens and write the list of them into
        # the variable 'query'.
        query = tokenizer.tokenize_reduced(query)
        
        # This list will contain documents in which the current word can
        # be found.
        docs = []
        for word in query:
        
            # Raise ValueError if the query doesn't match any key in the database.
            if word.wordform not in self.db:
                raise ValueError("The query doesn't match any key in the database")
            
            # Append dictionary {doc_name: positions} in 'docs' for each word of the query.
            docs.append(self.search(word.wordform))
                
                
        # Turn the first document name from the list 'docs' to a set and write it to 'files'.
        files = set(docs[0])
        
        for document in docs[1:]:
            
            # Each following document from 'docs' turn to a set too 
            # and intersect it with 'files'.
            files &= set(document)
            
        # This dictionary will be returned.
        result = {}
        
        # For each file name in the set 'files'
        for file_name in files:
            
            # For each dict in the list 'docs' create a key-value pair in a
            # dictionary 'result' with a file name as a key and an empty list as a key.
            # Than we extend the empty list with an array of the positions of the word in
            # this file.
            for dictionary in docs:
                result.setdefault(file_name, []).extend(dictionary[file_name])

                # Sort positions in each document of the result so that the lines and the positions are
                # in the ascending order.
                result[file_name].sort()
                
        return result

            
    
    
if __name__ == '__main__':
    a = SearchEngine('database')
    #print(a.search('Анна'))
    print(a.multi_search('Анна Павловна'))
