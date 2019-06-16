import shelve
import os
from indexation import PositionByLine
from tokenization import ToTokenize
from tokenization import TokenWithType
from search_engine import SearchEngine
class ContextWindow:

    def __init__(self, position, left_cont, right_cont, line):
        
        """
        Create an object of ContextWindow class.
        param@: 'position' - position of the word in question;
        param@: 'left_cont' - the left context of the word in question;
        param@: 'right_cont' - the right context of the word in question;
        param@: 'line' - a line in which the word in question is present.
        """

        self.line = line
        self.position = position
        self.left_cont = left_cont
        self.right_cont = right_cont
        
    def __eq__(self, obj):
        """
        This method is needed to compare the objects of class ContextWindow.
        """
        return (self.position == obj.position and self.left_cont == obj.left_cont
                and self.line == obj.line and self.right_cont == obj.right_cont)
    
    def __repr__(self):
        """
        This method creates a string representation of a ContextWindow.
        """
        return '(' + str(self.position) + ','+ str(self.left_cont) + ',' \
               + str(self.right_cont) + ',' + self.line + ')'

    
class GetContextWindow:
        
    def get_one_cw(self, window_size, file_path, p):        
        '''
        This method creates a context window for a one-word query.
        param@ window_size: window size.
        param@ file_path: a path to the file.
        param@ p: position of the word in question.
        return@: a context window.
        '''
        
        # Create an empty list and append position of the word into it
        # because later we will need to extend this list when we will
        # unite windows.
        position =[]
        position.append(p)

        # Create an object of ToTokenize().
        tokenizer = ToTokenize()

        # Open a given file.
        file = open(file_path, 'r')

        # For convenience write position in these variables.
        st = p.start
        end = p.end
        line_num = p.line

        
        # In the file find a line in which the word of the query is,
        # and write it to 'line'.
        for i, line in enumerate(file):
            if i == line_num:
                break

        file.close()

        # Write a tokenized substring into the variable 'right_tokens'
        right_tokens = list(tokenizer.tokenize_reduced(line[st:]))
        
        # If the window_size is bigger than the right substring,
        # than reduce the window size to the length of the substring.
        if window_size > len(right_tokens)-1:
            window_size = len(right_tokens)
            
        
        
        # For each token in enumerated 'right_tokens'.
        for i, token in enumerate(right_tokens):

            
            if i == window_size:
                break
        # Write end.
        right_border =  st + token.start + len(token.wordform)

      
        # This is a left substring. We write it to 'left_sub_line'
        # for our convenience.
        left_tokens = list(tokenizer.tokenize_reduced(line[:end]))

        if window_size > len(left_tokens):
                window_size = len(left_tokens)

 
        # Tokenize the left sub line in reversed order until it is
        # bigger than a context size and write the index
        # of the end of the last one in 'left_border'.
        for i, token in enumerate(left_tokens[::-1]):

            if i == window_size:
                break
        left_border = token.start
        
        cw = ContextWindow(position, left_border, right_border, line)

        return cw


    
    def unite_cws(self, search_results, window_size):
        '''
        This method creates a context window for each word of a query
        and unites those that intersect.
        param@ window_size: window size.
        param@ search_results : results of the search.
        return@: a list of context windows.
        '''
        
        # Create an empty dictionary in which keys are file names
        # and values are list of the context windows.
        cws = {}

        
        for file_name in search_results:

            # Create an empty list for context_windows.
            cws[file_name] = []

            # For each position get a context window.
            for position in search_results[file_name]:
                cw = self.get_one_cw(window_size, file_name, position)
                cws[file_name].append(cw)

        for file in cws:
            
            # This is a counter to allow us perform iterations.
            i = 0

            # For our convenience write a list of context windows
            # in 'array_windows'
            array_windows = cws[file_name]

            while i < len(cws[file]) - 1:
                #print(array_windows[i])

                # If the left context of the window is bigger than that of
                # the previous one, then we unite the windows.
                if (array_windows[i].right_cont > array_windows[i+1].left_cont
                and array_windows[i].line == array_windows[i+1].line):
                    array_windows[i].position.extend(array_windows[i+1].position)
                    array_windows[i].right_cont = array_windows[i + 1].right_cont                    

                    # Delete one of the united windows.
                    del array_windows[i + 1]
                i += 1
                    
        # Return a list of the context windows.                   
        return array_windows

    
if __name__ == '__main__':
    a = SearchEngine('database')
    c = GetContextWindow()
    #print(c.get_one_cw(5, 'text.txt', PositionByLine(10, 14, 0)))
    #print(c.unite_two_windows(ContextWindow(PositionByLine(11, 15, 0), 7, 19, 'ooh la la мама мыла раму 123  frf34'), ContextWindow(PositionByLine(16, 20, 0), 10, 24, 'ooh la la мама мыла раму123  frf34')))
    print(c.unite_cws(a.multi_search('Анна Павловна'), 2))
    #print(c.unite_cws(a.multi_search('мама мыла'), 2))
