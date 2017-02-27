# CURRENT SPRINT #
# Version 1-4 (Refinement) On Deck
    [ ] get_image_filename() [Version 1-3?]
        [ ] Consider changing list of nameSearch and string nameEnding to a dictionary combinations
        [ ] Build a get_image_name function since there's already a get_image_date function and have get_image_filename()
        glue them together?
    [ ] Refactor necessary Scraper Functions to utilize urlparse functionality (e.g., get root, valid URL)
    [ ] Write Accursed Dragon Scraper
    [ ] Wrap the new function calls in try/except/else statements since the new functions raise Exceptions
    [ ] Verify the XKCD Scraper
        [ ] Also, the algorithm did not have a good way of skipping over non-image content (see: Interactive flash shenanigans)
        [ ] Changing image URLs cause problems with the full URl indicator list (see: http://www.xkcd.com/1526/)... had to shoe horn in something to trim garbage off the beginning of the imageURL prior to urlopen()


# BACKLOG #
# New Functionality #
    [/] Template_Scraper.py
        [ ] Modify code to check for 'first' file after hitting max skips.  Continue(?) if not there. 
        (This requires extrication of is_this_URLs_file_already_downloaded(URL) into a Scraper Function function)
        [ ] Can't find a predictable method of ordering images (see: Awkward Zombie).  Try one of the following:
            [ ]   Provide a counter if a date is not found (e.g., if dateTime == '', counter = ???)
            [ ]   Strip some numbering scheme off the server's filename
            [ ]   Is it possible to strip metadata off the downloaded file?
        [ ] Store 404 images and/or their URLs and come back to them later?
        (This requires extrication of is_this_URLs_file_already_downloaded(URL) into a Scraper Function function)
        [ ] (Expanded) List of acceptable image file extensions
    [ ] Transition 'template_scraper.py' into an object oriented solution (see: Scraper Class)(Version 2-1)
    [ ] Dynamically determine which USER_AGENT string to use based on operating system. Auto-determine USER_AGENT by
        [ ] Dynamically determining the operating system (feasible)
        [ ] Reading the web browsers USER_AGENT (but how?)
    [ ] Add fidelity to is_URL_valid()
        [ ] Test that start indicators are at the beginning
        [ ] Test that stop indicators are at the end or immediately followed by a slash (/)
        [/] Include regex check for invalid URL characters (/^([!#$&-;=?-[]_a-z~]|%[0-9a-fA-F]{2})+$/) see:
            ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-._~:/?#[]@!$&'()*+,;=.
        [ ] Add fidelity to verify allowed characters are utilized properly (see: ftp://username:password@domain)
        [ ] Add some manner of sub-search which validates HTML codes from the .findall(URL) results
# Bugs #
    [ ] Write check for forbidden filename characters into trim_the_name() (Scraper Functions)
    [ ] Verify get_the_filename()/get_the_date()
        [ ] False positives on filename dates (see: http://www.xkcd.com/1779/... reading 20170120 just from 2017?!


# PREVIOUS SPRINTs #
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

# Version 1-3 (Robot Reader) In Progress 
    [X] Template_Scraper.py
        [X] ROBOTS.TXT!
        [X] Implement is_URL_valid()
    [X] OotS Scraper
        [X] Find 'latest' first 
        [X] GitP doesn't have a default-first URL like most
        [X] GitP includes a 'first' on their webpage
        [X] Add check to verify this is the 'first'
    [X] Consider extricating relative-URL-made-absolute-URL algorithm into a Scraper Function module function:
        [X] Allow for overlap between the relative URL and the baseURL
        [X] Allow for odd URLs that urllib does not like such as '//imgs.xkcd.com/comics/team_chat.png'
    [X] is_URL_abs() (Scraper Functions)
    [X] **Write Robot Reader functions to parse boolean dictionary returned by get_page_disposition()**
        [X] Extricate duplicate code into Scraper_Functions
            [X] Is this relative or an absolute URL <=-- Do this next and use it to fix XKCD's 'First' wrap-around problem
            [X] Fix problems with link that urllib doesn't like (see: //imgs.xkcd.com/comics/team_chat.png) <=-- Do this next and use it to fix XKCD's 'First' wrap-around problem
            [X] Sometimes there's redundancy between nav-back and base URL.
                [X] Utilize base URL for relative URL assignment?
                [X] .find() functionality to find an overlap match? (e.g., www.blah.com/comic/ & /comic/imgs/2016/01/...)
    [X] **Finish testing parse_robots_txt()**
    [X] XKCD
        [X] Template adaption needed a little mangling since //imgs.xkcd.com doesn't meet the full URL requirement
        [X] Even if it did, urllib doesn't like URLs like //imgs.xkcd.com/comics/team_chat.png
        [X] Temp fix... .replace('//', 'http://')
        [X] Also had to manually size the 'name' (see: Comic #) to ensure width, but there may be no fix for that
    [X] New everything.lower() then cleanup_filename function can't go back and find the original case-sensitive version in the html string.  Consider storing the original html string version prior to cleanup_filename function call (see: PVP - 20151231_Christmas-Special-2015-Part-19)
    [/] Write Cyanide and Happiness Scraper
    [ ] Write unittests for get_root_URL() in Robot_Reader_Function_Tests.py
