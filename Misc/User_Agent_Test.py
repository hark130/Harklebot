from urllib.request import urlopen
from urllib.request import urlretrieve
from urllib.request import Request
import urllib.error

USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0' # http://www.whoishostingthis.com/tools/user-agent/
currentURL = 'http://www.whoishostingthis.com/tools/user-agent/'
searchStart = '<div class="info-box user-agent">'
searchStop = '</div>'
userAgent = ''

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

# TRANSLATE PAGE
try:
    comicCharset = 'UTF-8' # DEFAULT
    comicContent = comic.read()
    comicContentDecoded = comicContent.decode(comicCharset, 'ignore')
except UnicodeError as error:
    print("Unable to decode URL {} with charset {}".format(currentURL, comicCharset))
    print("ERROR:\t{}\n{}".format(type(error),error))
    sys.exit()
else:
    comicHTML = comicContentDecoded.split('\n')

# FIND THE USER AGENT
try:
    for entry in comicHTML:
        if entry.find(searchStart) >= 0:
            userAgent = entry[entry.find(searchStart) + searchStart.__len__():]
            userAgent = userAgent[:userAgent.find(searchStop)]
            break
except Exception as error:
    print("Unable to decode URL {} with charset {}".format(currentURL, comicCharset))
    print("ERROR:\t{}\n{}".format(type(error),error))
    sys.exit()  
else:
    print("Your manufactured user agent is:\t{}".format(userAgent))




# OPEN THE WEB PAGE AGAIN
try:
    comicRequest = Request(currentURL)
    comic = urlopen(comicRequest)
except urllib.error.URLError as error:
    print("\nCannot open URL:\t{}".format(currentURL))
    print("ERROR:\t{} - {}".format(type(error),error))
    sys.exit()
else:
    print("\nOpened URL:\t{}".format(currentURL)) # DEBUGGING

# TRANSLATE PAGE
try:
    comicCharset = 'UTF-8' # DEFAULT
    comicContent = comic.read()
    comicContentDecoded = comicContent.decode(comicCharset, 'ignore')
except UnicodeError as error:
    print("Unable to decode URL {} with charset {}".format(currentURL, comicCharset))
    print("ERROR:\t{}\n{}".format(type(error),error))
    sys.exit()
else:
    comicHTML = comicContentDecoded.split('\n')

# FIND THE USER AGENT
try:
    for entry in comicHTML:
        if entry.find(searchStart) >= 0:
            userAgent = entry[entry.find(searchStart) + searchStart.__len__():]
            userAgent = userAgent[:userAgent.find(searchStop)]
            break
except Exception as error:
    print("Unable to decode URL {} with charset {}".format(currentURL, comicCharset))
    print("ERROR:\t{}\n{}".format(type(error),error))
    sys.exit()  
else:
    print("Your actual user agent is:\t{}".format(userAgent))
  
