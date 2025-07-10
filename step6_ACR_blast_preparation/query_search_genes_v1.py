import pandas as pd
import os
import sys

def process_gene_data(original_file, gene_list_file, output_dir):
    # Read the original file and gene list file
    original_data = pd.read_csv(original_file, sep="\t")
    gene_list = pd.read_csv(gene_list_file, header=None, names=["GeneID"])
    
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    results = []
    chromosome_mismatches = []

    for gene in gene_list["GeneID"]:
        # Find the row of the target gene
        gene_row = original_data[original_data["GeneID"] == gene]

        if not gene_row.empty:
            chromosome = gene_row.iloc[0]["Chromosome"]
            gene_start = gene_row.iloc[0]["Start"]
            gene_end = gene_row.iloc[0]["End"]

            # Filter chrom_data and reset index
            chrom_data = original_data[original_data["Chromosome"] == chromosome].reset_index(drop=True)

            # Find the index of the target gene in the chromosome data
            gene_index = chrom_data.index[chrom_data["GeneID"] == gene].tolist()[0]

            # Locate valid previous and next genes
            prev_gene = None
            for i in range(gene_index - 1, -1, -1):
                candidate_prev = chrom_data.iloc[i]
                if candidate_prev["Start"] < gene_start:
                    prev_gene = candidate_prev
                    break

            next_gene = None
            for i in range(gene_index + 1, len(chrom_data)):
                candidate_next = chrom_data.iloc[i]
                if candidate_next["End"] > gene_end:
                    next_gene = candidate_next
                    break

            # Fallback: Include the second previous or next gene if still invalid
            if prev_gene is None and gene_index > 1:
                prev_gene = chrom_data.iloc[max(gene_index - 2, 0)]  # Ensure no out-of-bounds access
            if next_gene is None and gene_index < len(chrom_data) - 2:
                next_gene = chrom_data.iloc[min(gene_index + 2, len(chrom_data) - 1)]  # Ensure no out-of-bounds access

            # Extract relevant details for results
            prev_chromosome = prev_gene["Chromosome"] if prev_gene is not None else None
            next_chromosome = next_gene["Chromosome"] if next_gene is not None else None

            results.append({
                "GeneID": gene,
                "Chromosome": chromosome,
                "Start": gene_start,  # Add start of the queried gene
                "End": gene_end,      # Add end of the queried gene
                "Prev_GeneID": prev_gene["GeneID"] if prev_gene is not None else None,
                "Prev_Chromosome": prev_chromosome,
                "Prev_Start": prev_gene["Start"] if prev_gene is not None else None,
                "Prev_End": prev_gene["End"] if prev_gene is not None else None,
                "Next_GeneID": next_gene["GeneID"] if next_gene is not None else None,
                "Next_Chromosome": next_chromosome,
                "Next_Start": next_gene["Start"] if next_gene is not None else None,
                "Next_End": next_gene["End"] if next_gene is not None else None
            })

            # Check for chromosome mismatches
            if (prev_chromosome != chromosome and prev_chromosome is not None) or \
               (next_chromosome != chromosome and next_chromosome is not None):
                chromosome_mismatches.append({
                    "GeneID": gene,
                    "Chromosome": chromosome,
                    "Start": gene_start,  # Add start of the queried gene
                    "End": gene_end,      # Add end of the queried gene
                    "Prev_GeneID": prev_gene["GeneID"] if prev_gene is not None else None,
                    "Prev_Chromosome": prev_chromosome,
                    "Prev_Start": prev_gene["Start"] if prev_gene is not None else None,
                    "Prev_End": prev_gene["End"] if prev_gene is not None else None,
                    "Next_GeneID": next_gene["GeneID"] if next_gene is not None else None,
                    "Next_Chromosome": next_chromosome,
                    "Next_Start": next_gene["Start"] if next_gene is not None else None,
                    "Next_End": next_gene["End"] if next_gene is not None else None
                })
        else:
            print(f"GeneID {gene} not found in the original file.")

    # Save results to files
    results_df = pd.DataFrame(results)
    results_file = os.path.join(output_dir, "gene_neighbors.csv")
    results_df.to_csv(results_file, index=False)
    print(f"Gene neighbors saved to: {results_file}")

    if chromosome_mismatches:
        mismatches_df = pd.DataFrame(chromosome_mismatches)
        mismatches_file = os.path.join(output_dir, "chromosome_mismatches.csv")
        mismatches_df.to_csv(mismatches_file, index=False)
        print(f"Chromosome mismatches saved to: {mismatches_file}")
    else:
        print("No chromosome mismatches found.")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python gene_neighbors.py <original_file> <gene_list_file> <output_dir>")
        sys.exit(1)

    original_file = sys.argv[1]
    gene_list_file = sys.argv[2]
    output_dir = sys.argv[3]

    process_gene_data(original_file, gene_list_file, output_dir)
