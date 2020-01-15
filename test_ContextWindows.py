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
        text1 = open('test_text.txt', 'w')
        text1.write('ooh la la мама мыла раму123  frf34')
        text1.close()
        text2 = open('test_text2.txt', 'w')
        text2.write('мама мыла окно')
        text2.close()
        text3 = open('test_text3.txt', 'w')
        text3.write('мама мыла еще что-нибудь')
        text3.close()
        indexer.index_by_line('test_text.txt')
        indexer.index_by_line('test_text2.txt')
        indexer.index_by_line('test_text3.txt')

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
            if single_file == "database" or single_file.startswith('database.'): 
                os.remove(single_file)
        os.remove('test_text.txt')
        os.remove('test_text2.txt')
        os.remove('test_text3.txt')
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

    def test_limited_bold_windows_runs_ok(self):
        '''
        Test that the programs runs fine provided the input of the correct type.
        '''
        window_size = 1
        doclimit = 3
        docoffset = 0
        lim_of_pairs = [(0,1), (1,7), (3, 2)]
        actual_result = self.get_cw.get_bold_cws_limited(self.search.multi_search('мама мыла'), window_size, doclimit, docoffset, lim_of_pairs)
        fake_result = {'test_text.txt': [([PositionByLine(10, 14, 0), PositionByLine(15, 19, 0)], 7, 23, 'la <b>мама</b> <b>мыла</b> раму')],
        'test_text2.txt': [([PositionByLine(0, 4, 0), PositionByLine(5, 9, 0)], 0, 9, '<b>мама</b> <b>мыла</b> окно')],
        'test_text3.txt': [([PositionByLine(0, 4, 0), PositionByLine(5, 9, 0)], 0, 9, '<b>мама</b> <b>мыла</b> еще что-нибудь')]}
        
    def test_limited_bold_windows_wrong_input(self):
        '''
        Test that TypeError is raised if the input is of the wrong type.
        '''
        with self.assertRaises(TypeError):
            self.get_cw.get_bold_cws_limited(self.search.multi_search('мама мыла'), 'LOL', 3, 0, [(0,1), (1,7), (3, 2)])
        with self.assertRaises(TypeError):
            self.get_cw.get_bold_cws_limited(self.search.multi_search('мама мыла'), 1, ['k', 'e', 'k'], 0, [(0,1), (1,7), (3, 2)])
        with self.assertRaises(TypeError):
            self.get_cw.get_bold_cws_limited(self.search.multi_search('мама мыла'), 1, 3, (1,2,3), [(0,1), (1,7), (3, 2)])
        with self.assertRaises(TypeError):
            self.get_cw.get_bold_cws_limited(self.search.multi_search('мама мыла'), 1, 3, 0, 'not a list')
        with self.assertRaises(TypeError):
            self.get_cw.get_bold_cws_limited(self.search.multi_search('мама мыла'), 1, 3, 0, [[0,1], [1,7], [3, 2]])
        with self.assertRaises(TypeError):
            self.get_cw.get_bold_cws_limited(self.search.multi_search('мама мыла'), 1, 3, 0, [('a',1), (1,7), (3, 2)])


    def test_limited_extended_windows_runs_ok(self):
        '''
        Test that the programs runs fine provided the input of the correct type.
        '''
        window_size = 1
        doclimit = 3
        docoffset = 0
        lim_of_pairs = [(0,1), (1,7), (3, 2)]
        actual_result = self.get_cw.get_extended_cws_limited(self.search.multi_search('мама мыла'), window_size, doclimit, docoffset)
        fake_result = {'test_text.txt': [([PositionByLine(10, 14, 0), PositionByLine(15, 19, 0)], 0, 33, 'ooh la la мама мыла раму123  frf34')],
        'test_text2.txt': [([PositionByLine(0, 4, 0), PositionByLine(5, 9, 0)], 0, 14, 'мама мыла окно')],
        'test_text3.txt': [([PositionByLine(0, 4, 0), PositionByLine(5, 9, 0)], 0, 24, 'мама мыла еще что-нибудь')]}
        
    def test_limited_extended_windows_wrong_input(self):
        '''
        Test that TypeError is raised if the input is of the wrong type.
        '''
        with self.assertRaises(TypeError):
            self.get_cw.get_extended_cws_limited(self.search.multi_search('мама мыла'), 'LOL', 0, 3)
        with self.assertRaises(TypeError):
            self.get_cw.get_extended_cws_limited(self.search.multi_search('мама мыла'), 1, ['k', 'e', 'k'], 1)
        with self.assertRaises(TypeError):
            self.get_cw.get_extended_cws_limited(self.search.multi_search('мама мыла'), 1, 3, (1,2,3))
        with self.assertRaises(TypeError):
            self.get_cw.get_extended_cws_limited([1,1,3], 1, 3, (1,2,3))


    def test_limited_united_windows_runs_ok(self):
        '''
        Test that the programs runs fine provided the input of the correct type.
        '''
        window_size = 1
        doclimit = 3
        docoffset = 0
        lim_of_pairs = [(0,1), (1,7), (3, 2)]
        actual_result = self.get_cw.get_united_cws_limited(self.search.multi_search('мама мыла'), window_size, doclimit, docoffset)
        fake_result = {'test_text.txt': [([PositionByLine(10, 14, 0), PositionByLine(15, 19, 0)], 10, 19, 'ooh la la мама мыла раму123  frf34')],
        'test_text2.txt': [([PositionByLine(0, 4, 0), PositionByLine(5, 9, 0)], 0, 9, 'мама мыла окно')],
        'test_text3.txt': [([PositionByLine(0, 4, 0), PositionByLine(5, 9, 0)], 0, 9, 'мама мыла еще что-нибудь')]}
        
    def test_limited_united_windows_wrong_input(self):
        '''
        Test that TypeError is raised if the input is of the wrong type.
        '''
        with self.assertRaises(TypeError):
            self.get_cw.get_united_cws_limited(self.search.multi_search(self.search.multi_search('мама мыла'), 'LOL', 0, 3))
        with self.assertRaises(TypeError):
            self.get_cw.get_united_cws_limited(self.search.multi_search(self.search.multi_search('мама мыла'), 1, ['k', 'e', 'k'], 1))
        with self.assertRaises(TypeError):
            self.get_cw.get_united_cws_limited(self.search.multi_search('мама мыла'), 1, 3, (1,2,3))
        with self.assertRaises(TypeError):
            self.get_cw.get_united_cws_limited([1,1,3], 1, 3, (1,2,3))
    
    def test_limited_several_windows_runs_ok(self):
        '''
        Test that the programs runs fine provided the input of the correct type.
        '''
        window_size = 1
        doclimit = 3
        docoffset = 0
        lim_of_pairs = [(0,1), (1,7), (3, 2)]
        actual_result = self.get_cw.get_united_cws_limited(self.search.multi_search('мама мыла'), window_size, doclimit, docoffset)
        fake_result = {'test_text.txt': [([PositionByLine(10, 14, 0),7, 19], 'ooh la la мама мыла раму123  frf34'),
                                        ([PositionByLine(15, 19, 0)], 10, 27, 'ooh la la мама мыла раму123  frf34')],
                        'test_text2.txt': [([PositionByLine(0, 4, 0)], 0, 9, 'мама мыла окно'),
                                        ([PositionByLine(5, 9, 0)], 0, 14, 'мама мыла окно')],
                        'test_text3.txt': [([PositionByLine(0, 4, 0)], 0, 9, 'мама мыла еще что-нибудь'),
                                        ([PositionByLine(5, 9, 0)], 0, 13, 'мама мыла еще что-нибудь')]}
        
    def test_limited_several_windows_wrong_input(self):
        '''
        Test that TypeError is raised if the input is of the wrong type.
        '''
        with self.assertRaises(TypeError):
            self.get_cw.get_several_cws_limited(self.search.multi_search(self.search.multi_search('мама мыла'), 'LOL', 0, 3))
        with self.assertRaises(TypeError):
            self.get_cw.get_several_cws_limited(self.search.multi_search(self.search.multi_search('мама мыла'), 1, ['k', 'e', 'k'], 1))
        with self.assertRaises(TypeError):
            self.get_cw.get_several_cws_limited(self.search.multi_search('мама мыла'), 1, 3, (1,2,3))
        with self.assertRaises(TypeError):
            self.get_cw.get_several_cws_limited([1,1,3], 1, 3, (1,2,3))


if __name__ == '__main__':
    unittest.main()
