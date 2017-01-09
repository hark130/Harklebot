import unittest
import Robot_Functions_v1

class GetPageDisposition(unittest.TestCase):

    def test_URL_not_a_string(self):
        try:
            Robot_Functions_v1.get_page_disposition(3.14, 'Harklebot')
        except TypeError as err:
            self.assertEqual(err.args[0], 'URL is not a string')
        except Exception as err:
            print(repr(err))
            self.fail('Raised the wrong exception')

    def test_user_agent_not_a_string_or_list(self):
        try:
            Robot_Functions_v1.get_page_disposition('www.google.com', 42)
        except TypeError as err:
            self.assertEqual(err.args[0], 'User Agent is not a string or a list')
        except Exception as err:
            print(repr(err))
            self.fail('Raised the wrong exception')
            
    def test_user_agent_list_contains_non_string(self):
        try:
            Robot_Functions_v1.get_page_disposition('www.google.com', ['me', 'you', 22])
        except TypeError as err:
            self.assertEqual(err.args[0], 'Found a User Agent that is not string:\t22')
        except Exception as err:
            print(repr(err))
            self.fail('Raised the wrong exception')

    # Ctrl-Alt-Del: Standard, well-formed input
    def test_cac_comic1(self):
        self.assertEqual(Robot_Functions_v1.get_page_disposition('http://www.cad-comic.com', ['Mozilla/5.0']),{'http://www.cad-comic.com':False})

    # Ctrl-Alt-Del: User agent is string, not a list of strings (still valid, merely misformed)
    def test_cac_comic2(self):
        self.assertEqual(Robot_Functions_v1.get_page_disposition('http://www.cad-comic.com', 'Mozilla/5.0'),{'http://www.cad-comic.com':False})

    # Ctrl-Alt-Del: User agent is a list of valid strings
    def test_cac_comic3(self):
        self.assertEqual(Robot_Functions_v1.get_page_disposition('http://www.cad-comic.com', ['Mozilla/5.0', 'Python-urllib/3.5']),{'http://www.cad-comic.com':False})

    # Saturday Morning Breakfast Cereal: Standard, well-formed input
    def test_smbc_comic1(self):
        self.assertEqual(Robot_Functions_v1.get_page_disposition('http://www.smbc-comics.com/comic/2011-07-23', ['Mozilla/5.0']),{'http://www.smbc-comics.com':True})

    # Saturday Morning Breakfast Cereal: User agent is string, not a list of strings (still valid, merely misformed)
    def test_smbc_comic2(self):
        self.assertEqual(Robot_Functions_v1.get_page_disposition('http://www.smbc-comics.com/comic/2011-07-23', 'Mozilla/5.0'),{'http://www.smbc-comics.com':True})

    # Saturday Morning Breakfast Cereal: User agent is a list of valid strings
    def test_smbc_comic3(self):
        self.assertEqual(Robot_Functions_v1.get_page_disposition('http://www.smbc-comics.com/comic/2011-07-23', ['Mozilla/5.0', 'Python-urllib/3.5']),{'http://www.smbc-comics.com':True})

    # XKCD: Standard, normal URL that can't be used to download the robots.txt file
    #       xkcd.com/433/ is valid and will show you a website but...
    #       urlopen(xkcd.com/robots.txt) will fail
    def test_xkcd_comic1(self):
        try:    
            Robot_Functions_v1.get_page_disposition('xkcd.com/433/', 'Mozilla/5.0')
        except ValueError as err:
            self.assertTrue(err.args[0].lower().find("unknown url type") >= 0)
        except Exception as err:
            print(repr(err))
            self.fail('Raised the wrong exception')

    # XKCD: User agent is string, not a list of strings (still valid, merely misformed)
    def test_xkcd_comic2(self):
        self.assertEqual(Robot_Functions_v1.get_page_disposition('http://www.xkcd.com/', ['Mozilla/5.0']),{'http://www.xkcd.com/personal':False})

    # XKCD: User agent is a list of valid strings
    def test_xkcd_comic3(self):
        self.assertEqual(Robot_Functions_v1.get_page_disposition('http://xkcd.com/1/', ['Mozilla/5.0', 'Python-urllib/3.5']),{'http://xkcd.com/personal':False})

    # Penny Arcade: Standard, well-formed input
    def test_pa_comic1(self):
        results = Robot_Functions_v1.get_page_disposition('https://www.penny-arcade.com/news/post/2017/01/04/vitreous-humor', ['Mozilla/5.0'])
        self.assertEqual(results['https://www.penny-arcade.com/feed'], False)
        self.assertEqual(results['https://www.penny-arcade.com/feed/podcasts-'], False)
        self.assertEqual(results['https://www.penny-arcade.com/feed/show-'], False)
        self.assertEqual(results['https://www.penny-arcade.com/feed/podcasts'], True)
        self.assertEqual(results['https://www.penny-arcade.com/feed/show'], True)

    # Penny Arcade: User agent is string, not a list of strings (still valid, merely misformed)
    def test_pa_comic2(self):
        results = Robot_Functions_v1.get_page_disposition('https://www.penny-arcade.com/patv/episode/cloudsourcing', 'Mozilla/5.0')
        self.assertEqual(results['https://www.penny-arcade.com/feed'], False)
        self.assertEqual(results['https://www.penny-arcade.com/feed/podcasts-'], False)
        self.assertEqual(results['https://www.penny-arcade.com/feed/show-'], False)
        self.assertEqual(results['https://www.penny-arcade.com/feed/podcasts'], True)
        self.assertEqual(results['https://www.penny-arcade.com/feed/show'], True)        

    # Penny Arcade: User agent is a list of valid strings
    def test_pa_comic3(self):
        results = Robot_Functions_v1.get_page_disposition('https://www.penny-arcade.com/comic/hub', ['Mozilla/5.0', 'Python-urllib/3.5'])
        self.assertEqual(results['https://www.penny-arcade.com/feed'], False)
        self.assertEqual(results['https://www.penny-arcade.com/feed/podcasts-'], False)
        self.assertEqual(results['https://www.penny-arcade.com/feed/show-'], False)
        self.assertEqual(results['https://www.penny-arcade.com/feed/podcasts'], True)
        self.assertEqual(results['https://www.penny-arcade.com/feed/show'], True)    

    # Player vs Player: Standard, well-formed input
    def test_pvp_comic1(self):
        results = Robot_Functions_v1.get_page_disposition('http://pvponline.com/comic/comic/you-are-cordially-invited', ['Mozilla/5.0'])
        self.assertEqual(results['http://pvponline.com'], False)

    # Player vs Player: User agent is string, not a list of strings (still valid, merely misformed)
    def test_pvp_comic2(self):
        results = Robot_Functions_v1.get_page_disposition('http://pvponline.com/comic/comic/you-are-cordially-invited', 'Mozilla/5.0')
        self.assertEqual(results['http://pvponline.com'], False)      

    # Player vs Player: User agent is a list of valid strings
    def test_pvp_comic3(self):
        results = Robot_Functions_v1.get_page_disposition('http://pvponline.com/comic/comic/you-are-cordially-invited', ['Mozilla/5.0', 'Python-urllib/3.5'])
        self.assertEqual(results['http://pvponline.com'], False) 

    # Player vs Player: User agent list is testing g_p_d()'s ability to read and process multiple applicable user-agents
    def test_pvp_comic3(self):
        results = Robot_Functions_v1.get_page_disposition('http://pvponline.com/comic/comic/you-are-cordially-invited', ['Mozilla/5.0', 'Python-urllib/3.5', 'Mediapartners-Google'])
        self.assertEqual(results['http://pvponline.com'], True) 

    # Giant in the Playground: Standard, well-formed input but odd user agent
    def test_gitp_comic1(self):
        results = Robot_Functions_v1.get_page_disposition('http://www.giantitp.com/index.html#MikB0bMhsuBgvawPHag', ['Harklebot'])
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
    def test_az_comic1(self):
        results = Robot_Functions_v1.get_page_disposition('http://awkwardzombie.com/index.php?page=0&comic=092616', ['Harklebot'])
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
    def test_az_comic2(self):
        results = Robot_Functions_v1.get_page_disposition('http://awkwardzombie.com/index.php?page=0&comic=092616', ['Googlebot'])
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
    def test_az_comic3(self):
        # Python's user agent will fail on the urlopen since awkward zombie blocks all contact from Python, image download or otherwises
        results = Robot_Functions_v1.get_page_disposition('http://awkwardzombie.com/index.php?page=0&comic=092616', ['Mozilla/6.9','Python-urllib/3.5'])
        self.assertEqual(results['http://awkwardzombie.com'], False) 

########################## WRITE MORE TESTS FOR AWKWARD ZOMBIE FROM OTHER USER AGENTS ######################################

class GetRootURL(unittest.TestCase):

    def test_URL_not_a_string(self):
        try:
            Robot_Functions_v1.get_root_URL(69)
        except TypeError as err:
            self.assertEqual(err.args[0], 'URL is not a string')
        except Exception as err:
            print(repr(err))
            self.fail('Raised the wrong exception')

    def test_normal_URL1(self):
        self.assertEqual(Robot_Functions_v1.get_root_URL('https://www.google.com/?gws_rd=ssl'), 'https://www.google.com')

    def test_normal_URL2(self):
        self.assertEqual(Robot_Functions_v1.get_root_URL('https://www.tutorialspoint.com/python/string_find.htm'), 'https://www.tutorialspoint.com')

    def test_normal_URL3(self):
        self.assertEqual(Robot_Functions_v1.get_root_URL('http://stackoverflow.com/questions/674764/examples-for-string-find-in-python'), 'http://stackoverflow.com')

    def test_normal_URL4(self):
        self.assertEqual(Robot_Functions_v1.get_root_URL('https://docs.python.org/2/library/string.html'), 'https://docs.python.org')

    def test_normal_URL5(self):
        self.assertEqual(Robot_Functions_v1.get_root_URL('https://www.google.com/?gws_rd=ssl#q=weird+website+links'), 'https://www.google.com')

    def test_normal_URL6(self):
        self.assertEqual(Robot_Functions_v1.get_root_URL('awkwardzombie.com/index.php?page=0&comic=122616'), 'awkwardzombie.com')

    def test_normal_URL7(self):
        self.assertEqual(Robot_Functions_v1.get_root_URL('www.smbc-comics.com/comic/2007-11-09'), 'www.smbc-comics.com')

    def test_normal_URL8(self):
        self.assertEqual(Robot_Functions_v1.get_root_URL('https://www.google.com/#q=who+owns+.com+tld'), 'https://www.google.com')

    # This test is very important as it validates the requirement to remove any subdirectories before locating the end (see: TLD) of hte base URL
    def test_normal_URL8(self):
        self.assertEqual(Robot_Functions_v1.get_root_URL('http://www.blogsearchengine.org/search.html?cx=partner-pub-9634067433254658%3A5laonibews6&cof=FORID%3A10&ie=ISO-8859-1&q=who+owns+the+.com+tld&sa.x=0&sa.y=0'), 'http://www.blogsearchengine.org')

    def test_str_not_a_URL1(self):
        try:
            Robot_Functions_v1.get_root_URL('http : / / www . google . com')
        except ValueError as err:
            self.assertEqual(err.args[0], 'URL is not a URL')
        except Exception as err:
            print(repr(err))
            self.fail('Raised the wrong exception')

    # This test is valid merely because get_root_URL() does not include any country-unique TLDs (e.g., .cz, .ru)
    def test_str_not_a_URL2(self):
        try:
            Robot_Functions_v1.get_root_URL('http://www.praguemorning.cz/google-czech-republic/')
        except ValueError as err:
            self.assertEqual(err.args[0], 'URL is not a URL')
        except Exception as err:
            print(repr(err))
            self.fail('Raised the wrong exception')


if __name__ == '__main__':
    unittest.main()
    print('Done testing')



#class TestSomeException( unittest.TestCase ):
#    def testRaiseWithArgs( self ):
#        try:
#            ... Something that raises the exception ...
#            self.fail( "Didn't raise the exception" )
#        except UnrecognizedAirportError, e:
#            self.assertEquals( "func", e.args[0] )
#            self.assertEquals( "arg1", e.args[1] )
#        except Exception, e:
#            self.fail( "Raised the wrong exception" )