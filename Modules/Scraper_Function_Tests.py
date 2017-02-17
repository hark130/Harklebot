from Scraper_Functions import find_the_date 
from Scraper_Functions import find_a_URL            # find_a_URL(htmlString, searchStart, searchStop)
from Scraper_Functions import get_image_filename    # get_image_filename(htmlString, [dateSearchPhrase], [nameSearchPhrase], nameEnding)
from Scraper_Functions import is_URL_abs            # is_URL_abs(baseURL, targetURL)
from Scraper_Functions import make_rel_URL_abs      # make_rel_URL_abs(baseURL, targetURL)
from Scraper_Functions import is_URL_valid          # is_URL_valid(URL)

import unittest
import os


class IsURLValid(unittest.TestCase):
    
    # Test 1 - TypeError('URL is not a string')
    def test01_TypeError01(self):
        try:
            result = is_URL_valid(420 / 1337)
        except TypeError as err:
            self.assertEqual(err.args[0], 'URL is not a string')
        except Exception as err:
            print(repr(err))
            self.fail('Raised the wrong exception')
    
    # Test 2 - TypeError('URL is not a string')
    def test02_TypeError02(self):
        try:
            result = is_URL_valid(['http://www.thisisnotastring.org'])
        except TypeError as err:
            self.assertEqual(err.args[0], 'URL is not a string')
        except Exception as err:
            print(repr(err))
            self.fail('Raised the wrong exception')
            
    # Test 3 - ValueError('URL is empty')
    def test03_ValueError01(self):
        try:
            result = is_URL_valid('')
        except ValueError as err:
            self.assertEqual(err.args[0], 'URL is empty')
        except Exception as err:
            print(repr(err))
            self.fail('Raised the wrong exception')
            
    # Test 4 - Valid Input
    def test04_ValidInput01(self):
        try:
            result = is_URL_valid('www.somesite.com')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(result)
            
    # Test 5 - Valid Input
    def test05_ValidInput02(self):
        try:
            result = is_URL_valid('http://www.somesite.org')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(result)
            
    # Test 5 - Valid Input
    def test05_ValidInput03(self):
        try:
            result = is_URL_valid('https://www.somesite.ph')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(result)
            
    # Test 5 - Messy Yet Valid Input
    def test05_MessyYetValidInput01(self):
        try:
            result = is_URL_valid('http://127.0.0.1:8080/test?v=123#this')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(result)
            
    # Test 6 - Messy Yet Valid Input
    def test06_MessyYetValidInput02(self):
        try:
            result = is_URL_valid('http://api.google.com/q?exp=a%7Cb')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(result)
             
    # Test 7 - Messy Yet Valid Input
    def test07_MessyYetValidInput03(self):
        try:
            result = is_URL_valid('http://[2001:db8:85a3::8a2e:370:7334]/foo/bar')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(result)        
            
    # Test 8 - Messy Yet Valid Input
    def test08_MessyYetValidInput04(self):
        try:
            result = is_URL_valid('http://www.amazon.com/s/ref=nb_sb_noss_1?url=search-alias%3Ddigital-text&amp;field-keywords=Phyllis+Zimbler+Miller')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(result)
            
    # Test 9 - Messy Yet Valid Input
    def test09_MessyYetValidInput05(self):
        try:
            result = is_URL_valid('ftp://username%3Apassword@domain')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(result)
            
    # Test 10 - Messy Yet Valid Input
    def test10_MessyYetValidInput06(self):
        try:
            result = is_URL_valid('https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=5&ved=0ahUKEwiYpIT04JfSAhVDLZoKHWF0CyEQFgg1MAQ&url=http%3A%2F%2Fwww.complex.com%2Flife%2F2016%2F05%2Fbest-hashtags-dragging-donald-trump&usg=AFQjCNHPGIS5_B0_t9wbjbqQenn8iZ165g&sig2=oAIU60SQ8-OtztfPlsSsTg&cad=rja')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(result)
            
    # Test 11 - Messy Yet Invalid Input
    def test11_MessyYetInvalidInput01(self):
        try:
            result = is_URL_valid('http://mw1.google.com/mw-earth-vectordb/kml-samples/gp/seattle/gigapxl/$[level]/r$[y]_c$[x].jpg')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertFalse(result)
            
    # Test 12 - Messy Yet Invalid Input
    def test12_MessyYetInvalidInput02(self):
        try:
            result = is_URL_valid('http://api.google.com/q?exp=a|b')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertFalse(result)
            
    # Test 13 - Messy Yet Invalid Input
    def test13_MessyYetInvalidInput03(self):
        try:
            result = is_URL_valid('http://example.com/wp-admin/load-scripts.php?c=1&load[]=swfobject,jquery,utils&ver=3.5')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertFalse(result)
            
    # Test 14 - Messy Yet Invalid Input
    def test14_MessyYetInvalidInput04(self):
        try:
            result = is_URL_valid('http://test.site/wp-admin/post.php?t=1347548645469?t=1347548651124?t=1347548656685?t=1347548662469?t=1347548672300?t=1347548681615?')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertFalse(result)
            
    # Test 15 - Messy Yet Invalid Input
    def test15_MessyYetInvalidInput05(self):
        try:
            result = is_URL_valid('http://blog.sergeys.us/beer?utm_source=feedburner&amp;utm_medium=feed&amp;utm_campaign=Feed:+SergeySus+(Sergey+Sus+Photography+%C2%BB+Blog)&amp;utm_content=Google+Reader')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertFalse(result)
            
    # Test 15 - Messy Yet Invalid Input
    def test15_MessyYetInvalidInput06(self):
        try:
            result = is_URL_valid('ftp://username:password@domain')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertFalse(result)
            
            
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
            
    # Test 20 - Tricky Input - Redundant slashes that are redundant
    def test20_TrickyInput10(self):
        try:
            result = make_rel_URL_abs('https://www.grumpyc.at/is/grumpy/', '/is/grumpy/sometimes.html')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(result == 'https://www.grumpyc.at/is/grumpy/sometimes.html')



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
            self.assertFalse(result) # Should probably be true

    # Test 15 - Tricky Input - Mixed up association of relative and aboslute
    def test15_TrickyInput06(self):
        try:
            result = is_URL_abs('http://pvponline.com', 'pvponline.com/comic/2017-02-16')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertFalse(result) # Should probably be true
            
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
            result = is_URL_abs('www.not_a_URL.cz', '2017-02-16')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertFalse(result)
            
    # Test 21 - Bad Input - Invalid baseURL
    def test21_BadInput02(self):
        try:
            result = is_URL_abs('www.not_a_URL.ca', 'URL')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertFalse(result)
            
    # Test 22 - Bad Input - Invalid baseURL
    def test22_BadInput03(self):
        try:
            result = is_URL_abs('https://definitely-not-a-URL.arpa', 'https://xkcd.com')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(result)
            
    # Test 23 - Bad Input - Invalid baseURL
    def test23_BadInput04(self):
        try:
            result = is_URL_abs('http://probably-not_a-URL.ba', 'www.smbc-comics.com')
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
#            self.assertFalse(result)      
            pass
            # Uncomment the test above once is_URL_valid() has been written to check for:
            #   Invalid URL characters
            #   Start indicators that are not at the beginning
            #   Ending indicators that are not at the end
            
    # Test 28 - Bad Input - Invalid targetURL
    def test28_BadURL05(self):
        try:
            result = is_URL_abs('https://www.xkcd.com/', 'websites typically begin with https: and end with a top-level domain like .com or .org')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
#            self.assertFalse(result)      
            pass
            # Uncomment the test above once is_URL_valid() has been written to check for:
            #   Invalid URL characters
            #   Start indicators that are not at the beginning
            #   Ending indicators that are not at the end  
            
    # Test 29 - Bad Input - Invalid targetURL
    def test29_BadURL06(self):
        try:
            result = is_URL_abs('https://www.xkcd.com/', 'websites typically begin with http: and end with a top-level domain like .com or .org')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
#            self.assertFalse(result)      
            pass
            # Uncomment the test above once is_URL_valid() has been written to check for:
            #   Invalid URL characters
            #   Start indicators that are not at the beginning
            #   Ending indicators that are not at the end 
            
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
            result = is_URL_abs('www.notaURL.ca', 'ThisisdefinitelynotaURLsinceitdoesnotincludeatopleveldomainlike.cz')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertFalse(result)  
            
    # Test 35 - Bad Input - Not a single valid URL
    def test35_BadURL12(self):
        try:
            result = is_URL_abs('http://Alphabet.cd', 'theAlphabetIsExtendedToInclude.bdAnd.be')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertFalse(result)  
            
    # Test 36 - Bad Input - Not a single valid URL
    def test36_BadURL13(self):
        try:
            result = is_URL_abs('www.Alphabet.de', 'AlphabetIsExtendedToInclude.asAnd.at')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertFalse(result)  

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

#    # Run all the tests!
#    unittest.main(verbosity=2)
    
# MakeRelURLAbs
    linkerSuite = unittest.TestLoader().loadTestsFromTestCase(MakeRelURLAbs)
    unittest.TextTestRunner(verbosity=2).run(linkerSuite)
    
# IsURLAbs
    linkerSuite = unittest.TestLoader().loadTestsFromTestCase(IsURLAbs)
    unittest.TextTestRunner(verbosity=2).run(linkerSuite)
    
# FindURL
    linkerSuite = unittest.TestLoader().loadTestsFromTestCase(FindURL)
    unittest.TextTestRunner(verbosity=2).run(linkerSuite)

#### THIS FUNCTION IS NOT YET DEFINED ####
## IsURLValid
#    linkerSuite = unittest.TestLoader().loadTestsFromTestCase(IsURLValid)
#    unittest.TextTestRunner(verbosity=2).run(linkerSuite)
 
#### BROKEN TESTS HERE ####
## GetImageFilename
#    linkerSuite = unittest.TestLoader().loadTestsFromTestCase(GetImageFilename)
#    unittest.TextTestRunner(verbosity=2).run(linkerSuite)


    print("Done Testing")
