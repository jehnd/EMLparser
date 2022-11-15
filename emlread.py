import csv
import email
import os
#import extractdata - replaced by regextext - kept for outline of possible class implementation
import regextext  # the regex decoding functions
import emloutput  # the output formatting

#various locations for files (internal working and end results) will need to edit only this to install
emlfolder = "eml directory here"  # email files
emlfolder = "test emls here"  # test folder for test emls
imagefolder = "image directory here"  # all image files
printfolder = "folder for images to be sent"  # where sorted will go
csvfolder = "folder for csv result"  # internal working csv
addressfolder = "folder for csv address"  # address folder for ship NOT IMPLEMENTED YET

#USER INPUTS THE BATCH NUMBER AND AMOUNT OF ORDERS
#Writes to batches.txt file in root folder these details for reference
batchnum = input('enter the batch number\n')
orderamount = input('enter the amount of emails to process\n')
#orderamount is used to check against output for errors in processing handled manually in bug testing

#creating file name for this batch's csv
batchcsv = "batch" + str(batchnum) + ".csv"

with open('batches.txt', 'a') as batchlog:
    batchlog.write('batchnumber: ' + batchnum + '\n')
    batchlog.write('\tnumber of orders: ' + orderamount + '\n')
batchlog.close()

#OPEN EACH EML IN FOLDER AND RETREIVE DATA
#WILL USE VARIABLE batchnum FROM USER
#GET DETAILS AND INPUT TO TWO CSVs FORMAT BELOW
#csv file format: id, OrderID, imagefilenames separated by commas
#csv address format: id, orderID, name, address1, city province postal
#read email file -> convert to plain text -> send to extract data which will return
#the necessary data to be written to csv

#opening all the files in a folder with email module
for root, dirs, files in os.walk(emlfolder, topdown=False):
    for name in files:
       
        #print(os.path.join(root, name))
        with open(os.path.join(root, name)) as email_file:
            email_message = email.message_from_file(email_file)
        
        #iterating multipart email - should this be nested in previous with?
        if email_message.is_multipart():
            for part in email_message.walk():
                ctype = part.get_content_type()
              
                #gets only the content that is plain text to be used by regex finds for extracting data
                if ctype == 'text/plain':
                    bufferarray = []
                    print()  # terminal output formatting
                    print()
                    message = str(part.get_payload(decode=True))  # gets email payload as message to be parsed
                    
                    #getting confirmation number
                    confirmationnumberread = regextext.getConfnum(message)
                    bufferarray.append(confirmationnumberread[0])

                    #getting filenames
                    filenamesread = regextext.getFilenames(message)

                    #getting quantity
                    filequantityread = regextext.getQuantity(message)

                    #getting billing and shipping together - may need to separate to aid in output
                    shippingread = regextext.getShipping(message)

                    billingread = regextext.getBilling(message)
                    
                    bufferarray.append(shippingread)
                    bufferarray.append(billingread)
                    
                    #iterating the file name outputs
                    i = 0
                    while i < len(filequantityread):  # weird while loop maybe change to check if any results found else print error at that level
                        if len(filenamesread) == len(filequantityread):  # length challenge to enter printing the returns
                            bufferarray.append(str(filequantityread[i]) + ' x ' + filenamesread[i])
                            quantity = int(filequantityread[i])

                            # moving each file with this function call
                            emloutput.movefiles(filenamesread[i], quantity, confirmationnumberread[0], imagefolder, printfolder)
                            #j = 0
                            #while j < quantity:
                            #    print(filenamesread[i], end = ' ')  # prints file name for quantity times for desired output
                            #    j = j + 1
                        else:
                            print("\tREAD ERROR IN ", confirmationnumberread[0])
                            # prints an error at this order to be manually checked for bugs stored in batch log
                            with open('batches.txt', 'a') as batchlogerr:
                                batchlogerr.write('ERROR IN:' + confirmationnumberread[0] + '\n')

                            batchlogerr.close()

                        i = i + 1

                    # sending buffer array to writecsvs for appending the csv file
                    emloutput.writecsvs(bufferarray, csvfolder, batchcsv)

                
        