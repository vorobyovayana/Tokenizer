from tokenization import ToTokenize
from tokenization import TokenWithType
import shelve

class Position(self, start, length):
    def __init__(self):
        self.start = start
        self.end = start + length

    def __repr__(self):
        
        return self.start + self.end

class ToIndex:
               
    def index(self, file_name):
        
        # Raise TypeError if the input type is not string      
        if not isinstance(text_file, str):
            raise(TypeError)
        
        # Open file
        text_file = open(file_name, 'r')
        # Read file and save as a string
        text_string = text_file.read
        # Tokenize the string and write it in the variable 'tokens'.
        tokens = tokenize_reduced(text_string)
        # Open database with name 'database'
        db = shelve.open('database')

        for token in tokens:
            # Create an object of class Position for a current token
            position = Position(token.start, len(token.wordform))
            # If the token is not in the database, add it.
            dict(db).setdefault(token, {})
            # If the filename is not in the dictionary, add it
            db[token].setdefault(file_name)
            # Write the dictionary 'db[token]' to a variable 'file_pos_dict'
            file_pos_dict = db[token]
            # Add to the end of the list of positions position of the current token
            file_pos_dict[file_name].append(position)
        db.close()
                
                    
if __name__ == '__main__':
    a = ToIndex()
a.index("text.txt")
