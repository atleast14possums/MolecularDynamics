import os
import subprocess
import glob
def tprgen(trng, dt,  wdir):    
                
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
    #aa_mdp = glob.glob(f'{wdir}/*aa.mdp')
    ca_mdp = glob.glob(f'{wdir}/*ca.mdp')

    # Temperature range will dictate the start and stopping points for what .tpr files will be generated
    # dt chooses the temeprature step in kelvin between each .tpr file
    #
    #
    trng = trng
    lower_temp, upper_temp = map(int, trng.split())

    dt = dt

    gro = glob.glob(f'{wdir}/*.gro')
    top = glob.glob(f'{wdir}/*.top')

    gro = gro[0]
    top = top[0]
    table = glob.glob(f'{wdir}/table.xvg')

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
            
            tpr_pro = subprocess.run(f"grompp -f {aa_mdp} -c {gro} -p {top} -o {wdir}/{sysnm}_{i}_aa -maxwarn 1", shell=True) # maxwarn is used to supress the warning about center of mass removal 
        tprfiles = glob.glob(f'{wdir}/*.tpr')

        for file in tprfiles:
            file = os.path.splitext(file)[0]
            if os.path.exists(f'{wdir}/{i}.xtc'):
                continue
            else:
                process = subprocess.run([f'for $file in *.tpr; do mdrun -v -deffnm {file} -table {table} -tablep {table}; done'], shell=True, cwd=wdir)
    if simvim _type == 'ca':
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
            tpr_pro = subprocess.run(f"grompp -f {aa_mdp} -c {gro}-p {top} -o {i}.tpr -maxwarn 1", shell=True)                                   
        tprfiles = glob.glob(f'{wdir}/*.tpr')

        #This is the point in which the gromacs will start running the generated simulations if you don't want to run the files comment out the next block
        #
        #
        for file in tprfiles:
            file = os.path.splitext(file)[0]
            if os.path.exists(f'{wdir}/{i}_aa.xtc'):
                continue
            else:
                process = subprocess.run([f'for $file in *.tpr; do mdrun -deffnm {file} -table {table} -tablep {table}; done'], shell=True, cwd=wdir)