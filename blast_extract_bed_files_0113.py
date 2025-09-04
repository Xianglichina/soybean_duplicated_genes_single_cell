#example usage: python blast_extract_bed_files_0113.py merged_file_new.blast 1202_acr_blast.tsv merged_blast.out

import csv
import re
import sys

def reformat_data(input1, input2, output_file):
    # Load data from input2 into memory for lookups
    acr_to_gene = {}
    combined_loc_to_matched_gene = {}

    with open(input2, 'r') as infile2:
        reader2 = csv.DictReader(infile2, delimiter='\t')
        for row in reader2:
            acr_to_gene[row['ACR']] = row['gene']
            combined_loc_to_matched_gene[f"{row['Gene_Chromosome']}_{row['Upstream_Start']}_{row['Downstream_End']}"] = row['matched_gene']

    # Process input1
    rows = []
    with open(input1, 'r') as infile1:
        reader1 = infile1.readlines()

        for line in reader1:
            fields = line.strip().split()
            query, subject = fields[0], fields[1]

            # Extract and split regions
            query_match = re.match(r"::(\w+):(\d+)-(\d+)", query)
            subject_match = re.match(r"::(\w+):(\d+)-(\d+)", subject)

            if query_match and subject_match:
                query_chromosome, query_start, query_end = query_match.groups()
                subject_chromosome, subject_start, subject_end = subject_match.groups()

                # Combine information for new columns
                query_combined = f"{query_chromosome}_{query_start}_{query_end}"
                subject_combined = f"{subject_chromosome}_{subject_start}_{subject_end}"

                # Find associated genes
                acr_associated_gene = acr_to_gene.get(query_combined, "NA")
                ref_associated_gene = combined_loc_to_matched_gene.get(subject_combined, "NA")

                # Get query and subject positions
                query_start_pos = int(fields[6])
                query_end_pos = int(fields[7])
                subject_start_pos = int(fields[8])
                subject_end_pos = int(fields[9])

                # Calculate percentage alignment
                percentage_alignment = abs(query_start_pos - query_end_pos) / abs(subject_start_pos - subject_end_pos)

                # Get bit score
                bit_score = float(fields[-1])

                # Store row with additional information
                rows.append({
                    "Query_Chromosome": query_chromosome,
                    "Query_Start": query_start,
                    "Query_End": query_end,
                    "Subject_Chromosome": subject_chromosome,
                    "Subject_Start": subject_start,
                    "Subject_End": subject_end,
                    "Query_Combined": query_combined,
                    "Subject_Combined": subject_combined,
                    "ACR_associated_gene": acr_associated_gene,
                    "ref_associated_gene": ref_associated_gene,
                    "Identity": fields[2],
                    "Alignment_Length": fields[3],
                    "Mismatches": fields[4],
                    "Gaps": fields[5],
                    "Query_Start_Pos": query_start_pos,
                    "Query_End_Pos": query_end_pos,
                    "Subject_Start_Pos": subject_start_pos,
                    "Subject_End_Pos": subject_end_pos,
                    "E_Value": fields[10],
                    "Bit_Score": bit_score,
                    "Percentage_Alignment": percentage_alignment
                })

    # Filter rows to retain only the highest bit score for each unique (Query_Combined, Subject_Combined)
    filtered_rows = {}
    for row in rows:
        key = (row["Query_Combined"], row["Subject_Combined"])
        if key not in filtered_rows or row["Bit_Score"] > filtered_rows[key]["Bit_Score"]:
            filtered_rows[key] = row

    # Write the filtered rows to the output file
    with open(output_file, 'w', newline='') as outfile:
        writer = csv.writer(outfile, delimiter='\t')
        writer.writerow([
            "Query_Chromosome", "Query_Start", "Query_End",
            "Subject_Chromosome", "Subject_Start", "Subject_End",
            "Query_Combined", "Subject_Combined",
            "ACR_associated_gene", "ref_associated_gene",
            "Identity", "Alignment_Length", "Mismatches", "Gaps",
            "Query_Start_Pos", "Query_End_Pos", "Subject_Start_Pos",
            "Subject_End_Pos", "E_Value", "Bit_Score", "Percentage_Alignment"
        ])
        for row in filtered_rows.values():
            writer.writerow([
                row["Query_Chromosome"], row["Query_Start"], row["Query_End"],
                row["Subject_Chromosome"], row["Subject_Start"], row["Subject_End"],
                row["Query_Combined"], row["Subject_Combined"],
                row["ACR_associated_gene"], row["ref_associated_gene"],
                row["Identity"], row["Alignment_Length"], row["Mismatches"], row["Gaps"],
                row["Query_Start_Pos"], row["Query_End_Pos"], row["Subject_Start_Pos"],
                row["Subject_End_Pos"], row["E_Value"], row["Bit_Score"], row["Percentage_Alignment"]
            ])

if __name__ == "__main__":
    # Provide input and output file names via command line arguments
    if len(sys.argv) != 4:
        print("Usage: python script.py <input_file1> <input_file2> <output_file>")
        sys.exit(1)

    input_file1 = sys.argv[1]
    input_file2 = sys.argv[2]
    output_file = sys.argv[3]

    reformat_data(input_file1, input_file2, output_file)
