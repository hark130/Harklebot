#################################################################################
################################### HARKLEBOT ###################################
############################## Template Scraper v1 ##############################
##################### https://github.com/hark130/Harklebot ######################
#################################################################################
# Version 1
#   Based on some intial variable settings (see: MODIFY THESE WHEN...):
#       Checks for save path based on webcomic name
#       Reads webpage html to find webcomic URL
#       Reads html in an attempt to find a date and/or comic name
#       Saves webcomic image with date (YYYMMDD) and a name (if found)
#       Reads webpage html to find prev webcomic
#       Continues walking/saving prev image files until first page is reached
#################################################################################


from urllib.request import urlopen
from urllib.request import urlretrieve
from urllib.request import Request
import urllib.error
import sys, os, time, random, re
# Hacky (?) method to keep modules separate from scraper code
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'Modules'))
from Scraper_Functions import find_the_date 
from Scraper_Functions import trim_the_name 
from Robot_Reader_Functions import get_root_URL

################################################
# MODIFY THESE WHEN ADAPTING TO A NEW WEBCOMIC #
################################################
### URL SETUP ###
webComicName = '___UPDATE___' # <=--------------------------=UPDATE=--------------------------=>
baseURL = '___UPDATE___' # <=--------------------------=UPDATE=--------------------------=>
targetComicURL = '___UPDATE___' # Original source
#targetComicURL = baseURL # Start here instead

### IMAGE URL SETUP ###
# Find the appropriate HTML line from a list of strings
imageSearchPhrase = ['___UPDATE___', '___UPDATE___', '___UPDATE___'] # <=--------------------------=UPDATE=--------------------------=>
# Find the beginning of the image reference
imageBeginPhrase = '___UPDATE___' # Probably 'src="' <=--------------------------=UPDATE=--------------------------=> 

### PREV URL SETUP ###
prevSearchPhrase = '___UPDATE___' # Probably 'Prev' <=--------------------------=UPDATE=--------------------------=>

### FIRST URL SETUP ###
firstSearchPhrase = '___UPDATE___' # Probably 'First' <=--------------------------=UPDATE=--------------------------=>

### DATE PARSING SETUP ###
dateSearchPhrase = ['___UPDATE___'] # <=--------------------------=UPDATE=--------------------------=>
#dateSearchPhrase = imageSearchPhrase
#dateDelimiter = ''

### NAME PARSING SETUP ###
nameSearchPhrase = '___UPDATE___' # Probably 'alt="' <=--------------------------=UPDATE=--------------------------=>
nameEnding = '___UPDATE___' # Probably '"' <=--------------------------=UPDATE=--------------------------=>
################################################
################################################
################################################

########################
### STATIC VARIABLES ###
########################
USER_AGENT = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:50.0) Gecko/20100101 Firefox/50.0' # http://www.whoishostingthis.com/tools/user-agent/
#USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0' # http://www.whoishostingthis.com/tools/user-agent/
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
# Windows 7 home path environment variable
if 'USERPROFILE' in os.environ:
    SAVE_PATH = os.path.join(os.environ['USERPROFILE'], 'Pictures', webComicName)
# Ubuntu 16.04 LTS home path environment variable
elif 'HOME' in os.environ:
    SAVE_PATH = os.path.join(os.environ['HOME'], 'Pictures', webComicName)
# ./Pictures/
else:
    SAVE_PATH = os.path.join('Pictures', webComicName)    

rootURL = get_root_URL(baseURL)
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
fullURLIndicatorList = [rootURL, baseURL, 'www', 'http']
numExistingSkips = 0        # Variable to store the number of files already found
num404Skips = 0             # Variable to store the number of missing webpages
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
            sleepyTime = random.randrange(0, MAX_SLEEP)
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
                        tempPrefix = baseURL # Default stance

                        for indicator in fullURLIndicatorList:
                            if firstURL.find(indicator) >= 0:
                                tempPrefix = ''
                                break
                        firstURL = tempPrefix + firstURL
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
        else:
            for entry in comicHTML:
                if entry.find(searchString) >= 0 and (entry.find(imageYear) < 0 or entry.find(imageMonth) < 0 or entry.find(imageDay) < 0 or imageYear == ''):
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
#                    print("Prev URL:\t{}".format(prevURL)) # DEBUGGING
                    currentURL = prevURL
                    # Changed tempPrefix = from baseURL to rootURL to avoid www.root.com/comics/ + /comics/20161213.png
                    tempPrefix = rootURL # Default stance
#                    tempPrefix = baseURL # Default stance

                    for indicator in fullURLIndicatorList:
                        if currentURL.find(indicator) >= 0:
                            tempPrefix = ''
                            break
                    currentURL = tempPrefix + currentURL

#                    print("Current URL:\t{}".format(currentURL)) # DEBUGGING
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

#    break # Artificial exit


