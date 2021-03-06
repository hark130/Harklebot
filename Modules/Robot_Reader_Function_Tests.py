import unittest
from urllib.error import HTTPError
from Robot_Reader_Functions import get_page_disposition     # get_page_disposition(baseURL, userAgent=['Python-urllib', 'Python-urllib/3.5'])
from Robot_Reader_Functions import robots_may_I             # robots_may_I(page_disposition, URL)


# This class specifically tests Robot Reader's ability to respond to Crawl-Delays
class CrawlDelayCombinedTest(unittest.TestCase):

    # Test 1 - http://www.managementcenter.org/robots.txt
    # Variable Crawl Delays
    # User-agent: *
    # Disallow: /wp-admin/
    # Crawl-delay: 30
    # User-agent: Googlebot
    # Crawl-delay: 10
    # User-agent: Googlebot-Mobile
    # Crawl-delay: 20
    # User-agent: AdsBot-Google-Mobile
    # Crawl-delay: 20
    # User-agent: TweetmemeBot
    # Crawl-delay: 120
    # User-agent: PaperLiBot
    # Crawl-delay: 60
    # User-agent: TinEye-bot
    # Crawl-delay: 500
    # User-agent: grapeshot
    # Crawl-delay: 30
    #def test01_MMC01(self):
    #    # Setup the test variables
    #    baseURL = 'http://www.managementcenter.org'
    #    userAgent = ['Harklebot', 'Python-urllib']
        
    #    # Call get_page_disposition()
    #    try:
    #        page_disposition = get_page_disposition(baseURL, userAgent)
    #    except Exception as err:
    #        print(repr(err))
    #        self.fail('Raised an exception')
    #    else:
    #        self.assertTrue(isinstance(page_disposition, dict))
    #        self.assertTrue(page_disposition.__len__() > 0)
            
    #    # A
    #    try:
    #        result = robots_may_I(page_disposition, 'Crawl-Delay:')
    #    except Exception as err:
    #        print(repr(err))
    #        self.fail('Raised an exception')
    #    else:
    #        self.assertTrue(isinstance(result, int))
    #        self.assertEqual(result, 30)      

    # Test 2 - http://www.nasdaq.com/robots.txt
    # Variable Crawl Delays
    #User-agent: *
    #Crawl-delay: 30
    #Disallow: /*.ashx$
    #Disallow: /personal-finance/bankrate-cc-results.aspx
    #Disallow: /personal-finance/bankrate-cd-results.aspx
    #Disallow: /personal-finance/bankrate-auto-results.aspx
    #Disallow: /personal-finance/bankrate-mma-results.aspx
    #Disallow: /personal-finance/bankrate-mortgage-results.aspx
    #User-agent: grapeshot
    #User-agent: Pipl
    #Disallow: /
    #User-agent: mediapartners-google
    #Crawl-delay: 0
    #User-agent: googlebot
    #Crawl-delay: 0
    #User-agent: googlebot-news
    #Crawl-delay: 0
    def test02_Nasdaq01(self):
        # Setup the test variables
        baseURL = 'http://www.nasdaq.com'
        userAgent = ['Harklebot', 'Python-urllib']
        
        # Call get_page_disposition()
        try:
            page_disposition = get_page_disposition(baseURL, userAgent)
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(isinstance(page_disposition, dict))
            self.assertTrue(page_disposition.__len__() > 0)
            
        # Check Crawl Delay
        self.assertTrue('Crawl-delay:' in page_disposition.keys())

        try:
            result = page_disposition['Crawl-delay:']
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(isinstance(result, int))
            self.assertEqual(result, 30)      

    # Test 3 - http://www.nasdaq.com/robots.txt
    # Variable Crawl Delays
    #User-agent: *
    #Crawl-delay: 30
    #Disallow: /*.ashx$
    #Disallow: /personal-finance/bankrate-cc-results.aspx
    #Disallow: /personal-finance/bankrate-cd-results.aspx
    #Disallow: /personal-finance/bankrate-auto-results.aspx
    #Disallow: /personal-finance/bankrate-mma-results.aspx
    #Disallow: /personal-finance/bankrate-mortgage-results.aspx
    #User-agent: grapeshot
    #User-agent: Pipl
    #Disallow: /
    #User-agent: mediapartners-google
    #Crawl-delay: 0
    #User-agent: googlebot
    #Crawl-delay: 0
    #User-agent: googlebot-news
    #Crawl-delay: 0
    def test03_Nasdaq02(self):
        # Setup the test variables
        baseURL = 'http://www.nasdaq.com'
        userAgent = ['mediapartners-google']
        
        # Call get_page_disposition()
        try:
            page_disposition = get_page_disposition(baseURL, userAgent)
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(isinstance(page_disposition, dict))
            self.assertTrue(page_disposition.__len__() > 0)
            
        # Check Crawl Delay
        self.assertTrue('Crawl-delay:' in page_disposition.keys())

        try:
            result = page_disposition['Crawl-delay:']
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(isinstance(result, int))
            self.assertEqual(result, 0)      

    # Test 4 - http://www.nasdaq.com/robots.txt
    # Variable Crawl Delays
    #User-agent: *
    #Crawl-delay: 30
    #Disallow: /*.ashx$
    #Disallow: /personal-finance/bankrate-cc-results.aspx
    #Disallow: /personal-finance/bankrate-cd-results.aspx
    #Disallow: /personal-finance/bankrate-auto-results.aspx
    #Disallow: /personal-finance/bankrate-mma-results.aspx
    #Disallow: /personal-finance/bankrate-mortgage-results.aspx
    #User-agent: grapeshot
    #User-agent: Pipl
    #Disallow: /
    #User-agent: mediapartners-google
    #Crawl-delay: 0
    #User-agent: googlebot
    #Crawl-delay: 0
    #User-agent: googlebot-news
    #Crawl-delay: 0
    def test04_Nasdaq03(self):
        # Setup the test variables
        baseURL = 'http://www.nasdaq.com'
        userAgent = ['Harklebot', 'googlebot']
        
        # Call get_page_disposition()
        try:
            page_disposition = get_page_disposition(baseURL, userAgent)
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(isinstance(page_disposition, dict))
            self.assertTrue(page_disposition.__len__() > 0)
            
        # Check Crawl Delay
        self.assertTrue('Crawl-delay:' in page_disposition.keys())

        try:
            result = page_disposition['Crawl-delay:']
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(isinstance(result, int))
            self.assertEqual(result, 0)      

    # Test 5 - https://www.pluralsight.com/robots.txt
    # Variable Crawl Delays
    #User-agent: Yandex
    #Disallow: /
    #Crawl-delay: 300
    #User-Agent: rogerbot
    #Disallow: /
    #Crawl-delay: 300
    #user-agent: AhrefsBot
    #disallow: /
    def test05_PS01(self):
        # Setup the test variables
        baseURL = 'https://www.pluralsight.com'
        userAgent = ['Harklebot']
        
        # Call get_page_disposition()
        try:
            page_disposition = get_page_disposition(baseURL, userAgent)
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(isinstance(page_disposition, dict))
            self.assertTrue(page_disposition.__len__() > 0)
            
        # Check Crawl Delay
        self.assertFalse('Crawl-delay:' in page_disposition.keys())

    # Test 6 - https://www.pluralsight.com/robots.txt
    # Variable Crawl Delays
    #User-agent: Yandex
    #Disallow: /
    #Crawl-delay: 300
    #User-Agent: rogerbot
    #Disallow: /
    #Crawl-delay: 300
    #user-agent: AhrefsBot
    #disallow: /
    def test06_PS02(self):
        # Setup the test variables
        baseURL = 'https://www.pluralsight.com'
        userAgent = ['Harklebot', 'Yandex']
        
        # Call get_page_disposition()
        try:
            page_disposition = get_page_disposition(baseURL, userAgent)
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(isinstance(page_disposition, dict))
            self.assertTrue(page_disposition.__len__() > 0)
            
        # Check Crawl Delay
        self.assertTrue('Crawl-delay:' in page_disposition.keys())

        try:
            result = page_disposition['Crawl-delay:']
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(isinstance(result, int))
            self.assertEqual(result, 300)      

    # Test 7 - http://www.crownaudio.com/robots.txt
    # Fractional Crawl Delays
    #User-agent: *
    #Sitemap: http://www.crownaudio.com/sitemap.xml
    #Crawl-delay: 4.5
    ## Yandex tries to pull support page as a jpeg for some reason
    #User-agent: Yandex
    #Disallow: /en-US/support.jpg
    #Disallow: /en/support.jpg
    ## Majestic12 bot hammers the site with DoS-style traffic
    #User-agent: MJ12bot
    #Disallow: /
    def test07_CA01(self):
        # Setup the test variables
        baseURL = 'http://www.crownaudio.com'
        userAgent = ['Harklebot']
        
        # Call get_page_disposition()
        try:
            page_disposition = get_page_disposition(baseURL, userAgent)
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(isinstance(page_disposition, dict))
            self.assertTrue(page_disposition.__len__() > 0)
            
        # Check Crawl Delay
        self.assertTrue('Crawl-delay:' in page_disposition.keys())

        try:
            result = page_disposition['Crawl-delay:']
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(isinstance(result, int))
            self.assertEqual(result, 5)      

    # Test 8 - http://www.crownaudio.com/robots.txt
    # Fractional Crawl Delays
    #User-agent: *
    #Sitemap: http://www.crownaudio.com/sitemap.xml
    #Crawl-delay: 4.5
    ## Yandex tries to pull support page as a jpeg for some reason
    #User-agent: Yandex
    #Disallow: /en-US/support.jpg
    #Disallow: /en/support.jpg
    ## Majestic12 bot hammers the site with DoS-style traffic
    #User-agent: MJ12bot
    #Disallow: /
    def test08_CA02(self):
        # Setup the test variables
        baseURL = 'http://www.crownaudio.com'
        userAgent = ['MJ12bot']
        
        # Call get_page_disposition()
        try:
            page_disposition = get_page_disposition(baseURL, userAgent)
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(isinstance(page_disposition, dict))
            self.assertTrue(page_disposition.__len__() > 0)
            
        # Check Crawl Delay
        self.assertTrue('Crawl-delay:' in page_disposition.keys())

        try:
            result = page_disposition['Crawl-delay:']
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(isinstance(result, int))
            self.assertEqual(result, 5)      

    # Test 9 - http://www.crownaudio.com/robots.txt
    # Fractional Crawl Delays
    #User-agent: *
    #Sitemap: http://www.crownaudio.com/sitemap.xml
    #Crawl-delay: 4.5
    ## Yandex tries to pull support page as a jpeg for some reason
    #User-agent: Yandex
    #Disallow: /en-US/support.jpg
    #Disallow: /en/support.jpg
    ## Majestic12 bot hammers the site with DoS-style traffic
    #User-agent: MJ12bot
    #Disallow: /
    def test09_CA02(self):
        # Setup the test variables
        baseURL = 'http://www.crownaudio.com'
        userAgent = ['MJ12bot']
        
        # Call get_page_disposition()
        try:
            page_disposition = get_page_disposition(baseURL, userAgent)
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(isinstance(page_disposition, dict))
            self.assertTrue(page_disposition.__len__() > 0)
            
        # Check Crawl Delay
        self.assertTrue('Crawl-delay:' in page_disposition.keys())

        try:
            result = page_disposition['Crawl-delay:']
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(isinstance(result, int))
            self.assertEqual(result, 5)      
             

# This class tests combined functionality from get_page_disposition() and robots_may_I()
# This class will not concern itself with testing input validation because each function has already been tested
# This class will attempt to find errors/loop holes/oversights in the combination of the two functions
class PageDispositionCombinedTest(unittest.TestCase):
    
    # Test 1 - http://www.smbc-comics.com/robots.txt
    # Robots.txt is blank
    def test01_SMBC01(self):
        # Setup the test variables
        baseURL = 'http://www.smbc-comics.com'
        userAgent = ['Harklebot', 'Python-urllib/3.5']
        
        # Call get_page_disposition()
        try:
            page_disposition = get_page_disposition(baseURL, userAgent)
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(isinstance(page_disposition, dict))
            self.assertTrue(page_disposition.__len__() > 0)
            
        # A
        try:
            result = robots_may_I(page_disposition, 'http://www.smbc-comics.com/comic/non-judgmental-parenting')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(isinstance(result, bool))
            self.assertTrue(result)      
            
        # B
        try:
            result = robots_may_I(page_disposition, 'http://www.smbc-comics.com/comic/')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(isinstance(result, bool))
            self.assertTrue(result)   
            
        # C
        try:
            result = robots_may_I(page_disposition, 'http://www.smbc-comics.com')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(isinstance(result, bool))
            self.assertTrue(result)   
            
    # Test 2 - https://www.xkcd.com/robots.txt
    # Robots.txt:
    #   User-agent: *
    #   Disallow: /personal/
    def test02_XKCD01(self):
        # Setup the test variables
        baseURL = 'https://www.xkcd.com'
        userAgent = ['Harklebot', 'Python-urllib/3.5']
        
        # Call get_page_disposition()
        try:
            page_disposition = get_page_disposition(baseURL, userAgent)
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(isinstance(page_disposition, dict))
            self.assertTrue(page_disposition.__len__() > 0)
            
        # Site A
        try:
            result = robots_may_I(page_disposition, 'https://www.xkcd.com/655/')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(isinstance(result, bool))
            self.assertTrue(result)      
            
        # Site B
        try:
            result = robots_may_I(page_disposition, 'https://www.xkcd.com')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(isinstance(result, bool))
            self.assertTrue(result)   
            
        # Site C
        try:
            result = robots_may_I(page_disposition, 'https://imgs.xkcd.com/comics/climbing.png')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(isinstance(result, bool))
            self.assertTrue(result)    
            
        # Site D
        try:
            result = robots_may_I(page_disposition, 'https://www.xkcd.com/personal/')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(isinstance(result, bool))
            self.assertFalse(result)  
            
    # Test 3 - https://www.cad-comic.com/robots.txt
    # Robots.txt:
    #   User-agent: *
    #   Disallow: /
    def test03_CAD01(self):
        # Setup the test variables
        baseURL = 'https://www.cad-comic.com/'
        userAgent = ['Harklebot', 'Python-urllib/3.5', 'Maklebot']
        
        # Call get_page_disposition()
        try:
            page_disposition = get_page_disposition(baseURL, userAgent)
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(isinstance(page_disposition, dict))
            self.assertTrue(page_disposition.__len__() > 0)
            
        # Site A
        try:
            result = robots_may_I(page_disposition, 'https://www.cad-comic.com/')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(isinstance(result, bool))
            self.assertFalse(result)      
            
        # Site B
        try:
            result = robots_may_I(page_disposition, 'https://www.cad-comic.com/sillies/')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(isinstance(result, bool))
            self.assertFalse(result)   
            
        # Site C
        try:
            result = robots_may_I(page_disposition, 'http://www.cad-forums.com/')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(isinstance(result, bool))
            self.assertFalse(result)    
            
        # Site D
        try:
            result = robots_may_I(page_disposition, 'https://ctrl-alt-del.myshopify.com/')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(isinstance(result, bool))
            self.assertFalse(result)  

        # Site E
        try:
            result = robots_may_I(page_disposition, 'https://www.cad-comic.com/sillies/20100604')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(isinstance(result, bool))
            self.assertFalse(result)  
            
    # Test 4 - https://www.penny-arcade.com/robots.txt
    # Robots.txt:
    #   User-agent: *
    #   Disallow: /feed/
    #   Disallow: /feed/podcasts-*
    #   Disallow: /feed/show-*
    #   Allow: /feed/podcasts
    #   Allow: /feed/show
    def test04_PA01(self):
        # Setup the test variables
        baseURL = 'https://www.penny-arcade.com'
        userAgent = ['Harklebot', 'Python-urllib/3.5', 'Maklebot']
        
        # Call get_page_disposition()
        try:
            page_disposition = get_page_disposition(baseURL, userAgent)
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(isinstance(page_disposition, dict))
            self.assertTrue(page_disposition.__len__() > 0)
            
        # Site A
        try:
            result = robots_may_I(page_disposition, 'https://www.penny-arcade.com')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(isinstance(result, bool))
            self.assertTrue(result)      
            
        # Site B
        try:
            result = robots_may_I(page_disposition, 'https://www.penny-arcade.com/feed/')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(isinstance(result, bool))
            self.assertFalse(result)   
            
        # Site C
        try:
            result = robots_may_I(page_disposition, 'https://www.penny-arcade.com/feed/podcasts/')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(isinstance(result, bool))
            self.assertTrue(result)    
            
        # Site D
        try:
            result = robots_may_I(page_disposition, 'https://www.penny-arcade.com/feed/show/')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(isinstance(result, bool))
            self.assertTrue(result)  

        # Site E
        try:
            result = robots_may_I(page_disposition, 'http://www.penny-arcade.com/news/post/2017/02/22/update-on-that-stolen-ps4-in-new-zealand')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(isinstance(result, bool))
            self.assertTrue(result)  
            
        # Site F
        try:
            result = robots_may_I(page_disposition, 'http://www.penny-arcade.com/patv/show/dlc-podcast-show')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(isinstance(result, bool))
            self.assertTrue(result)  
            
        # Site G
        try:
            result = robots_may_I(page_disposition, 'https://www.penny-arcade.com/feed/podcasts-are-fun')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(isinstance(result, bool))
            self.assertFalse(result)   
            
        # Site H
        try:
            result = robots_may_I(page_disposition, 'https://www.penny-arcade.com/feed/show-me-the-code')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(isinstance(result, bool))
            self.assertFalse(result)   
            
    # Test 5 - http://www.awkwardzombie.com/robots.txt - ['Harklebot', 'Python-urllib/3.5']
    # Robots.txt:
    #   User-agent: *
    #   Crawl-Delay: 30
    #   Disallow: /aggregator/
    #   Disallow: /tracker/
    #   Disallow: /archive/
    #   Disallow: /archive/*/
    #   Disallow: /event/
    #   Disallow: /event/*/
    #   Disallow: /comment/reply/
    #   Disallow: /node/add/
    #   Disallow: /user/
    #   Disallow: /files/
    #   Disallow: /popular/
    #   Disallow: /popular/*/
    #   Disallow: /xtracker/
    #   Disallow: /search/
    #   Disallow: /book/print/
    #   Disallow: /forward/
    #   Disallow: /taxonomy/
    #   Disallow: /node/*/print/
    #   Disallow: /node/print/
    #   Disallow: /node/
    #   Disallow: /blog/
    #   Disallow: /archive/
    #   Disallow: /print/
    #   Disallow: /taxonomy/
    def test05_AZ01(self):
        # Setup the test variables
        baseURL = 'http://www.awkwardzombie.com'
        userAgent = ['Harklebot', 'Python-urllib/3.5']
        
        # Call get_page_disposition()
        try:
            page_disposition = get_page_disposition(baseURL, userAgent)
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(isinstance(page_disposition, dict))
            self.assertTrue(page_disposition.__len__() > 0)
            
        # Site A
        try:
            result = robots_may_I(page_disposition, 'http://www.awkwardzombie.com/aggregator/')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(isinstance(result, bool))
            self.assertFalse(result)      
            
        # Site B
        try:
            result = robots_may_I(page_disposition, 'http://www.awkwardzombie.com/archive/')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(isinstance(result, bool))
            self.assertFalse(result)   
            
        # Site C
        try:
            result = robots_may_I(page_disposition, 'http://www.awkwardzombie.com/archive/jedi/')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(isinstance(result, bool))
            self.assertFalse(result)    
            
        # Site D
        try:
            result = robots_may_I(page_disposition, 'http://www.awkwardzombie.com/event/')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(isinstance(result, bool))
            self.assertFalse(result)  

        # Site E
        try:
            result = robots_may_I(page_disposition, 'http://www.awkwardzombie.com/event/extinction/')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(isinstance(result, bool))
            self.assertFalse(result)  
            
        # Site F
        try:
            result = robots_may_I(page_disposition, 'http://www.awkwardzombie.com/comment/reply/')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(isinstance(result, bool))
            self.assertFalse(result)  
            
        # Site G
        try:
            result = robots_may_I(page_disposition, 'http://www.awkwardzombie.com/node/add/')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(isinstance(result, bool))
            self.assertFalse(result)   
            
        # Site H
        try:
            result = robots_may_I(page_disposition, 'http://www.awkwardzombie.com/popular/')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(isinstance(result, bool))
            self.assertFalse(result)   
            
        # Site I
        try:
            result = robots_may_I(page_disposition, 'http://www.awkwardzombie.com/popular/mechanics/')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(isinstance(result, bool))
            self.assertFalse(result)  
            
        # Site I
        try:
            result = robots_may_I(page_disposition, 'http://www.awkwardzombie.com/node/print/')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(isinstance(result, bool))
            self.assertFalse(result)  
            
        # Site I
        try:
            result = robots_may_I(page_disposition, 'http://www.awkwardzombie.com/node/to/print/')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(isinstance(result, bool))
            self.assertFalse(result)  
            
        # Site J
        try:
            result = robots_may_I(page_disposition, 'http://www.awkwardzombie.com/forum/index.php')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(isinstance(result, bool))
            self.assertTrue(result)  
            
        # Site K
        try:
            result = robots_may_I(page_disposition, 'http://www.awkwardzombie.com/index.php?page=0&comic=013017')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(isinstance(result, bool))
            self.assertTrue(result)  
            
        # Site L
        try:
            result = robots_may_I(page_disposition, 'http://www.awkwardzombie.com/tracker/jacker/')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(isinstance(result, bool))
            self.assertFalse(result)  
                                  
        # Site M
        try:
            result = robots_may_I(page_disposition, 'http://www.awkwardzombie.com')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(isinstance(result, bool))
            self.assertTrue(result)  
                                  
        # Site N
        try:
            result = robots_may_I(page_disposition, 'http://www.awkwardzombie.com/I/made/up/this/path.html')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(isinstance(result, bool))
            self.assertTrue(result)  
            
    # Test 6 - http://www.awkwardzombie.com/robots.txt - ['Googlebot']
    # Robots.txt:
    #   User-agent: Googlebot
    #   Crawl-Delay: 30
    #   Disallow: /aggregator/
    #   Disallow: /tracker/
    #   Disallow: /archive/
    #   Disallow: /archive/*/
    #   Disallow: /event/
    #   Disallow: /event/*/
    #   Disallow: /comment/reply/
    #   Disallow: /node/add/
    #   Disallow: /user/
    #   Disallow: /files/
    #   Disallow: /popular/
    #   Disallow: /popular/*/
    #   Disallow: /xtracker/
    #   Disallow: /search/
    #   Disallow: /book/print/
    #   Disallow: /forward/
    #   Disallow: /taxonomy/
    #   Disallow: /node/*/print/
    #   Disallow: /node/print/
    #   Disallow: /node/
    #   Disallow: /blog/
    #   Disallow: /archive/
    #   Disallow: /print/
    #   Disallow: /taxonomy/
    def test06_AZ02(self):
        # Setup the test variables
        baseURL = 'http://www.awkwardzombie.com'
        userAgent = ['Googlebot']
        
        # Call get_page_disposition()
        try:
            page_disposition = get_page_disposition(baseURL, userAgent)
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(isinstance(page_disposition, dict))
            self.assertTrue(page_disposition.__len__() > 0)
            
        # Site A
        try:
            result = robots_may_I(page_disposition, 'http://www.awkwardzombie.com/aggregator/')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(isinstance(result, bool))
            self.assertFalse(result)      
            
        # Site B
        try:
            result = robots_may_I(page_disposition, 'http://www.awkwardzombie.com/archive/')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(isinstance(result, bool))
            self.assertFalse(result)   
            
        # Site C
        try:
            result = robots_may_I(page_disposition, 'http://www.awkwardzombie.com/archive/jedi/')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(isinstance(result, bool))
            self.assertFalse(result)    
            
        # Site D
        try:
            result = robots_may_I(page_disposition, 'http://www.awkwardzombie.com/event/')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(isinstance(result, bool))
            self.assertFalse(result)  

        # Site E
        try:
            result = robots_may_I(page_disposition, 'http://www.awkwardzombie.com/event/extinction/')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(isinstance(result, bool))
            self.assertFalse(result)  
            
        # Site F
        try:
            result = robots_may_I(page_disposition, 'http://www.awkwardzombie.com/comment/reply/')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(isinstance(result, bool))
            self.assertFalse(result)  
            
        # Site G
        try:
            result = robots_may_I(page_disposition, 'http://www.awkwardzombie.com/node/add/')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(isinstance(result, bool))
            self.assertFalse(result)   
            
        # Site H
        try:
            result = robots_may_I(page_disposition, 'http://www.awkwardzombie.com/popular/')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(isinstance(result, bool))
            self.assertFalse(result)   
            
        # Site I
        try:
            result = robots_may_I(page_disposition, 'http://www.awkwardzombie.com/popular/mechanics/')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(isinstance(result, bool))
            self.assertFalse(result)  
            
        # Site I
        try:
            result = robots_may_I(page_disposition, 'http://www.awkwardzombie.com/node/print/')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(isinstance(result, bool))
            self.assertFalse(result)  
            
        # Site I
        try:
            result = robots_may_I(page_disposition, 'http://www.awkwardzombie.com/node/to/print/')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(isinstance(result, bool))
            self.assertFalse(result)  
            
        # Site J
        try:
            result = robots_may_I(page_disposition, 'http://www.awkwardzombie.com/forum/index.php')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(isinstance(result, bool))
            self.assertTrue(result)  
            
        # Site K
        try:
            result = robots_may_I(page_disposition, 'http://www.awkwardzombie.com/index.php?page=0&comic=013017')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(isinstance(result, bool))
            self.assertTrue(result)  
            
        # Site L
        try:
            result = robots_may_I(page_disposition, 'http://www.awkwardzombie.com/tracker/jacker/')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(isinstance(result, bool))
            self.assertFalse(result)  
                                  
        # Site M
        try:
            result = robots_may_I(page_disposition, 'http://www.awkwardzombie.com')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(isinstance(result, bool))
            self.assertTrue(result)  
                                  
        # Site N
        try:
            result = robots_may_I(page_disposition, 'http://www.awkwardzombie.com/I/made/up/this/path.html')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(isinstance(result, bool))
            self.assertTrue(result)  
            
    # Test 7 - http://www.awkwardzombie.com/robots.txt - ['BotALot']
    # Robots.txt:
    #   User-agent: BotALot
    #   Disallow: /
    def test07_AZ03(self):
        # Setup the test variables
        baseURL = 'http://www.awkwardzombie.com'
        userAgent = ['BotALot']
        
        # Call get_page_disposition()
        try:
            page_disposition = get_page_disposition(baseURL, userAgent)
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(isinstance(page_disposition, dict))
            self.assertTrue(page_disposition.__len__() > 0)
            
        # Site A
        try:
            result = robots_may_I(page_disposition, 'http://www.awkwardzombie.com/aggregator/')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(isinstance(result, bool))
            self.assertFalse(result)      
            
        # Site B
        try:
            result = robots_may_I(page_disposition, 'http://www.awkwardzombie.com/archive/')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(isinstance(result, bool))
            self.assertFalse(result)   
            
        # Site C
        try:
            result = robots_may_I(page_disposition, 'http://www.awkwardzombie.com/archive/jedi/')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(isinstance(result, bool))
            self.assertFalse(result)    
            
        # Site D
        try:
            result = robots_may_I(page_disposition, 'http://www.awkwardzombie.com/event/')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(isinstance(result, bool))
            self.assertFalse(result)  

        # Site E
        try:
            result = robots_may_I(page_disposition, 'http://www.awkwardzombie.com/event/extinction/')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(isinstance(result, bool))
            self.assertFalse(result)  
            
        # Site F
        try:
            result = robots_may_I(page_disposition, 'http://www.awkwardzombie.com/comment/reply/')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(isinstance(result, bool))
            self.assertFalse(result)  
            
        # Site G
        try:
            result = robots_may_I(page_disposition, 'http://www.awkwardzombie.com/node/add/')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(isinstance(result, bool))
            self.assertFalse(result)   
            
        # Site H
        try:
            result = robots_may_I(page_disposition, 'http://www.awkwardzombie.com/popular/')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(isinstance(result, bool))
            self.assertFalse(result)   
            
        # Site I
        try:
            result = robots_may_I(page_disposition, 'http://www.awkwardzombie.com/popular/mechanics/')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(isinstance(result, bool))
            self.assertFalse(result)  
            
        # Site I
        try:
            result = robots_may_I(page_disposition, 'http://www.awkwardzombie.com/node/print/')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(isinstance(result, bool))
            self.assertFalse(result)  
            
        # Site I
        try:
            result = robots_may_I(page_disposition, 'http://www.awkwardzombie.com/node/to/print/')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(isinstance(result, bool))
            self.assertFalse(result)  
            
        # Site J
        try:
            result = robots_may_I(page_disposition, 'http://www.awkwardzombie.com/forum/index.php')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(isinstance(result, bool))
            self.assertFalse(result)  
            
        # Site K
        try:
            result = robots_may_I(page_disposition, 'http://www.awkwardzombie.com/index.php?page=0&comic=013017')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(isinstance(result, bool))
            self.assertFalse(result)  
            
        # Site L
        try:
            result = robots_may_I(page_disposition, 'http://www.awkwardzombie.com/tracker/jacker/')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(isinstance(result, bool))
            self.assertFalse(result)  
            
        # Site M
        try:
            result = robots_may_I(page_disposition, 'http://www.awkwardzombie.com')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(isinstance(result, bool))
            self.assertFalse(result)  
                                  
        # Site N
        try:
            result = robots_may_I(page_disposition, 'http://www.awkwardzombie.com/I/made/up/this/path.html')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue(isinstance(result, bool))
            self.assertFalse(result)  


class RobotsMayI(unittest.TestCase):
    
    # Test 1 - Invalid Input - TypeError('Page disposition is not a dictionary')
    def test01_InvalidInput01(self):
        try:
            result = robots_may_I(['www.nunya.bz', False], 'www.nunya.bz/get/outta/my.html')
        except TypeError as err:
            self.assertEqual(err.args[0], 'Page disposition is not a dictionary')
        except Exception as err:
            print(repr(err))
            self.fail('Raised the wrong exception')            
    
    # Test 2 - Invalid Input - ValueError('Page disposition is empty')
    def test02_InvalidInput02(self):
        try:
            result = robots_may_I({}, 'www.nunya.bz/get/outta/my.html')
        except ValueError as err:
            self.assertEqual(err.args[0], 'Page disposition is empty')
        except Exception as err:
            print(repr(err))
            self.fail('Raised the wrong exception')   
    
    # Test 3 - Invalid Input - ValueError('Page disposition contains a non-boolean value')
    def test03_InvalidInput03(self):
        try:
            result = robots_may_I({'www.nunya.bz/get/outta':True, 'www.nunya.bz':'Buzz off'}, 'www.nunya.bz/get/outta/my.html')
        except ValueError as err:
            self.assertEqual(err.args[0], 'Page disposition contains a non-boolean value')
        except Exception as err:
            print(repr(err))
            self.fail('Raised the wrong exception')   
    
    # Test 4 - Invalid Input - TypeError('URL is not a string')
    def test04_InvalidInput04(self):
        try:
            result = robots_may_I({'www.nunya.bz/get/outta':False, 'www.nunya.bz':True}, ['www', 'nunya', 'bz'])
        except TypeError as err:
            self.assertEqual(err.args[0], 'URL is not a string')
        except Exception as err:
            print(repr(err))
            self.fail('Raised the wrong exception')   
    
    # Test 5 - Invalid Input - ValueError('URL is empty')
    def test05_InvalidInput05(self):
        try:
            result = robots_may_I({'www.nunya.bz/get/outta':False, 'www.nunya.bz':True}, '')
        except ValueError as err:
            self.assertEqual(err.args[0], 'URL is empty')
        except Exception as err:
            print(repr(err))
            self.fail('Raised the wrong exception')   
    
    # Test 6 - Invalid Input - ValueError('URL is not a URL')
    def test06_InvalidInput06(self):
        try:
            result = robots_may_I({'www.nunya.bz/get/outta':False, 'www.nunya.bz':True}, 'This is still *DEFINITELY* not a valid URL!')
        except ValueError as err:
            self.assertEqual(err.args[0], 'URL is not a URL')
        except Exception as err:
            print(repr(err))
            self.fail('Raised the wrong exception')   
            
    # Test 7 - Valid Input (Manufactured)
    def test07_ValidInput01(self):
        page_disposition = {
            'https://www.github.com':True,
            'https://www.github.com/hark130':False,
            'https://www.github.com/hark130/Harklebot':True,
            'https://www.github.com/hark130/Harklebot/tree':False
        }
        
        try:
            result = robots_may_I(page_disposition, 'https://www.github.com')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertEqual(result, True)
            
    # Test 8 - Valid Input (Manufactured)
    def test08_ValidInput02(self):
        page_disposition = {
            'https://www.github.com':True,
            'https://www.github.com/hark130':False,
            'https://www.github.com/hark130/Harklebot':True,
            'https://www.github.com/hark130/Harklebot/tree':False
        }
        
        try:
            result = robots_may_I(page_disposition, 'https://www.github.com/hark130')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertEqual(result, False)
            
    # Test 9 - Valid Input (Manufactured)
    def test09_ValidInput03(self):
        page_disposition = {
            'https://www.github.com':True,
            'https://www.github.com/hark130':False,
            'https://www.github.com/hark130/Harklebot':True,
            'https://www.github.com/hark130/Harklebot/tree':False
        }
        
        try:
            result = robots_may_I(page_disposition, 'https://www.github.com/hark130/Harklebot')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertEqual(result, True)
            
    # Test 10 - Valid Input (Manufactured)
    def test10_ValidInput04(self):
        page_disposition = {
            'https://www.github.com':True,
            'https://www.github.com/hark130':False,
            'https://www.github.com/hark130/Harklebot':True,
            'https://www.github.com/hark130/Harklebot/tree':False
        }
        
        try:
            result = robots_may_I(page_disposition, 'https://www.github.com/hark130/Harklebot/tree')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertEqual(result, False)
            
    # Test 11 - Valid Input (Manufactured)
    def test11_ValidInput05(self):
        page_disposition = {
            'https://www.github.com':True,
            'https://www.github.com/hark130':False,
            'https://www.github.com/hark130/Harklebot':True,
            'https://www.github.com/hark130/Harklebot/tree':False
        }
        
        try:
            result = robots_may_I(page_disposition, 'https://www.github.com/hark130/Harklebot/tree/master')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertEqual(result, False)
            
    # Test 12 - Valid Input (Manufactured)
    def test12_ValidInput06(self):
        page_disposition = {
            'https://www.github.com':True,
            'https://www.github.com/hark130':False,
            'https://www.github.com/hark130/Harklebot':True,
            'https://www.github.com/hark130/Harklebot/tree':False
        }
        
        try:
            result = robots_may_I(page_disposition, 'https://www.github.com/hark130/Harklebot/blob/master/Logo/Harklebot%20v2.png')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertEqual(result, True)
        
    # Test 13 - Valid Input (Manufactured)
    def test13_ValidInput07(self):
        page_disposition = {
            'https://www.github.com':True,
            'https://www.github.com/hark130':False,
            'https://www.github.com/hark130/Harklebot':True,
            'https://www.github.com/hark130/Harklebot/tree':False
        }
        
        try:
            result = robots_may_I(page_disposition, 'https://github.com')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertEqual(result, True)
            
    # Test 14 - Valid Input (Manufactured)
    def test14_ValidInput08(self):
        page_disposition = {
            'https://www.github.com':True,
            'https://www.github.com/hark130':False,
            'https://www.github.com/hark130/Harklebot':True,
            'https://www.github.com/hark130/Harklebot/tree':False
        }
        
        try:
            result = robots_may_I(page_disposition, 'https://github.com/hark130')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertEqual(result, True)
            
    # Test 15 - Valid Input (Manufactured)
    def test15_ValidInput09(self):
        page_disposition = {
            'https://www.github.com':True,
            'https://www.github.com/hark130':False,
            'https://www.github.com/hark130/Harklebot':True,
            'https://www.github.com/hark130/Harklebot/tree':False
        }
        
        try:
            result = robots_may_I(page_disposition, 'https://github.com/hark130/Harklebot')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertEqual(result, True)
            
    # Test 16 - Valid Input (Manufactured)
    def test16_ValidInput10(self):
        page_disposition = {
            'https://www.github.com':True,
            'https://www.github.com/hark130':False,
            'https://www.github.com/hark130/Harklebot':True,
            'https://www.github.com/hark130/Harklebot/tree':False
        }
        
        try:
            result = robots_may_I(page_disposition, 'https://github.com/hark130/Harklebot/tree')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertEqual(result, True)
            
    # Test 17 - Valid Input (Manufactured)
    def test17_ValidInput11(self):
        page_disposition = {
            'https://www.github.com':True,
            'https://www.github.com/hark130':False,
            'https://www.github.com/hark130/Harklebot':True,
            'https://www.github.com/hark130/Harklebot/tree':False
        }
        
        try:
            result = robots_may_I(page_disposition, 'https://github.com/hark130/Harklebot/tree/master')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertEqual(result, True)
            
    # Test 18 - Valid Input (Manufactured)
    def test18_ValidInput12(self):
        page_disposition = {
            'https://www.github.com':True,
            'https://www.github.com/hark130':False,
            'https://www.github.com/hark130/Harklebot':True,
            'https://www.github.com/hark130/Harklebot/tree':False
        }
        
        try:
            result = robots_may_I(page_disposition, 'https://github.com/hark130/Harklebot/blob/master/Logo/Harklebot%20v2.png')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertEqual(result, True)


class GetPageDisposition(unittest.TestCase):

    def test01_URL_not_a_string(self):
        try:
            get_page_disposition(3.14, 'Harklebot')
        except TypeError as err:
            self.assertEqual(err.args[0], 'URL is not a string')
        except Exception as err:
            print(repr(err))
            self.fail('Raised the wrong exception')

    def test02_user_agent_not_a_string_or_list(self):
        try:
            get_page_disposition('www.google.com', 42)
        except TypeError as err:
            self.assertEqual(err.args[0], 'User Agent is not a string or a list')
        except Exception as err:
            print(repr(err))
            self.fail('Raised the wrong exception')
            
    def test03_user_agent_list_contains_non_string(self):
        try:
            get_page_disposition('www.google.com', ['me', 'you', 22])
        except TypeError as err:
            self.assertEqual(err.args[0], 'Found a User Agent that is not string:\t22')
        except Exception as err:
            print(repr(err))
            self.fail('Raised the wrong exception')

    # Ctrl-Alt-Del: Standard, well-formed input
    def test04_cad_comic1(self):
        try:
            page_disposition = get_page_disposition('http://www.cad-comic.com', ['Mozilla/5.0'])
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertEqual(page_disposition, {'/':False})

    # Ctrl-Alt-Del: User agent is string, not a list of strings (still valid, merely misformed)
    def test05_cad_comic2(self):
        try:
            page_disposition = get_page_disposition('http://www.cad-comic.com', 'Mozilla/5.0')
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertEqual(page_disposition, {'/':False})

    # Ctrl-Alt-Del: User agent is a list of valid strings
    def test06_cad_comic3(self):
        try:
            page_disposition = get_page_disposition('http://www.cad-comic.com', ['Mozilla/5.0', 'Python-urllib/3.5'])
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertEqual(page_disposition, {'/':False})

    # Saturday Morning Breakfast Cereal: Standard, well-formed input
    def test07_smbc_comic1(self):
        self.assertEqual(get_page_disposition('http://www.smbc-comics.com/comic/2011-07-23', ['Mozilla/5.0']),
                         {'http://www.smbc-comics.com':True})

    # Saturday Morning Breakfast Cereal: User agent is string, not a list of strings (still valid, merely misformed)
    def test08_smbc_comic2(self):
        self.assertEqual(get_page_disposition('http://www.smbc-comics.com/comic/2011-07-23', 'Mozilla/5.0'),
                         {'http://www.smbc-comics.com':True})

    # Saturday Morning Breakfast Cereal: User agent is a list of valid strings
    def test09_smbc_comic3(self):
        self.assertEqual(get_page_disposition('http://www.smbc-comics.com/comic/2011-07-23', ['Mozilla/5.0', 'Python-urllib/3.5']),
                         {'http://www.smbc-comics.com':True})

    # XKCD: Standard, normal URL that can't be used to download the robots.txt file
    #       xkcd.com/433/ is valid and will show you a website but...
    #       urlopen(xkcd.com/robots.txt) will fail
    def test10_xkcd_comic1(self):
        try:    
            get_page_disposition('xkcd.com/433/', 'Mozilla/5.0')
        except ValueError as err:
            self.assertTrue(err.args[0].lower().find("unknown url type") >= 0)
        except Exception as err:
            print(repr(err))
            self.fail('Raised the wrong exception')

    # XKCD: User agent is string, not a list of strings (still valid, merely misformed)
    def test11_xkcd_comic2(self):
        self.assertEqual(get_page_disposition('http://www.xkcd.com/', ['Mozilla/5.0']),{'http://www.xkcd.com/personal':False})

    # XKCD: User agent is a list of valid strings
    def test12_xkcd_comic3(self):
        self.assertEqual(get_page_disposition('http://xkcd.com/1/', ['Mozilla/5.0', 'Python-urllib/3.5']),{'http://xkcd.com/personal':False})

    # Penny Arcade: Standard, well-formed input
    def test13_pa_comic1(self):
        results = get_page_disposition('https://www.penny-arcade.com/news/post/2017/01/04/vitreous-humor', ['Mozilla/5.0'])
        self.assertEqual(results['https://www.penny-arcade.com/feed'], False)
        self.assertEqual(results['https://www.penny-arcade.com/feed/podcasts-'], False)
        self.assertEqual(results['https://www.penny-arcade.com/feed/show-'], False)
        self.assertEqual(results['https://www.penny-arcade.com/feed/podcasts'], True)
        self.assertEqual(results['https://www.penny-arcade.com/feed/show'], True)

    # Penny Arcade: User agent is string, not a list of strings (still valid, merely misformed)
    def test14_pa_comic2(self):
        results = get_page_disposition('https://www.penny-arcade.com/patv/episode/cloudsourcing', 'Mozilla/5.0')
        self.assertEqual(results['https://www.penny-arcade.com/feed'], False)
        self.assertEqual(results['https://www.penny-arcade.com/feed/podcasts-'], False)
        self.assertEqual(results['https://www.penny-arcade.com/feed/show-'], False)
        self.assertEqual(results['https://www.penny-arcade.com/feed/podcasts'], True)
        self.assertEqual(results['https://www.penny-arcade.com/feed/show'], True)        

    # Penny Arcade: User agent is a list of valid strings
    def test15_pa_comic3(self):
        results = get_page_disposition('https://www.penny-arcade.com/comic/hub', ['Mozilla/5.0', 'Python-urllib/3.5'])
        self.assertEqual(results['https://www.penny-arcade.com/feed'], False)
        self.assertEqual(results['https://www.penny-arcade.com/feed/podcasts-'], False)
        self.assertEqual(results['https://www.penny-arcade.com/feed/show-'], False)
        self.assertEqual(results['https://www.penny-arcade.com/feed/podcasts'], True)
        self.assertEqual(results['https://www.penny-arcade.com/feed/show'], True)    

    # Player vs Player: Standard, well-formed input
    def test16_pvp_comic1(self):
        results = get_page_disposition('http://pvponline.com/comic/comic/you-are-cordially-invited', ['Mozilla/5.0'])
        self.assertEqual(results['http://pvponline.com'], False)

    # Player vs Player: User agent is string, not a list of strings (still valid, merely misformed)
    def test17_pvp_comic2(self):
        results = get_page_disposition('http://pvponline.com/comic/comic/you-are-cordially-invited', 'Mozilla/5.0')
        self.assertEqual(results['http://pvponline.com'], False)      

    # Player vs Player: User agent is a list of valid strings
    def test18_pvp_comic3(self):
        results = get_page_disposition('http://pvponline.com/comic/comic/you-are-cordially-invited', ['Mozilla/5.0', 'Python-urllib/3.5'])
        self.assertEqual(results['http://pvponline.com'], False) 

    # Player vs Player: User agent list is testing g_p_d()'s ability to read and process multiple applicable user-agents
    def test19_pvp_comic3(self):
        results = get_page_disposition('http://pvponline.com/comic/comic/you-are-cordially-invited', ['Mozilla/5.0', 'Python-urllib/3.5', 'Mediapartners-Google'])
        self.assertEqual(results['http://pvponline.com'], True) 

    # Giant in the Playground: Standard, well-formed input but odd user agent
    def test20_gitp_comic1(self):
        results = get_page_disposition('http://www.giantitp.com/index.html#MikB0bMhsuBgvawPHag', ['Harklebot'])
        self.assertEqual(results['http://www.giantitp.com/forums/admincp'], False)
        self.assertEqual(results['http://www.giantitp.com/forums/clientscript'], False)
        self.assertEqual(results['http://www.giantitp.com/forums/cpstyles'], False)
        self.assertEqual(results['http://www.giantitp.com/forums/customavatars'], False)
        self.assertEqual(results['http://www.giantitp.com/forums/customprofilepics'], False)
        self.assertEqual(results['http://www.giantitp.com/forums/modcp'], False)
        self.assertEqual(results['http://www.giantitp.com/forums/ajax.php'], False)
        self.assertEqual(results['http://www.giantitp.com/forums/attachment.php'], False)
        self.assertEqual(results['http://www.giantitp.com/forums/calendar.php'], False)
        self.assertEqual(results['http://www.giantitp.com/forums/cron.php'], False)
        self.assertEqual(results['http://www.giantitp.com/forums/editpost.php'], False)
        self.assertEqual(results['http://www.giantitp.com/forums/global.php'], False)
        self.assertEqual(results['http://www.giantitp.com/forums/image.php'], False)
        self.assertEqual(results['http://www.giantitp.com/forums/inlinemod.php'], False)
        self.assertEqual(results['http://www.giantitp.com/forums/joinrequests.php'], False)
        self.assertEqual(results['http://www.giantitp.com/forums/login.php'], False)
        self.assertEqual(results['http://www.giantitp.com/forums/member.php'], False)
        self.assertEqual(results['http://www.giantitp.com/forums/memberlist.php'], False)
        self.assertEqual(results['http://www.giantitp.com/forums/misc.php'], False)
        self.assertEqual(results['http://www.giantitp.com/forums/moderator.php'], False)
        self.assertEqual(results['http://www.giantitp.com/forums/newattachment.php'], False)
        self.assertEqual(results['http://www.giantitp.com/forums/newreply.php'], False)
        self.assertEqual(results['http://www.giantitp.com/forums/newthread.php'], False)
        self.assertEqual(results['http://www.giantitp.com/forums/online.php'], False)
        self.assertEqual(results['http://www.giantitp.com/forums/poll.php'], False)
        self.assertEqual(results['http://www.giantitp.com/forums/postings.php'], False)
        self.assertEqual(results['http://www.giantitp.com/forums/printthread.php'], False)
        self.assertEqual(results['http://www.giantitp.com/forums/private.php'], False)
        self.assertEqual(results['http://www.giantitp.com/forums/profile.php'], False)
        self.assertEqual(results['http://www.giantitp.com/forums/register.php'], False)
        self.assertEqual(results['http://www.giantitp.com/forums/report.php'], False)
        self.assertEqual(results['http://www.giantitp.com/forums/reputation.php'], False)
        self.assertEqual(results['http://www.giantitp.com/forums/search.php'], False)
        self.assertEqual(results['http://www.giantitp.com/forums/sendmessage.php'], False)
        self.assertEqual(results['http://www.giantitp.com/forums/showgroups.php'], False)
        self.assertEqual(results['http://www.giantitp.com/forums/subscription.php'], False)
        self.assertEqual(results['http://www.giantitp.com/forums/threadrate.php'], False)
        self.assertEqual(results['http://www.giantitp.com/forums/usercp.php'], False)
        self.assertEqual(results['http://www.giantitp.com/forums/usernote.php'], False)

    # Awkward Zombie: Standard, well-formed input but odd user agent
    def test21_az_comic1(self):
        results = get_page_disposition('http://awkwardzombie.com/index.php?page=0&comic=092616', ['Harklebot'])
        # User Agent: *
        self.assertEqual(results['http://awkwardzombie.com/aggregator'], False)
        self.assertEqual(results['http://awkwardzombie.com/tracker'], False)
        self.assertEqual(results['http://awkwardzombie.com/archive'], False)
        self.assertEqual(results['http://awkwardzombie.com/archive'], False)
        self.assertEqual(results['http://awkwardzombie.com/event'], False)
        self.assertEqual(results['http://awkwardzombie.com/event'], False)
        self.assertEqual(results['http://awkwardzombie.com/comment/reply'], False)
        self.assertEqual(results['http://awkwardzombie.com/node/add'], False)
        self.assertEqual(results['http://awkwardzombie.com/user'], False)
        self.assertEqual(results['http://awkwardzombie.com/files'], False)
        self.assertEqual(results['http://awkwardzombie.com/popular'], False)
        self.assertEqual(results['http://awkwardzombie.com/popular'], False)
        self.assertEqual(results['http://awkwardzombie.com/xtracker'], False)
        self.assertEqual(results['http://awkwardzombie.com/search'], False)
        self.assertEqual(results['http://awkwardzombie.com/book/print'], False)
        self.assertEqual(results['http://awkwardzombie.com/forward'], False)
        self.assertEqual(results['http://awkwardzombie.com/taxonomy'], False)
#        self.assertEqual(results['http://awkwardzombie.com/node/*/print'], False)
        self.assertEqual(results['http://awkwardzombie.com/node/print'], False)
        self.assertEqual(results['http://awkwardzombie.com/node'], False)
        self.assertEqual(results['http://awkwardzombie.com/blog'], False)
        self.assertEqual(results['http://awkwardzombie.com/archive'], False)
        self.assertEqual(results['http://awkwardzombie.com/print'], False)
        self.assertEqual(results['http://awkwardzombie.com/taxonomy'], False)

    # Awkward Zombie: Standard, well-formed input but odd user agent
    def test22_az_comic2(self):
        results = get_page_disposition('http://awkwardzombie.com/index.php?page=0&comic=092616', ['Googlebot'])
        # User Agent: *
        self.assertEqual(results['http://awkwardzombie.com/aggregator'], False)
        self.assertEqual(results['http://awkwardzombie.com/tracker'], False)
        self.assertEqual(results['http://awkwardzombie.com/archive'], False)
        self.assertEqual(results['http://awkwardzombie.com/archive'], False)
        self.assertEqual(results['http://awkwardzombie.com/event'], False)
        self.assertEqual(results['http://awkwardzombie.com/event'], False)
        self.assertEqual(results['http://awkwardzombie.com/comment/reply'], False)
        self.assertEqual(results['http://awkwardzombie.com/node/add'], False)
        self.assertEqual(results['http://awkwardzombie.com/user'], False)
        self.assertEqual(results['http://awkwardzombie.com/files'], False)
        self.assertEqual(results['http://awkwardzombie.com/popular'], False)
        self.assertEqual(results['http://awkwardzombie.com/popular'], False)
        self.assertEqual(results['http://awkwardzombie.com/xtracker'], False)
        self.assertEqual(results['http://awkwardzombie.com/search'], False)
        self.assertEqual(results['http://awkwardzombie.com/book/print'], False)
        self.assertEqual(results['http://awkwardzombie.com/forward'], False)
        self.assertEqual(results['http://awkwardzombie.com/taxonomy'], False)
#        self.assertEqual(results['http://awkwardzombie.com/node/*/print'], False)
        self.assertEqual(results['http://awkwardzombie.com/node/print'], False)
        self.assertEqual(results['http://awkwardzombie.com/node'], False)
        self.assertEqual(results['http://awkwardzombie.com/blog'], False)
        self.assertEqual(results['http://awkwardzombie.com/archive'], False)
        self.assertEqual(results['http://awkwardzombie.com/print'], False)
        self.assertEqual(results['http://awkwardzombie.com/taxonomy'], False)

        # User Agent: Googlebot
        self.assertEqual(results['http://awkwardzombie.com/aggregator'], False)
        self.assertEqual(results['http://awkwardzombie.com/archive'], False)
        self.assertEqual(results['http://awkwardzombie.com/archive'], False)
        self.assertEqual(results['http://awkwardzombie.com/author'], False)
        self.assertEqual(results['http://awkwardzombie.com/event'], False)
        self.assertEqual(results['http://awkwardzombie.com/event'], False)
        self.assertEqual(results['http://awkwardzombie.com/event'], False)
        self.assertEqual(results['http://awkwardzombie.com/tracker'], False)
        self.assertEqual(results['http://awkwardzombie.com/comment/reply'], False)
        self.assertEqual(results['http://awkwardzombie.com/node/add'], False)
        self.assertEqual(results['http://awkwardzombie.com/user'], False)
        self.assertEqual(results['http://awkwardzombie.com/user'], False)
        self.assertEqual(results['http://awkwardzombie.com/files'], False)
        self.assertEqual(results['http://awkwardzombie.com/popular'], False)
        self.assertEqual(results['http://awkwardzombie.com/popular'], False)
        self.assertEqual(results['http://awkwardzombie.com/xtracker'], False)
        self.assertEqual(results['http://awkwardzombie.com/xtracker'], False)
        self.assertEqual(results['http://awkwardzombie.com/search'], False)
        self.assertEqual(results['http://awkwardzombie.com/book/print'], False)
        self.assertEqual(results['http://awkwardzombie.com/forward'], False)
        self.assertEqual(results['http://awkwardzombie.com/taxonomy'], False)
#        self.assertEqual(results['http://awkwardzombie.com/node/*/print'], False)
        self.assertEqual(results['http://awkwardzombie.com/node/print'], False)
        self.assertEqual(results['http://awkwardzombie.com/node'], False)
        self.assertEqual(results['http://awkwardzombie.com/blog'], False)
        self.assertEqual(results['http://awkwardzombie.com/archive'], False)
        self.assertEqual(results['http://awkwardzombie.com/print'], False)
        self.assertEqual(results['http://awkwardzombie.com/topic'], False)

    # Awkward Zombie: Standard, well-formed input with a Python user agent
    def test23_az_comic3(self):
        # Python's user agent will fail on the urlopen since awkward zombie blocks all contact from Python, image download or otherwises
        try:
            results = get_page_disposition('http://awkwardzombie.com/index.php?page=0&comic=092616')
        except HTTPError as err:
#            print(repr(err)) # DEBUGGING
            self.assertEqual(err.code, 403) # Awkward Zombie Disallows Python-urllib User Agents
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.fail('Should have raised an HTTPError 403 exception')

    # Awkward Zombie: Standard, well-formed input with a Mozilla and a Python user agent
    def test24_az_comic4(self):
        # Python's user agent will fail on the urlopen since awkward zombie blocks all contact from Python, image download or otherwises
        try:
            results = get_page_disposition('http://awkwardzombie.com/index.php?page=0&comic=092616', ['Mozilla/6.9','Python-urllib'])
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue('/' in results.keys())
            self.assertEqual(results['/'], False) 

    # Awkward Zombie: Standard, well-formed input with a modern Mozilla user agent
    def test25_az_comic5(self):
        # Python's user agent will fail on the urlopen since awkward zombie blocks all contact from Python, image download or otherwises
        try:
            results = get_page_disposition('http://awkwardzombie.com/index.php?page=0&comic=092616', ['Mozilla/6.9'])
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertFalse('/' in results.keys())
            self.assertTrue('Crawl-delay:' in results.keys())
            self.assertTrue(isinstance(results['Crawl-delay:'], int)) 
            self.assertEqual(results['Crawl-delay:'], 30) 

    # Awkward Zombie: Standard, well-formed input with an old(?) Mozilla user agent
    def test26_az_comic6(self):
        # Python's user agent will fail on the urlopen since awkward zombie blocks all contact from Python, image download or otherwises
        try:
            results = get_page_disposition('http://awkwardzombie.com/index.php?page=0&comic=092616', ['mozilla'])
        except Exception as err:
            print(repr(err))
            self.fail('Raised an exception')
        else:
            self.assertTrue('/' in results.keys())
            self.assertEqual(results['/'], False)
            self.assertTrue('Crawl-delay:' in results.keys())
            self.assertTrue(isinstance(results['Crawl-delay:'], int)) 
            self.assertEqual(results['Crawl-delay:'], 30) 


if __name__ == '__main__':

    # Run all the tests!
    unittest.main(verbosity=2, exit=False)

## CrawlDelayCombinedTest
#    linkerSuite = unittest.TestLoader().loadTestsFromTestCase(CrawlDelayCombinedTest)
#    unittest.TextTestRunner(verbosity=2).run(linkerSuite)

## RobotsMayI
#    linkerSuite = unittest.TestLoader().loadTestsFromTestCase(RobotsMayI)
#    unittest.TextTestRunner(verbosity=2).run(linkerSuite)
    
## GetPageDisposition
#    linkerSuite = unittest.TestLoader().loadTestsFromTestCase(GetPageDisposition)
#    unittest.TextTestRunner(verbosity=2).run(linkerSuite)

    print('Done testing')
