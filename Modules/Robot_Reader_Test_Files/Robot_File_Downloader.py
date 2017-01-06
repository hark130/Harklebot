# Robots Exclusion Standard
# https://en.wikipedia.org/wiki/Robots_exclusion_standard
# The robots exclusion standard, also known as the robots exclusion protocol or simply robots.txt, is a standard used by websites to communicate with web crawlers and other web robots.

# Sitemaps
# https://en.wikipedia.org/wiki/Sitemaps
# The Sitemaps protocol allows a webmaster to inform search engines about URLs on a website that are available for crawling.

from urllib.request import urlopen
from urllib.request import Request
import urllib.error
import os

# Fake user-agent
USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0' # http://www.whoishostingthis.com/tools/user-agent/

# List the home directories of the sites you want to download Robots.txt files from
LIST_O_SITES = [
'http://www.xkcd.com',
'http://www.businesscat.happyjar.com',
'https://www.penny-arcade.com',
'http://www.giantitp.com',
'http://pvponline.com',
'http://www.smbc-comics.com',
'http://awkwardzombie.com',
'http://www.cad-comic.com'
]

# Ordered list (most restrictive to least restrictive) of website beginnings
SITE_DELIMITER_START = ['www.', '//', ':', 'https', 'http']
# Unordered list of website TLDs
SITE_DELIMITER_STOP = ['.com', '.org', '.net', '.int', '.edu', '.gov', '.mil', '.arpa']

# Filename base
filenameSuffix = '_robots.txt'
# Filename storage location
SAVE_PATH = ''

for site in LIST_O_SITES:
    # 1. CREATE NEW URL FOR ROBOTS.TXT FILE
    robotURL = site + '/robots.txt'
    robotURL = robotURL.replace('//','/')       # Fixing www.site.com//robots.txt
    robotURL = robotURL.replace(':/','://')     # Fixing http:/www.site.com

    # 2. DOWNLOAD THE ROBOTS.TXT FILE
    try:
        robotRequest = Request(robotURL, headers={'User-Agent': USER_AGENT})
        with urlopen(robotRequest) as siteRobotFile:
            robotsFile = siteRobotFile.read().decode('UTF-8', 'ignore')
    except urllib.error.URLError as error:
        print("\nCannot open robots.txt URL:\t{}".format(robotURL))
        print("ERROR:\t{} - {}".format(type(error),error))
        sys.exit()
    else:
        print("\nOpened robots.txt from {}!".format(robotURL)) # DEBUGGING

        # 3. WRITE THE ROBOTS.TXT FILE TO DISK
        ## 3.1. Determine filename
        incomingFilename = site
        
        ### 3.1.1. Find the beginning of the website name
        for delimiterStart in SITE_DELIMITER_START:
            if incomingFilename.find(delimiterStart) >= 0:
                incomingFilename = incomingFilename[incomingFilename.find(delimiterStart) + delimiterStart.__len__():]
                break

        ### 3.1.2. Trim off any sub directories
        while incomingFilename.find('/') >= 0:
            incomingFilename = incomingFilename[:incomingFilename.find('/')]

        ### 3.1.3. Find the end of the website name
        for delimiterStop in SITE_DELIMITER_STOP:
            if incomingFilename.find(delimiterStop) >= 0:
                incomingFilename = incomingFilename[:incomingFilename.find(delimiterStop)]
                break

        ### 3.1.4. Finish creating the filename
        incomingFilename = incomingFilename + filenameSuffix

        ## 3.2. Write the file to disk
        with open(os.path.join(SAVE_PATH, incomingFilename), 'wb') as outFile:
            try:
                outFile.write(robotsFile.encode())
            except Exception as error:
                print("\nCannot write the following to file {}:\n\n{}\n".format(incomingFilename, robotsFile))
                print("ERROR:\t{} - {}".format(type(error),error))
                sys.exit()
            else:
                print("Successfully wrote {} to {}!".format(robotURL, incomingFilename))

    
