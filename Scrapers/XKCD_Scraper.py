### TO DO ###
# Some pages hold a .jpg instead of a .png

#from urllib import request
from urllib.request import urlopen
from urllib.request import urlretrieve
import urllib.error
import sys, os, time, random

defaultFilename = 'XKCD_Webcomic_'
targetWebsiteURL = 'http://www.xkcd.com'
currentURL = targetWebsiteURL
currentFileExtension = '.png'
imageURL = ''
# SAVE_PATH = os.getcwd() # old save location
SAVE_PATH = os.path.join(os.environ['USERPROFILE'], 'Pictures', 'xkcd')
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
    xkcd = urlopen(currentURL)
except urllib.error.URLError as error:
    print("ERROR:\t{} - {}".format(type(error),error))
    sys.exit()
else:
    print("\nOpened URL:\t{}".format(currentURL)) # DEBUGGING

# TESTING/LEARNING/DEBUGGING
#print("\nXKCD Headers:")
#for num, header in enumerate(xkcd.getheaders()):
#    print("Header #{}:\t{}".format(num,header))

while xkcd.getcode() == 200:
    # DETERMINE CHARSET OF PAGE
#    print("\nXKCD Charset:")
    xkcdContentType = xkcd.getheader('Content-Type')
    xkcdCharset = xkcdContentType[xkcdContentType.find('=') + 1:]
#    print("Charset:\t{}".format(xkcdCharset)) # DEBUGGING

    # PARSE HTML FOR IMAGE 2x.PNG URL
#    print("\nFetching Image URL:")
    xkcdContent = xkcd.read()
    xkcdContentDecoded = xkcdContent.decode(xkcdCharset)
    xkcdHTML = xkcdContentDecoded.split('\n')
    #print(xkcdContentDecoded)
    #print(xkcdHTML)
    for entry in xkcdHTML:
        if entry.find('2x.png') >= 0:
            # Trim the url
            imageURL = entry[entry.find('srcset="') + 'srcset="'.__len__():]
            imageURL = imageURL[:imageURL.find('.png') + '.png'.__len__()]
            currentFileExtension = '.png'
            break       # Found it. Stop looking now

    # DIDN'T FIND IMAGE 2x.PNG?  LOOK FOR NORMAL.PNG
    if imageURL.__len__() == 0:
        for entry in xkcdHTML:
            if entry.find('.png') >= 0 and entry.find('<img src="//imgs.xkcd.com/comics/') >= 0:
                imageURL = entry[entry.find('<img src="') + '<img src="'.__len__():]
                imageURL = imageURL[:imageURL.find('.png') + '.png'.__len__()]
                currentFileExtension = '.png'
                break       # Found it. Stop looking now      

    # DIDN'T FIND A .PNG?  MUST BE A .JPG
    if imageURL.__len__() == 0:
        for entry in xkcdHTML:
            if entry.find('.jpg') >= 0 and entry.find('<img src="//imgs.xkcd.com/comics/') >= 0:
                imageURL = entry[entry.find('<img src="') + '<img src="'.__len__():]
                imageURL = imageURL[:imageURL.find('.jpg') + '.jpg'.__len__()]
                currentFileExtension = '.jpg'
                break       # Found it. Stop looking now                 

    if imageURL.__len__() > 0:
        print("Image URL:\t{}".format(imageURL)) # DEBUGGING
    else:
        print("Did not find an image URL!")
#        sys.exit()

    # PARSE IMAGE.PNG URL FOR FILENAME
    ## http://xkcd.com/1771/<br />
    if imageURL.__len__() > 0:
        for entry in xkcdHTML:
            if entry.find('Permanent link to this comic') >= 0:
        #        print("Trim this:\t{}".format(entry)) # DEBUGGING
                incomingFilename = entry[entry.find('http://xkcd.com/') + 'http://xkcd.com/'.__len__():]
                incomingFilename = incomingFilename[:incomingFilename.find('/')]
                numZeros = 4 - incomingFilename.__len__()

                filenamePreamble = defaultFilename
                # Pad the filename for fixed width
                if numZeros > 0:
                    while numZeros > 0:
                        filenamePreamble = filenamePreamble + str('0')
                        numZeros -= 1
                incomingFilename = filenamePreamble + incomingFilename + currentFileExtension # Used to be '.png'
    #            print("Filename:\t{}".format(incomingFilename)) # DEBUGGING
                break

    # RETRIEVE THE FILE
    if imageURL.__len__() > 0:
        if os.path.exists(os.path.join(SAVE_PATH, incomingFilename)) == False:
            try:
                urlretrieve('http:' + imageURL, os.path.join(SAVE_PATH, incomingFilename))
            except Exception as error:
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
    if currentURL == targetWebsiteURL + '/1/':
        print("Finished scraping")
        break
    elif numSkips >= MAX_SKIPS and MAX_SKIPS > 0:
        print("{} files already found.\nEnding scrape.".format(numSkips))
        break

    # PROCEED TO THE PREVIOUS PAGE
    ## "prev" href="
#    print(xkcdHTML) # DEBUGGING
    for entry in xkcdHTML:
        if entry.find('"prev" href="') >= 0:
#            print("Trim this:\t{}".format(entry)) # DEBUGGING
            prevURL = entry[entry.find('"prev" href="') + '"prev" href="'.__len__():]
            prevURL = prevURL[:prevURL.find('/', 1) + 1]
#            print("Prev URL:\t{}".format(prevURL)) # DEBUGGING
            currentURL = targetWebsiteURL + prevURL
#            print("Prev URL:\t{}".format(currentURL)) # DEBUGGING
            break

    # RESET TEMP VARIABLES TO AVOID DUPE DOWNLOADS AND OTHER ERRORS
    incomingFilename = ''
    filenamePreamble = ''
    imageURL = ''
    currentFileExtension = ''

    try:
        xkcd = urlopen(currentURL)
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


