#############################
########### TO DO ###########
#############################
# List of acceptable file extensions
# Condense HTML search algorith to utilize the list of file extensions instead of separate code blocks
# Dynamically determine when to stop scraping
# Extricate Raw Image URL trimmer into function (see: forbidden filename characters)
# Error result for 404 not found on good link (see: Penny Arcade)
# Modify code to check for 'first' file after hitting max skips.  Continue(?) if not there.
# Protect against max filename length
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
webComicName = 'SMBC'
baseURL = 'http://www.smbc-comics.com'
#targetComicURL = baseURL # Original source
targetComicURL = 'http://www.smbc-comics.com/comic/2006-12-25' # Source of error

### IMAGE URL SETUP ###
imageSearchPhrase = 'www.smbc-comics.com/comics/'  # Find the appropriate HTML line
imageBeginPhrase = 'src="'  # Find the beginning of the image reference

### PREV URL SETUP ###
prevSearchPhrase = 'prev'

### DATE PARSING SETUP ###
dateSearchPhrase = imageSearchPhrase
dateDelimiter = ''

### NAME PARSING SETUP ###
nameSearchPhrase = '<title>Saturday Morning Breakfast Cereal - '
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
MAX_SLEEP = 30              # SECONDS
MAX_SKIPS = 10              # Point to stop looking
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
imageDate = ''              # Holds return value from find_the_date()
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

#    print("\nFetching Image URL:")
#    codeFile = open('HTML_code_file.txt', 'a')

#    for HTMLstatement in comicHTML:
#        try:
##            print("{}".format(HTMLstatement)) # DEBUGGING

#            # FIND ALL OCCURENCES OF THE YEAR
#            #if HTMLstatement.find('2016-') >= 0 and HTMLstatement.find('<title>') < 0:
#            #    print("FOUND DATE:\t{}".format(HTMLstatement)) # DEBUGGING

#            # FIND THE PAGES TITLE
#            #if HTMLstatement.find('<title>') >= 0:
#            #    pageTitle = HTMLstatement
#            #    print("TITLE:\t{}".format(HTMLstatement))
#            #    break

#            # WRITE THE HTML TO A FILE
#            codeFile.write(HTMLstatement + '\n')
#        except:
#            print("***Error printing this line of HTML***")

#    codeFile.close()

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
#        for entry in comicHTML:
#            #print("Entry:\t{}".format(entry)) # DEBUGGING
#            #if entry.find('meta property') >= 0 and entry.find('content="http://www.penny-arcade.com/comic/') >= 0:
#            #    dateTimeURL = entry
#            #    searchString = "http://www.penny-arcade.com/comic/"
#            #    break
#            if entry.find('input type="hidden" name="attributes[comic_title]" value="') >= 0:
#                dateTimeURL = entry
#                searchString = 'input type="hidden" name="attributes[comic_title]" value="'
#                break     

#        dateTimeURL = rawImageURL # Date is included in image URL HTML line           

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
            imageYear = ''
            imageMonth = ''
            imageDay = ''

#        # YEAR
##        searchString = "http://www.penny-arcade.com/comic/" # Set during previous parsing
#        if dateTimeURL.find(dateSearchPhrase) >= 0:
#            imageYear = dateTimeURL[dateTimeURL.find(dateSearchPhrase) + dateSearchPhrase.__len__():]
#            imageYear = imageYear[:imageYear.find(dateDelimiter)]
#            while imageYear.__len__() < 4:
#                imageYear = '0' + imageYear
#        else:
#            print("Did not find year in:\n{}".format(dateTimeURL)) # DEBUGGING
#            imageYear = '0000BAD_YEAR0000'
##        print("Year:\t{}".format(imageYear)) # DEBUGGING        

#        # MONTH
#        searchString = imageYear + dateDelimiter
#        if dateTimeURL.find(searchString) >= 0:
#            imageMonth = dateTimeURL[dateTimeURL.find(searchString) + searchString.__len__():]
#            imageMonth = imageMonth[:imageMonth.find(dateDelimiter)]
#            while imageMonth.__len__() < 2:
#                imageMonth = '0' + imageMonth
#        else:
#            print("Did not find month in:\n{}".format(dateTimeURL)) # DEBUGGING
#            imageMonth = '00BAD_MONTH00'
##        print("Month:\t{}".format(imageMonth)) # DEBUGGING 

#        # DAY
#        searchString = imageYear + imageMonth # We're looking for the combined occurrence since there isn't a directory for days
##        searchString = searchString + imageMonth + dateDelimiter
#        if dateTimeURL.find(searchString) >= 0:
#            imageDay = dateTimeURL[dateTimeURL.find(searchString) + searchString.__len__():]
##            imageDay = imageDay[:imageDay.find(dateEnding)]
#            imageDay = imageDay[:2]
#            while imageDay.__len__() < 2:
#                imageDay = '0' + imageDay

#        if imageDay.__len__() == 0:
#            # BUILD THE INCREMENTED SEARCH STRING
#            searchString = imageYear # First part
#            if int(imageMonth) < 9: # Needs a leading 0
#                searchString = searchString + '0'
#            searchString = searchString + str(int(imageMonth) + 1)
#            # SEARCH FOR NEWLY INCREMENTED SEARCH STRINGS
#            if dateTimeURL.find(searchString) >= 0:   # e.g., ./2015/02/20150301.img
#                imageMonth = searchString[-2:] # Get the string representation of the month from searchString
#                imageDay = dateTimeURL[dateTimeURL.find(searchString) + searchString.__len__():]
#    #            imageDay = imageDay[:imageDay.find(dateEnding)]
#                imageDay = imageDay[:2]
#                while imageDay.__len__() < 2:
#                    imageDay = '0' + imageDay            
#            else:
#                print("Did not find day in:\n{}".format(dateTimeURL)) # DEBUGGING
#                imageDay = '00BAD_DAY00'
##        print("Day:\t{}".format(imageDay)) # DEBUGGING 

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
            pass
        ## Append the filetype
        incomingFilename = incomingFilename + currentFileExtension
#        print("Filename:\t{}".format(incomingFilename)) # DEBUGGING

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
    if currentURL == "http://pvponline.com/comic/archive/1998/05":                   # hard coded First
        print("Finished scraping")
        break
    elif numSkips >= MAX_SKIPS and MAX_SKIPS > 0:
        print("{} files already found.\nEnding scrape.".format(numSkips))
        break

    # PROCEED TO THE PREVIOUS PAGE
    ## <A href="/comics/oots1060.html"><IMG src="/Images/redesign/ComicNav_Back.gif" alt="Previous Comic" title="Previous Comic" border="0">
#    print(comicHTML) # DEBUGGING
    prevURL = '' # Empty string is the 'continue' condition
    for entry in comicHTML:
        if prevURL.__len__() > 0:
            break
        elif entry.find(prevSearchPhrase) >= 0:
#            print("Trim this:\t{}".format(entry)) # DEBUGGING
            for subEntry in entry.lower().split('</a>'):
                if subEntry.find(prevSearchPhrase) >= 0 and subEntry.find('href="') >= 0:
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
    imageDate = ''              # Holds return value from find_the_date()
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


