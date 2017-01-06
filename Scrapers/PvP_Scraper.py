#############################
########### TO DO ###########
#############################
# List of acceptable file extensions
# Condense HTML search algorith to utilize the list of file extensions instead of separate code blocks
# Dynamically determine when to stop scraping
# Extricate Raw Image URL trimmer into function (see: forbidden filename characters)
# Error result for 404 not found on good link (see: Penny Arcade)
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
webComicName = 'PvP'
baseURL = 'http://pvponline.com/comic'
#targetComicURL = baseURL # Original source
#targetComicURL = 'http://pvponline.com/comic/x-gene' # Beginning of named images
targetComicURL = 'http://pvponline.com/comic/comic/you-are-cordially-invited' # Source of error

### IMAGE URL SETUP ###
imageSearchPhrase = 's3-us-west-2.amazonaws.com/pvponlinenew/img/comic/'  # Find the appropriate HTML line
imageBeginPhrase = 'src="'  # Find the beginning of the image reference

### PREV URL SETUP ###
prevSearchPhrase = 'Prev'

### DATE PARSING SETUP ###
dateSearchPhrase = imageSearchPhrase
#dateSearchPhrase = 'alt="Comic Image for '
dateDelimiter = '/'
#dateEnding = '"'

### NAME PARSING SETUP ###
nameSearchPhrase = '<title>PVP - '
nameEnding = '</title>'

################################################
################################################
################################################

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
currentFileExtension = ''   # File extension of current image to download
tempPrefix = ''             # Used to dynamically determine between relative and absolute URLs
validFileTypeList = ['.png', '.jpg', '.gif']
fullURLIndicatorList = [baseURL, 'www', 'http']
#########################
#########################
#########################

########################
### STATIC VARIABLES ###
########################
USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'
MAX_SLEEP = 30               # SECONDS
MAX_SKIPS = 1000              # Point to stop looking
numSkips = 0                # Variable to store the number of files already found
random.seed()
########################
########################
########################

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
imageName = ''
dateTimeURL = '' 
prevURL = ''
tempPrefix = ''
pageTitle = ''              # Holds the page's title HTML entry (will be parses for "Name" portion of filename)
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
#    sys.exit()    

try:
    comicRequest = Request(currentURL, headers={'User-Agent': USER_AGENT})
    comic = urlopen(comicRequest)
except urllib.error.URLError as error:
    print("\nCannot open URL:\t{}".format(currentURL))
    print("ERROR:\t{} - {}".format(type(error),error))
    sys.exit()
else:
    print("\nOpened URL:\t{}".format(currentURL)) # DEBUGGING

while comic.getcode() == 200:
    # DETERMINE CHARSET OF PAGE
#    print("\ncomic Charset:")
    comicContentType = comic.getheader('Content-Type')

    if comicContentType.find('=') < 0:
        comicCharset = 'UTF-8'
    else:
        comicCharset = comicContentType[comicContentType.find('=') + 1:]
#    print("Charset:\t{}".format(comicCharset)) # DEBUGGING

    # TRANSLATE PAGE
    comicContent = comic.read()
    comicContentDecoded = comicContent.decode(comicCharset)
    comicHTML = comicContentDecoded.split('\n')

#    print("\nFetching Image URL:")

    # FIND THE IMAGE .GIF
    for entry in comicHTML:
        #if entry.lower().find('title') >= 0: # DEBUGGING
        #    print(entry)
        if entry.find(imageSearchPhrase) >= 0:
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
#        sys.exit()

    # PARSE IMAGE URL FOR FILENAME
    if imageURL.__len__() > 0:
        for entry in comicHTML:
            if entry.find(dateSearchPhrase) >= 0:
                dateTimeURL = entry
#                print("Guessing the file date is:\t{}".format(find_the_date(dateTimeURL))) # TESTING
                imageDate = find_the_date(dateTimeURL)  
                break

        if imageDate.__len__() == 8 and imageDate != '00000000':
            imageYear = imageDate[:4]
            imageMonth = imageDate[4:6]
            imageDay = imageDate[6:]
        else:
            imageDate = find_the_date(comicHTML)

            if imageDate.__len__() == 8 and imageDate != '00000000':
                imageYear = imageDate[:4]
                imageMonth = imageDate[4:6]
                imageDay = imageDate[6:]
            else:
                imageYear = ''
                imageMonth = ''
                imageDay = ''
                print("Did not find an image date for URL:\t{}".format(currentURL)) # DEBUGGING
                sys.exit() # TESTING

        # NAME
        ## Find the title line in the page HTML
        searchString = nameSearchPhrase
        if rawImageURL.find(searchString) >= 0:
            pageTitle = rawImageURL
        elif currentURL.find(searchString) >= 0:
            pageTitle = rawImageURL
        else:
            for entry in comicHTML:
                if entry.find(searchString) >= 0 and (entry.find(imageYear) < 0 or entry.find(imageMonth) < 0 or entry.find(imageDay) < 0):
#                if entry.find(searchString) >= 0 and entry.find(imageYear) < 0: # BUG: Breaking for "...Christmas 2015..." titles
                    pageTitle = entry
                    break

        ## Parse it for a proper name
        if pageTitle.__len__() > 0:
            # TRIM RAW IMAGE URL
            imageName = pageTitle[pageTitle.find(searchString) + searchString.__len__():]
            imageName = imageName[:imageName.find(nameEnding)]
            # REMOVE UNWANTED CHARACTERS
            imageName = trim_the_name(imageName) 

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
            print("Did not find an image name for URL:\t{}".format(currentURL)) # DEBUGGING
#            sys.exit() # TESTING
        ## Final filename trimming
        incomingFilename = incomingFilename.replace('__','_')
        incomingFilename = incomingFilename.replace('--','-')  
        ## Append the filetype
        incomingFilename = incomingFilename + currentFileExtension
        print("Filename:\t{}".format(incomingFilename)) # DEBUGGING

    # DOWNLOAD THE FILE
    if imageURL.__len__() > 0 and incomingFilename.__len__() > 0:
        if os.path.exists(os.path.join(SAVE_PATH, incomingFilename)) == False:
            try:
                urlretrieve(imageURL, os.path.join(SAVE_PATH, incomingFilename))
            except Exception as error:
                print("Image failed to download:\t{}".format(imageURL))
                print("ERROR:\t{} - {}".format(type(error),error))
                sys.exit()    
            else:
                print("Image URL download successful:\t{}".format(incomingFilename)) # DEBUGGING
                skipping = False
        else:
            print("Filename {} already exists.".format(incomingFilename)) # DEBUGGING
            numSkips += 1
            skipping = True

    # STOP SCRAPING... IT'S THE END
    if currentURL == "http://www.giantitp.com/comics/oots0001.html":                   # hard coded First
        print("Finished scraping")
        break
    elif numSkips >= MAX_SKIPS and MAX_SKIPS > 0:
        print("{} files already found.\nEnding scrape.".format(numSkips))
        break

    # PROCEED TO THE PREVIOUS PAGE
#    print(comicHTML) # DEBUGGING
    prevURL = '' # Empty string is the 'continue' condition
    for entry in comicHTML:
        if prevURL.__len__() > 0:
            break
        elif entry.find(prevSearchPhrase) >= 0:
#            print("Trim this:\t{}".format(entry)) # DEBUGGING
            for subEntry in entry.split('</A>'):
                if subEntry.find(prevSearchPhrase) >= 0:
                    prevURL = subEntry[subEntry.find('href="') + 'href="'.__len__():]
                    prevURL = prevURL[:prevURL.find('"')]
        #            print("Prev URL:\t{}".format(prevURL)) # DEBUGGING
                    currentURL = prevURL
                    tempPrefix = baseURL # Default stance

                    for indicator in fullURLIndicatorList:
                        if currentURL.find(indicator) >= 0:
                            tempPrefix = ''
                            break
                    currentURL = tempPrefix + currentURL


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
    imageName = ''
    dateTimeURL = '' 
    prevURL = ''
    tempPrefix = ''
    pageTitle = ''              # Holds the page's title HTML entry (will be parses for "Name" portion of filename)

    try:
        comicRequest = Request(currentURL, headers={'User-Agent': USER_AGENT})
        comic = urlopen(comicRequest)
    except urllib.error.URLError as error:
        print("ERROR:\t{} - {}".format(type(error),error))
        sys.exit()
    else:
        print("\nOpened URL:\t{}".format(currentURL)) # DEBUGGING
        if skipping == False:
            sleepyTime = random.randrange(0, MAX_SLEEP)
            print("Sleeping {} seconds before download".format(sleepyTime))
            time.sleep(sleepyTime)


        
#    break # Artificial exit


