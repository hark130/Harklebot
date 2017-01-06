from urllib.request import urlopen
from urllib.request import urlretrieve
import urllib.error
import sys, os, time, random

defaultFilename = 'Business_Cat_Webcomic_'
targetComicURL = 'http://www.businesscat.happyjar.com/' # Original source
# targetComicURL = 'http://www.businesscat.happyjar.com/comic/secret-santa/' # Fast forwarding to error
currentURL = targetComicURL
currentFileExtension = '.png'
imageURL = ''               # Trimmed
rawImageURL = ''            # Un-trimmed
searchString = ''           # Used to parse raw HTML
SAVE_PATH = os.path.join(os.environ['USERPROFILE'], 'Pictures', 'Business_Cat')
MAX_SLEEP = 15               # SECONDS
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
    sys.exit()    

try:
    comic = urlopen(currentURL)
except urllib.error.URLError as error:
    print("ERROR:\t{} - {}".format(type(error),error))
    sys.exit()
else:
    print("\nOpened URL:\t{}".format(currentURL)) # DEBUGGING

# TESTING/LEARNING/DEBUGGING
#print("\ncomic Headers:")
#for num, header in enumerate(comic.getheaders()):
#    print("Header #{}:\t{}".format(num,header))

while comic.getcode() == 200:
    # DETERMINE CHARSET OF PAGE
#    print("\ncomic Charset:")
    comicContentType = comic.getheader('Content-Type')
    comicCharset = comicContentType[comicContentType.find('=') + 1:]
#    print("Charset:\t{}".format(comicCharset)) # DEBUGGING

    # PARSE HTML FOR IMAGE 2x.PNG URL
#    print("\nFetching Image URL:")
    comicContent = comic.read()
    comicContentDecoded = comicContent.decode(comicCharset)
    comicHTML = comicContentDecoded.split('\n')
#    print(comicContentDecoded) # DEBUGGING
#    print(comicHTML) # DEBUGGING
    for entry in comicHTML:
        if entry.find('.png') >= 0 and entry.find('<img src="http://www.businesscat.happyjar.com/wp-content/uploads/') >= 0:
            # Preserve inital html entry
            rawImageURL = entry
            # Trim the url
            imageURL = entry[entry.find('<img src="') + '<img src="'.__len__():]
            imageURL = imageURL[:imageURL.find('.png') + '.png'.__len__()]
            currentFileExtension = '.png'
            break       # Found it. Stop looking now

    # DIDN'T FIND IMAGE .PNG?  LOOK FOR .JPG
    if imageURL.__len__() == 0:
        for entry in comicHTML:
            if entry.find('.jpg') >= 0 and entry.find('<img src="http://www.businesscat.happyjar.com/wp-content/uploads/') >= 0:
                # Preserve inital html entry
                rawImageURL = entry
                # Trim the url
                imageURL = entry[entry.find('<img src="') + '<img src="'.__len__():]
                imageURL = imageURL[:imageURL.find('.jpg') + '.jpg'.__len__()]
                currentFileExtension = '.jpg'
                break       # Found it. Stop looking now                     

    if imageURL.__len__() > 0:
#        print("Raw URL:\t{}".format(rawImageURL)) # DEBUGGING
#        print("Image URL:\t{}".format(imageURL)) # DEBUGGING
        pass
    else:
        print("Did not find an image URL!")
#        sys.exit()

    # PARSE IMAGE.PNG URL FOR FILENAME
    ## http://www.businesscat.happyjar.com/wp-content/uploads/2016/12/2016-12-16-Broken.png
    if imageURL.__len__() > 0:
        # YEAR
        searchString = "uploads/"
        if rawImageURL.find(searchString) >= 0:
            imageYear = rawImageURL[rawImageURL.find(searchString) + searchString.__len__():]
            imageYear = imageYear[:imageYear.find('/')]
            while imageYear.__len__() < 4:
                imageYear = '0' + imageYear
        else:
            print("Did not find year in:\n{}".format(rawImageURL)) # DEBUGGING
            imageYear = '0000BAD_YEAR0000'

        # VERIFY YEAR
        tempYear = rawImageURL[rawImageURL.find(imageYear) + 8:]
        tempYear = tempYear[:4]
        if imageYear == tempYear:
#            print("Directory year {} == Filename year {} in {}".format(imageYear, tempYear, rawImageURL))
            pass
        else:
            print("ERROR:\tDirectory year {} != Filename year {} in {}".format(imageYear, tempYear, rawImageURL)) # DEBUGGING
#        print("Year:\t{}".format(imageYear)) # DEBUGGING        

        # MONTH
        searchString = imageYear + '/'
        if rawImageURL.find(searchString) >= 0:
            imageMonth = rawImageURL[rawImageURL.find(searchString) + searchString.__len__():]
            imageMonth = imageMonth[:imageMonth.find('/')]
            while imageMonth.__len__() < 2:
                imageMonth = '0' + imageMonth
        else:
            print("Did not find month in:\n{}".format(rawImageURL)) # DEBUGGING
            imageMonth = '00BAD_MONTH00'
#        print("Month:\t{}".format(imageMonth)) # DEBUGGING 

        # DAY
        searchString = searchString + imageMonth + '/' + imageYear + '-' + imageMonth + '-'
        if rawImageURL.find(searchString) >= 0:
            imageDay = rawImageURL[rawImageURL.find(searchString) + searchString.__len__():]
            imageDay = imageDay[:imageDay.find('-')]
            while imageDay.__len__() < 2:
                imageDay = '0' + imageDay
        elif rawImageURL.find(imageYear + '/' + imageMonth + '/') >= 0:
            imageDay = rawImageURL[rawImageURL.find(imageYear + '/' + imageMonth + '/') + 16:]
            imageDay = imageDay[:2]
        else:
            print("Did not find day in:\n{}".format(rawImageURL)) # DEBUGGING
            imageDay = '00BAD_DAY00'
#        print("Day:\t{}".format(imageDay)) # DEBUGGING 

        # NAME
        searchString = 'title="'
        if rawImageURL.find(searchString) >= 0:
            imageName = rawImageURL[rawImageURL.find(searchString) + searchString.__len__():]
            imageName = imageName[:imageName.find('"')]
            imageName = imageName.replace(' ', '-')
        else:
            print("Did not find the name in:\n{}".format(rawImageURL)) # DEBUGGING
            imageName = '00000000BAD_NAME00000000'
#        print("Name:\t{}".format(imageName)) # DEBUGGING 

        # CREATE FILENAME FROM PARSED DATA
        incomingFilename = defaultFilename + imageYear + imageMonth + imageDay + '_' + imageName + currentFileExtension
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
    if currentURL == "http://www.businesscat.happyjar.com/comic/coffee/":
        print("Finished scraping")
        break
    elif numSkips >= MAX_SKIPS and MAX_SKIPS > 0:
        print("{} files already found.\nEnding scrape.".format(numSkips))
        break

    # PROCEED TO THE PREVIOUS PAGE
    ## "prev" href="
#    print(comicHTML) # DEBUGGING
    for entry in comicHTML:
        #if entry.find("secret") >= 0:
        #    print(entry)
        if entry.find('navcomic-prev') >= 0:
#            print("Trim this:\t{}".format(entry)) # DEBUGGING
            prevURL = entry[entry.find('a href="') + 'a href="'.__len__():]
            prevURL = prevURL[:prevURL.find('"')]
#            print("Prev URL:\t{}".format(prevURL)) # DEBUGGING
#            currentURL = targetComicURL + prevURL # Not necessary since it's a full URL
            currentURL = prevURL
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

    try:
        comic = urlopen(currentURL)
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


