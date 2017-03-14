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
# Version 1.1
#   FIXED:  urlopen() doesn't like spaces in the URL
#           Example - http://www.smbc-comics.com/comics/1481723478-20161214 (1) (1).png
#           Called replace to change spaces to %20
#   FIXED:  False "full URL" hits from some URLs.  
#           Example - http://pvponline.com/comic/awwwhes-just-like-my-cat
#           Added some specificity to fullURLIndicatorList
#   FIXED:  First URL would find the wrong URL if starting on the first page
#           Example - http://www.smbc-comics.com/comic/2002-09-05 would consider
#               the random link to be the first link
#           Added a .split(</div>) to the First URL and Prev URL parsing
#   ADDED:  A safety check to verify the filename hasn't exceeded 255 characters
#################################################################################
#################################################################################
# Version 1.2
#   ADDING: If max download skips have been exceeded, check the first URL link
#               to see if it's been downloaded yet.  If so, stop scraping.
#               If not, continue scraping since we obviously haven't finished
#               yet.  If max download skips have been exceeded but there's not
#               first URL link then stop scraping as we have no way to know
#               if we're already done or not.
#   FIXED:  Slightly less hacky version of the sys.append statement to point
#               to the modules that are in a different directory
#   MODS:   This involves extricating imageURL --> filename conversion into the
#               scraper functions module.
# Version 1.2.1
#   FIXED:  Relative (vs Absolute) URL checks now utilize rootURL instead of
#               baseURL (CAD-Sillies was breaking)
#   ADDED:  is_URL_abs() functionality
#           make_rel_URL_abs() functionality
#           Incorporated is_URL_valid() into Template
#           Adding fidelity to the sys.path append to find the "Modules" folder
#           Start at 'Latest' functionality
#################################################################################
#################################################################################
# Version 1.3
#   ADDING: get_page_disposition() functionality
#   ADDING: robots_may_I() functionality
#   ADDING: Crawl-delay considerations
#################################################################################
#################################################################################
# Version 1.4
#   MOVING:     Extricating code into a find_the_name function that takes a dictionary
#   MODIFYING:  get_image_filename calls find_the_name instead of doing the work
#   MODIFYING:  Template_Scraper should construct a dictionary to pass to get_image_filename
#################################################################################


from urllib.request import urlopen
from urllib.request import urlretrieve
from urllib.request import Request
import urllib.error
import sys, os, time, random, re
from urllib.error import HTTPError

################
# LOAD MODULES #
################
from Scraper_Functions import is_URL_valid
from Scraper_Functions import find_a_URL 
from Scraper_Functions import get_image_filename
from Scraper_Functions import make_rel_URL_abs
from Robot_Reader_Functions import get_page_disposition
from Robot_Reader_Functions import robots_may_I

# Hacky (?) method to keep Harklebot modules separate from scraper code
## Verify path exists before adding it to sys.path
modulesPath = os.path.join(os.path.dirname(os.getcwd()), 'Modules')
if os.path.isdir(modulesPath) is True:
    print("Modules found at:\t{}".format(modulesPath)) # DEBUGGING
    sys.path.append(modulesPath)
else:
    print("Modules path not found") # DEBUGGING
    pass
################
################
################

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

### LATEST URL SETUP ###
# Fine the 'name' of the 'latest comic' navigation button
latestSearchPhrase = '___UPDATE___' # Probably 'Last' <=--------------------------=UPDATE=--------------------------=>

### PREV URL SETUP ###
# Find the 'name' of the obligatory 'Previous Comic' navigation button
prevSearchPhrase = '___UPDATE___' # Probably 'Prev' <=--------------------------=UPDATE=--------------------------=>

### FIRST URL SETUP ###
# Find the 'name' of the (mostly) obligatory 'First Comic' navigation button
# Set this to an empty string if the webcomic page does not provide for a 'First' navigation button
firstSearchPhrase = '___UPDATE___' # Probably 'First' <=--------------------------=UPDATE=--------------------------=>

### DATE PARSING SETUP ###
# This boolean determines the nature of the date search:  False == mandatory date, True == optional date
skipDateIfNotFound = False # False for most pages <=--------------------------=UPDATE=--------------------------=>
# Find the date from a list of strings to match in the page's HTML
dateSearchPhrase = ['___UPDATE___'] # Commonly == imageSearchPhrase <=--------------------------=UPDATE=--------------------------=>

### NAME PARSING SETUP ###
# Find the title of the image by searching for the following phrase in the HTML.  Could be in an imageURL tag, webpage title, or social media 'share' link
nameSearchPhrase = ['___UPDATE___', '___UPDATE___', '___UPDATE___'] # Probably ['alt="'] <=--------------------------=UPDATE=--------------------------=>
# Delimit the end of the image title with this string
nameEnding = ['___UPDATE___', '___UPDATE___', '___UPDATE___'] # Probably ['"'] <=--------------------------=UPDATE=--------------------------=>
################################################
# Modify these variables based on HTML details #
################################################

########################
### STATIC VARIABLES ###
########################
#USER_AGENT = 'Harklebot'   # We're almost ready to reveal ourselves to the Interwebs!
USER_AGENT = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:50.0) Gecko/20100101 Firefox/50.0' # http://www.whoishostingthis.com/tools/user-agent/
#USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0' # http://www.whoishostingthis.com/tools/user-agent/
MAX_SLEEP = 30              # SECONDS
MAX_EXISTING_SKIPS = 10     # Max number of existing files to skip over before stopping
MAX_404_SKIPS = 10          # Max number of missing images to skip over before stopping
MAX_FILENAME_LEN = 254      # Normal OS have it at 255.  Sub one for nul char(?)... just in case.
random.seed()
validFileTypeList = ['.png', '.jpg', '.gif']
obeyTheRobots = True        # Indicates whether or not the scraper will adhere to the 'recommendations' of the robots.txt file
########################
# Script constants #####
########################

#########################
### DYNAMIC VARIABLES ###
#########################
###################################################
# 0. Build the nameSearchPairs Ordered Dictionary #
###################################################
nameSearchPairs = OrderedDict()

## 0.1. INPUT VALIDATION
### 0.1.1. nameSearchPhrase --> list
if isinstance(nameSearchPhrase, str) is True:
    nameSearchPhrase = list(nameSearchPhrase)
elif isinstance(nameSearchPhrase, list) is False:
    raise TypeError('nameSearchPhrase is not a string or a list')
### 0.1.2. nameEnding --> list
if isinstance(nameEnding, str) is True:
    nameEnding = list(nameEnding)
elif isinstance(nameEnding, list) is False:
    raise TypeError('nameEnding is not a string or a list')
### 0.1.3. Test content
#### 0.1.3.1. Verify it isn't empty
if nameSearchPhrase.__len__() == 0 or nameEnding.__len__() == 0:
    raise ValueError('Name search criteria is required')
#### 0.1.3.2. Verify nameSearchPhrase only contains strings
for phrase in nameSearchPhrase:
    if isinstance(phrase, str) is False:
        raise TypeError('Name search criteria contains a non-string')
#### 0.1.3.3. Verify nameEnding only contains strings
for phrase in nameEnding:
    if isinstance(phrase, str) is False:
        raise TypeError('Name search criteria contains a non-string')

## 0.2. Validate the length to build the dictionary
if nameSearchPhrase.__len__() == nameEnding.__len__():
    for key, value in zip(nameSearchPhrase, nameEnding):
        nameSearchPairs[key] = value
elif nameSearchPhrase.__len__() > 0 and nameEnding.__len__() == 1
    for key in nameSearchPhrase:
        nameSearchPairs[key] = nameEnding[0]
else:
    raise ValueError('Mismatch in number of name search criteria')
    
## 0.3. Check your work
if nameSearchPairs.keys().__len__() == 0:
    raise ValueError('Name search criteria is missing keys')
elif nameSearchPairs.values().__len__() == 0:
    raise ValueError('Name search criteria is missing values')
else:
    print('Name search criteria has been built') # DEBUGGING
    pass
###################################################
# Built the nameSearchPairs Ordered Dictionary ####
###################################################

# Windows 7 home path environment variable
if 'USERPROFILE' in os.environ:
    SAVE_PATH = os.path.join(os.environ['USERPROFILE'], 'Pictures', webComicName)
# Ubuntu 16.04 LTS home path environment variable
elif 'HOME' in os.environ:
    SAVE_PATH = os.path.join(os.environ['HOME'], 'Pictures', webComicName)
# ./Pictures/
else:
    SAVE_PATH = os.path.join('Pictures', webComicName)    
# No longer needs rootURL... this kludge was properly replicated in make_rel_URL_abs()
#rootURL = get_root_URL(baseURL)
defaultFilename = webComicName + '_Webcomic_' 
currentURL = targetComicURL
firstURL = ''               # Holds 'first' URL and determines when to stop scraping
latestURL = ''              # Holds 'lastest' URL in case root webpage doesn't default to the 'lastest' comic (see: OotS)
# No longer needs fullURLIndicatorList... functionality extricated into is_URL_abs()
#fullURLIndicatorList = [rootURL, baseURL, 'www.', 'http:']
numExistingSkips = 0        # Variable to store the number of files already found
num404Skips = 0             # Variable to store the number of missing webpages
skipping = True             # Boolean variable used to determine when to 'fast forward' past image URLs that have already been downloaded
page_disposition = {baseURL:True} # Dictionary that holds the results of parsing a site's robots.txt file
crawlDelay = 0              # Variable to store a site's desired crawl speed based on the robots.txt file
#########################
# Run time update #######
#########################

######################
### TEMP VARIABLES ###
######################
incomingFilename = ''       # Local filename to save the incoming image download
imageURL = ''               # Trimmed image URL
currentFileExtension = ''   # File extension of current image to download
prevURL = ''                # Holds the URL associated with the 'Previous Comic' navigation link
tempPrefix = ''             # Used to dynamically determine between relative and absolute URLs
imageNameSuffix = ''        # Holds the unique filename suffix (missing prefix and filename extension)
######################
# Reset each loop ####
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

# READ ROBOTS.TXT
try:
    page_disposition = get_page_disposition(baseURL, USER_AGENT)
except HTTPError as err:
    if err.code == 404:
        print("{} does not appear to have a robots.txt file.".format(baseURL))
        page_disposition = {'/':True} # Allow everything
    else:
        raise(err)
except Exception as err:
    print("Error with get_page_disposition({}, {})".format(baseURL, USER_AGENT))
    print(repr(err))
else:
    if 'Crawl-delay:' in page_disposition.keys():
        if isinstance(page_disposition['Crawl-delay:'], int) is True:
            crawlDelay = page_disposition['Crawl-delay:']   

# COMMENCE SCRAPING
while True:
#while comic.getcode() == 200:
    # 1. OPEN THE WEB PAGE
    ## 1.1. Verify URL is valid
    try:
        if is_URL_valid(currentURL) is False:
            print("Invalid URL:\t{}".format(currentURL)) # DEBUGGING
            sys.exit()
    except Exception as err:
        print(repr(err))
        sys.exit()

    ## 1.2. Open the URL
    try:
        # Will we follow the recommendations of the robots.txt file with regards to Crawl-delay?
        if obeyTheRobots is True and crawlDelay > 0:
            # https://youtu.be/Udj-o2m39NA
            print("Sleeping {} seconds before requesting the next page".format(crawlDelay))
            time.sleep(crawlDelay)

        comicRequest = Request(currentURL, headers={'User-Agent': USER_AGENT})
        comic = urlopen(comicRequest)
    except urllib.error.URLError as error:
        print("\nCannot open URL:\t{}".format(currentURL))
        print("ERROR:\t{} - {}".format(type(error),error))
        sys.exit()
    else:
        print("\nOpened URL:\t{}".format(currentURL)) # DEBUGGING
        if skipping == False:
            # Randomize a value between 0 and MAX_SLEEP
            sleepyTime = random.randrange(0, MAX_SLEEP)

            # Will we follow the recommendations of the robots.txt file with regards to Crawl-delay?
            if obeyTheRobots is True:
                # If so, add the Crawl-delay value from the robots.txt file to the randomized sleep time
                sleepyTime = sleepyTime + crawlDelay

            # https://youtu.be/Udj-o2m39NA
            print("Sleeping {} seconds before download".format(sleepyTime))
            time.sleep(sleepyTime)


    # 2. DETERMINE CHARSET OF PAGE
#    print("\ncomic Charset:")
    comicContentType = comic.getheader('Content-Type')

    if comicContentType.find('=') < 0 or comicContentType.find('charset') < 0:
        comicCharset = 'UTF-8'
    else:
        comicContentType = comicContentType[comicContentType.find('charset'):]
        comicCharset = comicContentType[comicContentType.find('=') + 1:]
        comicCharset = comicCharset.replace(' ','')
#    print("Charset:\t{}".format(comicCharset)) # DEBUGGING


    # 3. TRANSLATE PAGE
    comicContent = comic.read()

    try:
#        comicCharset = 'UTF' # TESTING
        comicContentDecoded = comicContent.decode(comicCharset, 'ignore')
    except UnicodeError as error:
        print("Unable to decode URL {} with charset {}".format(currentURL, comicCharset))
        print("ERROR:\t{}\n{}".format(type(error),error))
        sys.exit()
    else:
#        comicHTML = comicContentDecoded.split('\n') # No longer necessary in Version 1-2
        # Sometimes, the name and/or date is in the URL (see: OotS)
        comicContentDecoded = currentURL + '\n' + comicContentDecoded # Prepend the HTML with the URL
        pass

#    print("\nFetching Latest URL:") # DEBUGGING
    # 4. FIND THE LATEST URL
    # Sites like Order of the Stick (OotS) do not default to their latest comic... they link to it
    # Don't do this if:
    #       latestSearchPhrase is not configured
    #       The target URL doesn't match the base (see: root) URL (an indication the script wanted to skip ahead)
    #       latestURL has already been assigned (it's already been found)
    if latestSearchPhrase.__len__() > 0 and targetComicURL == baseURL and latestURL.__len__() == 0:
        try:
            latestURL = find_a_URL(comicContentDecoded, latestSearchPhrase, 'href="', '"')

            latestURL = latestURL.replace('"', '') # find_a_URL() leaves the [searchEnd] on the return value
        except Exception as err:
            print("Error encountered with find_a_URL('latest')!") # DEBUGGING
            print(repr(err))
        else:
            if latestURL.__len__() > 0:
                try:
                    latestURL = make_rel_URL_abs(baseURL, latestURL)
                except Exception as err:
                    print("Error encountered with make_rel_URL_abs('latest')!") # DEBUGGING
                    print(repr(err))
    #                sys.exit() # Harsh... Not a big deal if you can't find 'latest' because this might be it
                else:
                    print("Latest URL:\t{}".format(latestURL)) # DEBUGGING 
                    currentURL = latestURL
                    continue # Go back to the top of the while loop

            
#    print("\nFetching First URL:") # DEBUGGING
    # 5. FIND THE FIRST URL
    # NEW PROCEDURE FOR VERSION 1-2
    # find_a_URL(htmlString, [searchPhrase], [searchStart], [searchEnd])

    ## 5.1. Find the first URL if there isn't already one
    if firstURL.__len__() == 0 and firstSearchPhrase.__len__() > 0:
        try:
            firstURL = find_a_URL(comicContentDecoded, firstSearchPhrase, 'href="', '"')
        except Exception as err:
            print("Error encountered with find_a_URL()!") # DEBUGGING
            print(repr(err))
            sys.exit() # Harsh...
        else:
            firstURL = firstURL.replace('"', '') # find_a_URL() leaves the [searchEnd] on the return value

    ## 5.2. Validate findings
    ### 5.2.1. firstURL empty and this is the first stop
    if firstURL.__len__() == 0 and (currentURL == targetComicURL or currentURL == latestURL): # Only check on first run
        #### 5.2.1.1. Check for search criteria... Sometimes, there's no "First URL" to find... Only print on first run
        if firstSearchPhrase.__len__() == 0: # and firstURL.__len__() == 0:
            print("First URL search criteria not configured.") # DEBUGGING  
        #### 5.2.2.1. If there's a search criteria configured but we didn't find a firstURL, something went wrong(?)
        else:
            print("First URL Not found with search criteria:\t{}".format(firstSearchPhrase)) # DEBUGGING  
    ### 5.2.2. Found firstURL on the first stop
    elif firstURL.__len__() > 0 and (currentURL == targetComicURL or currentURL == latestURL): # Found it first time
        #### 5.2.2.1. Ensure the firstURL is an absolute URL
        try:
            firstURL = make_rel_URL_abs(baseURL, firstURL)
        except Exception as err:
            print("Error encountered with make_rel_URL_abs()!") # DEBUGGING
            print(repr(err))
            sys.exit() # Harsh...
        else:
            print("First URL:\t{}".format(firstURL)) # DEBUGGING    

        #### 5.2.2.2. Ensure the firstURL is valid
        try:
            if is_URL_valid(firstURL) is False:
                print("Invalid URL:\t{}".format(firstURL)) # DEBUGGING
#                sys.exit() # Not necessary to abort if firstURL is not found
        except Exception as err:
            print(repr(err))
            sys.exit()


    # 6. FIND THE IMAGE .GIF
    # NEW PROCEDURE FOR VERSION 1-2
    # find_a_URL(htmlString, [searchPhrase], [searchStart], [searchEnd])
#    print("\nFetching Image URL:")
    try:
        imageURL = find_a_URL(comicContentDecoded, imageSearchPhrase, imageBeginPhrase, validFileTypeList)
    except Exception as err:
        print("Error encountered with find_a_URL()!") # DEBUGGING
        print(repr(err))
        sys.exit() # Harsh...
    else:
#        print("Image URL:\t{}".format(imageURL)) # DEBUGGING    
        pass


    # 7. CHANGE RELATIVE URLS TO ABSOLUTE URLS
    if imageURL.__len__() > 0:
        ## 7.1. Clean up any URLs that begin with '//' because Request() doesn't like them
        if imageURL.find('//') == 0:
            imageURL = 'http:' + imageURL
            
        ## 7.2. Ensure the imageURL is an absolute URL
        try:
            imageURL = make_rel_URL_abs(baseURL, imageURL)
        except Exception as err:
            print("Error encountered with make_rel_URL_abs()!") # DEBUGGING
            print(repr(err))
            sys.exit() # Harsh... consider running find_a_URL() again
        else:
#            print("Image URL:\t{}".format(imageURL)) # DEBUGGING
            pass

        ## 7.3. Ensure URL is valid
        try:
            if is_URL_valid(imageURL) is False:
                print("Invalid URL:\t{}".format(imageURL)) # DEBUGGING
                sys.exit()
        except Exception as err:
            print(repr(err))
            sys.exit()
    else:
        print("Did not find an image URL!")
        sys.exit()

        
    # 8. DETERMINE THE IMAGE FILE EXTENSION
    if imageURL.__len__() > 0:
        for extension in validFileTypeList:
            if imageURL.find(extension) == (imageURL.__len__() - extension.__len__()): # Verify the extension was found at the end
                currentFileExtension = extension
                break # Found it.  Stop looking.

        if currentFileExtension not in validFileTypeList:
            print("Unable to determine image file extension from image URL")
            sys.exit()

            
    # 9. PARSE IMAGE URL FOR FILENAME
    # NEW PROCEDURE FOR VERSION 1-2
    # get_image_filename(htmlString, [dateSearchPhrase], {nameSearchPairs}, skipDate=False)
    if imageURL.__len__() > 0:
        try:
            ## 9.1. Get the unique filename suffix (does not include prefix or file extension)
            imageNameSuffix = get_image_filename(comicContentDecoded, dateSearchPhrase, nameSearchPairs, skipDateIfNotFound)
        except Exception as err:
            print("Error encountered with get_image_filename()!") # DEBUGGING
            print(repr(err))
            sys.exit() # Harsh... consider running find_a_URL() again
        else:
#            print("Image name suffix:\t{}".format(imageNameSuffix)) # DEBUGGING
            
            if imageNameSuffix == '00000000':
                print("Unable to determine a valid filename for the image!")
                sys.exit()
            else:
                ## 9.2. Construct the local filename to save the image as
                incomingFilename = defaultFilename + imageNameSuffix + currentFileExtension

                ## 9.3. Final filename trimming
                incomingFilename = incomingFilename.replace('__','_')
                incomingFilename = incomingFilename.replace('--','-') 

                ## 9.4. Verify the intended filename hasn't exceeded the OS maximum
                if incomingFilename.__len__() > MAX_FILENAME_LEN:
                    incomingFilename = incomingFilename[:MAX_FILENAME_LEN - currentFileExtension.__len__()] + currentFileExtension      
            
#            print("Filename:\t{}".format(incomingFilename)) # DEBUGGING


    # 10. DOWNLOAD THE FILE
    if imageURL.__len__() > 0 and incomingFilename.__len__() > 0:
        ## 10.1. Verify the file doesn't exist so we're downloading it
        if os.path.exists(os.path.join(SAVE_PATH, incomingFilename)) == False:
            ### 10.1.2. Check the robots.txt for permission, if applicable
            if obeyTheRobots is False or robots_may_I(page_disposition, imageURL) is True:
                #### 10.1.2.1. Try to download it
                try:
                    # Utilizing a request-->urlopen-->write() in an attempt to...
                    # ...continue dodging websites that block webscrapers.
                    comicRequest = Request(imageURL, headers={'User-Agent': USER_AGENT})
                    with urlopen(comicRequest) as comic:
                        with open(os.path.join(SAVE_PATH, incomingFilename), 'wb') as outFile:
                            outFile.write(comic.read())

                except urllib.error.HTTPError as error:
                    print("Image failed to download:\t{}".format(imageURL))

                    #### 10.1.2.2. Handle 404 errors
                    if error.code == 404:
                        num404Skips += 1
                    #### 10.1.2.3. Abort on non 404 errors
                    else:
                        print("ERROR:\t{} - {}".format(type(error),error))
                        sys.exit()

                except Exception as error:
                    print("Image failed to download:\t{}".format(imageURL))
                    print(repr(error))
                    sys.exit()

                #### 10.1.2.4. Success   
                else:
                    print("Image URL download successful:\t{}".format(incomingFilename)) # DEBUGGING
                    skipping = False
            ### 10.1.3. Robots.txt forbids it
            else:
                print("The site forbids our access to URL:\t{}".format(imageURL))
                numExistingSkips += 1
                skipping = True

                ### 10.1.4. Some sites couple a Crawl-delay with a Disallow: /
                if crawlDelay > 0:
                    # https://youtu.be/Udj-o2m39NA
                    print("Sleeping {} seconds before moving on".format(crawlDelay))
                    time.sleep(crawlDelay)
        ## 10.2. The file exists so we're moving on
        else:
            print("Filename {} already exists.".format(incomingFilename)) # DEBUGGING
            numExistingSkips += 1
            skipping = True

            
    # 11. CHECK IF WE'VE HIT THE END
    ## 11.1. Current URL is actuall the first URL
    if currentURL == firstURL:                   # dynamically read First
        print("\nFinished scraping")
        break
    ## 11.2. We've exceeded the maximum number of skips
    elif numExistingSkips >= MAX_EXISTING_SKIPS and MAX_EXISTING_SKIPS > 0:
        print("\n{} files already found.\nEnding scrape.".format(numExistingSkips))
        break
    ## 11.3. This should only 'hit' if we start scraping on the first URL (see: Edge Case)
    elif firstURL.__len__() == 0 and firstSearchPhrase.__len__() > 0:
        print("\nMissing First URL.  We must be there.\nCurrent URL:\t{}\n".format(currentURL))
        break
    ## 11.4. We've exceeded the tolerable number of 404 errors
    elif num404Skips >= MAX_404_SKIPS:
        print("\n{} 'Not Found (404)' errors encountered.\nEnding scrape.".format(num404Skips))
        break
    ## 11.5. Penny Arcade edge case... First Comic URL different than Prev Comic URL on 2nd webpage
    ## First URL == http://www.penny-arcade.com/comic/1998/11/18
    ## Prev URL == http://www.penny-arcade.com/comic/1998/11/18/the-sin-of-long-load-times
    ## Solution... find the First URL inside the Prev URL
    elif currentURL.find(firstURL) == 0 and currentURL[firstURL.__len__():firstURL.__len__() + 1] == '/':
        print("\nFinished scraping (because we *mostly* hit the first URL)")
        print("First URL:\t{}\nCurrent URL:\t{}".format(firstURL, currentURL)) # DEBUGGING
        break

        
    # 12. PROCEED TO THE PREVIOUS PAGE
    # NEW PROCEDURE FOR VERSION 1-2
    # find_a_URL(htmlString, [searchPhrase], [searchStart], [searchEnd])
    ## 12.1. Get the URL associated with the 'Previous Comic' navigation button
    prevURL = find_a_URL(comicContentDecoded, prevSearchPhrase, 'href="', '"')

    prevURL = prevURL.replace('"', '') # find_a_URL() leaves the [searchEnd] on the return value

    ## 12.2. Validate the previous URL
    if prevURL.__len__() > 0:
        ### 11.2.1. Change relative URLs to absolute URLs
        try:
            prevURL = make_rel_URL_abs(baseURL, prevURL)
        except Exception as err:
            print("Error encountered with make_rel_URL_abs()!") # DEBUGGING
            print(repr(err))
            sys.exit() # Harsh... consider running find_a_URL() again
        else:
#            print("Prev URL:\t{}".format(prevURL)) # DEBUGGING
            currentURL = prevURL 
            # No need to validate this URL because it's validated at the top of the while loop
    else:
        print("\nMissing Previous URL.  We must be at the first page.\nCurrent URL:\t{}\n".format(currentURL))
        break


    # 13. RESET TEMP VARIABLES TO AVOID DUPE DOWNLOADS AND OTHER ERRORS
    incomingFilename = ''       # Local filename to save the incoming image download
    imageURL = ''               # Trimmed image URL
    currentFileExtension = ''   # File extension of current image to download
    prevURL = ''                # Holds the URL associated with the 'Previous Comic' navigation link
    tempPrefix = ''             # Used to dynamically determine between relative and absolute URLs
    imageNameSuffix = ''        # Holds the unique filename suffix (missing prefix and filename extension)

#    break # Artificial exit


