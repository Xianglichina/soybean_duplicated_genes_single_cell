import pandas as pd
import sys
from tqdm import tqdm

# Check if the user has provided the correct number of arguments
if len(sys.argv) != 5:
    print("Usage: python gene_matching.py <input1.csv> <input2.csv> <input3.csv> <output.csv>")
    sys.exit(1)

# Get the filenames from the command-line arguments
input1_file = sys.argv[1]
input2_file = sys.argv[2]
input3_file = sys.argv[3]
output_file = sys.argv[4]

# Define the column names for each input file since they do not have headers
input1_columns = ['ACR', 'gene']  # Columns for input1
input2_columns = ['Duplicate.1','Duplicate.2']  # Columns for input2
input3_columns = ['Gene', 'Gene_Chromosome', 'Gene_Start', 'Gene_End', 
                  'Upstream_Gene', 'Upstream_Chromosome', 'Upstream_Start', 'Upstream_End', 
                  'Downstream_Gene', 'Downstream_Chromosome',  # Renamed
                  'Downstream_Start', 'Downstream_End']  # Columns for input3

# Check for duplicate column names in input3_columns
if len(input3_columns) != len(set(input3_columns)):
    print("Duplicate column names found in input3_columns:")
    print(input3_columns)
    sys.exit(1)

# Load input3 fully as it is likely smaller
input3 = pd.read_csv(input3_file, sep=',', header=None, names=input3_columns)
input3['Gene'] = input3['Gene'].astype(str).str.strip()  # Ensure gene column is string

# Define a function to process each chunk of input1
def process_chunk(chunk):
    output_rows = []  # Initialize an empty list to store the output rows
    for index1, row1 in chunk.iterrows():
        gene = row1['gene']
        acr = row1['ACR']
        
        # Check for matches in Duplicate.1 column
        matches_dup1 = input2[input2['Duplicate.1'] == gene]
        for _, match_row in matches_dup1.iterrows():
            new_row = row1.copy()  # Duplicate the input1 row
            new_row['matched_gene'] = match_row['Duplicate.2']  # Add the corresponding Duplicate.2 gene
            
            # Check for additional information in input3
            match_gene_info = input3[input3['Gene'] == new_row['matched_gene']]
            if not match_gene_info.empty:
                for _, gene_row in match_gene_info.iterrows():
                    new_row['Gene_Chromosome'] = gene_row['Gene_Chromosome']  # Add Gene_Chromosome
                    new_row['Upstream_Gene'] = gene_row['Upstream_Gene']
                    new_row['Downstream_Gene'] = gene_row['Downstream_Gene']
                    new_row['Upstream_Start'] = gene_row['Upstream_Start']
                    new_row['Downstream_End'] = gene_row['Downstream_End']
            output_rows.append(new_row)

        # Check for matches in Duplicate.2 column
        matches_dup2 = input2[input2['Duplicate.2'] == gene]
        for _, match_row in matches_dup2.iterrows():
            new_row = row1.copy()  # Duplicate the input1 row
            new_row['matched_gene'] = match_row['Duplicate.1']  # Add the corresponding Duplicate.1 gene
            
            # Check for additional information in input3
            match_gene_info = input3[input3['Gene'] == new_row['matched_gene']]
            if not match_gene_info.empty:
                for _, gene_row in match_gene_info.iterrows():
                    new_row['Gene_Chromosome'] = gene_row['Gene_Chromosome']  # Add Gene_Chromosome
                    new_row['Upstream_Gene'] = gene_row['Upstream_Gene']
                    new_row['Downstream_Gene'] = gene_row['Downstream_Gene']
                    new_row['Upstream_Start'] = gene_row['Upstream_Start']
                    new_row['Downstream_End'] = gene_row['Downstream_End']
            output_rows.append(new_row)

    return output_rows

# Read input1 in chunks and process each chunk
chunk_size = 1000  # Set the size of each chunk
input2 = pd.read_csv(input2_file, sep=',', header=None, names=input2_columns)  # Load input2 fully
input2['Duplicate.1'] = input2['Duplicate.1'].astype(str).str.strip()  # Ensure string format
input2['Duplicate.2'] = input2['Duplicate.2'].astype(str).str.strip()  # Ensure string format

# Create an empty output file or overwrite the existing one
with open(output_file, 'w') as f:
    f.write('\t'.join(input1_columns) + '\tmatched_gene\tGene_Chromosome\tUpstream_Gene\tDownstream_Gene\tUpstream_Start\tDownstream_End\n')  # Write header

# Process each chunk and append results to output file
for chunk in pd.read_csv(input1_file, sep=',', header=None, names=input1_columns, chunksize=chunk_size):
    chunk['gene'] = chunk['gene'].astype(str).str.strip()  # Ensure gene column is string
    output_rows = process_chunk(chunk)
    
    # Write the output rows to the file
    if output_rows:
        output_df = pd.DataFrame(output_rows)
        output_df.to_csv(output_file, sep='\t', mode='a', header=False, index=False)  # Append to the output file

print(f"Script finished and output saved as '{output_file}'.")

