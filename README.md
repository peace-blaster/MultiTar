# MultiTar
 Takes batches of files in a directory, sorts them into N directories, and then compresses those directories using either `.tar.gz`, `.zip`. or `.rar`.
## Description:
 Often times large numbers of files need to be sent across network, and a single compressed archive proves too large for some systems to handle. This script automates the process of partitioning up the files, and compressing them into a variable number of archives to be sent one at a time. Note that these archives are independent- they don't need to be recombined prior to unpacking like with the stock `zip` utility found in most Linux-based operating systems.
## Usage:
 - `-p` or `--path`: Path to directory with files to archive.
 - `-t` or `--threads`: Number of parallel processes to use for copying and and archiving files. Default is 4.
 - `-s` or `--splits`: Number archives to split files into. Default is 4.
 
 Example usage: `python3 fileSplitter.py -p /Users/peaceblaster/Downloads/TST -t=8 -s=10`
## Notes:
 - Only supports `*nix` systems, and the `zip` and `rar` packages are required for the corresponding formats.
 - Target path cannot have subdirectories! This is to ensure evenness of package sizes, and prevent recursion issues
 - Script will make a directory called `DELIVERABLE` containing all archives and manifests.
 - Talk to devops/IT about appropriate amount of parallelization before use. In testing, this could easily reach 100% usage of all cores in a quad core CPU.
 - By default, script will use 4 threads and divide files into 4 archives.
## Known Bugs:
 - When large amounts of output are produced, it can sometimes obscure the prompt in the tty after completion. Typing `clear` will fix this. I am working to resolve this issue.
