#############################
########### TO DO ###########
#############################
# ROBOTS.TXT!
# Modify code to check for 'first' file after hitting max skips.  Continue(?) if not there.
# Protect against max filename length
# Can't find a predictable method of ordering images (see: Awkward Zombie):
#   Provide a counter if a date is not found (e.g., if dateTime == '', counter = ???)
#   -or-
#   Strip some numbering scheme off the server's filename
#   -or-
#   Is it possible to strip metadata off the downloaded file?
# Store 404 images and/or their URLs and come back to them later?
# Sometimes there's redundancy between nav-back and base URL.
#   Utilize base URL for relative URL assignment?
#   .find() functionality to find an overlap match? (e.g., www.blah.com/comic/ & /comic/imgs/2016/01/...)
# Extricate duplicate code into Scraper_Functions_v2 (e.g., is this relative or an absolute URL, strip a string through slicing)
#############################
#############################
#############################

from urllib.request import urlopen
from urllib.request import urlretrieve
from urllib.request import Request
import urllib.error
import sys, os, time, random, re
from Scraper_Functions_v2 import find_the_date 
from Scraper_Functions_v2 import trim_the_name 

################################################
# MODIFY THESE WHEN ADAPTING TO A NEW WEBCOMIC #
################################################
### URL SETUP ###
webComicName = 'Ctrl-Alt-Del_Sillies' # <=--------------------------=UPDATE=--------------------------=>
rootURL = 'http://www.cad-comic.com/' # <=--------------------------=UPDATE=--------------------------=>
baseURL = 'http://www.cad-comic.com/sillies/' # <=--------------------------=UPDATE=--------------------------=>
targetComicURL = baseURL # Original source
#targetComicURL = baseURL # Start here instead

### IMAGE URL SETUP ###
# Find the appropriate HTML line from a list of strings
## src="http://cdn2.cad-comic.com/comics/sillies-20161219-65f44.gif" alt="" title="" style="width: 625px; height: 252px" /><div
imageSearchPhrase = ['cdn2.cad-comic.com/comics/'] # <=--------------------------=UPDATE=--------------------------=>
# Find the beginning of the image reference
imageBeginPhrase = 'src="' # <=--------------------------=UPDATE=--------------------------=> 

### PREV URL SETUP ###
prevSearchPhrase = 'nav-back' # <=--------------------------=UPDATE=--------------------------=>

### FIRST URL SETUP ###
firstSearchPhrase = 'nav-first' # <=--------------------------=UPDATE=--------------------------=>

### DATE PARSING SETUP ###
#dateSearchPhrase = [''] # <=--------------------------=UPDATE=--------------------------=>
dateSearchPhrase = imageSearchPhrase

### NAME PARSING SETUP ###
nameSearchPhrase = 'title="' # <=--------------------------=UPDATE=--------------------------=>
nameEnding = '"' # <=--------------------------=UPDATE=--------------------------=>
################################################
################################################
################################################

########################
### STATIC VARIABLES ###
########################
# HARKLEBOT_USER_AGENT1 is the actual User Agent of this Firefox browser
HARKLEBOT_USER_AGENT1 = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0' # http://www.whoishostingthis.com/tools/user-agent/
HARKLEBOT_USER_AGENT2 = 'Mozilla/5.0'
HARKLEBOT_USER_AGENT3 = 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko' # Who is hosting this? w/ IE Version: 11.0.9600.18426
GOOGLEBOT2_1_USER_AGENT1 = 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)' # http://www.useragentstring.com/pages/useragentstring.php?name=Googlebot
GOOGLEBOT2_1_USER_AGENT2 = 'Googlebot/2.1 (+http://www.googlebot.com/bot.html)' # http://www.useragentstring.com/pages/useragentstring.php?name=Googlebot
GOOGLEBOT2_1_USER_AGENT3 = 'Googlebot/2.1 (+http://www.google.com/bot.html)' # http://www.useragentstring.com/pages/useragentstring.php?name=Googlebot
MOBILE_USER_AGENT1 = 'Mozilla/5.0 (Linux; Android 6.0; HTC_One_M8/6.20.502.5 Build/MRA58K) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/38.0.0.0 Mobile Safari/537.36' # Who is hosting this? w/ Uling
RANDOM_USER_AGENT2 = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11' # http://wolfprojects.altervista.org/articles/change-urllib-user-agent/
RANDOM_USER_AGENT3 = 'Opera/9.25 (Windows NT 5.1; U; en)' # http://wolfprojects.altervista.org/articles/change-urllib-user-agent/
RANDOM_USER_AGENT4 = 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)' # http://wolfprojects.altervista.org/articles/change-urllib-user-agent/
RANDOM_USER_AGENT5 = 'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)' # http://wolfprojects.altervista.org/articles/change-urllib-user-agent/
RANDOM_USER_AGENT6 = 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12' # http://wolfprojects.altervista.org/articles/change-urllib-user-agent/
RANDOM_USER_AGENT7 = 'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9' # http://wolfprojects.altervista.org/articles/change-urllib-user-agent/
# Which user agent do you want to use when contacting this website?  Update USER_AGENT with your choice.
USER_AGENT = HARKLEBOT_USER_AGENT1 # <=--------------------------=UPDATE=--------------------------=>
MAX_SLEEP = 30              # SECONDS
MAX_EXISTING_SKIPS = 10     # Max number of existing files to skip over before stopping
MAX_404_SKIPS = 10          # Max number of missing images to skip over before stopping
random.seed()
########################
########################
########################

#########################
### DYNAMIC VARIABLES ###
#########################
SAVE_PATH = os.path.join(os.environ['USERPROFILE'], 'Pictures', webComicName)
defaultFilename = webComicName + '_Webcomic_' 
currentURL = targetComicURL
imageURL = ''               # Trimmed
rawImageURL = ''            # Un-trimmed
searchString = ''           # Used to parse raw HTML
dateTimeURL = ''            # Used to hold the URL with clues as to the comic's date
firstURL = ''               # Used to hold the URL of the first page (and stop scrapinig)
currentFileExtension = ''   # File extension of current image to download
tempPrefix = ''             # Used to dynamically determine between relative and absolute URLs
validFileTypeList = ['.png', '.jpg', '.gif']
fullURLIndicatorList = [baseURL, 'www', 'http']
numExistingSkips = 0        # Variable to store the number of files already found
num404Skips = 0             # Variable to store the number of missing webpages
robotsFile = ''             # Variable to store the contents of www.rootURL.com/robots.txt
robotsList = []             # List of split entries from robotsFile so the original is preserved

# Build the URL to the robots.txt file
# Removing redundant slashes while also fixing any http://
robotURL = rootURL + '/robots.txt'
robotURL = robotURL.replace('//','/')       # Fixing www.site.com//robots.txt
robotURL = robotURL.replace(':/','://')     # Fixing http:/www.site.com
foundUserAgent = ''                         # Hold the applicable user-agent found in robots.txt
foundDisallows = []                         # List of the disallows applicable to the found user-agent
#########################
#########################
#########################

######################
### TEMP VARIABLES ###
######################
incomingFilename = ''
filenamePreamble = ''
imageURL = ''
rawImageURL = ''
currentFileExtension = ''
imageYear = ''
imageMonth = ''
imageDay = ''
imageDate = ''              # Holds return value from find_the_date()
imageName = ''
dateTimeURL = '' 
prevURL = ''
firstURL = ''               # Holds 'first' URL and determines when to stop scraping
tempPrefix = ''
pageTitle = ''              # Holds the page's title HTML entry (will be parses for "Name" portion of filename)
skipping = True             # Boolean variable used to determine when to 'fast forward' past image URLs that have already been downloaded
######################
######################
######################

# VERIFY SAVE DIRECTORY EXISTS
if os.path.exists(SAVE_PATH):
    if os.path.isdir(SAVE_PATH):
        print("Save directory exists:\t{}".format(SAVE_PATH))
    else:
        print("Save directory is not a directory!\nERROR:\t{}".format(SAVE_PATH))
        sys.exit()
else:
    print("Save directory does not exist!\nERROR:\t{}".format(SAVE_PATH))
    print("Creating save directory at:\t{}".format(SAVE_PATH))
    os.mkdir(SAVE_PATH) 

# CHECK ROBOTS.TXT
## Download robots.txt
try:
    comicRequest = Request(robotURL, headers={'User-Agent': USER_AGENT})
    with urlopen(comicRequest) as siteRobotFile:
        robotsFile = siteRobotFile.read().decode('UTF-8', 'ignore')
except urllib.error.URLError as error:
    print("\nCannot open robots.txt URL:\t{}".format(robotURL))
    print("ERROR:\t{} - {}".format(type(error),error))
    sys.exit()
else:
    print("\nOpened robots.txt from {}:\n{}".format(robotURL, robotsFile)) # DEBUGGING

## Check robots.txt
# User-agent: *
# Disallow: /
if robotsFile.__len__() > 0:
    robotsList = robotsFile.split('\n')
    print(robotsList) # DEBUGGING

    ### Find User-Agent
    for entry in robotsList:
        #### Found a User-agent line
        if entry.lower().find('user-agent:') >= 0:
            ##### Haven't found a user-agent for us yet
            if foundUserAgent.__len__() == 0:
                if entry.lower().find('harklebot') < 0 and entry.lower().find('*') < 0:
                    ###### Not meant for us
                    continue
                ###### Meant for us
                else:
                    foundUserAgent = entry.lower()
                    foundUserAgent = foundUserAgent[foundUserAgent.find('user-agent:') + 'user-agent:'.__len__():]
                    foundUserAgent = foundUserAgent.replace(' ','')
                    continue # Move to the next line so this user-agent doesn't get added to the found disallows
            ##### Already found a user-agent and we just hit the next line
            else:
                break # Done looking.  Found a user-agent AND found all the following disallows.
        if foundUserAgent.__len__() > 0 and entry.__len__() > 0:        # The following disallows should be for us
            foundDisallows.append(entry[entry.replace(' ','').find(':') + 1:])
            print("Found a disallow:\t{}".format(foundDisallows[foundDisallows.__len__() - 1])) # DEBUGGINGs
            

######################### NEXT TIME #########################
# Now fix the found disallows so that they contain full, trimmed URLs
# Then, build in functionality to severely limit download speeds or stop altogether
# This should include 'walking' the 'prev' entries
#############################################################


# COMMENCE SCRAPING
while True:
#while comic.getcode() == 200:
    # OPEN THE WEB PAGE
    try:
        comicRequest = Request(currentURL, headers={'User-Agent': USER_AGENT})
        comic = urlopen(comicRequest)
    except urllib.error.URLError as error:
        print("\nCannot open URL:\t{}".format(currentURL))
        print("ERROR:\t{} - {}".format(type(error),error))
        sys.exit()
    else:
        print("\nOpened URL:\t{}".format(currentURL)) # DEBUGGING
        if skipping == False:
            if MAX_SLEEP > 5:
                sleepyTime = random.randrange(5, MAX_SLEEP)
            else:
                sleepyTime = 5
            print("Sleeping {} seconds before download".format(sleepyTime))
            time.sleep(sleepyTime)

    # DETERMINE CHARSET OF PAGE
#    print("\ncomic Charset:")
    comicContentType = comic.getheader('Content-Type')

    if comicContentType.find('=') < 0 or comicContentType.find('charset') < 0:
        comicCharset = 'UTF-8'
    else:
        comicContentType = comicContentType[comicContentType.find('charset'):]
        comicCharset = comicContentType[comicContentType.find('=') + 1:]
        comicCharset.replace(' ','')
#    print("Charset:\t{}".format(comicCharset)) # DEBUGGING

    # TRANSLATE PAGE
    comicContent = comic.read()

    try:
#        comicCharset = 'UTF' # TESTING
        comicContentDecoded = comicContent.decode(comicCharset, 'ignore')
    except UnicodeError as error:
        print("Unable to decode URL {} with charset {}".format(currentURL, comicCharset))
        print("ERROR:\t{}\n{}".format(type(error),error))
        sys.exit()
    else:
        comicHTML = comicContentDecoded.split('\n')

#    print("\nFetching First URL:")
    # FIND THE FIRST URL
    if firstURL.__len__() == 0:
        for entry in comicHTML:
            if firstURL.__len__() > 0:
                break
            if entry.find(firstSearchPhrase) >= 0:
                for subEntry in entry.lower().split('</a>'):
                    if subEntry.find(firstSearchPhrase.lower()) >= 0 and subEntry.find('href="') >= 0:
                        firstURL = subEntry[subEntry.find('href="') + 'href="'.__len__():]
                        firstURL = firstURL[:firstURL.find('"')]
# BUG?  Nested comic URL (/sillies/) conflicted with relative 'prev' URL (/sillies/20151114/some.img)
# NOTE: This fix might break other scrapers
#                        tempPrefix = baseURL # Default stance 
                        tempPrefix = rootURL # Default stance

                        for indicator in fullURLIndicatorList:
                            if firstURL.find(indicator) >= 0:
                                tempPrefix = ''
                                break
                        firstURL = tempPrefix + firstURL

                        # Removing redundant slashes while also fixing any http://
                        firstURL = firstURL.replace('//','/')   # Fixing www.site.com//comic/imgs/20161230.png
                        firstURL = firstURL.replace(':/','://') # Fixing http:/www.site.com
                        
                        print("First URL:\t{}".format(firstURL)) # DEBUGGING
                        break # Found it. Stop looking now.

#    print("\nFetching Image URL:")
    # FIND THE IMAGE .GIF
    for entry in comicHTML:
        #if entry.lower().find('title') >= 0: # DEBUGGING
        #    print(entry)
        if imageURL.__len__() > 0:
            break
        for phrase in imageSearchPhrase:
            if entry.find(phrase) >= 0:
    #            print("FOUND THIS:\t{}".format(entry)) # DEBUGGING

                # Preserve inital html entry
                rawImageURL = entry

                # Determine file extension
                for extension in validFileTypeList:
                    if entry.find(extension) >= 0:
                        currentFileExtension = extension
                        break

                # Trim the URL
                imageURL = entry[entry.find(imageBeginPhrase) + imageBeginPhrase.__len__():]
                imageURL = imageURL[:imageURL.find(currentFileExtension) + currentFileExtension.__len__()]
                break       # Found it. Stop looking now                  

    if imageURL.__len__() > 0:
        tempPrefix = baseURL # Default stance

        for indicator in fullURLIndicatorList:
            if imageURL.find(indicator) >= 0:
                tempPrefix = ''
                break
        imageURL = tempPrefix + imageURL
#        print("Raw URL:\t{}".format(rawImageURL)) # DEBUGGING
#        print("Image URL:\t{}".format(imageURL)) # DEBUGGING
        pass
    else:
        print("Did not find an image URL!")
        sys.exit()

    # PARSE IMAGE URL FOR FILENAME
    if imageURL.__len__() > 0:   

        # DATE
        for entry in comicHTML:
            if imageDate.__len__() > 0 and imageDate != '00000000':
                break
            for phrase in dateSearchPhrase:
                if entry.find(phrase) >= 0:
                    dateTimeURL = entry
    #                print("Guessing the file date is:\t{}".format(find_the_date(dateTimeURL))) # TESTING
                    imageDate = find_the_date(dateTimeURL)    
                    if imageDate.__len__() > 0 and imageDate != '00000000':
                        break

        if imageDate.__len__() == 8 and imageDate != '00000000':
            imageYear = imageDate[:4]
            imageMonth = imageDate[4:6]
            imageDay = imageDate[6:]
        else:
            imageYear = ''
            imageMonth = ''
            imageDay = ''

        # NAME
        ## Find the title line in the page HTML
        searchString = nameSearchPhrase
        if rawImageURL.find(searchString) >= 0:
            pageTitle = rawImageURL
        elif currentURL.find(searchString) >= 0:
            pageTitle = currentURL
#            pageTitle = rawImageURL # BUG: Copy pasta error
        else:
            for entry in comicHTML:
                if entry.find(searchString) >= 0 and (entry.find(imageYear) < 0 or entry.find(imageMonth) < 0 or entry.find(imageDay) < 0 or imageYear == ''):
#                if entry.find(searchString) >= 0 and entry.find(imageYear) < 0: # BUG: Breaking for "...Christmas 2015..." titles
                    pageTitle = entry
                    break

        ## Parse it for a proper name
        if pageTitle.__len__() > 0:
            # TRIM RAW IMAGE URL
            imageName = pageTitle[pageTitle.find(searchString) + searchString.__len__():]
            imageName = imageName[:imageName.find(nameEnding)]
            # TRIM UNWANTED CHARACTERS
            imageName = trim_the_name(imageName)

            imageName = imageName.replace('39', "'") # Small quirk of the website

#            print("The name of this image is {}".format(imageName)) # DEBUGGING 
        else:
#            print("Did not find the name in:\n{}".format(currentURL)) # DEBUGGING
#            imageName = '00000000BAD_NAME00000000'
            pass
        
        # CREATE FILENAME FROM PARSED DATA
        ## Beginning
        incomingFilename = defaultFilename + imageYear + imageMonth + imageDay
        ## Include a name if one was found
        if imageName.__len__() > 0:
            incomingFilename = incomingFilename + '_' + imageName
        else:
            if imageYear.__len__() == 0 and imageMonth.__len__() == 0 and imageDay.__len__() == 0:
                print("Failed to find image tile or image date for Image URL:\n{}".format(imageURL))
                sys.exit()
            else:
                pass
        ## Final filename trimming
        incomingFilename = incomingFilename.replace('__','_')
        incomingFilename = incomingFilename.replace('--','-') 
        ## Append the filetype
        incomingFilename = incomingFilename + currentFileExtension
#        print("Filename:\t{}".format(incomingFilename)) # DEBUGGING

    # DOWNLOAD THE FILE
    if imageURL.__len__() > 0 and incomingFilename.__len__() > 0:
        if os.path.exists(os.path.join(SAVE_PATH, incomingFilename)) == False:
            try:
                # urlretrieve is being blocked by websites scanning user-agents...
                # ...for webscrapers like urllib.  urlretrieve was abandoned in...
                # ...lieu of request-->urlopen-->write() in an attempt to...
                # ...continue dodging websites that block webscrapers.
#                urlretrieve(imageURL, os.path.join(SAVE_PATH, incomingFilename))

                # Utilizing a request-->urlopen-->write() in an attempt to...
                # ...continue dodging websites that block webscrapers.
                comicRequest = Request(imageURL, headers={'User-Agent': USER_AGENT})
                with urlopen(comicRequest) as comic:
                    with open(os.path.join(SAVE_PATH, incomingFilename), 'wb') as outFile:
                        outFile.write(comic.read())

            except Exception as error:
                print("Image failed to download:\t{}".format(imageURL))

                # Handle 404 errors
                if error.code == 404:
                    num404Skips += 1
                else:
                    print("ERROR:\t{} - {}".format(type(error),error))
                    sys.exit()    
            else:
                print("Image URL download successful:\t{}".format(incomingFilename)) # DEBUGGING
                skipping = False
        else:
            print("Filename {} already exists.".format(incomingFilename)) # DEBUGGING
            numExistingSkips += 1
            skipping = True

    # STOP SCRAPING... IT'S THE END
    if currentURL == firstURL:                   # dynamically read First
        print("\nFinished scraping")
        break
    elif numExistingSkips >= MAX_EXISTING_SKIPS and MAX_EXISTING_SKIPS > 0:
        print("\n{} files already found.\nEnding scrape.".format(numExistingSkips))
        break
    elif firstURL.__len__() == 0:
        print("\nMissing First URL.  We must be there.\nCurrent URL:\t{}\nFirst URL:\t{}\n".format(currentURL,firstURL))
        break
    elif num404Skips >= MAX_404_SKIPS:
        print("\n{} 'Not Found (404)' errors encountered.\nEnding scrape.".format(num404Skips))
        break

    # PROCEED TO THE PREVIOUS PAGE
    prevURL = '' # Empty string is the 'continue' condition
    for entry in comicHTML:
        if prevURL.__len__() > 0:
            break
        elif entry.find(prevSearchPhrase) >= 0:
#            print("Trim this:\t{}".format(entry)) # DEBUGGING
            for subEntry in entry.lower().split('</a>'):
                if subEntry.find(prevSearchPhrase.lower()) >= 0 and subEntry.find('href="') >= 0:
                    prevURL = subEntry[subEntry.find('href="') + 'href="'.__len__():]
                    prevURL = prevURL[:prevURL.find('"')]
        #            print("Prev URL:\t{}".format(prevURL)) # DEBUGGING
                    currentURL = prevURL
                    # Changed tempPrefix = from baseURL to rootURL to avoid www.root.com/comics/ + /comics/20161213.png
                    tempPrefix = rootURL # Default stance
#                    tempPrefix = baseURL # Default stance

                    for indicator in fullURLIndicatorList:
                        if currentURL.find(indicator) >= 0:
                            tempPrefix = ''
                            break
                    currentURL = tempPrefix + currentURL

                    # Removing redundant slashes while also fixing any http://
                    currentURL = currentURL.replace('//','/')   # Fixing www.site.com//comic/imgs/20161230.png
                    currentURL = currentURL.replace(':/','://') # Fixing http:/www.site.com

        #            print("Current URL:\t{}".format(currentURL)) # DEBUGGING
                    break

    # RESET TEMP VARIABLES TO AVOID DUPE DOWNLOADS AND OTHER ERRORS
    incomingFilename = ''
    filenamePreamble = ''
    imageURL = ''
    rawImageURL = ''
    currentFileExtension = ''
    imageYear = ''
    imageMonth = ''
    imageDay = ''
    imageDate = ''              # Holds return value from find_the_date()
    imageName = ''
    dateTimeURL = '' 
    prevURL = ''
    tempPrefix = ''
    pageTitle = ''              # Holds the page's title HTML entry (will be parses for "Name" portion of filename)

    #try:
    #    comicRequest = Request(currentURL, headers={'User-Agent': USER_AGENT})
    #    comic = urlopen(comicRequest)
    #except urllib.error.URLError as error:
    #    print("ERROR:\t{} - {}".format(type(error),error))
    #    sys.exit()
    #else:
    #    print("\nOpened URL:\t{}".format(currentURL)) # DEBUGGING
    #    if skipping == False:
    #        sleepyTime = random.randrange(0, MAX_SLEEP)
    #        print("Sleeping {} seconds before download".format(sleepyTime))
    #        time.sleep(sleepyTime)
      
#    break # Artificial exit


