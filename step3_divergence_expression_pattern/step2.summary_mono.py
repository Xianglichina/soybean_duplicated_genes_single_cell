import pandas as pd
import argparse

# Set up argument parsing
parser = argparse.ArgumentParser(description='Count columns starting with "Glyma" and check if they are the same.')
parser.add_argument('input_file', help='Input file (CSV format)')
parser.add_argument('output_file', help='Output file (CSV format)')
args = parser.parse_args()

# Read the input data (CSV format)
df = pd.read_csv(args.input_file)

# Function to count Glyma columns and check if the values are the same
def count_and_check_same(row):
    # Extract values in columns 3 to 9 (0-based indices 2 to 8)
    values = row[2:9].values
    glyma_values = [v for v in values if isinstance(v, str) and v.startswith("Glyma.")]

    # Count the Glyma values
    count = len(glyma_values)
    
    # Check if all Glyma values are the same
    same = len(set(glyma_values)) == 1 if glyma_values else False
    
    return pd.Series([count, same])

# Apply the function row-wise and add new columns
df[['count', 'same']] = df.apply(count_and_check_same, axis=1)

# Write the output to a new file
df.to_csv(args.output_file, index=False)
