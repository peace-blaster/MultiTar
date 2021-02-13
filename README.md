# MultiTar
 Takes batches of files in a directory, sorts them into N directories, and then compresses those directories.
## Description:
 Often times large numbers of files need to be sent across network, and a single compressed archive proves too large for some systems to handle. This script automates the process of partitioning up the files, and compressing them into a variable number of archives to be sent one at a time. Note that these archives are independent- they don't need to be recombined prior to unpacking like with the stock zip utility found in most Linux-based operating systems.
## Notes:
 - When used CLI to make large numbers of tarballs, output can sometimes obscure the prompt in the tty after completion. Typing "clear" will fix this. I am working to resolve this issue.
 - Talk to devops/IT about appropriate amount of parallelization before use. In testing, this could easily reach 100% usage of all cores in a quad core CPU.
