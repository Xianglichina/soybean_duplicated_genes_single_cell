#!/bin/bash
#SBATCH --job-name=duplicated_gene_sets_tree
#SBATCH --partition=batch
#SBATCH --ntasks=1
#SBATCH --mem=20gb
#SBATCH --time=4:00:00
#SBATCH --output=duplicated_gene_sets_tree.%j.out
#SBATCH --error=duplicated_gene_sets_tree.%j.err
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user=xl20359@uga.edu

output_file="glyma_output_sets.txt"
echo -e "fam\tgeneA1\tgeneA2\tgeneB1\tgeneB2" > "$output_file"

for fam in legume.fam3.VLMQ.sup1B_trees/Legume.fam3*; do
  echo "Processing file: $fam"

  # Step 1: Simplify tree
  simplified=$(perl -pe '
    s/\(/</g; s/\)/>/g;
    s/([<,])(\w+)\.[^:]+:\d+\.\d+/$1$2/g;
    s/>\d+\.\d+/>/g;
    s/:\d+\.\d+//g
  ' "$fam")

  echo "Simplified tree snippet:"
  echo "$simplified" | head -5

  # Extract all <glyma,glyma> pairs
  matches=()
  tempfile=$(mktemp)
  echo "$simplified" | perl -nle 'while (/<(glyma),(glyma)>/g) { print "<$1,$2>" }' > "$tempfile"

  echo "Extracted pairs:"
  cat "$tempfile"

  while IFS= read -r line; do
    matches+=("$line")
  done < "$tempfile"
  rm "$tempfile"

  echo "Number of matched pairs: ${#matches[@]}"

  if [ "${#matches[@]}" -eq 2 ]; then
    echo "Matched Glyma groups:"
    echo "${matches[0]}"
    echo "${matches[1]}"
    echo ""

    # Step 2: Extract full gene IDs before ':' inside each parenthesis pair in original file
    perl -ne '
      BEGIN {
        $fam = "'"$fam"'";
        $fam =~ s|.*/||;
      }
      while (/\((glyma[^:]+):[^,]+,(glyma[^:]+):[^\)]+\)/gi) {
        if (!$seen1++) {
          ($a1, $a2) = ($1, $2);
        } elsif (!$seen2++) {
          ($b1, $b2) = ($1, $2);
        }
      }
      END {
        if ($a1 && $a2 && $b1 && $b2) {
          print "$fam\t$a1\t$a2\t$b1\t$b2\n";
        } else {
          print STDERR "No valid pairs found in original file for $fam\n";
        }
      }
    ' "$fam" >> "$output_file"

  else
    echo "Did not find exactly 2 Glyma pairs in $fam"
  fi
done
