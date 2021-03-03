# MultiTar
 Takes batches of files in a directory, sorts them into N directories, and then compresses those directories using either `.tar.gz`, `.zip`. or `.rar`.
 
## Description:
 Often times large numbers of files need to be sent across network, and a single compressed archive proves too large for some systems to handle. This script automates the process of partitioning up the files, and compressing them into a variable number of archives to be sent one at a time. Note that these archives are independent- they don't need to be recombined prior to unpacking like with the stock `zip` utility found in most Linux-based operating systems.
 
## Usage:
 - `-p` or `--path`: Path to directory with files to archive.
 - `-t` or `--threads`: Number of parallel processes to use for copying and and archiving files. Default is 4.
 - `-s` or `--splits`: Number archives to split files into. Cannot be used in conjunction with `-S`.
 - `-S` or `--splitsize`: Size of archives to create (GB). Cannot be used in conjunction with `-s`.
 
 Example usage: `python3 fileSplitter.py -p /Users/peaceblaster/Downloads/TST -t 8 -S 10` will partition the files found at `/Users/peaceblaster/Downloads/TST` into 10GB archives (unknown how many it will produce).
 
## Notes:
 - Only supports `*nix` systems, and the `zip` and `rar` packages are required for the corresponding formats.
 - Target path cannot have subdirectories! This is to ensure evenness of package sizes, and prevent recursion issues
 - Script will make a directory called `DELIVERABLE` containing all archives and manifests.
 - Talk to devops/IT about appropriate amount of parallelization before use. In testing, this could easily reach 100% usage of all cores in a quad core CPU.
 - Algorithm used for split size will result in "The Price is Right" logic (closest without going over), after sorting files by size- in practice, this will mean that the first few archives will contain the largest files, and may not reach 10GB, and by the end, archives will be as close to 10GB as possible.

## Known Bugs:
 - When large amounts of output are produced, it can sometimes obscure the prompt in the tty after completion. Typing `clear` will fix this. I am working to resolve this issue.
