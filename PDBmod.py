import os
import mdtraj
import numpy as np
import glob 

def coarspdb(workdir):
    def extract_ca(input_file, output_file):
        with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
            for line in infile:
                if line.startswith('ATOM') and line[13:15] == 'CA':
                    outfile.write(line)


    input_file = glob.glob(f'{workdir}/*.pdb')
    input_file = input_file[0]
    
    output_file = f'{workdir}/caonly.pdb'
    with open(f'{workdir}/GMPP log.txt', 'a') as f:
        f.write(f'Converting {input_file} to C alpha pdb: {output_file}')
    run =extract_ca(input_file, output_file)
