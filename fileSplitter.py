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

#arguments from argv
mainPath=sys.argv[1]

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
        for i in range(self.splitNum):
            try:
                os.system("mkdir set"+str(i))
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
                processes.add(subprocess.Popen(["cp", mainPath+f, "set"+str(i)]))
                if len(processes) >= self.threads:
                    os.wait()
                    processes.difference_update([p for p in processes if p.poll() is not None])
    def compressFiles(self):
        #Does the actualy file moving
        #iterate through target subdirectories, parallelizing copy process within each one
        processes=set()
        for i in range(self.splitNum):
            print("Starting compression for set "+str(i)+"/"+str(self.splitNum))
            #copypasta from stackexchange- idk for sure what this is doing
            processes.add(subprocess.Popen(["tar", "-czvf", "set"+str(i)+".tar.gz", "set"+str(i)]))
            if len(processes) >= self.threads:
                os.wait()
                os.system("clear")
                processes.difference_update([p for p in processes if p.poll() is not None])
        #print a ton of whitespace to address bug where parallel output outruns shell and user can't see prompt after completion
        os.system("clear")
        quit()

#used for development- ignore this
#def makeTestCase(n):
#    for i in range(n):
#        os.system('echo "hello" >> '+str(i)+'.txt')
#os.system("rm -rf set*")
#makeTestCase(40000)


#instantiate object
obj=targetPath(splitNum=40, threads=32)
#display some info
print("Found "+str(obj.fileCount)+" files.")
print("splitting into "+str(obj.splitNum)+" directories of "+str(math.floor(obj.fileCount/obj.splitNum))+" files each.")
prompt=input("Proceed? (y/n) ")
if prompt=='y':
    obj.makeFileLists()
    obj.makeSubdirectories()
    obj.moveFiles()
    obj.compressFiles()
print("complete!")
