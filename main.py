import os
from email import parser
import csv
from datetime import datetime
import numpy as np

# Location of the employee directories
rootDic = os.path.join(os.getcwd(),'enron_mail_20150507','maildir')
                
# Parses the emails in folder and its subdirectories 
# and writes the number of messages between
# two email addresses to a csv-file as determined by entryWriter              
def extractContact(folder,entryWriter):
    # Dictionary to include all (sender,recipient) : count elements
    countDict = dict()
    def inner(subDic):
        for file in os.listdir(subDic):
            currentPath = os.path.join(subDic,file)
            # Recurse when encountering a directory
            if os.path.isdir(currentPath) :
                inner(currentPath)
            else :
                # Read the email
                f = open(currentPath,'r',errors = 'replace')
                # Parse the email
                content = parser.Parser().parsestr(f.read())
                f.close()
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
    inner(folder)
    # Write the dictionary to the csv-file
    for key,value in countDict.items():
        entryWriter.writerow({'sender': key[0],'recipient': key[1],'count': value})
 
# Calls extractContact for files in directories 
# whose name contains the substring "keyword"
# Passes the write location along with the csvwriter
def folderWalk(keyword,csvwriter):
    # Loop through the employees
    for empl in os.listdir(rootDic):
        emplFileP = os.path.join(rootDic,empl)
        # Consider each directory separately
        for folder in os.listdir(emplFileP):
            if (folder.find(keyword) != -1):
                extractContact(os.path.join(emplFileP,folder),csvwriter)
                
# Calculates average number of emails per weekday for employee empl
# and writes it to a csv-file via entryWriter
# inboxLoc passes the inbox filepath
def dailyAverage(empl,inboxLoc,entryWriter):
    # How many emails received in a given week day
    emailCumu = np.zeros(7)
    # How many given weekdays are observed
    dayCumu = np.zeros(7)
    # What dates have already been observed
    observedDates = set()
    def inner(subDic):
        for file in os.listdir(subDic):
            currentPath = os.path.join(subDic,file)
            # Recurse when encountering a directory
            if os.path.isdir(currentPath):
                inner(currentPath)
            else:
                # Read the email
                f = open(currentPath,'r',errors = 'replace')
                # Parse the email
                content = parser.Parser().parsestr(f.read())
                f.close()
                # Remove the time zone name from the date and parse the string
                dateEmail = datetime.strptime((content['Date'].split("(")[0]),"%a, %d %b %Y %X %z ")
                # Add email to cumulative 
                emailCumu[dateEmail.weekday()] += 1
                # If a new date is observed, add new observed weekday
                if dateEmail.date() not in observedDates:
                    observedDates.add(dateEmail.date())
                    dayCumu[dateEmail.weekday()] += 1
    inner(inboxLoc)
    # Return zero if there are no emails for a given weekday
    averageWeekday = np.divide(emailCumu,dayCumu,out = np.zeros_like(emailCumu),where = dayCumu != 0)
    for day in range(7):
        entryWriter.writerow({'employee': empl,'day_of_week': day, 'avg_count': averageWeekday[day]})

        
# Calls dailyAverage for all files in inbox directories
# and their subdirectories
# Passes write location along with csvwriter        
def inboxWalk(csvwriter):
    # Loop through the employees
    for empl in os.listdir(rootDic):
        emplFileP = os.path.join(rootDic,empl)
        if 'inbox' in os.listdir(emplFileP):
            dailyAverage(empl,os.path.join(emplFileP,'inbox'),csvwriter)
        
# Task 1        
with open('emails_sent_totals.csv','w') as totalFile:
    # Create a csv-writer for the file
    entryWriter = csv.DictWriter(totalFile,fieldnames=['sender','recipient','count'])
    entryWriter.writeheader()
    folderWalk('sent',entryWriter)

# Task 2
with open('emails_sent_average_per_weekday.csv','w') as averageFile:
    entryWriter = csv.DictWriter(averageFile,fieldnames=['employee','day_of_week','avg_count'])
    entryWriter.writeheader()
    inboxWalk(entryWriter)
