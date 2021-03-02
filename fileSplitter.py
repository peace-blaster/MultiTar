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
##           USAGE: python3 fileSplitter.py -P /path/to/directory        ##
##                                                                       ##
###########################################################################

#/Users/peaceblaster/Library/Mobile Documents/com~apple~CloudDocs/CODE/FILE_SPLIT_COPY/MultiTar

#imports
import os
import subprocess
import math
import sys
import argparse
import time

#get CLI arguments
parser = argparse.ArgumentParser()
parser.add_argument("-p", "--path", help="full path to target directory")
parser.add_argument("-t", "--threads", help="Number of threads to use", type=int)
parser.add_argument("-s", "--splits", help="Number archives to split files into", type=int)
parser.add_argument("-S", "--splitsize", help="Size of archives to create (GB)", type=int)
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
if args.splitsize:
    splitsize=args.splitsize
    splits=None
if args.splits:
    splits=args.splits
    splitsize=None
if args.splits and args.splitsize:
    print('Cannot specify splitsize and number of splits, please choose one.')
    quit()
if not args.splits and not args.splitsize:
    print('No split size or number of splits given. Defaulting to 2GB archives...')
    splitsize=2
def help():
    #print some helpful stuff
    print('USAGE: python3 fileSplitter.py -P /path/to/directory')

#print initial info
print("Target directory: ", mainPath)

class targetPath:
    #########################
    # setup and validation: #
    #########################
    def __init__(self, splitNum=2, threads=4):
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
        self.numArchives=0
        self.fileSizes={}
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
    def makeFileLists_splits(self):
        #makes list of lists containing files partitioned into self.splitNum partitions
        #makes empty list object
        self.fileSplit=list(range(self.splitNum))
        for f in range(self.splitNum):
            self.fileSplit[f]=[]
        for i in range(len(self.files)):
            self.fileSplit[i % self.splitNum].append(self.files[i])
        #get number of archives for other methods:
        self.numArchives=self.splitNum

    def makeSubdirectories(self):
        #makes the empty subdirectories on the filesystem
        if not self.numArchives:
            raise RuntimeError("self.numArchives not created yet")
            return 0
        #make containing directory for the deliverable:
        os.system("mkdir "+mainPath+"/DELIVERABLE")
        for i in range(self.numArchives):
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
        for i in range(self.numArchives):
            print("Starting copy for set "+str(i+1)+"/"+str(self.splitNum+1))
            processes=set()
            for f in self.fileSplit[i]:
                print(f)
                #copypasta from stackexchange- idk for sure what this is doing
                processes.add(subprocess.Popen(["cp", mainPath+"/"+f, mainPath+"/set"+str(i)]))
                if len(processes) >= self.threads:
                    os.wait()
                    processes.difference_update([p for p in processes if p.poll() is not None])
                print('waiting for child processes to complete...')
                for p in processes:
                    p.communicate()
                    p.wait()
                x=os.popen('echo ""').read()
        #I'm VERY tired of the system ignoring os.wait(), doing this instead:
        print('waiting for child processes to complete...')
        for p in processes:
            p.communicate()
            p.wait()
        x=os.popen('echo ""').read()

    def makeFileLists_size(self):
        #make a list of dicts with file name and size
        for filename in self.files:
            self.fileSizes[filename]=os.path.getsize(mainPath+'/'+filename)
        #the matching algorithm: it's ineligant, but given it's not yet moving anything, this should be ok:
        currentItem=0
        currentItemSize=0
        self.fileSplit=[[]]
        self.fileSizes=sorted(self.fileSizes.items(), key = lambda kv: kv[1], reverse=True)
        # start with empty directory, loop through files. If adding file to current set would go over size, make a new one and start again, if not, add it.
        for i in range(len(self.fileSizes)):
            #see if new file would put partition over mandated size:
            if currentItemSize+self.fileSizes[i][1]>10**9*self.splitNum and currentItem == 0: #recall it was in GB
                #if it's the first one, make it standalone instead of making a new empty one:
                self.fileSplit=[[self.fileSizes[i][0]],[]]
                currentItem=currentItem+1
                currentItemSize=0
            elif currentItemSize+self.fileSizes[i][1]>10**9*self.splitNum:
                #if yes, then start a new one:
                print('Size at {}. Starting new archive...'.format(currentItemSize))
                currentItem=currentItem+1
                currentItemSize=0
                self.fileSplit.append([self.fileSizes[i][0]])
                currentItemSize=currentItemSize+self.fileSizes[i][1]
            else:
                #if not, add it and move on:
                self.fileSplit[currentItem].append(self.fileSizes[i][0])
                currentItemSize=currentItemSize+self.fileSizes[i][1]
        #get number of archives for other methods:
        self.numArchives=len(self.fileSplit)

    #compression methods:
    def compressFilesTar(self):
        #Does the actualy file moving
        #iterate through target subdirectories, parallelizing copy process within each one
        processes=set()
        for i in range(self.numArchives):
            print("Starting compression for set "+str(i)+"/"+str(self.numArchives))
            #copypasta from stackexchange- idk for sure what this is doing
            processes.add(subprocess.Popen(["tar", "-czvf", mainPath+"/DELIVERABLE/set"+str(i)+".tar.gz", mainPath+"/set"+str(i)]))
            if len(processes) >= self.threads:
                os.wait()
                processes.difference_update([p for p in processes if p.poll() is not None])
            print('waiting for child processes to complete...')
            for p in processes:
                p.communicate()
                p.wait()
            x=os.popen('echo ""').read()
    def compressFilesZip(self):
        #Does the actualy file moving
        #iterate through target subdirectories, parallelizing copy process within each one
        processes=set()
        for i in range(self.numArchives):
            print("Starting compression for set "+str(i)+"/"+str(self.numArchives))
            #copypasta from stackexchange- idk for sure what this is doing
            processes.add(subprocess.Popen(["zip", "-r", "-j", mainPath+"/DELIVERABLE/set"+str(i)+".zip", mainPath+"/set"+str(i)]))
            if len(processes) >= self.threads:
                os.wait()
                processes.difference_update([p for p in processes if p.poll() is not None])
            print('waiting for child processes to complete...')
            for p in processes:
                p.communicate()
                p.wait()
            x=os.popen('echo ""').read()
    def compressFilesRar(self):
        #Does the actualy file moving
        #iterate through target subdirectories, parallelizing copy process within each one
        processes=set()
        for i in range(self.numArchives):
            print("Starting compression for set "+str(i)+"/"+str(self.numArchives))
            #copypasta from stackexchange- idk for sure what this is doing
            #"q" should suppress output so it isn't annoying like with the tarball method
            processes.add(subprocess.Popen(["rar", "a", mainPath+"/DELIVERABLE/set"+str(i)+".rar", mainPath+"/set"+str(i)]))
            if len(processes) >= self.threads:
                os.wait()
                processes.difference_update([p for p in processes if p.poll() is not None])
            print('waiting for child processes to complete...')
            for p in processes:
                p.communicate()
                p.wait()
            x=os.popen('echo ""').read()
    #ending tasks:
    def makeManifest(self):
        #make manifests for each archive
        for i in range(self.numArchives):
            print("Creating manifest for set"+str(i))
            filelink=open(mainPath+"/DELIVERABLE/set"+str(i)+"_file_list.txt","w+")
            for f in self.fileSplit[i]:
                filelink.write(f+"\n")
            filelink.close()
    def cleanSubDirectories(self):
        #remove all the subdirectories now that we have archives
        for i in range(self.numArchives):
            os.system("rm -rf "+mainPath+"/set"+str(i))

#used for development- ignore this
#def makeTestCase(n):
#    for i in range(n):
#        os.system('echo "hello" >> '+str(i)+'.txt')
#os.system("rm -rf "+mainPath+"/set*")
#os.system("rm -rf "+mainPath+"/DELIVERABLE")
#makeTestCase(40000)


#instantiate object
if splits:
    obj=targetPath(splitNum=splits, threads=threads)
else:
    obj=targetPath(threads=threads)
#display some info
print("Found "+str(obj.fileCount)+" files.")
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
    if splitsize:
        obj.makeFileLists_size()
        obj.makeSubdirectories()
    else:
        obj.makeFileLists_splits()
        obj.makeSubdirectories()
    obj.moveFiles()
    obj.makeManifest()
    if method=='1':
        obj.compressFilesTar()
    if method=='2':
        obj.compressFilesZip()
    if method=='3':
        obj.compressFilesRar()
    obj.cleanSubDirectories()
print("complete!")
