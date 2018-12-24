import shelve
import os
import unittest
from search_engine import SearchEngine
from indexation import ToIndex
from indexation import PositionByLine

class TestSearchEngine(unittest.TestCase):

    def setUp(self):
        '''
        Create an indexer, create a text file,
        index it, then delete the file and the indexer.
        Then create an object of SearchEngine()
        '''
        indexer = ToIndex('database')
        self.maxDiff = None
        text = open('test_text.txt', 'w')
        text.write('mama мыла ramu')
        text.close()
        indexer.index_by_line('test_text.txt')
        del indexer
        self.search_eng = SearchEngine('database')

    def tearDown(self):
        '''
        In this method we destroy an object of SearchEngine()
        and delete 'database'.
        '''
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
        '''
        Test that ValueError is raised if the query is an empty string.
        '''
        
        with self.assertRaises(ValueError):
            self.search_eng.search("")
            
    def test_query_not_in_db(self):
        '''
        Test that ValueError is raised if the query is not
        in database.
        '''
        with self.assertRaises(ValueError):
            self.search_eng.multi_search('crocodile')

    def test_query_is_a_number(self):
        """
        If the query is a number raise TypeError.
        """        
        with self.assertRaises(TypeError):
            self.search_eng.search(42)

    def test_program_runs_okay(self):
        '''
        Test that program runs as expected given there is one word in the query
        and one file in the database.
        '''
        search_res = self.search_eng.search('мыла')
        ref_dict = {'test_text.txt': [5, 9, 0]}
        self.assertEqual(ref_dict, search_res)
        
class MultiSearchEngine(unittest.TestCase):
    
    def setUp(self):
        '''
        In this method we create an indexer, create a text file,
        index it, then delete the file and the indexer.
        Then create an object of SearchEngine()
        '''
        indexer = ToIndex('database')
        self.maxDiff = None
        text = open('test_text.txt', 'w')
        text.write('Ах, не говорите мне про Австрию! \
                    Я ничего не понимаю, может быть')
        text.close()
        another_text = open('another_test_text.txt', 'w')
        another_text.write('но Австрия никогда не хотела и не хочет войны.\
                            Она предает нас')
        another_text.close()
        indexer.index_by_line('another_test_text.txt')
        indexer.index_by_line('test_text.txt')
        del indexer
        self.search_eng = SearchEngine('database')
    
    def tearDown(self):
        '''
        In this method we destroy an object of SearchEngine()
        and delete 'database'.
        '''
        del self.search_eng
        files = os.listdir()
        for single_file in files:
            if single_file == "database": 
                os.remove(single_file)
            else:        

                if single_file.startswith('database.'):                                                            
                    os.remove(single_file)
        os.remove('test_text.txt')
        os.remove('another_test_text.txt')
    def test_empty_query(self):
        '''
        Test that ValueError is raised if the query is an empty string.
        '''
        with self.assertRaises(ValueError):
            self.search_eng.search("")
            
    def test_query_not_in_db(self):
        '''
        Test that ValueError is raised if the query is not
        in database.
        '''
        with self.assertRaises(ValueError):
            self.search_eng.multi_search('crocodile')

    def test_query_is_a_number(self):
        """
        If the input is a number raise TypeError.
        """        
        with self.assertRaises(TypeError):
            self.search_eng.search(42)
            
    def test_program_runs_okay_with_one_word_query(self):
        '''
        Test that program runs as expected given there is one word
        in the query and two files in the database.
        '''

        search_res = self.search_eng.search('Австрия')
        ref_dict = {'test_text.txt': [24, 31, 0], 'another_test_text.txt': [3, 10, 0]}
        self.assertEqual(ref_dict, search_res)

    def test_program_runs_okay_with_several_word_query(self):
        '''
        Test that program runs as expected given there are two words
        in the query and two files in the database.
        '''
        search_res = self.search_eng.search('про Австрию')
        ref_dict = {'test_text.txt': [20, 23, 0, 24, 31, 0]}
        self.assertEqual(ref_dict, search_res)

if __name__ == '__main__':
    unittest.main()
        
