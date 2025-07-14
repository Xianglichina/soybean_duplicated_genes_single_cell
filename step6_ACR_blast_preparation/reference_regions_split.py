import os

# List all input files
input_files = [f for f in os.listdir('.') if f.startswith('reference_regions_Gm') and f.endswith('.tsv')]

for file in input_files:
    with open(file, 'r') as f:
        lines = f.readlines()
    
    # Extract header and split lines
    header = lines[0]
    first_20000 = lines[:20000]
    rest = [header] + lines[20000:]
    
    # Generate output filenames
    base = os.path.splitext(file)[0]
    first_20000_file = f"{base}_first_20000_lines.tsv"
    rest_file = f"{base}_rest_of_the_lines.tsv"
    
    # Write to output files
    with open(first_20000_file, 'w') as f:
        f.writelines(first_20000)
    
    with open(rest_file, 'w') as f:
        f.writelines(rest)
