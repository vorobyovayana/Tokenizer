import unittest
from tokenizationworks import ToTokenize

class TestTokenize(unittest.TestCase):
    
    def setUp(self):
        """
        Create an object of the class ToTokenize.
        """
        self.token= ToTokenize()

    def test_input_is_an_empty_string(self):
        """
        Test that if the input is an empty string than
        the empty list of tokens is returned.
        """
        tokens=self.token.tokenize("")
        self.assertEqual(len(tokens),0)    
            
    def test_input_type_is_a_number(self):
        """
        Test that if the input is an integer than TypeError is raised.
        """
        with self.assertRaises(TypeError):
            self.token.tokenize(42)
    
    def test_input_type_is_a_list(self):
        """
        Test that if the input is a list than TypeError is raised.
        """
        with self.assertRaises(TypeError):
            self.token.tokenize([1,2,3,4])
    
    def test_input_type_is_a_dict(self):
        """
        Test that if the input is a dictionary than TypeError is raised.
        """
        with self.assertRaises(TypeError):
            self.token.tokenize({1:2,3:4})
   
    def test_input_type_is_a_tuple(self):
        """
        Test that if the input is a tuple than TypeError is raised.
        """
        with self.assertRaises(TypeError):
            self.token.tokenize((1,2,3,4))
                   
    def test_the_first_char_is_alpha(self):
        """
        Test that the method functions correctly
        if the first character is alphabetical. 
        """
        tokens=self.token.tokenize("name 'self' is not defined")
        self.assertEqual(tokens[0].wordform[0], "n")
        self.assertIsInstance(tokens, list)
        self.assertEqual(len(tokens),5)

    
    def test_the_first_char_is_not_alpha(self):
        """
        Test that the method functions correctly
        if the first character is not alphabetical.
        """
        tokens=self.token.tokenize(" name 'self' is not defined")
        self.assertEqual(tokens[0].wordform[0], "n")
        self.assertIsInstance(tokens, list)
        self.assertEqual(len(tokens),5)

    
    def test_the_last_char_is_alpha(self):
        """
        Test that the method functions correctly
        if the last character is alphabetical.
        """
        tokens=self.token.tokenize("name 'self' is not defined")
        self.assertEqual(tokens[4].wordform[-1],"d")
        self.assertIsInstance(tokens, list)
        self.assertEqual(len(tokens),5)

    
    def test_the_last_char_is_not_alpha(self):
        """
        Test that the method functions correctly
        if the last character is not alphabetical.
        """
        
        tokens=self.token.tokenize("name 'self' is not defined!")
        self.assertEqual(tokens[4].wordform[-1], "d")
        self.assertIsInstance(tokens, list)
        self.assertEqual(len(tokens),5)

class TestTokenizeWithGenerator(unittest.TestCase):
    
    def setUp(self):
        """
        Create an object of the class ToTokenize.
        """
        self.token= ToTokenize()

    def test_input_is_an_empty_string(self):
        """
        Test that if the input is an empty string than
        the empty list of tokens is returned.
        """
        tokens=list(self.token.tokenize_with_generator(""))
        self.assertEqual(len(tokens),0)   
            
    def test_input_type_is_a_number(self):
        """
        Test that if the input is an integer than TypeError is raised.
        """
        with self.assertRaises(TypeError):
            tokens=list(self.token.tokenize_with_generator(42))
            self.token.tokens
    
    def test_input_type_is_a_list(self):
        """
        Test that if the input is a list than TypeError is raised.
        """
        with self.assertRaises(TypeError):
            tokens=list(self.token.tokenize_with_generator([1,2,3,4]))
            self.token.tokens
    
    def test_input_type_is_a_dict(self):
        """
        Test that if the input is a dictionary than TypeError is raised.
        """
        with self.assertRaises(TypeError):
            tokens=list(self.token.tokenize_with_generator({1:2,3:4}))
            self.token.tokens
   
    def test_input_type_is_a_tuple(self):
        """
        Test that if the input is a tuple than TypeError is raised.
        """
        with self.assertRaises(TypeError):
            tokens=list(self.token.tokenize_with_generator((1,2,3,4)))
            self.token.tokens
    def test_the_first_char_is_alpha(self):
        """
        Test that the method functions correctly
        if the first character is alphabetical. 
        """
        tokens=list(self.token.tokenize_with_generator("name 'self' is not defined"))
        self.assertEqual(tokens[0].start,0)
        self.assertEqual(tokens[0].wordform, "name")
        self.assertIsInstance(tokens, list)
        self.assertEqual(len(tokens),5)

    def test_the_first_char_is_not_alpha(self):
        """
        Test that the method functions correctly
        if the first character is not alphabetical.
        """
        tokens=list(self.token.tokenize_with_generator(" name 'self' is not defined"))
        self.assertEqual(tokens[0].start,1)
        self.assertEqual(tokens[0].wordform, "name")
        self.assertIsInstance(tokens, list)
        self.assertEqual(len(tokens),5)

    
    def test_the_last_char_is_alpha(self):
        """
        Test that the method functions correctly
        if the last character is alphabetical.
        """
        tokens=list(self.token.tokenize_with_generator("name 'self' is not defined"))
        self.assertEqual(tokens[0].start,0)
        self.assertEqual(tokens[0].wordform, "name")
        self.assertIsInstance(tokens, list)
        self.assertEqual(len(tokens),5)


    
    def test_the_last_char_is_not_alpha(self):
        """
        Test that the method functions correctly
        if the last character is not alphabetical.
        """
        tokens=list(self.token.tokenize_with_generator("name 'self' is not defined!"))
        self.assertEqual(tokens[0].start,0)
        self.assertEqual(tokens[0].wordform, "name")
        self.assertIsInstance(tokens, list)
        self.assertEqual(len(tokens),5)


class TestTokenizeWithTypes(unittest.TestCase):
    
    def setUp(self):
        """
        Create an object of the class ToTokenize.
        """
        self.token= ToTokenize()

    def test_input_is_an_empty_string(self):
        """
        Test that if the input is an empty string than
        the empty list of tokens is returned.
        """
        tokens=list(self.token.tokenize_with_types(""))
        self.assertEqual(len(tokens),0)   
            
    def test_input_type_is_a_number(self):
        """
        Test that if the input is an integer than TypeError is raised.
        """
        with self.assertRaises(TypeError):
            tokens=list(self.token.tokenize_with_types(42))
            self.token.tokens
    
    def test_input_type_is_a_list(self):
        """
        Test that if the input is a list than TypeError is raised.
        """
        with self.assertRaises(TypeError):
            tokens=list(self.token.tokenize_with_types([1,2,3,4]))
            self.token.tokens
    
    def test_input_type_is_a_dict(self):
        """
        Test that if the input is a dictionary than TypeError is raised.
        """
        with self.assertRaises(TypeError):
            tokens=list(self.token.tokenize_with_types({1:2,3:4}))
            self.token.tokens
   
    def test_input_type_is_a_tuple(self):
        """
        Test that if the input is a tuple than TypeError is raised.
        """
        with self.assertRaises(TypeError):
            tokens=list(self.token.tokenize_with_types((1,2,3,4)))
            self.token.tokens
    
    def test_the_first_char_is_alpha(self):
        """
        Test that the method functions correctly
        if the first character is alphabetical. 
        """
        tokens=list(self.token.tokenize_with_types("name 'self' is not defined"))
        self.assertEqual(tokens[0].start,0)
        self.assertEqual(tokens[0].wordform, "name")
        self.assertIsInstance(tokens, list)
        self.assertEqual(len(tokens),11)
        self.assertEqual(tokens[0].tp, 'a')
        self.assertEqual(tokens[1].tp, 's')
        self.assertEqual(tokens[2].tp, 'p')
        
    def test_the_first_char_is_not_alpha(self):
        """
        Test that the method functions correctly
        if the first character is not alphabetical.
        """
        tokens=list(self.token.tokenize_with_types(" name 'self' is not defined"))
        self.assertEqual(tokens[0].start,0)
        self.assertEqual(tokens[0].wordform, " ")
        self.assertIsInstance(tokens, list)
        self.assertEqual(len(tokens),12)
        self.assertEqual(tokens[0].tp, 's')
        self.assertEqual(tokens[1].tp, 'a')
        self.assertEqual(tokens[3].tp, 'p')

    
    def test_the_last_char_is_alpha(self):
        """
        Test that the method functions correctly
        if the last character is alphabetical.
        """
        tokens=list(self.token.tokenize_with_types("name 'self' is not defined"))
        self.assertEqual(tokens[0].start,0)
        self.assertEqual(tokens[0].wordform, "name")
        self.assertIsInstance(tokens, list)
        self.assertEqual(len(tokens),11)
        self.assertEqual(tokens[0].tp, 'a')
        self.assertEqual(tokens[1].tp, 's')
        self.assertEqual(tokens[2].tp, 'p')

    
    def test_the_last_char_is_not_alpha(self):
        """
        Test that the method functions correctly
        if the last character is not alphabetical.
        """
        tokens=list(self.token.tokenize_with_types("name 'self' is not defined!"))
        self.assertEqual(tokens[0].start,0)
        self.assertEqual(tokens[0].wordform, "name")
        self.assertIsInstance(tokens, list)
        self.assertEqual(len(tokens),12)
        self.assertEqual(tokens[0].tp, 'a')
        self.assertEqual(tokens[1].tp, 's')
        self.assertEqual(tokens[2].tp, 'p')       
         

if __name__ == '__main__':
    unittest.main()
