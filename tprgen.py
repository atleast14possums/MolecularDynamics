import os
import subprocess
import glob
import pathlib
def tprgen(tlow, thigh, dt,  wdir):
    log = f'{wdir}/GMPP log.txt'
    with open(f'{wdir}/GMPP log.txt', 'a') as f:
        f.write(f'Starting tprgen with Temperature lower bound={tlow}, Temperature upper bound={thigh}')
        f.close()

    # The preferred mdp settings for these coars graining simulations are generated via the smog server 
    #  https://smog-server.org/prepare_a_simulation.html, 
    # 
    #
    #
    #
    #
    #
    # !!!!!IMPORTANT!!!!!!
    # for the smog server coars graining you will need to copy the .mdp settings from the smog server please title them ending with aa.mdp and ca.mdp respectively
    # cont_file refers to native contact files produced by coars graining with the Smog-Server https://smog-server.org/prepare_a_simulation.html, 
    # although the data can be worked using the standard mdtraj pair selections
    aa_mdp = glob.glob(f'{wdir}/*aa.mdp')
    ca_mdp = glob.glob(f'{wdir}/*ca.mdp')
    ca_mdp = '/work/LAS/jroche-lab/twatch/MD/smogca.mdp'
    #ca_mdp = str(pathlib.Path(ca_mdp).stem)
    with open(f'{log}', 'a') as f:
        f.write(f'Using {ca_mdp}')
        f.close()
    # Temperature range will dictate the start and stopping points for what .tpr files will be generated
    # dt chooses the temeprature step in kelvin between each .tpr file
    #
    #
    
    lower_temp, upper_temp = tlow, thigh

    dt = dt

    gro = glob.glob(f'{wdir}/*.gro')
    top = glob.glob(f'{wdir}/*.top')
    sim_type = 'ca'
    gro = gro[0]
    
    top = top[0]
    
    with open(f'{wdir}/GMPP log.txt', 'a') as f:
        f.write(f'.gro file used: {gro} \n .top file used: {top}')
    table = f'/{wdir}/table.xvg'
    
    if sim_type == 'aa':
        with open(aa_mdp, 'r') as f:
            lines = f.readlines()
            
        ref_t_found = False
        gen_temp_found = False

        for i in range(lower_temp, upper_temp+1, dt):
            if os.path.exists(f'{wdir}/{sysnm}_{i}_aa.tpr'):
                continue
            new_lines = []
            for line in lines:
                if line.startswith('ref_t'):
                    new_line = f'ref_t = {i}\n'
                    ref_t_found = True
                elif line.startswith('gen_temp'):
                    new_line = f'gen_temp = {i}\n'
                    gen_temp_found = True
                else:
                    new_line = line
                new_lines.append(new_line)

            if not ref_t_found:
                new_lines.append(f'ref_t = {i}\n')
            if not gen_temp_found:
                new_lines.append(f'gen_temp = {i}\n')

            with open(aa_mdp, 'w') as f:
                f.writelines(new_lines)  
            # generate tprs 
            
            tpr_pro = subprocess.run(f"grompp -f {aa_mdp} -c {gro}.gro -p {top}.top -o {i} -maxwarn 1 -backup no", shell=True) # maxwarn is used to supress the warning about center of mass removal 
        tprfiles = glob.glob(f'{wdir}/*.tpr')

        for file in tprfiles:
            file = os.path.splitext(file)[0]
            if os.path.exists(f'{wdir}/{i}.xtc'):
                continue
            else:
                process = subprocess.run([f'mdrun -v -deffnm {file} -table {table} -tablep {table}'], shell=True, cwd=wdir)
    if sim_type == 'ca':
        with open(ca_mdp, 'r') as f:
            lines = f.readlines()

        ref_t_found = False
        gen_temp_found = False

        for i in range(lower_temp, upper_temp+1, dt):
            if os.path.exists(f'{wdir}/{i}.tpr'):
                continue
            new_lines = []
            for line in lines:
                if line.startswith('ref_t'):
                    new_line = f'ref_t = {i}\n'
                    ref_t_found = True
                elif line.startswith('gen_temp'):
                    new_line = f'gen_temp = {i}\n'
                    gen_temp_found = True
                else:
                    new_line = line
                new_lines.append(new_line)

            if not ref_t_found:
                new_lines.append(f'ref_t = {i}\n')
            if not gen_temp_found:
                new_lines.append(f'gen_temp = {i}\n')

            with open(ca_mdp, 'w') as f:
                f.writelines(new_lines)   
            # generate tprs 
            
            tpr_pro = subprocess.run(f"grompp -f {ca_mdp} -c {gro} -p {top} -o {wdir}/{i}.tpr -maxwarn 1", shell=True)                                   
        tprfiles = glob.glob('*.tpr')

        #This is the point in which the gromacs will start running the generated simulations if you don't want to run the files comment out the next block
        #
        #
        


        tprfiles = glob.glob(f'{wdir}/*.tpr')

        with open(f'{log}', 'a') as f:
            f.write(f"Found {len(tprfiles)} TPR files to run")
            f.close()
    

        for tpr_file in tprfiles:
            base_name = os.path.splitext(os.path.basename(tpr_file))[0]
            xtc_file = f'{wdir}/{base_name}.xtc'
    
            if os.path.exists(xtc_file):
                with open(f'{log}', 'a') as f:
                    f.write(f"Skipping {base_name} - output already exists\n")
                continue
    
            with open(f'{log}', 'a') as f:
                f.write(f"Starting simulation for {base_name}\n")
    
    # Run each simulation and wait for completion
            result = subprocess.run(f'mdrun -v -deffnm {base_name} -table {table} -tablep {table}', shell=True, cwd=wdir, capture_output=True, text=True)
    
            if result.returncode == 0:
                with open(f'{log}', 'a') as f:
                    f.write(f"Successfully completed {base_name}\n")
            else:
                with open(f'{log}', 'a') as f:
                    f.write(f"Error in {base_name}: {result.stderr}\n")
