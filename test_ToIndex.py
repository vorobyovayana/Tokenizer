import unittest
from indexation import ToIndex

class ToIndex:

    def setUp(self):
        """
        Create an object of the class ToTokenize.
        """
        self.token = ToIndex()


    def test_filename_exists(self):
        
        with self.assertRaises(ValueError):
            self.token.index("D:\nofile")
         

    def test_input_is_a_number(self):
        
        with self.assertRaises(TypeError):
            self.token.index(42)
    
    def test_input_is_a_list(self):
        
        with self.assertRaises(TypeError):
            self.token.index([1, 2, 3, 4])
 
    def test_input_is_a_dict(self):
        
        with self.assertRaises(TypeError):
            self.token.index({1:2, 3:4})

    def test_input_is_a_tuple(self):
        
        with self.assertRaises(TypeError):
            self.token.index((1, 2, 3, 4))

    def test_db_was_created(self):
        
        db = dict(self.token.index("test_text"))
        files = os.listdir
        extensions=[".dat", ".dir", ".bak"]
        file_presence= False
        for file in files:
            for extension in extensions:
                if file.endswith(extension):
                    file_presence = True
        self.assertEqual(file_presence, True)
        

    def test_if_all_tokens_are_unique(self):

        db = dict(self.token.index("test_text"))
        ref_dict = {'mama':{'test_text':[0,4]}, 'mila': {'test_text':[5,9]}, 'ramu': {'test_text': [10, 14]}}
        self.assertEqual(len(db), 3)
        self.assertEqual(ref['mama'], db['mama'])
        files = os.listdir
        extensions=[".dat", ".dir", ".bak"]
        for file in files:
            for extension in extensions:
                if file.endswith(extension):
                    os.remove("D:\python_projects\\" + file + extension)

    def test_if_not_all_tokens_are_unique(self):

        db = dict(self.token.index("test_text_not_unique"))
        ref_dict= { 'mama': {'test_text_not_unique': [0, 4, 5, 9], 'mila': {'test_text_not_unique': [10, 14]}}, 'ramu': {'test_text_not_unique': [15, 19]}}
        self.assertEqual(len(db), 4)
        self.assertEqual(ref['mama'], db['mama'])
        files = os.listdir
        extensions=[".dat", ".dir", ".bak"]
        for file in files:
            for extension in extensions:
                if file.endswith(extension):
                    os.remove("D:\python_projects\\" + file + extension)
    
        

if __name__ == '__main__':
    unittest.main()
