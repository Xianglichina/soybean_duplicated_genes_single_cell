# scripts/extract_coords.py

import csv

# Define the input and output file paths from Snakemake
input_file = snakemake.input[0]
output_file = snakemake.output[0]

# List to store extracted data
extracted_data = []

# Open the input file and read the data
with open(input_file, 'r') as infile:
    reader = csv.DictReader(infile, delimiter='\t')  # Using DictReader to access columns by name

    # Iterate over each row and extract the relevant coordinates
    for row in reader:
        # Split the ACR column into chromosome, start, and end
        acr_parts = row['ACR'].split('_')
        acr_chromosome = acr_parts[0]
        acr_start = acr_parts[1]
        acr_end = acr_parts[2]
        
        # Get reference coordinates from the other columns and rename them
        ref_chromosome = row['Gene_Chromosome']
        ref_start = row['Upstream_Start']
        ref_end = row['Downstream_End']

        # Append the extracted query and reference coordinates
        extracted_data.append([acr_chromosome, acr_start, acr_end, ref_chromosome, ref_start, ref_end])

# Define the header for the output file, renaming ref coordinates
header = ['ACR_chromosome', 'ACR_start', 'ACR_end', 'ref_chromosome', 'ref_start', 'ref_end']

# Write the extracted data to the output file
with open(output_file, 'w', newline='') as outfile:
    writer = csv.writer(outfile, delimiter='\t')
    
    # Write the header
    writer.writerow(header)
    
    # Write the extracted rows
    writer.writerows(extracted_data)

