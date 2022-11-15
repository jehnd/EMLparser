#REGULAR EXPRESSION DECODING OF EMAIL TO GET DATA 
#REGEX1...5 are all able to be changed to retreive whatever data is being looked for
#In the current usage it is designed to work with emlread specifically for those datapoints
#should be altered to match desired format of output
#these could be simplified to be way more elegant of an implementation 
#if the function received the regex from the call and the returns were simple
#handling of unexpected results is better done here than in the calling code


import re

regex1 = r"DSC_........"  # find image file names - need to enumerate the results
regex2 = r"(?<=\\n)\d(?=x)"  # find quantity of image files - match enumerated results to the previous search and extract integer value
regex3 = r"#\d\d\d\d\d\d\d"  # find confirmation id from msg
regex4 = r"(?<=Billed to:).*?(?=ship)"  # find billing address - removes decoded spacing/new line calls
regex5 = r"(?<=Shipping to:).*?(?=order)" #find shipping address - removes decoded spacing/new line calls

# gets the file names return is an array of an unknown number of file names (array length should match for each call for error checking - handled in emlread)
def getFilenames (msg):
    matches = re.finditer(regex1, msg, re.MULTILINE | re.IGNORECASE)
    matcharray = []

    for matchNum, match in enumerate(matches, start=1):
        
        #print ("Match {matchNum} was found at {start}-{end}: {match}".format(matchNum = matchNum, start = match.start(), end = match.end(), match = match.group()))
        matcharray.append("{match}".format(matchNum = matchNum, start = match.start(), end = match.end(), match = match.group()))
    
    return matcharray

#gets the quantity independent of listed file names for checking file read success - in the instance the file names do not match the expected submissions
def getQuantity (msg):
    matches2 = re.finditer(regex2, msg, re.MULTILINE)
    matcharray2 = []

    for matchNum, match in enumerate(matches2, start=1):
        
        #print ("Match {matchNum} was found at {start}-{end}: {match}".format(matchNum = matchNum, start = match.start(), end = match.end(), match = match.group()))
        matcharray2.append("{match}".format(matchNum = matchNum, start = match.start(), end = match.end(), match = match.group()))

    return matcharray2

#gets the provided confirmation number for tracking purposes returns as array - needs to change to string
def getConfnum (msg):
    matches3 = re.finditer(regex3, msg, re.MULTILINE)
    matcharray3 = []

    for matchNum, match in enumerate(matches3, start=1):
        
        #print ("Match {matchNum} was found at {start}-{end}: {match}".format(matchNum = matchNum, start = match.start(), end = match.end(), match = match.group()))
        matcharray3.append("{match}".format(matchNum = matchNum, start = match.start(), end = match.end(), match = match.group()))

    return matcharray3

#gets the billing and shipping address returns both as independent strings may need to split up into different requests to aid in output form
def getShipping (msg):
    matches4 = re.search(regex4, msg, re.IGNORECASE)
    match4 = ''

    if matches4:
        match4 = ("{match}".format(start = matches4.start(), end = matches4.end(), match = matches4.group()))
        match4 = match4.replace('\\n', ' ')
        match4 = match4.replace('\\t', '')
        match4 = match4.replace('\\', '')

    return match4

def getBilling (msg):
    matches5 = re.search(regex5, msg, re.IGNORECASE)
    match5 = ''

    if matches5:
        match5 = ("{match}".format(start = matches5.start(), end = matches5.end(), match = matches5.group()))
        match5 = match5.replace('\\n', ' ')
        match5 = match5.replace('\\t', '')
        match5 = match5.replace('\\', '')

    return match5