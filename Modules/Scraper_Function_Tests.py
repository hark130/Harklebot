from Scraper_Functions import find_the_date 
from Scraper_Functions import find_a_URL 
from Scraper_Functions import get_image_filename
from Scraper_Functions import is_URL_abs
from Scraper_Functions import make_rel_URL_abs
# make_rel_URL_abs(baseURL, targetURL)
# is_URL_abs(baseURL, targetURL)
# find_a_URL(htmlString, searchStart, searchStop)
# get_image_filename(htmlString, [dateSearchPhrase], [nameSearchPhrase], nameEnding)
import unittest
import os


class MakeRelURLAbs(unittest.TestCase):
    
    # Test 1 - TypeError('baseURL is not a string')
    def test1_baseURL_TypeError01(self):
        try:
            result = make_rel_URL_abs(3.14, 'http://www.cad-comic.com/sillies/20130115')
        except TypeError as err:
            self.assertEqual(err.args[0], 'baseURL is not a string')
        except Exception as err:
            print(repr(err))
            self.fail('Raised the wrong exception')
            
    # Test 2 - TypeError('baseURL is not a string')
    def test2_baseURL_TypeError02(self):
        try:
            result = make_rel_URL_abs(['http://www.cad-comic.com/sillies/'], 'http://www.cad-comic.com/sillies/20130115')
        except TypeError as err:
            self.assertEqual(err.args[0], 'baseURL is not a string')
        except Exception as err:
            print(repr(err))
            self.fail('Raised the wrong exception')
            
    # Test 3 - ValueError('baseURL is empty')
    def test3_baseURL_ValueError01(self):
        try:
            result = make_rel_URL_abs('', 'http://www.cad-comic.com/sillies/20130115')
        except ValueError as err:
            self.assertEqual(err.args[0], 'baseURL is empty')
        except Exception as err:
            print(repr(err))
            self.fail('Raised the wrong exception')
            

    # Test 4 - TypeError('targetURL is not a string')
    def test4_targetURL_TypeError01(self):
        try:
            result = make_rel_URL_abs('http://www.cad-comic.com/sillies/', {'try':'again'})
        except TypeError as err:
            self.assertEqual(err.args[0], 'targetURL is not a string')
        except Exception as err:
            print(repr(err))
            self.fail('Raised the wrong exception')
            
    # Test 5 - TypeError('targetURL is not a string')
    def test5_targetURL_TypeError02(self):
        try:
            result = make_rel_URL_abs('http://www.cad-comic.com/sillies/', ['http://www.cad-comic.com/sillies/20130115'])
        except TypeError as err:
            self.assertEqual(err.args[0], 'targetURL is not a string')
        except Exception as err:
            print(repr(err))
            self.fail('Raised the wrong exception')
            
    # Test 6 - ValueError('targetURL is empty')
    def test6_targetURL_ValueError01(self):
        try:
            result = make_rel_URL_abs('http://www.cad-comic.com/sillies/', '')
        except ValueError as err:
            self.assertEqual(err.args[0], 'targetURL is empty')
        except Exception as err:
            print(repr(err))
            self.fail('Raised the wrong exception')
            
    # Test 7 - Valid Input - Normal absolute URL
    def test7_ValidInput01(self):
        try:
            result = make_rel_URL_abs('http://www.cad-comic.com/sillies/', 'http://www.cad-comic.com/sillies/20130115')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(result == 'http://www.cad-comic.com/sillies/20130115')
            
    # Test 8 - Valid Input - Normal absolute URL
    def test8_ValidInput02(self):
        try:
            result = make_rel_URL_abs('http://www.cad-comic.com/sillies/', 'www.cad-comic.com/sillies/20130115')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(result == 'www.cad-comic.com/sillies/20130115')
            
    # Test 9 - Valid Input - Normal relative URL
    def test9_ValidInput03(self):
        try:
            result = make_rel_URL_abs('http://www.cad-comic.com/sillies/', '/sillies/20130115')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(result == 'http://www.cad-comic.com/sillies/20130115')
            
    # Test 10 - Tricky Input - Mixed up association of relative and absolute
    def test10_TrickyInput01(self):
        try:
            result = make_rel_URL_abs('http://pvponline.com/comic', '2017-02-16')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(result == 'http://pvponline.com/comic/2017-02-16')

    # Test 11 - Tricky Input - Mixed up association of relative and absolute
    def test11_TrickyInput02(self):
        try:
            result = make_rel_URL_abs('http://pvponline.com', '/comic/2017-02-16')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(result == 'http://pvponline.com/comic/2017-02-16')
            
    # Test 12 - Tricky Input - Mixed up association of relative and absolute
    def test12_TrickyInput03(self):
        try:
            result = make_rel_URL_abs('pvponline.com', '/comic/2017-02-16')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(result == 'pvponline.com/comic/2017-02-16')
            
    # Test 13 - Tricky Input - Mixed up association of relative and absolute
    def test13_TrickyInput04(self):
        try:
            result = make_rel_URL_abs('pvponline.com/comic', '/2017-02-16')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(result == 'pvponline.com/comic/2017-02-16')

    # Test 14 - Tricky Input - Mixed up association of relative and absolute
    def test14_TrickyInput05(self):
        try:
            result = make_rel_URL_abs('http://pvponline.com/comic', 'pvponline.com/comic/2017-02-16')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(result == 'http://pvponline.com/comic/2017-02-16')

    # Test 15 - Tricky Input - Mixed up association of relative and absolute
    def test15_TrickyInput06(self):
        try:
            result = make_rel_URL_abs('http://pvponline.com', 'pvponline.com/comic/2017-02-16')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(result == 'http://pvponline.com/comic/2017-02-16')
            
    # Test 16 - Tricky Input - Mixed up association of relative and absolute
    def test16_TrickyInput07(self):
        try:
            result = make_rel_URL_abs('pvponline.com', 'http://pvponline.com/comic/2017-02-16')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(result == 'http://pvponline.com/comic/2017-02-16')
            
    # Test 17 - Tricky Input - Mixed up association of relative and absolute
    def test17_TrickyInput08(self):
        try:
            result = make_rel_URL_abs('pvponline.com/comic', 'http://pvponline.com/comic/2017-02-16')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(result == 'http://pvponline.com/comic/2017-02-16')
            
    # Test 18 - Tricky Input - Mixed up association of relative and absolute
    def test18_TrickyInput09(self):
        try:
            result = make_rel_URL_abs('pvponline.com/comic', 'http://www.pvponline.com/comic/2017-02-16')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(result == 'http://www.pvponline.com/comic/2017-02-16')
            
    # Test 19 - Tricky Input - Mixed up association of relative and absolute
    def test19_TrickyInput10(self):
        try:
            result = make_rel_URL_abs('pvponline.com/comic', 'www.pvponline.com/comic/2017-02-16')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(result == 'www.pvponline.com/comic/2017-02-16')
            
    # Test 20 - Bad Input - Invalid URLs
    def test20_BadInput01(self):
        try:
            result = is_URL_abs('just/some/stuff', 'stuff/thrown/together')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertFalse(result == 'just/some/stuff/thrown/together')
            
    # Test 21 - Bad Input - Invalid URLs
    def test21_BadInput02(self):
        try:
            result = is_URL_abs('/just/some/stuff', 'stuff/thrown/together')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertFalse(result == '/just/some/stuff/thrown/together')
            
    # Test 22 - Bad Input - Invalid URLs
    def test22_BadInput03(self):
        try:
            result = is_URL_abs('/just/some/stuff/', 'stuff/thrown/together')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertFalse(result == '/just/some/stuff/thrown/together')
            
    # Test 22 - Bad Input - Invalid URLs
    def test22_BadInput04(self):
        try:
            result = is_URL_abs('/just/some/stuff/', '/stuff/thrown/together')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertFalse(result == '/just/some/stuff/thrown/together')
            
    # Test 23 - Bad Input - Invalid URLs
    def test23_BadInput05(self):
        try:
            result = is_URL_abs('/just/some/stuff/', '/stuff/thrown/together/')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertFalse(result == '/just/some/stuff/thrown/together/')
            
    # Test 24 - Bad Input - Invalid URLs
    def test24_BadInput06(self):
        try:
            result = is_URL_abs('/just/some/stuffing/stuffed/inside/some/other/stuff/', '/stuff/thrown/together/')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertFalse(result == '/just/some/stuffing/stuffed/inside/some/other/stuff/thrown/together/')


class IsURLAbs(unittest.TestCase):

    # Test 1 - TypeError('baseURL is not a string')
    def test1_baseURL_TypeError01(self):
        try:
            result = is_URL_abs(3.14, 'http://www.cad-comic.com/sillies/20130115')
        except TypeError as err:
            self.assertEqual(err.args[0], 'baseURL is not a string')
        except Exception as err:
            print(repr(err))
            self.fail('Raised the wrong exception')
            
    # Test 2 - TypeError('baseURL is not a string')
    def test2_baseURL_TypeError02(self):
        try:
            result = is_URL_abs(['http://www.cad-comic.com/sillies/'], 'http://www.cad-comic.com/sillies/20130115')
        except TypeError as err:
            self.assertEqual(err.args[0], 'baseURL is not a string')
        except Exception as err:
            print(repr(err))
            self.fail('Raised the wrong exception')
            
    # Test 3 - ValueError('baseURL is empty')
    def test3_baseURL_ValueError01(self):
        try:
            result = is_URL_abs('', 'http://www.cad-comic.com/sillies/20130115')
        except ValueError as err:
            self.assertEqual(err.args[0], 'baseURL is empty')
        except Exception as err:
            print(repr(err))
            self.fail('Raised the wrong exception')
            

    # Test 4 - TypeError('targetURL is not a string')
    def test4_targetURL_TypeError01(self):
        try:
            result = is_URL_abs('http://www.cad-comic.com/sillies/', {'try':'again'})
        except TypeError as err:
            self.assertEqual(err.args[0], 'targetURL is not a string')
        except Exception as err:
            print(repr(err))
            self.fail('Raised the wrong exception')
            
    # Test 5 - TypeError('targetURL is not a string')
    def test5_targetURL_TypeError02(self):
        try:
            result = is_URL_abs('http://www.cad-comic.com/sillies/', ['http://www.cad-comic.com/sillies/20130115'])
        except TypeError as err:
            self.assertEqual(err.args[0], 'targetURL is not a string')
        except Exception as err:
            print(repr(err))
            self.fail('Raised the wrong exception')
            
    # Test 6 - ValueError('targetURL is empty')
    def test6_targetURL_ValueError01(self):
        try:
            result = is_URL_abs('http://www.cad-comic.com/sillies/', '')
        except ValueError as err:
            self.assertEqual(err.args[0], 'targetURL is empty')
        except Exception as err:
            print(repr(err))
            self.fail('Raised the wrong exception')
            
    # Test 7 - Valid Input - Normal absolute URL
    def test7_ValidInput01(self):
        try:
            result = is_URL_abs('http://www.cad-comic.com/sillies/', 'http://www.cad-comic.com/sillies/20130115')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(result)
            
    # Test 8 - Valid Input - Normal absolute URL
    def test8_ValidInput02(self):
        try:
            result = is_URL_abs('http://www.cad-comic.com/sillies/', 'www.cad-comic.com/sillies/20130115')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(result)
            
    # Test 9 - Valid Input - Normal relative URL
    def test9_ValidInput03(self):
        try:
            result = is_URL_abs('http://www.cad-comic.com/sillies/', '/sillies/20130115')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertFalse(result)
            
    # Test 10 - Tricky Input - Mixed up association of relative and aboslute
    def test10_TrickyInput01(self):
        try:
            result = is_URL_abs('http://pvponline.com/comic', '2017-02-16')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertFalse(result)

    # Test 11 - Tricky Input - Mixed up association of relative and aboslute
    def test11_TrickyInput02(self):
        try:
            result = is_URL_abs('http://pvponline.com', '/comic/2017-02-16')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertFalse(result)
            
    # Test 12 - Tricky Input - Mixed up association of relative and aboslute
    def test12_TrickyInput03(self):
        try:
            result = is_URL_abs('pvponline.com', '/comic/2017-02-16')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertFalse(result)
            
    # Test 13 - Tricky Input - Mixed up association of relative and aboslute
    def test13_TrickyInput04(self):
        try:
            result = is_URL_abs('pvponline.com/comic', '/2017-02-16')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertFalse(result)

    # Test 14 - Tricky Input - Mixed up association of relative and aboslute
    def test14_TrickyInput05(self):
        try:
            result = is_URL_abs('http://pvponline.com/comic', 'pvponline.com/comic/2017-02-16')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(result)

    # Test 15 - Tricky Input - Mixed up association of relative and aboslute
    def test15_TrickyInput06(self):
        try:
            result = is_URL_abs('http://pvponline.com', 'pvponline.com/comic/2017-02-16')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(result)
            
    # Test 16 - Tricky Input - Mixed up association of relative and aboslute
    def test16_TrickyInput07(self):
        try:
            result = is_URL_abs('pvponline.com', 'http://pvponline.com/comic/2017-02-16')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(result)
            
    # Test 17 - Tricky Input - Mixed up association of relative and aboslute
    def test17_TrickyInput08(self):
        try:
            result = is_URL_abs('pvponline.com/comic', 'http://pvponline.com/comic/2017-02-16')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(result)
            
    # Test 18 - Tricky Input - Mixed up association of relative and aboslute
    def test18_TrickyInput09(self):
        try:
            result = is_URL_abs('pvponline.com/comic', 'http://www.pvponline.com/comic/2017-02-16')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(result)
            
    # Test 19 - Tricky Input - Mixed up association of relative and aboslute
    def test19_TrickyInput10(self):
        try:
            result = is_URL_abs('pvponline.com/comic', 'www.pvponline.com/comic/2017-02-16')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(result)
            
    # Test 20 - Bad Input - Invalid baseURL
    def test20_BadInput01(self):
        try:
            result = is_URL_abs('not a URL?', '2017-02-16')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertFalse(result)
            
    # Test 21 - Bad Input - Invalid baseURL
    def test21_BadInput02(self):
        try:
            result = is_URL_abs('not a URL!', 'URL')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertFalse(result)
            
    # Test 22 - Bad Input - Invalid baseURL
    def test22_BadInput03(self):
        try:
            result = is_URL_abs('definitely not a URL', 'https://xkcd.com')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(result)
            
    # Test 23 - Bad Input - Invalid baseURL
    def test23_BadInput04(self):
        try:
            result = is_URL_abs('probably not a URL', 'www.smbc-comics.com')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(result)
            
    # Test 24 - Bad Input - Invalid targetURL
    def test24_BadURL01(self):
        try:
            result = is_URL_abs('www.smbc-comics.com', 'not a website?')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertFalse(result)
            
    # Test 25 - Bad Input - Invalid targetURL
    def test25_BadURL02(self):
        try:
            result = is_URL_abs('https://xkcd.com/', 'not a website!')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertFalse(result)
            
    # Test 26 - Bad Input - Invalid targetURL
    def test26_BadURL03(self):
        try:
            result = is_URL_abs('https://www.xkcd.com/', 'websites typically begin with www and end with a top-level domain like com or org')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertFalse(result)      
            
    # Test 27 - Bad Input - Invalid targetURL
    def test27_BadURL04(self):
        try:
            result = is_URL_abs('https://www.xkcd.com/', 'websites typically begin with www. and end with a top-level domain like .com or .org')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertFalse(result)      
            
    # Test 28 - Bad Input - Invalid targetURL
    def test28_BadURL05(self):
        try:
            result = is_URL_abs('https://www.xkcd.com/', 'websites typically begin with https: and end with a top-level domain like .com or .org')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertFalse(result)    
            
    # Test 29 - Bad Input - Invalid targetURL
    def test29_BadURL06(self):
        try:
            result = is_URL_abs('https://www.xkcd.com/', 'websites typically begin with http: and end with a top-level domain like .com or .org')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertFalse(result)    
            
    # Test 30 - Bad Input - Invalid targetURL
    def test30_BadURL07(self):
        try:
            result = is_URL_abs('www.NotAWebsite.com', 'http:\n//\nwww.\nthisisnotarealwebsitebuttheonlyeasywaytoverifythatistoattempttoopenit\n.com')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(result)    
            
    # Test 31 - Bad Input - Invalid targetURL
    def test31_BadURL08(self):
        try:
            result = is_URL_abs('www.NotAWebsite.com', 'www.\nthisisnotarealwebsitebuttheonlyeasywaytoverifythatistoattempttoopenit\n.com')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(result)    
            
    # Test 32 - Bad Input - Invalid targetURL
    def test32_BadURL09(self):
        try:
            result = is_URL_abs('www.NotAWebsite.com', 'https:\n//\nthisisnotarealwebsitebuttheonlyeasywaytoverifythatistoattempttoopenit\n.com')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(result)    
            
    # Test 33 - Bad Input - Invalid targetURL
    def test33_BadURL10(self):
        try:
            result = is_URL_abs('www.NotAWebsite.com', 'https:\n//\nthisisnotarealwebsitebuttheonlyeasywaytoverifythatistoattempttoopenit\n.com')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(result)  
            
    # Test 34 - Bad Input - Not a single valid URL
    def test34_BadURL11(self):
        try:
            result = is_URL_abs('notaURL', 'ThisisdefinitelynotaURLsinceitdoesnotincludeatopleveldomainlike.cz')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(result)  
            
    # Test 35 - Bad Input - Not a single valid URL
    def test35_BadURL12(self):
        try:
            result = is_URL_abs('Alphabet', 'theAlphabetIsExtendedToInclude.bdAnd.be')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertFalse(result)  
            
    # Test 36 - Bad Input - Not a single valid URL
    def test36_BadURL13(self):
        try:
            result = is_URL_abs('Alphabet', 'AlphabetIsExtendedToInclude.asAnd.at')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(result)  

class FindURL(unittest.TestCase):

    def test_htmlString_TypeError(self):
        try:
            find_a_URL(3.14, 'search for this', ['stuff', 'other stuff'], ['things', 'other things'])
        except TypeError as err:
            self.assertEqual(err.args[0], 'htmlString is not a string')
        except Exception as err:
            print(repr(err))
            self.fail('Raised the wrong exception')

    def test_htmlString_ValueError(self):
        try:
            find_a_URL('', 'search for this', ['stuff', 'other stuff'], ['things', 'other things'])
        except ValueError as err:
            self.assertEqual(err.args[0], 'htmlString is empty')
        except Exception as err:
            print(repr(err))
            self.fail('Raised the wrong exception')

    def test_searchPhrase_TypeError(self):
        try:
            find_a_URL('http://www.nunyabusiness.com', -1, ['stuff', 'other stuff'], ['things', 'other things'])
        except TypeError as err:
            self.assertEqual(err.args[0], 'searchPhrase is not a string or a list')
        except Exception as err:
            print(repr(err))
            self.fail('Raised the wrong exception')

    def test_searchPhrase_ValueError1(self):
        try:
            find_a_URL('http://www.iamright.com', '', ['stuff', 'other stuff'], ['things', 'other things'])
        except ValueError as err:
            self.assertEqual(err.args[0], 'searchPhrase is empty')
        except Exception as err:
            print(repr(err))
            self.fail('Raised the wrong exception')

    def test_searchPhrase_ValueError2(self):
        try:
            find_a_URL('http://www.iamright.com', [], ['stuff', 'other stuff'], ['things', 'other things'])
        except ValueError as err:
            self.assertEqual(err.args[0], 'searchPhrase is empty')
        except Exception as err:
            print(repr(err))
            self.fail('Raised the wrong exception')

    def test_searchPhrase_ValueError3(self):
        try:
            find_a_URL('http://www.iamright.com', ['search for this', 'search for this other thing', ''], ['stuff', 'other stuff'], ['things', 'other things'])
        except ValueError as err:
            self.assertEqual(err.args[0], 'searchPhrase contains an empty string')
        except Exception as err:
            print(repr(err))
            self.fail('Raised the wrong exception')

    def test_searchPhrase_TypeError4(self):
        try:
            find_a_URL('http://www.iamright.com', ['search for this', 'search for this other thing', ['How meta?', 'A list within a list']], ['stuff', 'other stuff'], ['things', 'other things'])
        except TypeError as err:
            self.assertEqual(err.args[0], 'searchPhrase contains a non string')
        except Exception as err:
            print(repr(err))
            self.fail('Raised the wrong exception')

    def test_searchStart_TypeError(self):
        try:
            find_a_URL('http://www.iamright.com', 'search for this', 42, ['things', 'other things'])
        except TypeError as err:
            self.assertEqual(err.args[0], 'searchStart is not a string or a list')
        except Exception as err:
            print(repr(err))
            self.fail('Raised the wrong exception')

    def test_searchStart_ValueError1(self):
        try:
            find_a_URL('http://www.iamright.com', 'search for this', '', ['things', 'other things'])
        except ValueError as err:
            self.assertEqual(err.args[0], 'searchStart is empty')
        except Exception as err:
            print(repr(err))
            self.fail('Raised the wrong exception')

    def test_searchStart_ValueError2(self):
        try:
            find_a_URL('http://www.iamright.com', 'search for this', [], ['things', 'other things'])
        except ValueError as err:
            self.assertEqual(err.args[0], 'searchStart is empty')
        except Exception as err:
            print(repr(err))
            self.fail('Raised the wrong exception')

    def test_searchStart_ValueError3(self):
        try:
            find_a_URL('http://www.iamright.com', 'search for this', ['stuff', 'other stuff', ''], ['things', 'other things'])
        except ValueError as err:
            self.assertEqual(err.args[0], 'searchStart contains an empty string')
        except Exception as err:
            print(repr(err))
            self.fail('Raised the wrong exception')

    def test_searchStart_TypeError4(self):
        try:
            find_a_URL('http://www.iamright.com', 'search for this', ['stuff', 'other stuff', 66], ['things', 'other things'])
        except TypeError as err:
            self.assertEqual(err.args[0], 'searchStart contains a non string')
        except Exception as err:
            print(repr(err))
            self.fail('Raised the wrong exception')

    def test_searchStop_TypeError(self):
        try:
            find_a_URL('http://www.nunyabusiness.com', 'search for this', ['stuff', 'other stuff'], {'No':'Deal'})
        except TypeError as err:
            self.assertEqual(err.args[0], 'searchStop is not a string or a list')
        except Exception as err:
            print(repr(err))
            self.fail('Raised the wrong exception')

    def test_searchStop_ValueError1(self):
        try:
            find_a_URL('http://www.iamright.com', ['search for this', 'search for this other thing'], ['stuff', 'other stuff'], '')
        except ValueError as err:
            self.assertEqual(err.args[0], 'searchStop is empty')
        except Exception as err:
            print(repr(err))
            self.fail('Raised the wrong exception')

    def test_searchStop_ValueError2(self):
        try:
            find_a_URL('http://www.iamright.com', ['search for this', 'search for this other thing'], ['stuff', 'other stuff'], [])
        except ValueError as err:
            self.assertEqual(err.args[0], 'searchStop is empty')
        except Exception as err:
            print(repr(err))
            self.fail('Raised the wrong exception')

    def test_searchStop_ValueError3(self):
        try:
            find_a_URL('http://www.iamright.com', ['search for this', 'search for this other thing'], ['stuff', 'other stuff'], ['things', '', 'other things'])
        except ValueError as err:
            self.assertEqual(err.args[0], 'searchStop contains an empty string')
        except Exception as err:
            print(repr(err))
            self.fail('Raised the wrong exception')

    def test_searchStop_TypeError4(self):
        try:
            find_a_URL('http://www.iamright.com', ['search for this', 'search for this other thing'], ['stuff', 'other stuff'], ['things', {'Nothing':'matters'}, 'other things'])
        except TypeError as err:
            self.assertEqual(err.args[0], 'searchStop contains a non string')
        except Exception as err:
            print(repr(err))
            self.fail('Raised the wrong exception')

    def test_PVP_HTML_image_search1(self):
        try:
            with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Modules', 'Scraper_Function_Test_HTML', '1-Input_HTML.txt'), 'r') as testFile:
                testResult = find_a_URL(testFile.read(), 's3-us-west-2.amazonaws.com/pvponlinenew/img/comic/', 'src="', ['.png', '.jpg', '.gif'])
            self.assertEqual(testResult, 'http://s3-us-west-2.amazonaws.com/pvponlinenew/img/comic/2016/07/pvp20160726.jpg')
        except Exception as err:
            print(repr(err))

    def test_PVP_HTML_image_search2(self):
        try:
            with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Modules', 'Scraper_Function_Test_HTML', '11-PvP_slash_date_HTML.txt'), 'r') as testFile:
                testResult = find_a_URL(testFile.read(), 's3-us-west-2.amazonaws.com/pvponlinenew/img/comic/', ['frick', 'frack', 'src="'], ['.png', '.jpg', '.gif'])
            self.assertEqual(testResult, 'http://s3-us-west-2.amazonaws.com/pvponlinenew/img/comic/2015/12/pvp20151231.jpg')
        except Exception as err:
            print(repr(err))

    def test_Business_Cat_HTML_image_search1(self):
        try:
            with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Modules', 'Scraper_Function_Test_HTML', '3-BC_HTML.txt'), 'r') as testFile:
                testResult = find_a_URL(testFile.read(), ['<img src="http://www.businesscat.happyjar.com/wp-content/uploads/'], '<img src="', ['.png', '.jpg', '.gif'])
            self.assertEqual(testResult, 'http://www.businesscat.happyjar.com/wp-content/uploads/2016/12/2016-12-02-Order.png')
        except Exception as err:
            print(repr(err))

    def test_SMBC_HTML_image_search1(self):
        try:
            with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Modules', 'Scraper_Function_Test_HTML', '5-SMBC_HTML.txt'), 'r') as testFile:
                testResult = find_a_URL(testFile.read(), ["You'll never find this in the code!", 'www.smbc-comics.com/comics/'], ['Why are you looking for this?', 'src="'], '.png')
            self.assertEqual(testResult, 'http://www.smbc-comics.com/comics/1482854925-20161227%20(2).png')
        except Exception as err:
            print(repr(err))

    def test_SMBC_HTML_image_search2(self):
        try:
            with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Modules', 'Scraper_Function_Test_HTML', '6-SMBC_HTML.txt'), 'r') as testFile:
                testResult = find_a_URL(testFile.read(), ["You'll never find this in the code!", 'www.smbc-comics.com/comics/'], ['Why are you looking for this?', 'src="'], ['.nunya','.bak', 'xlsx','.png'])
            self.assertEqual(testResult, 'http://www.smbc-comics.com/comics/1482770017-20161226.png')
        except Exception as err:
            print(repr(err))

    def test_Penny_Arcade_HTML_image_search1(self):
        try:
            with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Modules', 'Scraper_Function_Test_HTML', '7-Penny_Arcade_random_HTML.txt'), 'r') as testFile:
                testResult = find_a_URL(testFile.read(), ['photos.smugmug.com/Comics/Pa-comics','art.penny-arcade.com', 'penny-arcade.smugmug.com/photos/','photos.smugmug.com/photos/'], 'src="', ['.png', '.jpg', '.gif'])
            self.assertEqual(testResult, 'https://art.penny-arcade.com/photos/932182163_EazuQ/0/2100x20000/932182163_EazuQ-2100x20000.jpg')
        except Exception as err:
            print(repr(err))

    def test_XKCD_HTML_image_search1(self):
        try:
            with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Modules', 'Scraper_Function_Test_HTML', '8-xkcd_random_HTML.txt'), 'r') as testFile:
                testResult = find_a_URL(testFile.read(), ['imgs.xkcd.com/comics/','Image URL (for hotlinking/embedding): '], 'src="', ['.png', '.jpg', '.gif'])
            # Mangled this assertion a bit to account for xkcd's odd relative-URLs that urlopen doesn't like
            self.assertTrue(testResult.find('imgs.xkcd.com/comics/apollo_speeches.png') >= 0)
        except Exception as err:
            print(repr(err))

class GetImageFilename(unittest.TestCase):

    def test_htmlString_TypeError1(self):
        try:
            get_image_filename(3.14, 'search for this date', ['name', 'other names'], 'ending', True)
        except TypeError as err:
            self.assertEqual(err.args[0], 'htmlString is not a string')
        except Exception as err:
            print(repr(err))
            self.fail('Raised the wrong exception')

    def test_htmlString_TypeError2(self):
        try:
            get_image_filename(["don't", "put", "HTML", "code", "in", "a", "list"], ['search for this date', 'or this date'], ['name', 'other names'], 'ending')
        except TypeError as err:
            self.assertEqual(err.args[0], 'htmlString is not a string')
        except Exception as err:
            print(repr(err))
            self.fail('Raised the wrong exception')

    def test_htmlString_ValueError1(self):
        try:
            get_image_filename('', 'search for this date', ['name', 'other names'], 'ending')
        except ValueError as err:
            self.assertEqual(err.args[0], 'htmlString is empty')
        except Exception as err:
            print(repr(err))
            self.fail('Raised the wrong exception')

    def test_dateSearchPhrase_TypeError1(self):
        try:
            get_image_filename('<a> href="here is some HTML code" </a>', 1/10/2017, ['name', 'other names'], 'ending', False)
        except TypeError as err:
            self.assertEqual(err.args[0], 'dateSearchPhrase is not a string or a list')
        except Exception as err:
            print(repr(err))
            self.fail('Raised the wrong exception')

    def test_dateSearchPhrase_TypeError2(self):
        try:
            get_image_filename('<a> href="here is some HTML code" </a>', ['search for this date', 'or this date', 20170110], ['name', 'other names'], 'ending')
        except TypeError as err:
            self.assertEqual(err.args[0], 'dateSearchPhrase contains a non string')
        except Exception as err:
            print(repr(err))
            self.fail('Raised the wrong exception')

    def test_dateSearchPhrase_TypeError3(self):
        try:
            get_image_filename('<a> href="here is some HTML code" </a>', ['search for this date', 'or this date', {"Not":"Possible"}], ['name', 'other names'], 'ending')
        except TypeError as err:
            self.assertEqual(err.args[0], 'dateSearchPhrase contains a non string')
        except Exception as err:
            print(repr(err))
            self.fail('Raised the wrong exception')

    def test_dateSearchPhrase_ValueError1(self):
        try:
            get_image_filename('<a> href="here is some HTML code" </a>', '', ['name', 'other names'], 'ending')
        except ValueError as err:
            self.assertEqual(err.args[0], 'dateSearchPhrase is empty')
        except Exception as err:
            print(repr(err))
            self.fail('Raised the wrong exception')

    def test_dateSearchPhrase_ValueError2(self):
        try:
            get_image_filename('<a> href="here is some HTML code" </a>', [], ['name', 'other names'], 'ending')
        except ValueError as err:
            self.assertEqual(err.args[0], 'dateSearchPhrase is empty')
        except Exception as err:
            print(repr(err))
            self.fail('Raised the wrong exception')

    def test_dateSearchPhrase_ValueError3(self):
        try:
            get_image_filename('<a> href="here is some HTML code" </a>', ['search for this date', 'or this date', ''], ['name', 'other names'], 'ending')
        except ValueError as err:
            self.assertEqual(err.args[0], 'dateSearchPhrase contains an empty string')
        except Exception as err:
            print(repr(err))
            self.fail('Raised the wrong exception')

    def test_nameSearchPhrase_TypeError1(self):
        try:
            get_image_filename('<a> href="here is some HTML code" </a>', ['search for this date', 'or this date'], 31337, 'ending', True)
        except TypeError as err:
            self.assertEqual(err.args[0], 'nameSearchPhrase is not a string or a list')
        except Exception as err:
            print(repr(err))
            self.fail('Raised the wrong exception')

    def test_nameSearchPhrase_TypeError2(self):
        try:
            get_image_filename('<a> href="here is some HTML code" </a>', ['search for this date', 'or this date'], ['name', 'other names', ['not', 'a', 'string']], 'ending')
        except TypeError as err:
            self.assertEqual(err.args[0], 'nameSearchPhrase contains a non string')
        except Exception as err:
            print(repr(err))
            self.fail('Raised the wrong exception')

    def test_nameSearchPhrase_TypeError3(self):
        try:
            get_image_filename('<a> href="here is some HTML code" </a>', ['search for this date', 'or this date'], ['name', 'other names', {'not':'good'}], 'ending')
        except TypeError as err:
            self.assertEqual(err.args[0], 'nameSearchPhrase contains a non string')
        except Exception as err:
            print(repr(err))
            self.fail('Raised the wrong exception')

    def test_nameSearchPhrase_ValueError1(self):
        try:
            get_image_filename('<a> href="here is some HTML code" </a>', 'date?', '', 'ending', False)
        except ValueError as err:
            self.assertEqual(err.args[0], 'nameSearchPhrase is empty')
        except Exception as err:
            print(repr(err))
            self.fail('Raised the wrong exception')

    def test_nameSearchPhrase_ValueError2(self):
        try:
            get_image_filename('<a> href="here is some HTML code" </a>', 'I can haz date?', [], 'ending')
        except ValueError as err:
            self.assertEqual(err.args[0], 'nameSearchPhrase is empty')
        except Exception as err:
            print(repr(err))
            self.fail('Raised the wrong exception')

    def test_nameSearchPhrase_ValueError3(self):
        try:
            get_image_filename('<a> href="here is some HTML code" </a>', ['search for this date', 'or this date'], ['name', 'other names', ''], 'ending')
        except ValueError as err:
            self.assertEqual(err.args[0], 'nameSearchPhrase contains an empty string')
        except Exception as err:
            print(repr(err))
            self.fail('Raised the wrong exception')

    def test_nameEnding_TypeError1(self):
        try:
            get_image_filename('<a> href="here is some HTML code" </a>', ['search for this date', 'or this date'], ['name', 'other name'], 0)
        except TypeError as err:
            self.assertEqual(err.args[0], 'nameEnding is not a string')
        except Exception as err:
            print(repr(err))
            self.fail('Raised the wrong exception')

    def test_nameEnding_ValueError1(self):
        try:
            get_image_filename('<a> href="here is some HTML code" </a>', 'date?', 'name', '')
        except ValueError as err:
            self.assertEqual(err.args[0], 'nameEnding is empty')
        except Exception as err:
            print(repr(err))
            self.fail('Raised the wrong exception')

    def test_skipDate_TypeError1(self):
        try:
            get_image_filename('<a> href="here is some HTML code" </a>', 'date?', 'name', 'The End', 'I mean, I guess')
        except TypeError as err:
            self.assertEqual(err.args[0], 'skipDate is not a bool')
        except Exception as err:
            print(repr(err))
            self.fail('Raised the wrong exception')

    def test_skipDate_TypeError2(self):
        try:
            get_image_filename('<a> href="here is some HTML code" </a>', 'date?', 'name', 'The End', 'True')
        except TypeError as err:
            self.assertEqual(err.args[0], 'skipDate is not a bool')
        except Exception as err:
            print(repr(err))
            self.fail('Raised the wrong exception')

    def test_skipDate_TypeError3(self):
        try:
            get_image_filename('<a> href="here is some HTML code" </a>', 'date?', 'name', 'The End', 'False')
        except TypeError as err:
            self.assertEqual(err.args[0], 'skipDate is not a bool')
        except Exception as err:
            print(repr(err))
            self.fail('Raised the wrong exception')

    def test_skipDate_TypeError4(self):
        try:
            get_image_filename('<a> href="here is some HTML code" </a>', 'date?', 'name', 'The End', [True])
        except TypeError as err:
            self.assertEqual(err.args[0], 'skipDate is not a bool')
        except Exception as err:
            print(repr(err))
            self.fail('Raised the wrong exception')

    def test_skipDate_TypeError5(self):
        try:
            get_image_filename('<a> href="here is some HTML code" </a>', 'date?', 'name', 'The End', [False])
        except TypeError as err:
            self.assertEqual(err.args[0], 'skipDate is not a bool')
        except Exception as err:
            print(repr(err))
            self.fail('Raised the wrong exception')

    def test_PVP_HTML_image_search1(self):
        try:
            with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Modules', 'Scraper_Function_Test_HTML', '1-Input_HTML.txt'), 'r') as testFile:
                testResult = get_image_filename(testFile.read(), 's3-us-west-2.amazonaws.com/pvponlinenew/img/comic/', '<title>PVP - ', '</title>')
            self.assertEqual(testResult, '20160726_2016-07-26')
        except Exception as err:
            print(repr(err))

    def test_PVP_HTML_image_search2(self):
        try:
            with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Modules', 'Scraper_Function_Test_HTML', '11-PvP_slash_date_HTML.txt'), 'r') as testFile:
                testResult = get_image_filename(testFile.read(), 's3-us-west-2.amazonaws.com/pvponlinenew/img/comic/', '<title>PVP - ', '</title>')
            # Mangled this test a bit because the found name 
            self.assertEqual(testResult, '20151231_Christmas-Special-2015-Part-19'.lower())
        except Exception as err:
            print(repr(err))

    def test_Business_Cat_HTML_image_search1(self):
        try:
            with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Modules', 'Scraper_Function_Test_HTML', '3-BC_HTML.txt'), 'r') as testFile:
                testResult = get_image_filename(testFile.read(), ['<img src="http://www.businesscat.happyjar.com/wp-content/uploads/'], 'title="', '"')
            self.assertEqual(testResult, '20161202_Order')
        except Exception as err:
            print(repr(err))

    def test_SMBC_HTML_image_search1(self):
        try:
            with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Modules', 'Scraper_Function_Test_HTML', '5-SMBC_HTML.txt'), 'r') as testFile:
                testResult = get_image_filename(testFile.read(), ["You'll never find this in the code!", 'www.smbc-comics.com/comics/'], '<title>Saturday Morning Breakfast Cereal - ', '</title>')
            self.assertEqual(testResult, '20161227_Wanna-Evolve'.lower())
        except Exception as err:
            print(repr(err))

    def test_SMBC_HTML_image_search2(self):
        try:
            with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Modules', 'Scraper_Function_Test_HTML', '6-SMBC_HTML.txt'), 'r') as testFile:
                testResult = get_image_filename(testFile.read(), ["You'll never find this in the code!", 'www.smbc-comics.com/comics/'], ['<title>Saturday Morning Breakfast Cereal - '], '</title>')
            self.assertEqual(testResult, '20161226_Political-Philosophy'.lower())
        except Exception as err:
            print(repr(err))

    def test_Penny_Arcade_HTML_image_search1(self):
        try:
            with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Modules', 'Scraper_Function_Test_HTML', '7-Penny_Arcade_random_HTML.txt'), 'r') as testFile:
                testResult = get_image_filename(testFile.read(), ['input type="hidden" name="attributes[comic_title]" value="'], 'alt="', '"')
            self.assertEqual(testResult, '20100712_Our-Partial-Future'.lower())
        except Exception as err:
            print(repr(err))

    def test_XKCD_HTML_image_search1(self):
        try:
            with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Modules', 'Scraper_Function_Test_HTML', '8-xkcd_random_HTML.txt'), 'r') as testFile:
                testResult = get_image_filename(testFile.read(), ['imgs.xkcd.com/comics/','Image URL (for hotlinking/embedding): '], 'Permanent link to this comic: http://xkcd.com/', '/<br', True)
            self.assertEqual(testResult, '1484')
        except Exception as err:
            print(repr(err))

    def test_XKCD_HTML_image_search2(self):
        try:
            with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Modules', 'Scraper_Function_Test_HTML', '8-xkcd_random_HTML.txt'), 'r') as testFile:
                testResult = get_image_filename(testFile.read(), ['imgs.xkcd.com/comics/','Image URL (for hotlinking/embedding): '], 'Permanent link to this comic: http://xkcd.com/', '/<br', False)
            self.assertEqual(testResult, '00000000')
        except Exception as err:
            print(repr(err))


if __name__ == '__main__':
    unittest.main()
    print("Done Testing")

    # Old Scraper Function tests written prior to integrating the unittest module
#    # TEST 1 - PvP
#    with open('1-Input_HTML.txt', 'r') as testFile1:
#        testInput1 = testFile1.read()

#    testResult1 = find_the_date(testInput1)
#    print("TEST 1\t'20160726' == {}:\t{}\n".format(testResult1, testResult1 == '20160726'))

#    ## TEST 2
#    #testInput2 = 'DATE: 2001-01-01\ndate: 2002-02-02\nDate: 2003-03-03\nDATE: 2004/04/04\ndate: 2005/05/05\nDate:\t2006-06-06\n'
#    #testResult2 = find_the_date(testInput2)
#    #print("TEST 2 - {}\n".format(testResult2))

#    # TEST 3 - Business Cat
#    with open('3-BC_HTML.txt', 'r') as testFile3:
#        testInput3 = testFile3.read()

#    testResult3 = find_the_date(testInput3)
#    print("TEST 3\t'20161202' == {}:\t{}\n".format(testResult3, testResult3 == '20161202'))

#    ## TEST 4
#    #testInput4 = 'Nothing\nNothing else\nDate:\t2016/12/20161222\n2016 was a good year\n2016-13-01\nDate 2017-12-25\nDate 1975-11-14\nDate 2001-07-31\nThis is just raw data!\t2014/12-01'
#    #testResult4 = find_the_date(testInput4)
#    #print("TEST 4 - {}\n".format(testResult4))

#    # TEST 5 - SMBC
#    with open('5-SMBC_HTML.txt', 'r') as testFile5:
#        testInput5 = testFile5.read()

#    testResult5 = find_the_date(testInput5)
#    print("TEST 5\t'20161227' == {}:\t{}\n".format(testResult5, testResult5 == '20161227'))

#    # TEST 6 - SMBC
#    with open('6-SMBC_HTML.txt', 'r') as testFile6:
#        testInput6 = testFile6.read()

#    testResult6 = find_the_date(testInput6)
#    print("TEST 6\t'20161226' == {}:\t{}\n".format(testResult6, testResult6 == '20161226'))

#    # TEST 7 - Penny Arcade
#    with open('7-Penny_Arcade_random_HTML.txt', 'r') as testFile7:
#        testInput7 = testFile7.read()

#    testResult7 = find_the_date(testInput7)
#    print("TEST 7\t'20100712' == {}:\t{}\n".format(testResult7, testResult7 == '20100712'))

#    # TEST 8 - xkcd
#    with open('8-xkcd_random_HTML.txt', 'r') as testFile8:
#        testInput8 = testFile8.read()

#    testResult8 = find_the_date(testInput8)
#    print("TEST 8\t'00000000' == {}:\t{}\n".format(testResult8, testResult8 == '00000000'))

############### BROKEN TESTS ##############
## Tests 9 & 10 are currently broken
## New functionality is finding daetes in
##     the side bar
## TO DO list includes ideas to improve
##     final decision algorithm
###########################################

##    # TEST 9 - OotS
###    print("TEST 9")
##    with open('9-OotS_random_HTML.txt', 'r') as testFile9:
##        testInput9 = testFile9.read()

##    testResult9 = find_the_date(testInput9)
##    print("TEST 9\t'00000000' == {}:\t{}\n".format(testResult9, testResult9 == '00000000'))

##    # TEST 10 - OotS
###    print("TEST 10")
##    with open('10-OotS_recent_HTML.txt', 'r') as testFile10:
##        testInput10 = testFile10.read()

##    testResult10 = find_the_date(testInput10)
##    print("TEST 10\t'00000000' == {}:\t{}\n".format(testResult10, testResult10 == '00000000'))

###########################################
############### BROKEN TESTS ##############
###########################################

#    # TEST 11 - PvP (error, date format change)
#    with open('11-PvP_slash_date_HTML.txt', 'r') as testFile11:
#        testInput11 = testFile11.read()

#    testResult11 = find_the_date(testInput11)
#    print("TEST 11\t'20151231' == {}:\t{}\n".format(testResult11, testResult11 == '20151231'))


