import os
import sys
import pandas as pd

def split_by_chromosome(input_file, output_dir):
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Read the input file
    df = pd.read_csv(input_file, sep='\t')

    # Get unique values in the first column
    chromosomes = df[df.columns[0]].unique()

    # For each unique value, create a separate file
    for chrom in chromosomes:
        chrom_df = df[df[df.columns[0]] == chrom]
        
        # Construct the output file path
        output_file = os.path.join(output_dir, f"reference_regions_{chrom}.tsv")
        
        # Save the file with the same header
        chrom_df.to_csv(output_file, sep='\t', index=False)

if __name__ == "__main__":
    # Ensure the correct number of command line arguments are provided
    if len(sys.argv) != 3:
        print("Usage: python split_file.py <input_file> <output_dir>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_dir = sys.argv[2]

    # Run the split function
    split_by_chromosome(input_file, output_dir)
