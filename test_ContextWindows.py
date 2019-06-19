import shelve
import os
import unittest
from search_engine import SearchEngine
from context_windows import ContextWindow
from context_windows import Contexter
from indexation import ToIndex
from indexation import PositionByLine

class TestContexter(unittest.TestCase):

    def setUp(self):        
        '''
        Create an indexer, an object of Contexter, an object of SearchEngine,
        a text_file. Also indexes the text file.  Then delet the indexer.      
        '''
        indexer = ToIndex('database')
        self.get_cw = Contexter()
        self.maxDiff = None
        text = open('test_text.txt', 'w')
        text.write('ooh la la мама мыла раму123  frf34')
        text.close()
        indexer.index_by_line('test_text.txt')
        del indexer
        self.search = SearchEngine('database')
        
    def tearDown(self):
        '''
        In this method we destroy an object of SearchEngine(),
        delete 'database' and text file.
        '''
        del self.search
        files = os.listdir()
        for single_file in files:
            if single_file == "database": 
                os.remove(single_file)
            else:        

                if single_file.startswith('database.'):                                                            
                    os.remove(single_file)
        os.remove('test_text.txt')
    
    def test_right_input_type(self):
        '''
        Test that TypeError is raised if the search_results is an empty dictionary.
        '''
        with self.assertRaises(TypeError):
            self.get_cw.get_one_cw([4, 5], 'text.txt', PositionByLine(10, 14, 0))
         
        with self.assertRaises(TypeError):
            self.get_cw.get_one_cw(5, 13, PositionByLine(10, 14, 0))        

        with self.assertRaises(TypeError):
            self.get_cw.get_one_cw(5, 'text.txt', (10, 14, 0))

        with self.assertRaises(TypeError):
            self.get_cw.get_united_cws(self.search.multi_search('мама мыла'), '1')
            
        with self.assertRaises(TypeError):
            self.get_cw.get_united_cws([4, 5], 1)

        with self.assertRaises(TypeError):
            self.get_cw.get_extended_cws(self.search.multi_search('мама мыла'), '1')
            
        with self.assertRaises(TypeError):
            self.get_cw.get_extended_cws([4, 5], 1)

        with self.assertRaises(TypeError):
            self.get_cw.get_bold_cws(self.search.multi_search('мама мыла'), '1')
            
        with self.assertRaises(TypeError):
            self.get_cw.get_bold_cws([4, 5], 1)
    
    def test_empty_dict_of_search_results(self):
        '''
        Test that methods run ok if search results is an empty dictionary.
        '''
        window_size = 1

        u_actual_cw = self.get_cw.get_united_cws({}, window_size)
        u_ref_cw = {}
        self.assertEqual(u_ref_cw, u_actual_cw)

        e_actual_cw = self.get_cw.get_extended_cws({}, window_size)
        e_ref_cw = {}
        self.assertEqual(e_ref_cw, e_actual_cw)

        b_actual_cw = self.get_cw.get_bold_cws({}, window_size)
        b_ref_cw = {}
        self.assertEqual(b_ref_cw, b_actual_cw)
    
        
    def test_get_one_cw_runs_correctly(self):
        '''
        Test that we get one context window correctly.
        '''
        positions = PositionByLine(10, 14, 0)
        window_size = 1
        ref_cw = ContextWindow([PositionByLine(10, 14, 0)],7,19, 'ooh la la мама мыла раму123  frf34')
        actual_cw = self.get_cw.get_one_cw(window_size, 'test_text.txt', positions)
        self.assertEqual(ref_cw, actual_cw)


    def test_window_size_is_bigger_than_line(self):
        '''
        Test that program runs ok if the window size is bigger than a length of th line.
        '''
        positions = PositionByLine(10, 14, 0)
        window_size = 5
        ref_cw = ContextWindow([PositionByLine(10, 14, 0)],0,34, 'ooh la la мама мыла раму123  frf34')
        actual_cw = self.get_cw.get_one_cw(window_size, 'test_text.txt', positions)
        self.assertEqual(ref_cw, actual_cw)

 
    def test_windows_are_united_correctly(self):        
        '''
        Test that two context windows are united correctly.
        '''
        window_size = 1
        positions1 = PositionByLine(10, 14, 0)
        positions2 = PositionByLine(15, 19, 0)
        window1 = self.get_cw.get_one_cw(window_size, 'test_text.txt', positions1)
        window2 = self.get_cw.get_one_cw(window_size, 'test_text.txt', positions2)
        united_cws = self.get_cw.unite_windows(window1, window2)
        ref_united_cws = [([PositionByLine(10, 14, 0), PositionByLine(15, 19, 0)], 7, 23, 'ooh la la мама мыла раму123  frf34')]
    
    def test_windows_are_extended_correctly(self): 
        '''
        Test that we context window is extended correctly.
        '''
        window_size = 1
        actual_cw = self.get_cw.get_extended_cws(self.search.multi_search('мама мыла'), window_size)
        ref_cw = {'test_text.txt' :[([PositionByLine(10, 14, 0), PositionByLine(15, 19, 0)], 0, 33, 'ooh la la мама мыла раму123  frf34')]}

    def test_windows_are_bolded_correctly(self):
        '''
        Test that words are made bold correctly.
        '''
        window_size = 1
        actual_cw = self.get_cw.get_bold_cws(self.search.multi_search('мама мыла'), window_size)
        ref_cw = {'test_text.txt' :[([PositionByLine(10, 14, 0), PositionByLine(15, 19, 0)], 7, 23, 'la <b>мама</b> <b>мыла</b> раму')]}

        

if __name__ == '__main__':
    unittest.main()
