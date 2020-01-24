import os
from email import parser
import csv
from datetime import datetime
import numpy as np

# Location of the employee directories
rootDic = os.path.join(os.getcwd(),'enron_mail_20150507','maildir')
                
# Parses the emails contained in subdirectories of empl that contain
# the string 'sent' and writes the number of messages between
# two email addresses to a csv-file as determined by entrywriter            
def extractContact(empl,entryWriter):
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
    for folder in os.listdir(empl):
        currentLoc = os.path.join(empl,folder)
        # Consider only subdirectories that contain the string 'sent'
        # in their name
        if os.path.isdir(currentLoc) and 'sent' in folder:
            inner(currentLoc)
    # Write the dictionary to the csv-file
    for key,value in countDict.items():
        entryWriter.writerow({'sender': key[0],'recipient': key[1],'count': value})
                 
# Calculates average number of emails per weekday for employee emplName
# and writes it to a csv-file via entryWriter
# empl passes the employee filepath
def dailyAverage(emplName,empl,entryWriter):
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
    for folder in os.listdir(empl):
        currentLoc = os.path.join(empl,folder)
        # Consider only directories that contain the word 'inbox'
        # in their name
        if os.path.isdir(currentLoc) and 'inbox' in folder:
            inner(currentLoc)
    # Return zero if there are no emails for a given weekday
    averageWeekday = np.divide(emailCumu,dayCumu,out = np.zeros_like(emailCumu),where = dayCumu != 0)
    for day in range(7):
        entryWriter.writerow({'employee': emplName,'day_of_week': day, 'avg_count': averageWeekday[day]})

                
# Task 1        
with open('emails_sent_totals.csv','w') as totalFile:
    # Create a csv-writer for the file
    entryWriter = csv.DictWriter(totalFile,fieldnames=['sender','recipient','count'])
    entryWriter.writeheader()
    # Consider all employees
    for emplName in os.listdir(rootDic):
        emplFileP = os.path.join(rootDic,emplName)
        extractContact(emplFileP,entryWriter)

# Task 2
with open('emails_sent_average_per_weekday.csv','w') as averageFile:
    entryWriter = csv.DictWriter(averageFile,fieldnames=['employee','day_of_week','avg_count'])
    entryWriter.writeheader()
    # Consider all employees
    for emplName in os.listdir(rootDic):
        emplFileP = os.path.join(rootDic,emplName)
        dailyAverage(emplName,emplFileP,entryWriter)
