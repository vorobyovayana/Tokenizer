import shelve
import os
import unittest
from search_engine import SearchEngine
from indexation import ToIndex
from indexation import PositionByLine

class TestSearchEngine(unittest.TestCase):

    def setUp(self):
        indexer = ToIndex('database')
        self.maxDiff = None
        text = open('test_text.txt', 'w')
        text.write('mama мыла ramu')
        text.close()
        indexer.index_by_line('test_text.txt')
        del indexer
        self.search_eng = SearchEngine('database')

    def tearDown(self):

        del self.search_eng
        files = os.listdir()
        for single_file in files:
            if single_file == "database": 
                os.remove(single_file)
            else:        

                if single_file.startswith('database.'):                                                            
                    os.remove(single_file)
        os.remove('test_text.txt')
        
    def test_empty_query(self):
        
        with self.assertRaises(ValueError):
            self.search_eng.search("")

    def test_query_is_a_number(self):
        """
        If the input is a number raise TypeError.
        """        
        with self.assertRaises(TypeError):
            self.search_eng.search(42)

    def test_program_runs_okay(self):
        search_res = self.search_eng.search('мыла')
        ref_res = {'test_text.txt': [5, 9, 0]}
        self.assertEqual(ref_res, search_res)


if __name__ == '__main__':
    unittest.main()
        
