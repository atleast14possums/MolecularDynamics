import seaborn as sns

import numpy as np

import pathlib

import glob



def bimodal(wdir):
    bimodal = False
    foldingtemp = None  # Initialize as None

    xvgs = glob.glob(f'{wdir}/*potential.xvg')

    

    for file in xvgs:

        data = np.loadtxt(file, comments=['@', '#'], usecols=(1,))

        output = sns.histplot(data=data, stat='probability')

        patches = output.patches

        bin_edges = [patch.get_x() for patch in patches]

        ro = [patch.get_height() for patch in patches]



        # Find first maximum (from left)

        maxf = 0

        maxfi = 0

        for i, v in enumerate(ro):

            if v > maxf:

                maxf = v

                maxfi = i

        

        # Find last maximum (from right)

        maxr = 0

        maxri = 0

        for i, v in enumerate(reversed(ro)):

            if v > maxr:

                maxr = v

                maxri = len(ro) - 1 - i  # Convert back to original index

        

        # Check if bimodal

        if maxfi != maxri and abs(maxfi - maxri) > len(ro) * 0.3:  # Adjust threshold as needed

            foldingtemp = int(pathlib.Path(file).stem.split('_')[0])
            bimodal = True
            break  # If you only want the first bimodal temp found
        else:
            return bimodal, 0
    

    return bimodal, foldingtemp
