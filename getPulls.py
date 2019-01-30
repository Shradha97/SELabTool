import requests
import git
import shutil
import os
import stat
import lizard
from pathlib import Path
import matplotlib.pyplot as plt

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
    newfiles = []
    for subdir, dirs, files in os.walk(rootDir):
        for file in files:
            filepath = Path(subdir + os.sep + file)
            if filepath.suffix in extensions:
                newfiles.append(file)
                paths.append(str(filepath))
    return paths, newfiles

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
def displayFunctionData(func, CCsum):
    CC=func.cyclomatic_complexity
    print(func.long_name)
    print("\tLines of Code: ",func.nloc)
    print("\tToken Count: ",func.token_count)
    print("\tCyclomatic Complexity: ",CC)
    return CCsum+CC


#Displays the analysis results cleanly
def prettyPrint(analysis):
    print()
    totalCCsum = []
    for file in analysis:
        CCsum = 0
        displayMetaData(analysis[file])
        print("\nFunctions:")
        for num,fun in enumerate(analysis[file].function_list):
            print(num+1,'. ',end='')
            CCsum = displayFunctionData(fun, CCsum)
            print()
        totalCCsum.append(CCsum)
    print('\n\n')
    return totalCCsum

#Displays the variation of CC over the pull requests on a graph
def prettyPrintGraph():
    #For testfile 1
    X1 = list(graphinfo["TestFile1"].keys())
    Y1 = list(graphinfo["TestFile1"].values())

    #For testfile 2
    X2 = list(graphinfo["TestFile2"].keys())
    Y2 = list(graphinfo["TestFile2"].values())

    plt.subplot(2,1,1)
    plt.plot(X1, Y1)
    plt.ylabel("Cyclomatic Complexity")
    plt.xlabel("Pull Requests")
    plt.title("CC visualization for TestFile1")

    plt.subplot(2,1,2)
    plt.plot(X2, Y2)
    plt.ylabel("Cyclomatic Complexity")
    plt.xlabel("Pull Requests")
    plt.title("CC visualization for TestFile2")

    plt.subplots_adjust(hspace=1)
    plt.show()


repo = "korolvs/snake_nn"

if __name__ == "__main__":
    print("Fetching Pull requests")
    rjson = getPulls(repo)
    if type(rjson) == type({'a':'b'}):
        print("Repository not found")
    else:
        print("Getting Pull Request Names")
        repos = getForkNames(rjson)[:2]
        if repos == []:
            print("No merged pulls found")
        else:
            repoFolders = []
            graphinfo = {}
            print("Cloning All Repositories("+str(len(repos))+")")
            for num,repo in enumerate(repos):
                print("Cloning repository",num+1)
                repoFolders.append(cloneRepo(repo,"testFile"+str(num+1)))
            print("Cloning complete. Performing analysis\n")
            for i in range(len(repoFolders)):
                info = {}
                print("Repository : ",repos[i],'\n')
                paths, newfiles = getFiles(repoFolders[i])
                totalCCsum = prettyPrint(applyLizard(paths))
                for j, name in enumerate(newfiles):
                    info[newfiles[j]]=totalCCsum[j]
                graphinfo["TestFile"+str(i+1)]=info
        print("----------------------------------------------------------------------------------------")
    print("Analysis complete. Visualizing CC variation for pull requests\n")
    prettyPrintGraph()
    print()


## cloneRepo("https://github.com/RohithS98/Pysnake.git","test")
