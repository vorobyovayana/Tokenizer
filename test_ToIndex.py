import unittest
import shelve
import os
from indexation import ToIndex


class ToIndex(unittest.TestCase):

    def setUp(self):
        """
        In this method we create an indexer, a position and a text file.
        """
        self.indexer = ToIndex('database')
        self.text_file = open("test_text.txt", "w")
  
    def tearDown(self):
        """
        In this method we destroy database and file text.
        """
        files = os.listdir
        extensions = [".dat", ".dir", ".bak"]
        for single_file in files:
            if single_file == "database": 
                    os.remove(single_file)
            else:        
                for extension in extensions:
                    if single_file.startswith("database" + extension):                                                            
                        os.remove(file + extension)
        os.remove(text_file.txt)
        
    
    def test_file_does_not_exists(self):
        """
        If the file does not exist raise ValueError.
        """        
        with self.assertRaises(ValueError):
            self.indexer.index("D:\nofile")
         

    def test_input_is_a_number(self):
        """
        If the input is a number raise TypeError.
        """        
        with self.assertRaises(TypeError):
            self.indexer.index(42)
    
    def test_input_is_a_list(self):
        """
        If the input is a list raise TypeError.
        """ 
        with self.assertRaises(TypeError):
            self.indexer.index([1, 2, 3, 4])
 
    def test_input_is_a_tuple(self):
        """
        If the input is a tuple raise TypeError.
        """ 
        with self.assertRaises(TypeError):
            self.idexer.index((1, 2, 3, 4))

    def test_db_was_created(self):
        """
        Test that the database was created.
        """
        self.text_file.write( "mama mila ramu")
        self.text_file.close("test_text")
        db = dict(self.indexer.index("test_text"))
        files = os.listdir
        extensions = [".dat", ".dir", ".bak"]
        database_presence = False
        for single_file in files:
            for extension in extensions:
                if single_file.startswith("database" + extension):
                    database_presence = True
                elif single_file == "database":
                    database_presence = True
        self.assertTrue(file_presence)
        

    def test_if_all_tokens_are_unique(self):
        """
        Test that indexer runs correctly if each token occurs only once.
        """
        self.text_file.write( "mama mila ramu")
        self.text_file.close("test_text")
        db = dict(self.indexer.index("test_text"))               
        ref_dict = {
            'mama' : {'test_text':[Position(0,4)]},
            'mila' : {'test_text':[Position(5,9)]},
            'ramu' : {'test_text': [Position(10,14)]}
        }
        self.assertEqual(len(db), 3)
        self.assertEqual(ref['mama'], db['mama'])

    def test_if_not_all_tokens_are_unique(self):
        """
        Test that indexer runs correctly if some tokens occur more than once.
        """
        self.text_file.write( "mama mama mila ramu")
        self.text_file.close("test_text")
        db = dict(self.indexer.index("test_text"))       
        ref_dict = {
            'mama': {'test_text': [Position(0,4), Position(5,9)]},
            'mila': {'test_text': [Position(10,14)]},
            'ramu': {'test_text': [Position(15,19)]}
        }
        self.assertEqual(len(db), 4)
        self.assertEqual(ref['mama'], db['mama'])
   


if __name__ == '__main__':
    unittest.main()

