import subprocess
import shutil
import os
import tempfile
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

        file_name = os.path.splitext(os.path.basename(xtc))[0]  # Remove .xtc extension

        output_file = f'{file_name}_whole.xtc'

        

        process_whole = subprocess.Popen(

            ['trjconv', '-f', xtc, '-s', tpr, '-o', f'{output_file}', '-pbc', 'whole'], 

            stdout=subprocess.PIPE, 

            stdin=subprocess.PIPE,

            stderr=subprocess.PIPE,

            text=True

        )

        

       

        stdout, stderr = process_whole.communicate(input="0")
        
        

        if process_whole.returncode != 0:

            with open(f'{wrkdir}/GMPP log.txt', 'a') as f:

                f.write(f"Error in whole step: {stderr}\n")

            return None

        

        return output_file



    def nopbc(xtc, tpr):

        file_name = os.path.splitext(os.path.basename(xtc))[0]  # Remove .xtc extension

        output_file = f'{file_name}_nopbc.xtc'

        

        process_nopbc = subprocess.Popen(

            ['trjconv', '-f', xtc, '-s', tpr, '-o', f'{output_file}', '-pbc', 'nojump', '-center'], 

            stdout=subprocess.PIPE, 

            stdin=subprocess.PIPE,

            stderr=subprocess.PIPE,

            text=True

        )

        


        stdout, stderr = process_nopbc.communicate(input="0")
        
        with open(f'{wrkdir}/GMPP log.txt', 'a') as f:
            f.write(f"nopbc debug - input file: {xtc}\n")
            f.write(f"nopbc debug - file exists: {os.path.exists(xtc)}\n")
            f.write(f"nopbc debug - tpr file: {tpr}\n")
            f.write(f"nopbc debug - tpr exists: {os.path.exists(tpr)}\n")

        if process_nopbc.returncode != 0:

            with open(f'{wrkdir}/GMPP log.txt', 'a') as f:

                f.write(f"Error in nopbc step: {stderr}\n")

            return None

            

        return output_file



    def skip(xtc, tpr, wrkdir):

        file_name = os.path.splitext(os.path.basename(xtc))[0]  # Remove .xtc extension

        



        output_dir = f'{wrkdir}'

        output_file = f'{file_name}_skip.xtc'

        

        process_skip = subprocess.Popen(

            ['trjconv', '-f', xtc, '-s', tpr, '-o', output_file, '-skip', '100'], 

            stdout=subprocess.PIPE, 

            stdin=subprocess.PIPE,

            stderr=subprocess.PIPE,

            text=True

        )

        

     

        stdout, stderr = process_skip.communicate(input="0")
        
        

        if process_skip.returncode != 0:

            with open(f'{wrkdir}/GMPP log.txt', 'a') as f:

                f.write(f"Error in skip step: {stderr}\n")

            return None

            

        return output_file



    

    xtc_files = glob.glob(f'{wrkdir}/*.xtc')

    tpr_files = glob.glob(f'{wrkdir}/*.tpr')




    temp_dir = tempfile.mkdtemp()
    
    try:
        xtc_files = glob.glob(f'{wrkdir}/*.xtc')
        tpr_files = glob.glob(f'{wrkdir}/*.tpr')
        
        if not xtc_files or not tpr_files:
            with open(f'{wrkdir}/GMPP log.txt', 'a') as f:
                f.write(f"No .xtc or .tpr files found in {wrkdir}\n")
            return
        
        for i in xtc_files:
            for j in tpr_files:
                x = os.path.splitext(os.path.basename(i))[0]
                y = os.path.splitext(os.path.basename(j))[0]
                if y == x:
                    # Copy input files to temp directory
                    temp_xtc = os.path.join(temp_dir, os.path.basename(i))
                    temp_tpr = os.path.join(temp_dir, os.path.basename(j))
                    shutil.copy2(i, temp_xtc)
                    shutil.copy2(j, temp_tpr)
                    
                    # Process in temp directory
                    os.chdir(temp_dir)  # Change to temp directory
                    
                    # Now your functions can use just filenames
                    xtc_whole = whole(os.path.basename(i), os.path.basename(j))
                    if xtc_whole:
                        xtc_nopbc = nopbc(xtc_whole, os.path.basename(j))
                        if xtc_nopbc:
                            xtc_final = skip(xtc_nopbc, os.path.basename(j))
                            if xtc_final:
                                # Copy final result back to working directory
                                final_output = f"{x}_final.xtc"  # or whatever naming you want
                                shutil.copy2(xtc_final, os.path.join(wrkdir, final_output))
                    
                    # Change back to original directory
                    os.chdir(wrkdir)
    
    finally:
        # Clean up temp directory
        shutil.rmtree(temp_dir)
