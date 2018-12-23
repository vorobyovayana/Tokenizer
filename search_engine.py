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
            raise TypeError('The query is not a string')
        if query == "":
            raise ValueError('Empty query')
        if query not in self.db.keys():
            return ValueError("The query doesn't match any key in the database")
        
        return self.db[query]
        '''
        def multi_search(self, query):
        
        tokenizer = ToTokenize()
        tokens = tokenizer.tokenize.reduced(query)
        docs = []
        positions = []
        for token in tokens:
            for key in self.db[token].keys():
                docs.append(key)
                file_pos = self.db[token]
                for doc in docs:
                    positions.append(file_pos[doc])
        for 
        '''
    def search_multiple(self, query):
        """Search database and return filenames
        and positions for one or more words
        @param query -- one or more words, positions of which are returned
        """
        if not isinstance(query, str):
            raise TypeError('Inappropriate argument type.')
        if query == '':
            return {}
        token = ToTokenize()
        words = token.tokenize_reduced(query)
        results = []
        keys = []
        for word in words:
            if str(word) not in self.db:
                return {}
            dic = self.db[word]
            results.append(set(dic))
            for key in dic:
                keys.append(key)
        keys = set(keys)
        # remove files in which not all the searched words are present
        for files in results:
            keys &= files
        positions = {}
        for file in keys:
            for word in words:
                positions.setdefault(file, []).extend(self.db[str(word)][file])
        return positions
        
        
        
    
    
if __name__ == '__main__':
    a = SearchEngine('database')
    print(a.search('mila'))
    print(a.search_multiple('mama'))
