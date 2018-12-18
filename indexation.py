from tokenization import ToTokenize
from tokenization import TokenWithType
import shelve
import os

class Position:
    def __init__(self, start, end):
        self.start = start
        self.end = end
        
    def __repr__(self):
        
        return str(self.start) + ', ' + str(self.end)

    def __eq__(self, obj):

        return self.start == obj.start and self.end == obj.end
    

class ToIndex:
    
    def __init__(self, db_name):

        self.db = shelve.open(db_name, writeback=True)

    def __del__(self):

        self.db.close()
               
    def index(self, file_name):
        #self.db.clear()
        # Raise TypeError if the input type is not string      
        if not isinstance(file_name, str):
            raise(TypeError)

        files = os.listdir()
        if file_name not in files:
            raise(ValueError)
        
        tokenizer = ToTokenize()
        # Open file
        text_file = open(file_name, 'r')
        # Read file and save as a string
        text_string = text_file.read()
        text_file.close()
        tokens = tokenizer.tokenize_reduced(text_string)
        for token in tokens:
            position = Position(token.start, token.start + len(token.wordform))
            self.db.setdefault(token.wordform, {}).setdefault(file_name, []).append(position)

        
        self.db.sync()
        
        

                
                    
if __name__ == '__main__':
    a = ToIndex('database')
    a.index("text.txt")
    a.index("text2.txt")
