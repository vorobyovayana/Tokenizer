"""
This module was made to chunk a string into wordforms.
It consists of two classes: class Token and class ToTokenize.
"""
import unicodedata
import shelve


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

class TokenWithType(Token):

    def __init__(self, s, wordform, tp):

        self.wordform = wordform
        self.start = s
        self.tp=tp

    def __repr__(self):
        """
        This method creates a string representation of a token.
        """
        return self.tp + ", " + "'"+self.wordform + "'"


class ToTokenize:
    """
    The method produces tokenization in terms of method tokenize().
    It takes a  string, chunks it into tokens and returns a list of tokens.
    """
    def tokenize(self, stream):
        """
        This method produces tokenization on an alphabetical string.
        @param: a string
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

            # If a character is the beginning of the whole stream
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
                token = Token(start, stream[start:i])
                tokens.append(token)

        # Usually, a token is created and appended to the list of tokens
        # only if the current character is not alphabetical.
        # If the stream ends with an alphabetical character
        # the token of the last wordform is not created.
        # That's why we need to create it manually in the case bellow.
        if stream[-1].isalpha():
            token = Token(start, stream[start:])
            tokens.append(token)
        return tokens

    def tokenize_with_generator(self,stream):
        """
        This method produces tokenization on an alphabetical string.
        It does not return a list of tokens. Instead we use 'yield'.
        @param: a string
        @return: tokens
        """

        # Raise TypeError if the input type is not string
        if not isinstance(stream,str):
            raise(TypeError)

        # Raise ValueError if the input string is empty.
        if len(stream) == 0:
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
            # then we tokencreate a token and write the begining of the wordform
            # to the attribute 'start'
            # and the wordform -- a slice of the string from the 'start'
            # to the current character -- to the attribute 'word_form'.
            elif (not c.isalpha() and stream[i - 1].isalpha()) and (i!=0):
                token = Token(start, stream[start:i])

                # Yield a current token.
                yield token

        # Usually, a token is created and appended to the list of tokens
        # only if the current character is not alphabetical.
        # If the stream ends with an alphabetical character
        # the token of the last wordform is not created.
        # That's why we need to create it manually in the case bellow.
        if stream[-1].isalpha():
            token = Token(start, stream[start:])

            # Yield a current token.
            yield token

    @staticmethod
    def get_type(i):
        """
        This static method is used to define a type of a character
        """

        # If the character is alphabetical, write 'a' into the variable 'tp'.
        if i.isalpha():
            tp='a'
        # If the character is digit, write 'd' into the variable 'tp'.
        elif i.isdigit():
            tp= 'd'
        # If the character is a space, write 's' into the variable 'tp'.
        elif i.isspace():
            tp='s'
        # If the character is a punctuation character, write 'p'
        # into the variable 'tp'.
        elif unicodedata.category(i).startswith('P'):
            tp='p'
        else:
            tp = 'o'
        return tp

    def tokenize_with_types(self, stream):
        """
        This method produces tokenization on a string.
        We consider four types of tokens: alphabetical,
        digital, punctuation tokens
        and tokens consisting of one or more spaces.
        The method yields a type of the token and the srting representation
        of the token.
        @param: a string
        @return: a token
        """

        # Raise TypeError if the input type is not string
        if not isinstance(stream, str):
            raise(TypeError)

        # Raise ValueError if the input string is empty.
        if len(stream) == 0:
            return

        # Enumerate all the characters in stream.
        for i,c in enumerate(stream):

            # Save the type of the current character to a variable 'curr_tp'
            curr_tp = self.get_type(stream[i])

            # If a character is the begining of the whole stream
            # we save the index of the character to the variable 'start'.
            if (i == 0) :
                start = i

                # Save the current character to a variable 'prev_tp'
                # so on the next iteration we know the type of the previous
                # character.
                prev_tp = curr_tp
                
            # If a type of the current character is not the same with the type
            # of the character previous to it
            # then we create a token and write the begining of the wordform
            # to the attribute 'start'
            # and the wordform -- a slice of the string from the 'start'
            # to the current character -- to the attribute 'word_form'.
            elif (curr_tp != prev_tp):
                token = TokenWithType(start, stream[start:i], prev_tp)


                # Yield a current token.
                yield token
                # Write the index of the current character
                # to the variable 'start'
                start = i


                # Save the current character to a variable 'prev_tp'
                # so on the next iteration we know the type of the previous
                # character.
                prev_tp = curr_tp

            
        # Usually, a token is created and appended to the list of tokens
        # only if a type of the current character is not the same with the type
        # of the character previous to it
        # If the last character of the stream and the one previous to it
        # have the same type then the token of the last wordform
        # is not created.
        # That's why we need to create it manually in the case bellow.
        if (i == len(stream)-1) and (curr_tp == prev_tp ):
            token = TokenWithType(start, stream[start:], prev_tp)

            # Yield a current token.
            yield token

            # Write the index of the current character to the variable 'start'
            start = i

        # If a type of the current character is not the same with the type
        # of the character previous to it than only the last
        # character is yielded.
        elif (i == len(stream)-1) and (curr_tp != prev_tp ):
            token = TokenWithType(start, stream[-1], prev_tp)
            
            # Yield a current token.
            yield token

            # Write the index of the current character to the variable 'start'
            start = i

    def tokenize_reduced(self, stream):
        """"
        This method is used to return only alphabetic and digital characters.
        @param: a string
        @return: a token
        """
        for token in (self.tokenize_with_types(stream)):
            if token.tp == 'a' or token.tp == 'd':
                yield token


            
if __name__ == '__main__':
    a = ToTokenize()
    #print(a.tokenize(" name 'self' is not defined!"))
    #for i in (a.tokenize_with_generator("Usually, a token is created and appended to the list of tokens")):
        #print(i)
    #for i in (a.tokenize_with_types("The method is needed e356to create tokens")):
        #print(i)
    
    for i in ((a.tokenize_reduced("E123tokeni   zation.py78655a"))):
        print(i.wordform)  
