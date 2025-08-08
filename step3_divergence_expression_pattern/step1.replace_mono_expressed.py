import pandas as pd
import sys

# Get input and output file names from command line arguments
input1_file = sys.argv[1]  # Main input file
expression_files = sys.argv[2:9]  # Seven expression files
output_file = sys.argv[9]  # Output file

# Load input1
df_input1 = pd.read_csv(input1_file, sep=",", encoding="utf-8")

# Load all expression data into a dictionary
expression_data = {}
for file in expression_files:
    tissue_name = file.replace("_filter_one_expression_expressed.csv", "")
    df_exp = pd.read_csv(file, sep=",", encoding="utf-8")
    expression_data[tissue_name] = df_exp.set_index("Gene_Pair")["expressed"].to_dict()

# Iterate over columns that start with "expression_type_" and replace "mono_expressed"
for col in df_input1.columns:
    if col.startswith("expression_type_"):
        tissue = col.replace("expression_type_", "")
        if tissue in expression_data:
            df_input1[col] = df_input1.apply(
                lambda row: expression_data[tissue].get(row["Gene_Pair"], row[col])
                if row[col] == "mono_expressed" else row[col], axis=1)

# Save the modified dataframe
df_input1.to_csv(output_file, index=False, sep=",", encoding="utf-8")
