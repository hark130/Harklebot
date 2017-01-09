# Fix Existing Code #
    * OotS Scraper
        * Find 'latest' first 
        * GitP doesn't have a default-first URL like most
        * GitP includes a 'first' on their webpage
        * Add check to verify this is the 'first'
    * SMBC Scraper
        * Reset 'home' once it's done downloading (Already complete?)
        * Determine why 'prev' algorithm wraps around to 'last' after reaching 'first'
    * Template_Scraper.py
        * Penny Arcade
            * Old scraper loops around to newest once it hits oldest (why?)
            * Should stop when it hits first
            * Adapt Penny Arcade scraper from Template and test
        * Modify code to check for 'first' file after hitting max skips.  Continue(?) if not there.
        * Can't find a predictable method of ordering images (see: Awkward Zombie):
            *   Provide a counter if a date is not found (e.g., if dateTime == '', counter = ???)
                *   -or-
            *   Strip some numbering scheme off the server's filename
                *   -or-
            *   Is it possible to strip metadata off the downloaded file?
        * Store 404 images and/or their URLs and come back to them later?
        * Extricate duplicate code into Scraper_Functions_v2 (e.g., is this relative or an absolute URL, strip a string through slicing)
        * Sometimes there's redundancy between nav-back and base URL.
            * Utilize base URL for relative URL assignment?
            * .find() functionality to find an overlap match? (e.g., www.blah.com/comic/ & /comic/imgs/2016/01/...)
        * ROBOTS.TXT!
        * (Expanded) List of acceptable image file extensions
        * XKCD
            * Template adaption needed a little mangling since //imgs.xkcd.com doesn't meet the full URL requirement
            * Even if it did, urllib doesn't like URLs like //imgs.xkcd.com/comics/team_chat.png
            * Temp fix... .replace('//', 'http://')
            * Also had to manually size the 'name' (see: Comic #) to ensure width, but there may be no fix for that
            * Also, the algorithm did not have a good way of skipping over non-image content (see: Interactive flash shenanigans)
            * Changing image URLs cause problems with the full URl indicator list (see: http://www.xkcd.com/1526/)... had to shoe horn in something to trim garbage off the beginning of the imageURL prior to urlopen()
        * SMBC
            * Some of the downloads did not come with a date.  What gives?  (e.g., Car Seat, Life Changes, The Largest Number)
            * When starting at the first page, "random" link is read as "first" link.  Consider .split(</div>) instead of or
            in addition to the .split(<a>) when first determining the "first" link.
    * trim_the_name() (Scraper Functions)
        * Implement check for forbidden filename characters

# Complete In-Progress Code #
    * PvP Scraper
        * In the history of their site, absolute URLs become relative
        * Include something to dynamically determine what type of URL it's reading
    * Write unittests for get_root_URL() in Robot_Reader_Function_Tests.py
    * **Finish testing parse_robots_txt()**

# Backlog #
    * **Write Robot Reader functions to parse boolean dictionary returned by get_page_disposition()**
    * Sanitize current scraper into 'template_scraper.py'
    * Transition previously functional scrapers into newer template_scraper.py
    * Write Cyanide and Happiness Scraper
    * Write Accursed Dragon Scraper
    * Transition 'template_scraper.py' into an object oriented solution (see: Scraper Class)
