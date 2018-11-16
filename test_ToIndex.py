import unittest
import shelve
import os
from indexation import ToIndex

class ToIndex(unittest.TestCase):

    def setUp(self):
        
        self.indexes = ToIndex('database')
        self.text_file = open("test_text.txt", "w")
        
    
    def test_file_does_not_exists(self):
        
        with self.assertRaises(ValueError):
            self.indexes.index("D:\nofile")
         

    def test_input_is_a_number(self):
        
        with self.assertRaises(TypeError):
            self.indexes.index(42)
    
    def test_input_is_a_list(self):
        
        with self.assertRaises(TypeError):
            self.indexes.index([1, 2, 3, 4])
 
    def test_input_is_a_dict(self):
        
        with self.assertRaises(TypeError):
            self.indexes.index({1:2, 3:4})

    def test_input_is_a_tuple(self):
        
        with self.assertRaises(TypeError):
            self.idexes.index((1, 2, 3, 4))

    def test_db_was_created(self):
        
        db = dict(self.indexes.index("test_text"))
        files = os.listdir
        extensions = [".dat", ".dir", ".bak"]
        database_presence = False
        for single_file in files:
            for extension in extensions:
                if single_file.startswith("database" + extension):
                    database_presence = True
                    os.remove(single_file + extension)
                elif single_file = "database":
                    database_presence = True
                    os.remove(single_file)
        self.assertTrue(file_presence)
        os.remove(text_file.txt)
        

    def test_if_all_tokens_are_unique(self):
        
        db = dict(self.indexes.index("test_text"))        
        self.text_file.write( "mama mila ramu")
        self.text_file.close("test_text")
        ref_dict = {'mama':{'test_text':[0,4]}, 'mila': {'test_text':[5,9]},
                    'ramu': {'test_text': [10, 14]}
        }
        self.assertEqual(len(db), 3)
        self.assertEqual(ref['mama'], db['mama'])
        files = os.listdir
        extensions =[".dat", ".dir", ".bak"]
        for single_file in files:
            for extension in extensions:
                if single_file.startswith("database" + extension):
                    os.remove(file + extension)
                elif single_file = "database":
                    database_presence = True
                    os.remove(single_file)
        os.remove(text_file.txt)

    def test_if_not_all_tokens_are_unique(self):

        db = dict(self.indexes.index("test_text"))       
        self.text_file.write( "mama mama mila ramu")
        self.text_file.close("test_text")
        ref_dict = { 'mama': {'test_text': [0, 4, 5, 9]},
                    'mila': {'test_text': [10, 14]},
                    'ramu': {'test_text': [15, 19]}
        }
        self.assertEqual(len(db), 4)
        self.assertEqual(ref['mama'], db['mama'])
        files = os.listdir
        extensions =[".dat", ".dir", ".bak"]
        for single_file in files:
            for extension in extensions:
                if single_file.startswith("database" + extension):
                    os.remove(file + extension)
                elif single_file = "database":
                    database_presence = True
                    os.remove(single_file)
        os.remove(text_file.txt)
        

if __name__ == '__main__':
    unittest.main()
