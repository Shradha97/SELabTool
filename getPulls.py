import requests
import git
import shutil
import os
import stat
import lizard
from pathlib import Path

#Valid extensions for applying code complexity analysis
extensions = {
    '.c' : 'C',
    '.cpp' : 'C++',
    '.java' : 'Java',
    '.py' : 'Python',
    '.js' : 'JavaScript'
}

###############################################################
#Does not work
#Delete the temporary directory created while cloning the repository
def removeFolder(top):
    for root, dirs, files in os.walk(top, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))
##############################################################

#Creates a new temporary folder for cloning repository
#If it already exists, it deletes it and creates a new folder
def createFolder(fname):
    try:
        os.mkdir(fname)
    except:
        print(fname)
        removeFolder(fname)
        os.mkdir(fname)

#Gets the pull requests of the given repository and returns the json
def getPulls(repo):
    url = "https://api.github.com/repos/"+repo+"/pulls?state=all+state=closed"
    r = requests.get(url)
    return r.json()

def getForkNames(r):
    forks = []
    for i in r:
        if i['merged_at'] != None and i['head']['repo']:
            forks.append(i['head']['repo']['clone_url'])
    return forks

#Clones the repository with given git url and stores it in directory with given name
def cloneRepo(gitrepo,dirName):
    fname = os.path.dirname(__file__)+r"\temp_"+dirName
    createFolder(fname)
    git.Git(fname).clone(gitrepo)
    return fname

#Scans all the files in a directory and extracts file paths which have supported extensions
def getFiles(rootDir):
    paths = []
    for subdir, dirs, files in os.walk(rootDir):
        for file in files:
            filepath = Path(subdir + os.sep + file)
            if filepath.suffix in extensions:
                paths.append(str(filepath))
    return paths

#Applies analysis on all the files on the list of files
def applyLizard(fileList):
    analysis = {}
    for i in fileList:
        analysis[i] = lizard.analyze_file(i)
    return analysis

#Display File Data
def displayMetaData(fileInfo):
    print("File Name: ",fileInfo.filename)
    print("Lines of Code: ",fileInfo.nloc)
    print("Token Count: ",fileInfo.token_count)

#Display Function Data
def displayFunctionData(func):
    print(func.long_name)
    print("\tLines of Code: ",func.nloc)
    print("\tToken Count: ",func.token_count)
    print("\tCyclomatic Complexity: ",func.cyclomatic_complexity)

#Displays the analysis results cleanly
def prettyPrint(analysis):
    print()
    for file in analysis:
        displayMetaData(analysis[file])
        print("\nFunctions:")
        for num,fun in enumerate(analysis[file].function_list):
            print(num+1,'. ',end='')
            displayFunctionData(fun)
            print()
    print('\n\n')

repo = input("Enter repository name:")
#repo = "korolvs/snake_nn"

if __name__ == "__main__":
    print("Fetching Pull requests")
    rjson = getPulls(repo)
    if type(rjson) == type({'a':'b'}):
        print("Repository not found")
    else:
        print("Getting fork names")
        repos = getForkNames(rjson)[:2]
        repoFolders = []
        print("Cloning All Repositories("+str(len(repos))+")")
        for num,repo in enumerate(repos):
            print("Cloning repository",num+1)
            repoFolders.append(cloneRepo(repo,"testFile"+str(num+1)))
        print("Cloning complete. Performing analysis\n")
        for i in range(len(repoFolders)):
            print("Repository : ",repos[i],'\n')
            prettyPrint(applyLizard(getFiles(repoFolders[i])))
            print("----------------------------------------------------------------------------------------")
        print()
## cloneRepo("https://github.com/RohithS98/Pysnake.git","test")
