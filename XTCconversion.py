import subprocess
import os
import glob

#
# This script is for gmx trjconv for gromacs versions < 4.6 not using the gmx wrapper to take standard .xtc and .tpr files and generate a 'whole' molecule, remove pbc, and skip 100 frames
# Whole is a standard process that makes any molecules that "break" in the simulation one piece again
# nopbc is a process that recenters the molecule so the periodicity doesn't effect analysis
# skip is done primarily to condense the data enough to make it recognizable rather than trying to fit every frame into the analysis we can take a spread out sample of the data
# and use that to analyze native contacts and thermodynamics of the system
#


def xtcmods(wrkdir):
    
    def whole(xtc, tpr):

        file_name = os.path.basename(xtc)
        process_whole = subprocess.Popen(["gmx", 'trjconv', '-f', '1ubqcalpha.xtc', '-s', '1ubqcalpha.tpr', '-o','f{file_name}_whole.xtc', '-pbc', 'whole'], stdout=subprocess.PIPE, stdin=subprocess.PIPE)
        process_whole.stdin.write("3\n")

        process_whole.wait()
        return process_whole

    def nopbc(xtc, tpr):
        
        file_name = os.path.basename(xtc)
        process_nopbc = subprocess.Popen(["gmx", 'trjconv', '-f', '1ubqcalpha.xtc', '-s', '1ubqcalpha.tpr', '-o','f{file_name}_nopbc.xtc', '-pbc', 'mol', '-center'], stdout=subprocess.PIPE, stdin=subprocess.PIPE)

    # select calpha group from index
        process_nopbc.stdin.write("3\n")

        process_nopbc.wait()
        return process_nopbc

    def skip(xtc, tpr):

        file_name = os.path.basename(xtc)
        process_skip = subprocess.Popen(['trjconv', '-f', '1ubqcalpha.xtc', '-s', '1ubqcalpha.tpr', '-o','f{wrkdir}/xtc/{file_name}_skip.xtc', '-skip', '100'], stdout=subprocess.PIPE, stdin=subprocess.PIPE)
        process_skip.stdin.write("3\n")

        process_skip.wait()
        return process_skip 

    
    xtc = glob.glob(f'{wrkdir}/*.xtc')
    tpr = glob.glob(f'{wrkdir}/*.tpr')
    for i,j in zip(xtc, tpr):
        xtc_whole = whole(i, j)
        xtc_nopbc = nopbc(xtc_whole, j)
        xtc_skip = skip(xtc_nopbc, j)