'''
This module was made to perform search on a database.
It consists of one class -- SearchEngine.
'''
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
        '''
        This method performs search for a single word query.
        @param query: this is a query.
        @return: a dictionary with file names as keys and a list of
        positions as values.
        '''
        # Raise TypeError if the input type is not string      
        if not isinstance(query, str):
            raise TypeError
        
        # If the query is an empty string return an empty dictionary.
        if query == "":
            return {}
        
        # If the query doesn't match any key in the database return an empty dictionary.
        if query not in self.db:
            return {}
        
        # Return dictionary with files that match the query as keys and
        # positions of the query in these files as values.
        else:
            return self.db[query]

    def multi_search(self, query):
        '''
        This method performs search for a multiple word query.
        @param query: this is a query.
        @return: a dictionary with names of the files in which all the words of the query
        are present and list of positions of the words of a query as values.
        '''
        
        # Raise TypeError if the input type is not string 
        if not isinstance(query, str):
            raise TypeError
        
        # If the query is an empty string return an empty dictionary.
        if query == "":
            return {}
        
        # Create an object of ToTokenize().
        tokenizer = ToTokenize()
        
        # Chunk the query into tokens and write the list of them into
        # the variable 'query'.
        query = tokenizer.tokenize_reduced(query)
        
        # This list will contain documents in which the current word can
        # be found.
        docs = []
        
        for word in query:
        
            # If the query doesn't match any key in the database return an empty dictionary.
            if word.wordform not in self.db:
                return {}
            
            # Append a dictionary {doc_name: positions} in 'docs' for each word of the query.
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
            # dictionary 'result' with a file name as a key and an empty list as a value.
            # Than we extend the empty list with an array of the positions of the word in
            # this file.
            for dictionary in docs:
                result.setdefault(file_name, []).extend(dictionary[file_name])


                # Sort the result so that the lines and the positions are
                # in the ascending order.
                result[file_name].sort()
                
        return result
    



  
    
if __name__ == '__main__':
    a = SearchEngine('database')

    #print(a.search('Николай'))

    print(a.multi_search('Николай Ростов'))

    
