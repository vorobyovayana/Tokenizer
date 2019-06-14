import shelve
import os
import unittest
from search_engine import SearchEngine
from context_windows import ContextWindow
from context_windows import GetContextWindow
from indexation import ToIndex
from indexation import PositionByLine

class TestGetOneContextWindow(unittest.TestCase):

    def setUp(self):
        
        indexer = ToIndex('database')
        self.search = SearchEngine('database')
        self.get_cw = GetContextWindow()
        text = open('test_text.txt', 'w')
        text.write('ooh la la мама мыла раму123  frf34')
        text.close()
        indexer.index_by_line('test_text.txt')

        del indexer
        
    def tearDown(self):
        
        del self.search
        os.remove('test_text.txt')


    def test_get_one_cw_correctly(self):

        positions = PositionByLine(10, 14, 0)
        window_size = 1
        ref_cw = ContextWindow([PositionByLine(10, 14, 0)],7,19, 'ooh la la мама мыла раму123  frf34')
        actual_cw = self.get_cw.get_one_cw(window_size, 'test_text.txt', positions)
        self.assertEqual(ref_cw, actual_cw)


    def test_window_size_is_bigger_than_line(self):

        positions = PositionByLine(10, 14, 0)
        window_size = 5
        ref_cw = ContextWindow([PositionByLine(10, 14, 0)],0,34, 'ooh la la мама мыла раму123  frf34')
        actual_cw = self.get_cw.get_one_cw(window_size, 'test_text.txt', positions)
        self.assertEqual(ref_cw, actual_cw)

    def test_windows_are_united_correctly(self):

        window_size = 1
        print(self.search.multi_search('мама мыла'))
        actual_cw = self.get_cw.unite_cws(self.search.multi_search('мама мыла'), window_size)
        ref_cw = [([(0, 4, 0), (5, 9, 0)], 0, 14, 'мама мыла раму долго')]
        self.assertEqual(ref_right_cont, actual_right_cont)


        

if __name__ == '__main__':
    unittest.main()
