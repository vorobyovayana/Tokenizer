import shelve
import os
import re
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

    def get_several_cws(self, search_results, window_size):

        
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
                
        return cws

    
    def unite_cws(self, cws):
        '''
        This method unites intersected context windows.
        param@ cws: a dictionary of context windows.
        return@: a dictionary of context windows with united intersections.
        '''
        
        for file in cws:
            
            # This is a counter to allow us perform iterations.
            i = 0

            # For our convenience write a list of context windows
            # in 'array_windows'
            array_windows = cws[file]

            while i < len(cws[file]) - 1:
                
                # If context windows are intersected, unite them.
                if self.check_intersection(array_windows[i], array_windows[i + 1]) == True:
                    
                    array_windows[i] = self.unite_windows(array_windows[i], array_windows[i + 1])

                    # Delete the second window.
                    del array_windows[i + 1]

                i +=1

            return array_windows

    def check_intersection(self, cw_1, cw_2):
        '''
        This method checks if two windows are intersected.
        param@ cw_1: the first window.
        param@ cw_2: the second window.
        return@: a boolean variable that is 'True' if the windows are intersected.
        '''

        intersection = False

        # If the left context of the window is bigger than that of
        # the another one,
        # and the line of the window is same as that of
        # the another one, then the windows are intersected.
        if (cw_1.right_cont > cw_2.left_cont
        and cw_1.line == cw_2.line):
            
            intersection = True
            
        return intersection
        

    def unite_windows(self, cw_1, cw_2):  
        '''
        This method unites two intersected windows.
        param@ cw_1: the first window.
        param@ cw_2: the second window.
        return@: a united window
        '''
        
        # Add the position of the second window to that of the
        # first one.
        cw_1.position.extend(cw_2.position)
        # Write right context of the second window tothat of the
        # first one.
        cw_1.right_cont = cw_2.right_cont

        return cw_1

    def get_united_cws(self, search_results, window_size):
        '''
        This method provides context windows for a multi-word query
        and unite intersected windows.
        param@ window_size: window size.
        param@ search_results : results of the search.
        return@: a dictionary of united context windows.
        '''

        cws = self.get_several_cws(search_results, window_size)

        for file in cws:
            cws[file] = self.unite_cws(cws)

        return cws
    
    def extend_window_to_sentence(self, cw):
        '''
        This method extends a context window to the boundaries
        of a sentence it is situated in.
        '''

        # Create a pattern with regular expressions to detect
        # the end and the beginning of the sentence.
        end_pattern = re.compile(r'[.?!]\s[A-ZА-Я]')
        start_pattern = re.compile(r'[A-ZА-Я]\s[.?!]')

        # For convenienve write substrings on the left and on the right
        # of the window into single variables.
        left_substr = cw.line[: cw.left_cont + 1]
        right_substr = cw.line[cw.right_cont :]
        
        # Search a substring that matches our pattern on
        # 'left_substr' and 'right_substr'.
        # For convenience write the result to variables
        # 'start' and 'end'.
        start = re.search(start_pattern, left_substr)
        end = re.search(end_pattern, right_substr)


        # If there is a substring that matches our 'end_pattern'
        # than we move the position of the right context to the
        # first character of this substring.
        if end != None:
            cw.right_cont = cw.right_cont + end.start()

        # Otherwise we move the position of the right context to the
        # end of the line in which the context window is situated.
        else:
            cw.right_cont = len(cw.line)

        # If there is a substring that matches our 'start_pattern'
        # than we move the position of the left context to the
        # first character of this substring.
        if start != None:
            cw.left_cont = cw.left_cont - start.start()

        # Otherwise we move the position of the left context to the
        # start of the line in which the context window is situated.
        else:
            cw.left_cont = 0

    def get_extended_cws(self, search_results, window_size):

        '''
        This method extends a context window to the boundaries
        of a sentence it is situated in.
        param@ window_size: window size.
        param@ search_results : results of the search.
        return@: a dictionary of extended context windows without intersections.
        '''
        
        # Get a context window for each word of the query.
        cws = self.get_several_cws(search_results, window_size)

        for file in cws:
            for cw in cws[file]:
                # Extend the context to the boundaries of the sentence.
                self.extend_window_to_sentence(cw)
        # Unite intersected windows.
        cws = self.unite_cws(cws)

        return cws

    def make_it_bold(self, cw):
        #is not finished
        
        i = 0
        result_line = ''
        for pos in cw.position:

            for i, char in enumerate(cw.line):

                if i == pos.start:
                    print(i, 'i', pos.start, 'st')
                    result_line += '<b>'
                
                if i == pos.end:
                    result_line += '</b>'
                result_line += char

        cw.line = result_line
        
            #cw.line = cw.line[: pos.start] + '<b>' + cw.line[pos.start : pos.end] + '</b>' + cw.line[pos.end:]
            #cw.line = cw.line[: pos.start] + '<strong>' + cw.line[pos.start : pos.end] + '</strong>' + cw.line[pos.end:]
        return cw
        
    def get_bold_cws(self, search_results, window_size):        
        #is not finished
        

        cws = self.get_several_cws(search_results, window_size)
        
        for file in cws:
            for cw in cws[file]:
                self.make_it_bold(cw)
        return cws

    
if __name__ == '__main__':
    a = SearchEngine('database')
    c = GetContextWindow()
    #print(c.get_one_cw(5, 'text.txt', PositionByLine(10, 14, 0)))
    #print(c.get_united_cws(a.multi_search('Анна Павловна'), 2))
    print(c.get_extended_cws(a.multi_search('Анна Павловна'), 2))
    #print(c.unite_cws(a.multi_search('мама мыла'), 2))
    #print(c.get_bold_cws(c.get_united_cws(a.multi_search('Анна Павловна'), 2), ))
