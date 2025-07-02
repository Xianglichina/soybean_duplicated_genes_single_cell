# paralog_coexpression.R

### ........................................................... ###
### script to calculate the paralog pair coexpression relative 
### to all other expressed genes in the data
###
### specificity of paralog pair correlation is used as a proxy
### for functional similarity in later analysis
### ........................................................... ###

# Function to calculate specificity of coexpression
calc_spec <- function (res, np, nL){    
  ranks = 1:nL
  mini = sum(ranks[1:np])
  range = np * (nL - np)
  
  temp1 = t(apply(res, 1, function(x) rank(x, ties.method = "average")))      
  spec1 <- (temp1 - mini) / range   
  temp2 = t(apply(t(res), 1, function(x) rank(x, ties.method = "average")))      
  spec2 <- (temp2 - mini) / range
  spec = 0.5 * (spec1 + t(spec2))
  
  return(spec)  # return full matrix
}

# Main function to calculate coexpression
main <- function() {
  # Get command-line arguments
  args <- commandArgs(trailingOnly = TRUE)
  if (length(args) != 2) {
    stop("Please provide two input files: 1) paralog pairs file, 2) coexpression network file")
  }
  
  paralog_file <- args[1]
  network_file <- args[2]
  
  # Load table of paralog pairs
  df <- read.csv(paralog_file)
  
  # Load gene coexpression network
  load(network_file) # Assumes network file is an .Rdata file containing 'prionet_atlas'
  diag(prionet_atlas) <- 0
  
  # Calculate specificity of coexpression
  corrspec <- calc_spec(prionet_atlas, 1, dim(prionet_atlas)[1])
  
  # Get expressolog scores for paralog pairs
  allgenes <- rownames(corrspec)
  df$coexpression <- NA
  
  for (id in 1:nrow(df)) {
    g1 <- match(df$Gene1[id], allgenes)
    g2 <- match(df$Gene2[id], allgenes)
    
    if (!is.na(g1 + g2)) {
      df$coexpression[id] <- corrspec[g1, g2] 
    }
  }
  
  # Save results
  output_file <- paste0(tools::file_path_sans_ext(network_file), "_paralog_pair_coexpression.csv")
  write.table(df, output_file, sep = ',', row.names = FALSE, col.names = TRUE, quote = FALSE)
  
  cat("Results saved to:", output_file, "\n")
}

# Run the script
main()
