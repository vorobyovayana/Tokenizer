import unittest
import shelve
import os
from indexation import ToIndex
from indexation import Position

class TestToIndex(unittest.TestCase):

    def setUp(self):
        """
        In this method we create an indexer.
        """
        self.indexer = ToIndex('database')
        self.maxDiff = None
       
  
    def tearDown(self):
        """
        In this method we delete the indexer and destroy the database.
        """
        del self.indexer
        files = os.listdir()

        for single_file in files:
            if single_file == "database": 
                os.remove(single_file)
            else:        

                if single_file.startswith('database.'):                                                            
                    os.remove(single_file)
        
        
    
    def test_file_does_not_exists(self):
        """
        If the file does not exist raise ValueError.
        """        
        with self.assertRaises(ValueError):
            self.indexer.index("nofile.txt")
         

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
            self.indexer.index((1, 2, 3, 4))

    def test_db_was_created(self):
        """
        Test that the database was created.
        """
        
        db = dict(shelve.open('database'))
        text_file = open("test_text.txt", "w")
        text_file.write("mama mila ramu")
        text_file.close()
        files = os.listdir()
        database_presence = False
        for single_file in files:
            if single_file == "database":
                database_presence = True
            else:
                if single_file.startswith("database."):
                    database_presence = True               
        self.assertTrue(database_presence)
        os.remove("test_text.txt")
        

    def test_if_all_tokens_are_unique(self):
        """
        Test that indexer runs correctly if each token occurs only once.
        """
        text_file = open("test_text.txt", "w")
        text_file.write("mama mila ramu")
        text_file.close()
        self.indexer.index('test_text.txt')
        db = shelve.open('database')               
        ref_dict = {'mama' : {'test_text.txt':[Position(0,4)]},
                    'mila' : {'test_text.txt':[Position(5,9)]},
                    'ramu' : {'test_text.txt': [Position(10,14)]}
                    }
        
        self.assertEqual(len(db), 3)
        self.assertEqual(ref_dict, dict(db))
        os.remove("test_text.txt")
        

    def test_if_not_all_tokens_are_unique(self):
        """
        Test that indexer runs correctly if some tokens occur more than once.
        """
        text_file = open("test_text.txt", "w")
        text_file.write("mama mama mila ramu")
        text_file.close()
        self.indexer.index('test_text.txt')
        db = shelve.open('database')       
        ref_dict = {'mama': {'test_text.txt': [Position(0,4), Position(5,9)]},
                    'mila': {'test_text.txt': [Position(10,14)]},
                    'ramu': {'test_text.txt': [Position(15,19)]}
                    }
        
        self.assertEqual(len(db), 3)
        self.assertEqual(ref_dict, dict(db))
        os.remove("test_text.txt")


        
    def test_if_indexing_more_than_one_file(self):
        """
        Test that indexer runs correctly if two files are being indexed.
        """
        text_file = open('test_text.txt', 'w')
        text_file.write('mama mila ramu')
        text_file.close()
        self.indexer.index('test_text.txt')
        another_text_file = open("another_test_text.txt", 'w')
        another_text_file.write('mama')
        another_text_file.close()
        self.indexer.index('another_test_text.txt')
        db = shelve.open('database')
        ref_dict = {
                    'mama': {'another_test_text.txt': [Position(0,4)],
                             'test_text.txt': [Position(0,4)]},
                    'mila': {'test_text.txt': [Position(5,9)]},
                    'ramu': {'test_text.txt': [Position(10,14)]}
                    }
        
        self.assertEqual(ref_dict, dict(db))
        os.remove("test_text.txt")
        os.remove("another_test_text.txt")

if __name__ == '__main__':
    unittest.main()

