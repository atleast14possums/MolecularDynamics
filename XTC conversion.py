import subprocess
import os

#
# This script is for gmx trjconv to take standard .xtc and .tpr files and generate a 'whole' molecule, remove pbc, and skip 100 frames
# Whole is a standard process that makes any molecules that "break" in the simulation one piece again
# nopbc is a process that recenters the molecule so the periodicity doesn't effect analysis
# skip is done primarily to condense the data enough to make it recognizable rather than trying to fit every frame into the analysis we can take a spread out sample of the data
# and use that to analyze native contacts and thermodynamics of the system
#

def whole(xtc, tpr):

    print('The script is converting your xtc file to represent the complete molecule')

    
   
    with open('f{file_name}_whole.xtc', 'w') as f:
        np.savetxt(f, xtc)
        f.close()
    
    
    file_name = os.path.basename(xtc)
    process_whole = subprocess.Popen(["gmx", 'trjconv', '-f', '1ubqcalpha.xtc', '-s', '1ubqcalpha.tpr', '-o','f{file_name}_whole.xtc', '-pbc', 'whole'], stdout=subprocess.PIPE, stdin=subprocess.PIPE)
    process_whole.stdin.write("3\n")

    process_whole.wait()
    return process_whole

def nopbc(xtc, tpr):

    

    
    
    with open('f{file_name}_whole_nopbc.xtc', 'w') as f:
        np.savetxt(f, xtc)
        f.close()
    
        
    file_name = os.path.basename(xtc)
    process_nopbc = subprocess.Popen(["gmx", 'trjconv', '-f', '1ubqcalpha.xtc', '-s', '1ubqcalpha.tpr', '-o','f{file_name}_nopbc.xtc', '-pbc', 'mol', '-center'], stdout=subprocess.PIPE, stdin=subprocess.PIPE)

# select calpha group from index
    process_nopbc.stdin.write("3\n")

    process_nopbc.wait()
    return process_nopbc

def skip(xtc, tpr):

    
    
    with open('f{file_name}_skip.xtc', 'w') as f:
        np.savetxt(f, xtc)
        f.close()
    
        
    file_name = os.path.basename(xtc)
    process_skip = subprocess.Popen(["gmx", 'trjconv', '-f', '1ubqcalpha.xtc', '-s', '1ubqcalpha.tpr', '-o','f{file_name}_skip.xtc', '-skip', '100'], stdout=subprocess.PIPE, stdin=subprocess.PIPE)
    process_skip.stdin.write("3\n")

    process_skip.wait()
    return process_skip 

xtc = 'xtcpath'
tpr = 'tprpath'

xtc_whole = whole(xtc, tpr)
xtc_nopbc = nopbc(xtc_whole, tpr)
xtc_skip = skip(xtc_nopbc, tpr)