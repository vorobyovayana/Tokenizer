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
            # Append documents in which the current word can be found.
            docs.append(self.db[word.wordform])
        # Turn the first document name into a set and write it into 'files'
        files = set(docs[0])
        
        for document in docs[1:]:
            # Each document name from the list "docs" (except for the first one)
            # we intersect with 'files'
            files &= set(document)
            
        # This dictionary will be returned.
        result = {}
        
        for file_name in files:
            for doc_name in docs:
                # Write the names of the document and the corresponding positions into 'result'.
                result.setdefault(file_name, []).extend(doc_name[file_name])
        return result
    
    def get_context_window(self, query):
        tokenizer = ToTokenize()
        query = tokenizer.tokenize_reduced(query)
        for word in query:
            line_num = word.line
        
            

            
    
    
if __name__ == '__main__':
    a = SearchEngine('database')
    print(a.multi_search('Анна Павловна'))
