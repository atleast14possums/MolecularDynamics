def extract_ca(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            if line.startswith('ATOM') and line[13:15] == 'CA':
                outfile.write(line)


input_file = 'path/to/input/.pdb'
output_file = 'path/to/output/.pdb'