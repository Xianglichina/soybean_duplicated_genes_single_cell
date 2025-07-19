import pandas as pd
import sys

def load_expression_data(file1):
    # Read gene expression data from Input 1
    expression_df = pd.read_csv(file1, index_col=0)
    return expression_df

def load_gene_pairs(file2):
    # Read gene pairs from Input 2, using the first and third columns
    gene_pairs_df = pd.read_csv(file2, usecols=[0, 2], header=None)
    gene_pairs_df.columns = ['Gene1', 'Gene2']
    return gene_pairs_df

def get_shared_column_name(col_name1, col_name2):
    # Find the shared part between two column names (before the first '.' or '_' delimiter)
    return ''.join([c1 for c1, c2 in zip(col_name1, col_name2) if c1 == c2]).strip('_.')

def generate_gene_pair_dataframe(expression_df, gene_pairs_df):
    pair_data = []
    
    # Number of replicates in expression data (assumed to be in pairs of two)
    num_columns = expression_df.shape[1]
    num_replicates = 2  # Two replicates per condition/cell type
    
    # Iterate over each gene pair
    for _, row in gene_pairs_df.iterrows():
        gene1, gene2 = row['Gene1'], row['Gene2']
        
        # Check if gene1 and gene2 exist in the expression dataframe, otherwise fill with zeroes
        gene1_data = expression_df.loc[gene1] if gene1 in expression_df.index else pd.Series([0] * num_columns, index=expression_df.columns)
        gene2_data = expression_df.loc[gene2] if gene2 in expression_df.index else pd.Series([0] * num_columns, index=expression_df.columns)
        
        # Iterate over every two columns (paired replicates)
        for i in range(0, num_columns, num_replicates):
            col1, col2 = expression_df.columns[i], expression_df.columns[i+1]
            
            # Extract the shared name part (e.g., "heart" if col1="heart_1" and col2="heart_2")
            shared_name = get_shared_column_name(col1, col2)
            
            # Add the expression values of both genes for the pair of replicates
            pair_data.append({
                "Gene_Pair": f"{gene1} vs {gene2}",
                "Gene1_Replicate_1": gene1_data.iloc[i],
                "Gene1_Replicate_2": gene1_data.iloc[i+1],
                "Gene2_Replicate_1": gene2_data.iloc[i],
                "Gene2_Replicate_2": gene2_data.iloc[i+1],
                "Cell_Type": shared_name  # Include the shared part of the column names
            })
    
    # Convert the pair data to a DataFrame
    pair_df = pd.DataFrame(pair_data).set_index("Gene_Pair")
    return pair_df

def main(file1, file2, output_file):
    # Load the input files
    expression_df = load_expression_data(file1)
    gene_pairs_df = load_gene_pairs(file2)
    
    # Generate the gene pair dataframe
    gene_pair_expression_df = generate_gene_pair_dataframe(expression_df, gene_pairs_df)
    
    # Output the dataframe to a CSV file
    gene_pair_expression_df.to_csv(output_file)
    
    # Print success message
    print(f"Gene pair expression data has been saved to {output_file}")

if __name__ == "__main__":
    # Command-line arguments for input files
    if len(sys.argv) != 4:
        print("Usage: python script.py <expression_data.csv> <gene_pairs.csv> <output_file.csv>")
        sys.exit(1)
    
    # Assign command-line arguments to variables
    file1 = sys.argv[1]  # Gene expression data file
    file2 = sys.argv[2]  # Gene pairs file
    output_file = sys.argv[3]  # Output file to save the result
    
    # Run the main function
    main(file1, file2, output_file)
