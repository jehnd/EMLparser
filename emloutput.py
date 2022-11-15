# output and file sorting for emlread
# will process the image file operations for orders in expected format
# will output two csv files per batch
# csvfile1 is addresses
# csvfile2 is for error checking and contains all info scraped from order emails

#data will be loaded into buffer in emlread for each order and passed in a function call to be added to csv's for file sorting

import os
import csv
import shutil

# writecsvs function to write to csvs info is passed to function and can be of unknown length
# return is confirmation of write maybe not needed tho
def writecsvs (orderinfo, csvfolder, csvfile):
    with open(os.path.join(csvfolder, csvfile), 'a', newline = '') as file:
        writer = csv.writer(file)
        writer.writerow(orderinfo)

# moves the files based on filename, quantity, renames with confirmation number and controlled location with emlread vars
def movefiles (filename, quantity, confnum, sourcefolder, targetfolder):
    filepath = os.path.join(sourcefolder, filename)
    i = 0
    while i < quantity:
        shutil.copy(filepath, os.path.join(targetfolder, str(i) + '_' + confnum + '_' + filename))
        i = i + 1
    returnstring = str(i) + " x " + filename + " moved to " + sourcefolder
    return returnstring
    