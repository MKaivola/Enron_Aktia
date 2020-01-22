import os
import email
import csv

rootDic = os.path.join(os.getcwd(),'enron_mail_20150507','maildir')
                
# Parses the emails in folder and writes the number of messages between
# two email addresses to a csv-file as determined by entrywriter
def extractContact(folder,entrywriter):
    # Dictionary to include all (sender,recipient) : count
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
 
# Calls extractContact for files in a folder 
# whose name contains the substring "keyword"
# Passes the write location along with the csvwriter
def folderWalk(keyword,csvwriter):
    # Loop through the employees
    for empl in os.listdir(rootDic):
        emplFileP = os.path.join(rootDic,empl)
        for folder in os.listdir(emplFileP):
            if (folder.find(keyword) != -1):
                extractContact(os.path.join(emplFileP,folder),csvwriter)
                
def dailyAverage(empl,inboxLoc,entrywriter):
    emailCumu = np.zeros(7)
    dayCumu = np.zeros(7)
    for file in os.listdir(inboxLoc):
        if (os.path.isfile(os.path.join(inboxLoc,file)) != True):
            continue
        # Read the email
        f = open(os.path.join(inboxLoc,file),'r')
        # Parse the email
        content = email.parser.Parser().parsestr(f.read())
        date = dateutil.parser.parse(content['Date'],"%d, %b %Y %X %z %Z")
        
# Call dailyAverage for all files in inbox folder
# Passes write location along with csvwriter        
def inboxWalk(csvwriter):
    for empl in os.listdir(rootDic):
        emplFileP = os.path.join(rootDic,empl)
        if 'inbox' in os.listdir(emplFileP):
            dailyAverage(empl,os.path.join(emplFileP,'inbox'),csvwriter)
        
# Task 1

totalFile = open('emails_sent_totals.csv','w')
# Create a csv-writer for the file
entryWriter = csv.DictWriter(totalFile,fieldnames=['Sender','Receiver','Count'])
entryWriter.writeheader()
folderWalk('sent',entryWriter)
totalFile.close()
