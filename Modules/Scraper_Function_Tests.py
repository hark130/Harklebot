from Scraper_Functions_v2 import find_the_date 

if __name__ == '__main__':

    # TEST 1 - PvP
    with open('1-Input_HTML.txt', 'r') as testFile1:
        testInput1 = testFile1.read()

    testResult1 = find_the_date(testInput1)
    print("TEST 1\t'20160726' == {}:\t{}\n".format(testResult1, testResult1 == '20160726'))

    ## TEST 2
    #testInput2 = 'DATE: 2001-01-01\ndate: 2002-02-02\nDate: 2003-03-03\nDATE: 2004/04/04\ndate: 2005/05/05\nDate:\t2006-06-06\n'
    #testResult2 = find_the_date(testInput2)
    #print("TEST 2 - {}\n".format(testResult2))

    # TEST 3 - Business Cat
    with open('3-BC_HTML.txt', 'r') as testFile3:
        testInput3 = testFile3.read()

    testResult3 = find_the_date(testInput3)
    print("TEST 3\t'20161202' == {}:\t{}\n".format(testResult3, testResult3 == '20161202'))

    ## TEST 4
    #testInput4 = 'Nothing\nNothing else\nDate:\t2016/12/20161222\n2016 was a good year\n2016-13-01\nDate 2017-12-25\nDate 1975-11-14\nDate 2001-07-31\nThis is just raw data!\t2014/12-01'
    #testResult4 = find_the_date(testInput4)
    #print("TEST 4 - {}\n".format(testResult4))

    # TEST 5 - SMBC
    with open('5-SMBC_HTML.txt', 'r') as testFile5:
        testInput5 = testFile5.read()

    testResult5 = find_the_date(testInput5)
    print("TEST 5\t'20161227' == {}:\t{}\n".format(testResult5, testResult5 == '20161227'))

    # TEST 6 - SMBC
    with open('6-SMBC_HTML.txt', 'r') as testFile6:
        testInput6 = testFile6.read()

    testResult6 = find_the_date(testInput6)
    print("TEST 6\t'20161226' == {}:\t{}\n".format(testResult6, testResult6 == '20161226'))

    # TEST 7 - Penny Arcade
    with open('7-Penny_Arcade_random_HTML.txt', 'r') as testFile7:
        testInput7 = testFile7.read()

    testResult7 = find_the_date(testInput7)
    print("TEST 7\t'20100712' == {}:\t{}\n".format(testResult7, testResult7 == '20100712'))

    # TEST 8 - xkcd
    with open('8-xkcd_random_HTML.txt', 'r') as testFile8:
        testInput8 = testFile8.read()

    testResult8 = find_the_date(testInput8)
    print("TEST 8\t'00000000' == {}:\t{}\n".format(testResult8, testResult8 == '00000000'))

############## BROKEN TESTS ##############
# Tests 9 & 10 are currently broken
# New functionality is finding daetes in
#     the side bar
# TO DO list includes ideas to improve
#     final decision algorithm
##########################################

#    # TEST 9 - OotS
##    print("TEST 9")
#    with open('9-OotS_random_HTML.txt', 'r') as testFile9:
#        testInput9 = testFile9.read()

#    testResult9 = find_the_date(testInput9)
#    print("TEST 9\t'00000000' == {}:\t{}\n".format(testResult9, testResult9 == '00000000'))

#    # TEST 10 - OotS
##    print("TEST 10")
#    with open('10-OotS_recent_HTML.txt', 'r') as testFile10:
#        testInput10 = testFile10.read()

#    testResult10 = find_the_date(testInput10)
#    print("TEST 10\t'00000000' == {}:\t{}\n".format(testResult10, testResult10 == '00000000'))

##########################################
############## BROKEN TESTS ##############
##########################################

    # TEST 11 - PvP (error, date format change)
    with open('11-PvP_slash_date_HTML.txt', 'r') as testFile11:
        testInput11 = testFile11.read()

    testResult11 = find_the_date(testInput11)
    print("TEST 11\t'20151231' == {}:\t{}\n".format(testResult11, testResult11 == '20151231'))

