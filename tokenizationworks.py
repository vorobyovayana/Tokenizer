"""
This module was made to chunk a string into wordforms.
It consists of two classes: class Token and class ToTokenize.
"""


class Token:
    """
    Class Token is needed to create objects of Token type.
    The objects have two attributes:
    'start' which is an index of the first character of a wordform,
    and 'wordform' which is the wordform.
    """

    def __init__(self, s, wordform):
        """
        The method is needed to create tokens --
        objects that have two attributes:
        @param: starting index
        @param: a word form
        """

        self.wordform = wordform
        self.start = s

    def __repr__(self):
        """
        This method creates a string representation of a token.
        """
        return self.wordform


class ToTokenize:
    """
    The method produces tokenization in terms of method tokenize().
    It takes a  string, chunks it into tokens and returns a list of tokens.
    """

    def tokenize(self, stream):
        """
        This method produces tokenization on an alphabetical string.
        @params: a string
        @return: a list of tokens
        """
        # Raise TypeError if the input type is not string.
        if not isinstance(stream,str):
            raise(TypeError)

        # Raise ValueError if the input string is empty.
        if len(stream)==0:
            return []
        
        # Create a list of tokens which we are going to return.
        tokens = []

        # Enumerate all the characters in stream.
        for i, c in enumerate(stream):

            # If a character is the begining of the whole stream
            # or if the character previous to it is not alphabetical
            # we save the index of the character to the variable 'start'
            if (i == 0 and c.isalpha()) or (c.isalpha() and not stream[i - 1].isalpha()):
                start = i

            # If the character is not alphabetical
            # and the character previous to it is alphabetical
            # then we create a token and write the begining of the wordform
            # to the attribute 'start'
            # and the wordform -- a slice of the string from the 'start'
            # to the current character -- to the attribute 'word_form'.
            elif (not c.isalpha() and stream[i - 1].isalpha()) and (i!=0):
                token = Token(None, "")
                token.start = start
                token.wordform = stream[start:i]
                tokens.append(token)

        # Usually, a token is created and appended to the list of tokens
        # only if the current character is not alphabetical.
        # If the stream ends with an alphabetical character
        # the token of the last wordform would not be created.
        # That's why we need to create it manually in the case bellow.
        if stream[-1].isalpha():
            token = Token(None, "")
            token.start = start
            token.wordform = stream[start:]
            tokens.append(token)
        return tokens

    def tokenize_with_generator(self,stream):
        """
        This method produces tokenization on an alphabetical string.
        It does not return a list of tokens. Instead we use 'yield'.
        @params: a string
        @return: tokens
        """

        # Raise TypeError if the input type is not string
        if not isinstance(stream,str):
            raise(TypeError)

        # Raise ValueError if the input string is empty.
        if len(stream)==0:
            return

        # Enumerate all the characters in stream.
        for i,c in enumerate(stream):

            # If a character is the begining of the whole stream
            # or if the character previous to it is not alphabetical
            # we save the index of the character to the variable 'start'
            if (i == 0 and c.isalpha()) or (c.isalpha() and not stream[i - 1].isalpha()):
                start = i

            # If the character is not alphabetical
            # and the character previous to it is alphabetical
            # then we create a token and write the begining of the wordform
            # to the attribute 'start'
            # and the wordform -- a slice of the string from the 'start'
            # to the current character -- to the attribute 'word_form'.
            elif (not c.isalpha() and stream[i - 1].isalpha()) and (i!=0):
                token = Token(None, "")
                token.start = start
                token.wordform = stream[start:i]
                
                # Yield a current token.
                yield token

            # Usually, a token is created and appended to the list of tokens
            # only if the current character is not alphabetical.
            # If the stream ends with an alphabetical character
            # the token of the last wordform would not be created.
            # That's why we need to create it manually in the case bellow.
        if stream[-1].isalpha():
            token = Token(None, "")
            token.start = start
            token.wordform = stream[start:]
            
            # Yield a current token.
            yield token
        

a = ToTokenize()
#print(a.tokenize(" name 'self' is not defined!"))
for i in (a.tokenize_with_generator("Usually, a token is created and appended to the list of tokens")):
    print(i)

