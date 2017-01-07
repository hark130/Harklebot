# Fix Existing Code #
    * **Repository creation/folder segmentation likely broke all the relative references to necessary modules... clone and fix!**
    * OotS Scraper
        * Find 'latest' first 
        * GitP doesn't have a default-first URL like most
        * GitP includes a 'first' on their webpage
    * SMBC Scraper
        * Reset 'home' once it's done downloading (Already complete?)
        * Determine why 'prev' algorithm wraps around to 'last' after reaching 'first'

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
