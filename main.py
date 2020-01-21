
import os

rootDic = os.path.join(os.getcwd(),"enron_mail_20150507")

# Calls folderFunc for all files in a folder 
# whose name contains the substring "keyword"
def folderWalk(keyword,folderFunc):
    # Loop through the employees
    for empl in os.listdir(rootDic):
        emplFileP = os.path.join(rootDic,empl)
        for folder in os.listdir(emplFileP):
            if (folder.find(keyword) != -1):
                folderFunc(os.path.join(emplFileP,folder))
