import shelve
import os
from indexation import PositionByLine
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
        if query not in self.db.keys():
            return ValueError("The query doesn't match any key in the database")
        # Return dictionary with files that match the query as keys and
        # positions of the query in these files as values.
        return self.db[query]

    def multi_search(self, query):
        
        # Raise TypeError if the input type is not string 
        if not isinstance(query, str):
            raise TypeError
        
        # Raise ValueError if the query doesn't match any key in the database.
        if query == "":
            raise ValueError('Empty query')
        # Create an object of ToTokenize().
        tokenizer = ToTokenize()
        # Chunk the query into tokens and write the list of them into
        # the variable 'query'.
        query = tokenizer.tokenize_reduced(query)
        # This list will contain lists of documents for each word of the query.
        list_of_docs = []
        dictionaries = []
        for word in query:
            # Return dictionary with files that match the query as keys and
            # positions of the query in these files as values.
            if word not in self.db.keys():
                return ValueError("The query doesn't match any key in the database")
            else:
                # This list will contain documents in which the current word can
                # be found.
                docs = []
                # Append documents in which the current word can be found.
                docs.append(self.db[word].keys())
                dictionaries.append(self.db[word])
                # Apend the list of document for the current word
                # to the list of documents for all words of the query.
                list_of_docs.append(docs)
                
        # Turn the 'list_of_docs' into a set and write it
        # to the variable 'list_of_docs'.
        list_of_docs = set(list_of_docs)
        # Write the first list of documents to the variable 'document'.
        document = list_of_docs[0]
        
        for doc in list_of_docs[1:]:
            # Intersect the current list of documents with the following one
            # and write it to the variable 'document'.
            # Thus, 'document' contains files in which every word from
            # the query is present.
            document &= list_of_docs[1:]
        # This dictionary will be returned.
        result = {}
        for doc_name in document:
            for dictionary in dictionaries:
                
                # Write the name of the document and the positions into 'result'.
                result.setdefault(doc_name, []).extend(dictionary[doc_name])
        return result

            
    
    
if __name__ == '__main__':
    a = SearchEngine('database')
    print(a.multi_search('mila'))
