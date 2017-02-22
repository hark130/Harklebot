import sys
from urllib.request import urlopen
from urllib.request import Request
import urllib.error
import re
from Scraper_Functions import trim_a_URL
from Scraper_Functions import get_root_URL
from Scraper_Functions import get_URL_parent_path


'''
    Purpose: Read the parsed results of a page's robots.txt file and determine if a particular URL is permitted or not
    Input:
        page_disposition - A dictionary of URL 'answers' returned by get_page_disposition
        URL - The URL the user agent is asking to access
    Output:
        True if robots.txt permits
        False if robots.txt forbids
    Exceptions:
        TypeError('Page disposition is not a dictionary')
        ValueError('Page disposition is empty')
        ValueError('Page disposition contains a non-boolean value')
        TypeError('URL is not a string')
        ValueError('URL is empty')
        ValueError('URL is not a URL')
'''
def robots_may_I(page_disposition, URL):
    retVal = True
    
    # 1. INPUT VALIDATION
    ## 1.1. Page Disposition
    ### 1.1.1. Verify it's a dictionary
    if isinstance(page_disposition, dict) is False:
        raise TypeError('Page disposition is not a dictionary')
    ### 1.1.2. Verify it has content
    elif page_disposition.keys().__len__() == 0:
        raise ValueError('Page disposition is empty')
    ### 1.1.3. Verify it contains boolean keys
    else:
        for value in page_disposition.values():
            if isinstance(value, bool) is False:
                raise ValueError('Page disposition contains a non-boolean value')
                
    ## 1.2. URL
    ### 1.2.1. Verify URL is a string
    if isinstance(URL, str) is False:
        raise TypeError('URL is not a string')
    ### 1.2.2. Verify URL is not blank
    elif URL.__len__() == 0:
        raise ValueError('URL is empty')
    ### 1.2.3. Verify URL is valid
    elif is_URL_valid(URL) is False:
        raise ValueError('URL is not a URL')
    else:
        trimmedURL = trim_a_URL(URL)
        rootURL = get_root_URL(URL)
        
        
    
    
    
    
    
    return retVal


'''
    Purpose: Open a site's robots.txt file, parse it, and return a dictionary of URL:bool
    Input:
        baseURL - website to find a robots.txt file
        *userAgent - string or list of strings to utilize when parsing,
            the first of which will be used to download the robots.txt file
    Returns (examples):
        {'www.fullURL.com/comic':True, 'www.fullURL.com':False}            (White List)
        {'www.fullURL.com/forums':False, 'www.fullURL.com':True}           (Black List)
        {'www.fullURL.com/comic':True, 'www.fullURL.com/private/':False}   (Grey List)
        {'www.fullURL.com':False}                                          (Bad Robot List)
        {'www.fullURL.com':True}                                           (Good Robot List)     
    Exceptions:
        TypeError('URL is not a string')
        TypeError('User Agent is not a string or a list')
        TypeError('Found a User Agent that is not string:\t{}'.format(agent))
    NOTE:   
        This function merely prepares everything prior to dictionary creation
        Calls parse_robots_txt() to actually create the dictionary
        All trailing slashes (/) are removed (e.g., 'www.fullURL.com/comic' becomes 'www.fullURL.com/comic/'
'''
def get_page_disposition(baseURL, userAgent=['Python-urllib/3.5']):

    retVal = {}
    robotsFile = ''

    # Ordered list (most restrictive to least restrictive) of website beginnings
    SITE_DELIMITER_START = ['www.', '//', ':', 'https', 'http']
    # Unordered list of website TLDs
    SITE_DELIMITER_STOP = ['.com', '.org', '.net', '.int', '.edu', '.gov', '.mil', '.arpa']

    # 1. INPUT VALIDATION
    if isinstance(baseURL, str) is False:
        raise TypeError('URL is not a string')
    if isinstance(userAgent, str) is True:
        userAgent = [userAgent]
    elif isinstance(userAgent, list) is False:
        raise TypeError('User Agent is not a string or a list')

    for agent in userAgent:
        if isinstance(agent, str) is False:
            raise TypeError('Found a User Agent that is not string:\t{}'.format(agent))

    # 2. ADD A CATCH ALL USER AGENT
    if '*' not in userAgent:
        userAgent.append('*')
         
    # 3. TRIM THE URL
    try:
        trimmedURL = trim_a_URL(baseURL)
        trimmedURL = get_root_URL(trimmedURL)
    except Exception as err:
        print(repr(err))
#        sys.exit()
    else:
#        print("Original URL:\t{}\nTrimmed URL:\t{}".format(baseURL, trimmedURL)) # DEBUGGING
        pass

    # 4. GET THE ROBOTS.TXT FILE
    ## 4.1. Prepare download URL
    robotURL = trimmedURL + '/robots.txt'
    robotURL = robotURL.replace('//','/').replace(':/','://')

#    if robotURL.find('http') < 0 and robotURL.find('www') < 0:
##        robotURL = 'www.' + robotURL
#        robotURL = 'http://' + robotURL

    ## 4.2. Download the file
    try:
        robotRequest = Request(robotURL, headers={'User-Agent': userAgent[0]})
        with urlopen(robotRequest) as siteRobotFile:
            robotsFile = siteRobotFile.read().decode('UTF-8', 'ignore')
    except urllib.error.URLError as error:
        print("\nCannot open robots.txt URL:\t{}".format(robotURL))
        print("ERROR:\t{} - {}".format(type(error),error))
#        sys.exit()
    else:
#        print("\nOpened robots.txt from {}!".format(robotURL)) # DEBUGGING
        pass

    # 5. PARSE THE ROBOTS.TXT FILE
    if robotsFile.__len__() >= 0:
#        print(robotsFile) # DEBUGGING    
        retVal = parse_robots_txt(trimmedURL, robotsFile, userAgent)

    return retVal


'''
    Purpose: Parse a site's robot.txt file and return a dictionary of URL:bool
    Input:
        baseURL - website to find a robots.txt file
        robotsFile - raw robots.txt content as a string
        *userAgent - string or list of strings to utilize when parsing,
            the first of which will be used to download the robots.txt file
    Returns (examples):
        {'www.fullURL.com/comic/':True, 'www.fullURL.com':False}            (White List)
        {'www.fullURL.com/forums/':False, 'www.fullURL.com':True}           (Black List)
        {'www.fullURL.com/comic/':True, 'www.fullURL.com/private/':False}   (Grey List)
        {'www.fullURL.com':False}                                           (Bad Robot List)
        {'www.fullURL.com':True}                                            (Good Robot List)     
    Exceptions:
        TypeError('Robots file is not a string')
        TypeError('Base URL is not a string')
        TypeError('User Agent is not a string or a list')
        TypeError('Found a User Agent that is not string:\t{}'.format(agent))
    TO DO:
        Entries such as Awkward Zombie's 'Disallow: /node/*/print/' are not properly handled since
            all wildcards are removed.  Consider reintegrating wildcards into the algorithm. In
            the meantime, entries such as '/node/*/print/' are added as '/node/'
'''
def parse_robots_txt(baseURL, robotsFile, userAgent=['Python-urllib/3.5']):

    retVal = {}
    
    # 1. INPUT VALIDATION
    if isinstance(robotsFile, str) is False:
        raise TypeError('Robots file is not a string')
    elif isinstance(baseURL, str) is False:
        raise TypeError('Base URL is not a string')
    elif isinstance(userAgent, str) is True:
        userAgent = [userAgent]
    elif isinstance(userAgent, list) is False:
        raise TypeError('User Agent is not a string or a list')

    for agent in userAgent:
        if isinstance(agent, str) is False:
            raise TypeError('Found a User Agent that is not string:\t{}'.format(agent))

    # 2. ENSURE BASE URL IS CLEAN
    try:
        baseURL = trim_a_URL(baseURL)
    except Exception as err:
        print(repr(err))

    # 2. PARSE THE CONTENTS
    ## 2.1. Split the contents
#    robotsEntryList = robotsFile.split('\n') # By itself, this statement missed out on \r delimiters
    robotsEntryList = re.split('\r|\n', robotsFile)

    ## 2.2. Check for empty Robots.txt file
    if robotsFile == '':
        retVal.update({baseURL:True})
        return retVal

    ## 2.3. Check for each user agent
    ### readInstructions usage
    ###     False means continue searching for an applicable user-agent
    ###     True means start reading Allows and Disallows into the dictionary
    readInstructions = False
    instructionAction = False # Used to determine whether to make a False or True dictionary entry

#    print("robotsEntryList has {} entries".format(robotsEntryList.__len__())) # TESTING

    for entry in robotsEntryList:
        # Clean up entry (e.g., 'Disallow: ' vs. 'Disallow:')
        entry = entry.replace(' ','')
############################## REVERSE FIND ON ENTRY AND AGENT STILL INCLUDES GARBAGE (e.g., User-agent:) IN ENTRY AND WON'T REVERSE FIND
        if entry.find('User-agent:') >= 0:
            # Toggle readInstructions when another User-agent entry is found
            if readInstructions is True:
                readInstructions = False
            for agent in userAgent:
                if readInstructions is True:
                    break
                if entry.find(agent) >= 0 or agent.find(entry) >= 0:
                    readInstructions = True # Next entries will be read as Allows and Disallows
#                    print("Agent {} found in:\t{}".format(agent, entry)) # DEBUGGING
                    continue

        ## 2.4. Read instructions
        elif readInstructions is True and (entry.find('Disallow:') >= 0 or entry.find('Allow:') >= 0):
            ### 2.4.1. Determine instruction
            if entry.find('Disallow:') >= 0:
                instructionAction = False
            elif entry.find('Allow:') >= 0:
                instructionAction = True
            else: # This should never match
                instructionAction = False
                continue

            ### 2.4.2. Read URL
            addThis = entry[entry.find(':') + ':'.__len__():]

            #### '/'
            if addThis == '/':
                addThis = baseURL
            #### '' no entry (e.g., Disallow: )
            elif addThis.__len__() == 0:
                instructionAction = not instructionAction # toggle the boolean value
                addThis = baseURL
            #### '/private/'
            elif addThis[0:1] == '/':
                addThis = trim_a_URL(baseURL + addThis)
            #### WRITE SOMETHING TO PARSE WILDCARDS (e.g., '/private/*/super_private/')
            else:
                print("You found some edge case!") # DEBUGGING
                sys.exit()    

            ### 2.4.3 Remove wildcards from the URL
            addThis = addThis.replace('*','')               

            ## 2.5. Add that instruction to the dictionary as a full URL with boolean answer to the question, "Can I scrape this?"
            ### 2.5.1. Test for its existence
            if addThis in retVal:
#                print("Found a duplicate entry!") # DEBUGGING

                if retVal[addThis] != instructionAction:    
                    # This means both an Allow and Disallow have been found for the given user agents
                    # Default to Allow
                    retVal[addThis] = True
            else:
                ### 2.5.2. It doesn't exist, so add it
                retVal.update({addThis:instructionAction})

    return retVal

