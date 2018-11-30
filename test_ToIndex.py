import unittest
import shelve
import os
from indexation import ToIndex


class ToIndex(unittest.TestCase):

    def setUp(self):
        """
        In this method we create an indexer and a text file.
        """
        self.indexer = ToIndex('database')
        self.text_file = open("test_text.txt", "w")
  
    def tearDown(self):
        """
        In this method we destroy the database and the file text.
        """
        files = os.listdir()
        extensions = [".dat", ".dir", ".bak"]
        for single_file in files:
            if single_file == "database": 
                os.remove(single_file)
            else:        
                for extension in extensions:
                    if single_file.startswith("database" + extension):                                                            
                        os.remove(single_file + extension)
        os.remove("test_text.txt")
        
    
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
        db = dict(self.indexer.index("test_text.txt"))
        self.text_file.write("mama mila ramu")
        self.text_file.close()
        files = os.listdir()
        extensions = [".dat", ".dir", ".bak"]
        database_presence = False
        for single_file in files:
            if single_file == "database":
                database_presence = True
            else:
                for extension in extensions:
                    if single_file.startswith("database" + extension):
                        database_presence = True               
        self.assertTrue(database_presence)
        

    def test_if_all_tokens_are_unique(self):
        """
        Test that indexer runs correctly if each token occurs only once.
        """
        self.text_file.write( "mama mila ramu")
        self.text_file.close("test_text")
        db = dict(self.indexer.index("test_text.txt"))               
        ref_dict = {'mama' : {'test_text.txt':[Position(0,4)]},
                    'mila' : {'test_text.txt':[Position(5,9)]},
                    'ramu' : {'test_text.txt': [Position(10,14)]}
                   }
        self.assertEqual(len(db), 3)
        self.assertEqual(ref_dict, db)
        

    def test_if_not_all_tokens_are_unique(self):
        """
        Test that indexer runs correctly if some tokens occur more than once.
        """
        self.text_file.write("mama mama mila ramu")
        self.text_file.close()
        db = dict(self.indexer.index("test_text.txt"))       
        ref_dict = {'mama': {'test_text.txt': [Position(0,4), Position(5,9)]},
                    'mila': {'test_text.txt': [Position(10,14)]},
                    'ramu': {'test_text.txt': [Position(15,19)]}
                    }
        self.assertEqual(len(db), 4)
        self.assertEqual(ref_dict, db)

    def test_if_indexing_more_than_one_file(self):
        """
        Test that the method runs correctly if more than one text file is indexed.
        """
        self.text_file.write('mama mila ramu')
        self.text_file.close()
        another_text_file = open("another_test_text.txt", "w")
        another_text_file.write('mama ne mila ramu')
        another_text_file.close()
        self.indexer.index("test_text.txt")
        self.indexer.index("another_test_text.txt")
        files = os.listdir()
        extensions = [".dat", ".dir", ".bak"]
        for single_file in files:
            if single_file == "database":
                db = shelve.open(single_file)
            else:
                for extension in extensions:
                    if single_file.startswith("database" + extension):
                        db = shelve.open(single_file)
        ref_dict = {'mama': {'test_text.txt': [Position(0,4)], 'another_test_text.txt': [Position(0,4)]},
                    'ne': {'another_test_text.txt': [Position(5,7)]}
                    'mila': {'test_text.txt': [Position(5,9)], 'another_test_text.txt': [Position(8,12)]},
                    'ramu': {'test_text.txt': [Position(10,14)], 'another_test_text.txt': [Position(13,17)]}
                    }
        self.assertEqual(ref_dict, dict(db))
        os.remove('another_text_file.txt')


if __name__ == '__main__':
    unittest.main()
