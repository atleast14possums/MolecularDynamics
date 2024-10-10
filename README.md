README

The files in this repository are going to be molecular dynamic anaylsis and input files. 
Most analysis script is designed to work with the smog-server generated files, although they are not necessary there will just need to be a few 
changes made. 


ExtractandCompileCapdb.py will generate a C-alpha only .pdb from any existing pdb file for coars grained analysis. 

QnP is a contact analysis script that will provide Q(t) plots with 2 different methods, Best-Hummer and a more straight forward analysis 
adaptable to different situations. 
As well as a probability heatmap which will have a much better clarity and resolution with Smog-Server contact files.

tprgen2 can generate and execute a series of .tpr files for gromacs for a user defined temperature range and step. 
