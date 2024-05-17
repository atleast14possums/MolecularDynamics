# This code is designed for reading multiple text files of the same format and compiling them into one file with the relevant data
# This can be combined with pyplot to produce a graph of the collective data
# Reading xvg

import re

# Adding and reading multiple files of one type to a variable for mass analysis
import os 
  
# Folder Path 
path = "Enter Folder Path"
  
# Change the directory 

os.chdir(path) 
  
# Read text File 
  
  
def read_text_file(file_path): 
    with open(file_path, 'r') as f: 
        print(f.read()) 
  
  
# iterate through all file 
for file in os.listdir(): 
    # Check whether file is in text format or not 
    if file.endswith(".txt"): 
        file_path = f"{path}\{file}"
  # Nested For/IF statement can be replaced with file_path.endswith((.txt))
        # call read text file function 
        read_text_file(file_path) 

with open('file_path', 'r') as f:
    for line in f:
        m = re.search(r'xaxis\s+label\s+"([^"]+)"', line)
        if m is not None:
            xaxis = m.group(1)
        m = re.search(r'yaxis\s+label\s+"([^"]+)"', line)
        if m is not None:
            yaxis = m.group(1)
        if line.startswith('@ s0 legend'):
            break
    df = pd.read_csv(f, names=[xaxis, yaxis], delim_whitespace=True)
    f.close()
    
print(df)        
