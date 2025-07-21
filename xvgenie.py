import subprocess

import glob

import os



def xvgenie(wdir):

    

    log_file = f'{wdir}/GMPP log.txt'

    

    edrs = glob.glob(f'{wdir}/*.edr')

    for file in edrs:

        base_name = os.path.splitext(os.path.basename(file))[0]

        output_file = f"{base_name}_potential.xvg"

        

        # For GROMACS 4.5.7, use subprocess with "Potential" string

        process = subprocess.Popen(

            ["g_energy", "-f", file, "-o", output_file],  # Note: g_energy for 4.5.7

            stdin=subprocess.PIPE,

            stdout=subprocess.PIPE,

            stderr=subprocess.PIPE,

            text=True

        )

        

        # Send "Potential" and then empty line to confirm

        stdout, stderr = process.communicate(input="Potential\n\n")

        

        with open(log_file, 'a') as log:

            if process.returncode != 0:

                log.write(f"Error processing {file}: {stderr}\n")

            else:

                log.write(f"Generated {output_file}\n")


