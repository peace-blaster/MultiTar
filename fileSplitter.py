# __________                          ___.   .__                   __
# \______   \ ____ _____    ____  ____\_ |__ |  | _____    _______/  |_  ___________
#  |     ___// __ \\__  \ _/ ___\/ __ \| __ \|  | \__  \  /  ___/\   __\/ __ \_  __ \
#  |    |   \  ___/ / __ \\  \__\  ___/| \_\ \  |__/ __ \_\___ \  |  | \  ___/|  | \/
#  |____|    \___  >____  /\___  >___  >___  /____(____  /____  > |__|  \___  >__|
#                \/     \/     \/    \/    \/          \/     \/            \/


###########################################################################
##                                                                       ##
##                          File Splitter                                ##
##                                                                       ##
###########################################################################
##                                                                       ##
##      splits large sets of files into directories, compresses them     ##
##                                                                       ##
##              USAGE: python3 fileSplitter.py /path/to/directory        ##
##                                                                       ##
###########################################################################

#imports
import os
import subprocess
import math
import sys
import argparse

#get CLI arguments
parser = argparse.ArgumentParser()
parser.add_argument("-p", "--path", help="full path to target directory")
parser.add_argument("-t", "--threads", help="Number of threads to use", type=int)
parser.add_argument("-s", "--splits", help="Number archives to split files into", type=int)
args=parser.parse_args()
if not args.path:
    help()
    print("main path not provided!")
    quit()
else:
    mainPath=args.path
if not args.threads:
    print("Defaulting to 4 threads")
    threads=4
else:
    threads=args.threads
if not args.splits:
    print("Defaulting to 4 archives")
    splits=4
else:
    splits=args.splits

def help():
    #print some helpful stuff

#print initial info
print("Target directory: ", mainPath)

class targetPath:
    #########################
    # setup and validation: #
    #########################
    def __init__(self, splitNum=4, threads=4):
        if not self.validatePath():
            raise ValueError("Path provided is invalid")
            print("Path provided is invalid, quitting")
            quit()
        self.files=os.listdir(mainPath)
        if not self.checkSubdirectories():
            raise ValueError("Path provided contains subdirectories")
            print("Path provided contains subdirectories, quitting")
            quit()
        self.fileCount=len(self.files)
        self.threads=threads
        #number of subdirectories to make for splitting files:
        self.splitNum=splitNum
        self.fileSplit=[]
        self.subDirExists=False
    def validatePath(self):
        #ensures path is valid on host OS
        if os.path.exists(mainPath):
            return True
    def checkSubdirectories(self):
        #ensures there are no contained subdirectories
        for f in self.files:
            if os.path.isdir(f):
                return False
        return True
    #####################
    # useful functions: #
    #####################
    def makeFileLists(self):
        #makes list of lists containing files partitioned into self.splitNum partitions
        #makes empty list object
        self.fileSplit=list(range(self.splitNum))
        for f in range(self.splitNum):
            self.fileSplit[f]=[]
        for i in range(len(self.files)):
            self.fileSplit[i % self.splitNum].append(self.files[i])
    def makeSubdirectories(self):
        #makes the empty subdirectories on the filesystem
        if not self.fileSplit:
            raise RuntimeError("self.fileSplit not created yet")
            return 0
        #make containing directory for the deliverable:
        os.system("mkdir "+mainPath+"/DELIVERABLE")
        for i in range(self.splitNum):
            try:
                os.system("mkdir "+mainPath+"/set"+str(i))
            except:
                raise RuntimeError("Unable to create directory")
                print("Unable to create directory 'set"+str(i)+"', quitting")
                quit()
            self.subDirExists=True
    def moveFiles(self):
        #Does the actualy file moving
        #iterate through target subdirectories, parallelizing copy process within each one
        for i in range(self.splitNum):
            print("Starting copy for set "+str(i)+"/"+str(self.splitNum))
            processes=set()
            for f in self.fileSplit[i]:
                #copypasta from stackexchange- idk for sure what this is doing
                processes.add(subprocess.Popen(["cp", mainPath+"/"+f, mainPath+"/set"+str(i)]))
                if len(processes) >= self.threads:
                    os.wait()
                    processes.difference_update([p for p in processes if p.poll() is not None])
        os.wait() #to prevent overlap issues
    #compression methods:
    def compressFilesTar(self):
        #Does the actualy file moving
        #iterate through target subdirectories, parallelizing copy process within each one
        processes=set()
        for i in range(self.splitNum):
            print("Starting compression for set "+str(i)+"/"+str(self.splitNum))
            #copypasta from stackexchange- idk for sure what this is doing
            processes.add(subprocess.Popen(["tar", "-czvf", mainPath+"/DELIVERABLE/set"+str(i)+".tar.gz", mainPath+"/set"+str(i)]))
            if len(processes) >= self.threads:
                os.wait()
                processes.difference_update([p for p in processes if p.poll() is not None])
        #print a ton of whitespace to address bug where parallel output outruns shell and user can't see prompt after completion
        os.wait() #to prevent overlap issues
    def compressFilesZip(self):
        #Does the actualy file moving
        #iterate through target subdirectories, parallelizing copy process within each one
        processes=set()
        for i in range(self.splitNum):
            print("Starting compression for set "+str(i)+"/"+str(self.splitNum))
            #copypasta from stackexchange- idk for sure what this is doing
            processes.add(subprocess.Popen(["zip", "-r", "-j", mainPath+"/DELIVERABLE/set"+str(i)+".zip", mainPath+"/set"+str(i)]))
            if len(processes) >= self.threads:
                os.wait()
                processes.difference_update([p for p in processes if p.poll() is not None])
        #print a ton of whitespace to address bug where parallel output outruns shell and user can't see prompt after completion
        os.wait() #to prevent overlap issues
    def compressFilesRar(self):
        #Does the actualy file moving
        #iterate through target subdirectories, parallelizing copy process within each one
        processes=set()
        for i in range(self.splitNum):
            print("Starting compression for set "+str(i)+"/"+str(self.splitNum))
            #copypasta from stackexchange- idk for sure what this is doing
            #"q" should suppress output so it isn't annoying like with the tarball method
            processes.add(subprocess.Popen(["rar", "a", mainPath+"/DELIVERABLE/set"+str(i)+".rar", mainPath+"/set"+str(i)]))
            if len(processes) >= self.threads:
                os.wait()
                processes.difference_update([p for p in processes if p.poll() is not None])
        #print a ton of whitespace to address bug where parallel output outruns shell and user can't see prompt after completion
        os.wait() #to prevent overlap issues
    #ending tasks:
    def makeManifest(self):
        #make manifests for each archive
        for i in range(self.splitNum):
            print("Creating manifest for set"+str(i))
            filelink=open(mainPath+"/DELIVERABLE/set"+str(i)+"_file_list.txt","w+")
            for f in self.fileSplit[i]:
                filelink.write(f+"\n")
            filelink.close()
    def cleanSubDirectories(self):
        #remove all the subdirectories now that we have archives
        for i in range(self.splitNum):
            os.system("rm -rf "+mainPath+"/set"+str(i))

#used for development- ignore this
#def makeTestCase(n):
#    for i in range(n):
#        os.system('echo "hello" >> '+str(i)+'.txt')
#os.system("rm -rf "+mainPath+"/set*")
#os.system("rm -rf "+mainPath+"/DELIVERABLE")
#makeTestCase(40000)


#instantiate object
obj=targetPath(splitNum=splits, threads=splits)
#display some info
print("Found "+str(obj.fileCount)+" files.")
print("splitting into "+str(obj.splitNum)+" directories of "+str(math.floor(obj.fileCount/obj.splitNum))+" files each.")
prompt=input("Proceed? (y/n) ")
if prompt.lower()=='y':
    loop=True
    method=''
    while loop==True:
        prompt=input("Select compression method:\n 1.) .tar.gz\n 2.) .zip (requires 'zip' package- DO NOT USE WITHOUT)\n 3.) .rar (requires 'rar' package- DO NOT USE WITHOUT)\n 4.) quit\n")
        if prompt not in ['1','2','3','4']:
            print("invalid selection!")
        else:
            method=prompt
            loop=False
            if method=='4':
                quit()
    obj.makeFileLists()
    obj.makeSubdirectories()
    obj.moveFiles()
    if method=='1':
        obj.compressFilesTar()
    if method=='2':
        obj.compressFilesZip()
    if method=='3':
        obj.compressFilesRar()
    obj.makeManifest()
    obj.cleanSubDirectories()
print("complete!")
