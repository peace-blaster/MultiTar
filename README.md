# MultiTar
 Takes batches of files in a directory, sorts them into N directories, and then compresses those directories using either `.tar.gz`, `.zip`. or `.rar`.
## Description:
 Often times large numbers of files need to be sent across network, and a single compressed archive proves too large for some systems to handle. This script automates the process of partitioning up the files, and compressing them into a variable number of archives to be sent one at a time. Note that these archives are independent- they don't need to be recombined prior to unpacking like with the stock zip utility found in most Linux-based operating systems.
## Notes:
 -Only supports `*nix` systems, and the `zip` and `rar` packages are required for the corresponding formats.
 -Target path cannot have subdirectories! This is to ensure evenness of package sizes, and prevent recursion issues
 -Script will make a directory called "DELIVERABLE" containing all archives and manifests.
 -Talk to devops/IT about appropriate amount of parallelization before use. In testing, this could easily reach 100% usage of all cores in a quad core CPU.
 -By default, script will use 4 threads and divide files into 4 archives. This can be changed manually on line 124. CLI arguments for this may be added in the future.
## Known Bugs:
 -`.zip` archives will contain junk paths. Easiest fix is to use the `-j` flag when unzipping. I do not forsee a solution for this issue.
 -When large amounts of output are produced, it can sometimes obscure the prompt in the tty after completion. Typing `clear` will fix this. I am working to resolve this issue.
