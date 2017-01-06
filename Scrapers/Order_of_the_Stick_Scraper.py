######### TO DO #########
### JUST FOR THIS ONE ###
# Add check to verify this is the 'first'
#########################


#############################
########### TO DO ###########
#############################
# Dictionary of forbidden filename characters and their replacements (e.g., .replace(' ','-'))
# List of acceptable file extensions
# Condense HTML search algorith to utilize the list of file extensions instead of separate code blocks
#############################
#############################
#############################


from urllib.request import urlopen
from urllib.request import urlretrieve
from urllib.request import Request
import urllib.error
import sys, os, time, random

################################################
# MODIFY THESE WHEN ADAPTING TO A NEW WEBCOMIC #
################################################
webComicName = 'Order_of_the_Stick'
baseURL = 'http://www.giantitp.com'
targetComicURL = 'http://www.giantitp.com/comics/oots1061.html' # Original source
#targetComicURL = 'http://www.giantitp.com/comics/oots0001.html' # First
currentFileExtension = '.gif'
imageSearchPhrase = 'src="/comics/images/'  # Find the appropriate HTML line
imageBeginPhrase = 'src="'  # Find the beginning of the image reference
prevSearchPhrase = 'title="Previous Comic"'
################################################
################################################
################################################

USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'
SAVE_PATH = os.path.join(os.environ['USERPROFILE'], 'Pictures', webComicName)
defaultFilename = webComicName + '_Webcomic_' 
currentURL = targetComicURL
imageURL = ''               # Trimmed
rawImageURL = ''            # Un-trimmed
searchString = ''           # Used to parse raw HTML
dateTimeURL = ''            # Used to hold the URL with clues as to the comic's date
MAX_SLEEP = 15              # SECONDS
MAX_SKIPS = 10              # Point to stop looking
numSkips = 0                # Variable to store the number of files already found
random.seed()

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
    # PARSE HTML FOR IMAGE 2x.PNG URL
#    print("Decoded Content:\n{}".format(comicContentDecoded)) # DEBUGGING
#    print("HTML:\n{}".format(comicHTML)) # DEBUGGING

    for entry in comicHTML:
        if entry.find('.gif') >= 0 and entry.find(imageSearchPhrase) >= 0:
#            print("FOUND THIS:\t{}".format(entry)) # DEBUGGING
            # Preserve inital html entry
            rawImageURL = entry
            # Trim the url
            imageURL = entry[entry.find(imageBeginPhrase) + imageBeginPhrase.__len__():]
            imageURL = imageURL[:imageURL.find('.gif') + '.gif'.__len__()]
            currentFileExtension = '.gif'
            break       # Found it. Stop looking now

    # DIDN'T FIND IMAGE .GIF?  LOOK FOR .PNG    
    if imageURL.__len__() == 0:
        for entry in comicHTML:
            if entry.find('.png') >= 0 and entry.find(imageSearchPhrase) >= 0:
#                print("FOUND THIS:\t{}".format(entry)) # DEBUGGING
                # Preserve inital html entry
                rawImageURL = entry
                # Trim the url
                imageURL = entry[entry.find(imageBeginPhrase) + imageBeginPhrase.__len__():]
                imageURL = imageURL[:imageURL.find('.png') + '.png'.__len__()]
                currentFileExtension = '.png'
                break       # Found it. Stop looking now

    # DIDN'T FIND IMAGE .PNG?  LOOK FOR .JPG
    if imageURL.__len__() == 0:
        for entry in comicHTML:
            if entry.find('.jpg') >= 0 and entry.find(imageSearchPhrase) >= 0:
#                print("FOUND THIS:\t{}".format(entry)) # DEBUGGING
                # Preserve inital html entry
                rawImageURL = entry
                # Trim the url
                imageURL = entry[entry.find(imageBeginPhrase) + imageBeginPhrase.__len__():]
                imageURL = imageURL[:imageURL.find('.jpg') + '.jpg'.__len__()]
                currentFileExtension = '.jpg'
                break       # Found it. Stop looking now                     

    if imageURL.__len__() > 0:
        if imageURL.find(baseURL) < 0:
            imageURL = baseURL + imageURL # HTML makes relative reference
#        print("Raw URL:\t{}".format(rawImageURL)) # DEBUGGING
#        print("Image URL:\t{}".format(imageURL)) # DEBUGGING
        pass
    else:
        print("Did not find an image URL!")
#        sys.exit()

    # PARSE IMAGE.PNG URL FOR FILENAME
    ## <meta property="og:url" content="http://www.penny-arcade.com/comic/2016/12/19" />'
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

#        # YEAR
##        searchString = "http://www.penny-arcade.com/comic/" # Set during previous parsing
#        if dateTimeURL.find(searchString) >= 0:
#            imageYear = dateTimeURL[dateTimeURL.find(searchString) + searchString.__len__():]
#            imageYear = imageYear[:imageYear.find('-')]
#            while imageYear.__len__() < 4:
#                imageYear = '0' + imageYear
#        else:
#            print("Did not find year in:\n{}".format(dateTimeURL)) # DEBUGGING
#            imageYear = '0000BAD_YEAR0000'

##        print("Year:\t{}".format(imageYear)) # DEBUGGING        

#        # MONTH
#        searchString = imageYear + '-'
#        if dateTimeURL.find(searchString) >= 0:
#            imageMonth = dateTimeURL[dateTimeURL.find(searchString) + searchString.__len__():]
#            imageMonth = imageMonth[:imageMonth.find('-')]
#            while imageMonth.__len__() < 2:
#                imageMonth = '0' + imageMonth
#        else:
#            print("Did not find month in:\n{}".format(dateTimeURL)) # DEBUGGING
#            imageMonth = '00BAD_MONTH00'
##        print("Month:\t{}".format(imageMonth)) # DEBUGGING 

#        # DAY
#        searchString = searchString + imageMonth + '-'
#        if dateTimeURL.find(searchString) >= 0:
#            imageDay = dateTimeURL[dateTimeURL.find(searchString) + searchString.__len__():]
#            imageDay = imageDay[:imageDay.find(':')]
#            while imageDay.__len__() < 2:
#                imageDay = '0' + imageDay
#        else:
#            print("Did not find day in:\n{}".format(dateTimeURL)) # DEBUGGING
#            imageDay = '00BAD_DAY00'
##        print("Day:\t{}".format(imageDay)) # DEBUGGING 

        # NAME
        searchString = 'oots'
        if rawImageURL.find(searchString) >= 0:
            imageName = rawImageURL[rawImageURL.find(searchString) + searchString.__len__():]
            imageName = imageName[:imageName.find(currentFileExtension)]
            imageName = imageName.replace(' ', '-')
            imageName = imageName.replace('.', '')
            imageName = imageName.replace(',', '')
            imageName = imageName.replace('&#8217;', "'")
        elif currentURL.find(searchString) >= 0:
            imageName = currentURL[currentURL.find(searchString) + searchString.__len__():]
            imageName = imageName[:imageName.find('.htm')]
            imageName = imageName.replace(' ', '-')
            imageName = imageName.replace('.', '')
            imageName = imageName.replace(',', '')
            imageName = imageName.replace('&#8217;', "'")            
        else:
            print("Did not find the name in:\n{}".format(rawImageURL)) # DEBUGGING
            imageName = '00000000BAD_NAME00000000'
#        print("Name:\t{}".format(imageName)) # DEBUGGING 

        # CREATE FILENAME FROM PARSED DATA
        incomingFilename = defaultFilename + imageName + currentFileExtension
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
    ## <A href="/comics/oots1060.html"><IMG src="/Images/redesign/ComicNav_Back.gif" alt="Previous Comic" title="Previous Comic" border="0">
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
        #            currentURL = targetComicURL + prevURL # Not necessary since it's a full URL
                    currentURL = prevURL
                    currentURL = baseURL + currentURL
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


