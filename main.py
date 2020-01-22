
import os
import email
import csv


rootDic = os.path.join(os.getcwd(),"enron_mail_20150507")

# Calls folderFunc for files in a folder 
# whose name contains the substring "keyword"
def folderWalk(keyword,folderFunc):
    # Loop through the employees
    for empl in os.listdir(rootDic):
        emplFileP = os.path.join(rootDic,empl)
        for folder in os.listdir(emplFileP):
            if (folder.find(keyword) != -1):
                folderFunc(os.path.join(emplFileP,folder))

# Parses the emails in folder and writes the entries to file via entrywriter
def extractContact(folder,entryvwriter):
    # Dictionary to include all (sender,recipient) : count pairs
    countDict = dict()
    for file in os.listdir(folder):
        # Read the email
        f = open(os.path.join(folder,file),'r')
        # Parse the email
        content = email.parser.Parser().parsestr(f.read())
        sender = content['From']
        # Go through all the recipient headers
        for header in ['To','cc','bcc']:
            # Check whether the header is empty
            if (content[header] != None):
                # Extract the individual recipients
                receivers = [name.strip() for name in content[header].split(', ')]
                # Add the message to the dictionary
                for receiver in receivers:
                    key = (sender,receiver)
                    countDict[key] = countDict.get(key,0) + 1
    # Write the dictionary to the csv-file
    for key,value in countDict.items():
        entryWriter.writerow({'Sender': key[0],'Receiver': key[1],'Count': value})
