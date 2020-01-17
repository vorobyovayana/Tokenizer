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
        param@: a query
        return@: a dictionary with file names as keys and a list of
        positions as values.
        '''
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
        '''
        This method performs search for a multiple words query.
        param@: a query
        return@: a dictionary with file names in which the words of the query
        are present and list of positions of the words of a query as values.
        '''        
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
            # If the query doesn't match any key in the database return an empty dictionary.
            if word.wordform not in self.db:
                return {}            
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
            # Sort the result so that the lines and the positions are
            # in the ascending order.
            result[file_name].sort()              
        return result
 
    def limited_multi_search(self, query, doclimit, docoffset):
        '''
        This method performs multi-word search and returns a limited number
        of documents containing it.
        param@ 'query': a query.
        param@ 'doclimit': a number of documents to be returned.
        param@ 'docoffset': a number of the first document to be returned.
        return@: a dictionary with file names in which the words of the query
        are present and list of positions of the words of a query as values.
        '''
        if docoffset < 0:
            docoffset = 0        
        # Raise TypeError if the input type is not string 
        if not isinstance(query, str):
            raise TypeError        
        # Return an empty dictionary if the query is an empty string.
        if query == "":
            return {}        
        # Raise ValueError if the doclimit is not int.
        if not isinstance(doclimit, int):
            raise TypeError
        # Raise ValueError if the docoffset is not int.
        if not isinstance(docoffset, int):
            raise TypeError        
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
        # Sorting file names in the chronological order.
        sorted_file_names = sorted(files)
        # Iterating through the file names.
        for i, file_name in enumerate(sorted_file_names):
            # Exit the cycle if 'i' is out of limit.
            if i >= docoffset + doclimit:
                break
            if i >= docoffset:
                # For each dict in the list 'docs' create a key-value pair in a
                # dictionary 'result' with a file name as a key and an empty list as a key.
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
    #print(a.search('Анна'))    
    print(a.limited_multi_search('Князь Андрей', 3, 0))
    
