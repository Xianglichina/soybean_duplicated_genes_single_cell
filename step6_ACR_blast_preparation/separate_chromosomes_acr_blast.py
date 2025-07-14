import os
import pandas as pd
import argparse

# Argument parsing
parser = argparse.ArgumentParser(description='Split a file into multiple files based on the prefix in the first column, keeping the header in all files.')
parser.add_argument('input_file', type=str, help='Path to the input CSV file.')
parser.add_argument('output_dir', type=str, help='Directory to save the output files.')
args = parser.parse_args()

# Create the output directory if it doesn't exist
os.makedirs(args.output_dir, exist_ok=True)

# Read the input file into a pandas dataframe (tab-separated, and keeping the header)
df = pd.read_csv(args.input_file, sep='\t')

# Extract the first part of the first column before the first '_'
df['prefix'] = df.iloc[:, 0].str.extract(r'^(Gm\d+)_')

# Get the unique prefixes (e.g., Gm01, Gm02, ..., Gm20)
unique_values = df['prefix'].unique()

# Iterate over the unique prefixes and split the dataframe
for value in unique_values:
    if pd.isna(value):  # Skip rows without a valid prefix
        continue
    # Filter the rows where the first column starts with the unique value
    df_filtered = df[df['prefix'] == value]
    
    # Save the filtered dataframe to a separate file (including the header, excluding the 'prefix' column)
    output_file = os.path.join(args.output_dir, f'acr_blast_{value}.tsv')
    df_filtered.drop(columns=['prefix']).to_csv(output_file, sep='\t', index=False)
    print(f'Saved {output_file}')
