# Fix Existing Code #
    [ ] OotS Scraper
        [ ] Find 'latest' first 
        [ ] GitP doesn't have a default-first URL like most
        [ ] GitP includes a 'first' on their webpage
        [ ] Add check to verify this is the 'first'
    [ ] get_image_filename() [Version 1-3?]
        [ ] Consider changing list of nameSearch and string nameEnding to a dictionary combinations
        [ ] Build a get_image_name function since there's already a get_image_date function and have get_image_filename()
        glue them together?
        [ ] New everything.lower() then cleanup_filename function can't go back and find the original case-sensitive version in the html string.  Consider storing the original html string version prior to cleanup_filename function call (see: PVP - 20151231_Christmas-Special-2015-Part-19)
    [/] Template_Scraper.py
        [ ] Wrap the new function calls in try/except/else statements since the new functions raise Exceptions
        [ ] Auto-determine USER_AGENT by
            [ ] Dynamically determining the operating system (feasible)
            [ ] Reading the web browsers USER_AGENT (but how?)
        [ ] Modify code to check for 'first' file after hitting max skips.  Continue(?) if not there. 
        (This requires extrication of is_this_URLs_file_already_downloaded(URL) into a Scraper Function function)
        [ ] Can't find a predictable method of ordering images (see: Awkward Zombie).  Try one of the following:
            [ ]   Provide a counter if a date is not found (e.g., if dateTime == '', counter = ???)
            [ ]   Strip some numbering scheme off the server's filename
            [ ]   Is it possible to strip metadata off the downloaded file?
        [ ] Store 404 images and/or their URLs and come back to them later?
        (This requires extrication of is_this_URLs_file_already_downloaded(URL) into a Scraper Function function)
        [ ] Extricate duplicate code into Scraper_Functions (e.g., is this relative or an absolute URL, strip a string through slicing)
        [ ] Sometimes there's redundancy between nav-back and base URL.
            [ ] Utilize base URL for relative URL assignment?
            [ ] .find() functionality to find an overlap match? (e.g., www.blah.com/comic/ & /comic/imgs/2016/01/...)
        [ ] ROBOTS.TXT!
        [ ] (Expanded) List of acceptable image file extensions
        [ ] XKCD
            [ ] Template adaption needed a little mangling since //imgs.xkcd.com doesn't meet the full URL requirement
            [ ] Even if it did, urllib doesn't like URLs like //imgs.xkcd.com/comics/team_chat.png
            [ ] Temp fix... .replace('//', 'http://')
            [ ] Also had to manually size the 'name' (see: Comic #) to ensure width, but there may be no fix for that
            [ ] Also, the algorithm did not have a good way of skipping over non-image content (see: Interactive flash shenanigans)
            [ ] Changing image URLs cause problems with the full URl indicator list (see: http://www.xkcd.com/1526/)... had to shoe horn in something to trim garbage off the beginning of the imageURL prior to urlopen()
    [ ] trim_the_name() (Scraper Functions)
        [ ] Implement check for forbidden filename characters

# Complete In-Progress Code #
    [ ] Write unittests for get_root_URL() in Robot_Reader_Function_Tests.py
    [ ] **Finish testing parse_robots_txt()**

# Backlog #
    [ ] **Write Robot Reader functions to parse boolean dictionary returned by get_page_disposition()**
    [ ] Sanitize current scraper into 'template_scraper.py'
    [ ] Transition previously functional scrapers into newer template_scraper.py
    [ ] Write Cyanide and Happiness Scraper
    [ ] Write Accursed Dragon Scraper
    [ ] Transition 'template_scraper.py' into an object oriented solution (see: Scraper Class)
    [ ] Dynamically determine which USER_AGENT string to use based on operating system
    [ ] Consider extricating relative-URL-made-absolute-URL algorithm into a Scraper Function module function:
        [ ] Allow for overlap between the relative URL and the baseURL
        [ ] Allow for odd URLs that urllib does not like such as '//imgs.xkcd.com/comics/team_chat.png'

# Version 1-2 Completed
    [X] Template_Scraper.py
        [X] Validate each reused variable after code is refactored in Version 1-2
        [X] Penny Arcade
            [X] Old scraper loops around to newest once it hits oldest (why?)
            [X] Should stop when it hits first
            [X] Adapt Penny Arcade scraper from Template and test
        [X] SMBC
            [X] Some of the downloads did not come with a date.  What gives?  (e.g., Car Seat, Life Changes, The Largest Number)
            Answer:  They legitimately don't have an appropriate date on that page.  Not even find_the_date() gets it right.
            [X] When starting at the first page, "random" link is read as "first" link.  Consider .split(</div>) instead of or
            in addition to the .split(<a>) when first determining the "first" link.
        [X] PvP Scraper
            [X] In the history of their site, absolute URLs become relative
            [X] Include something to dynamically determine what type of URL it's reading
