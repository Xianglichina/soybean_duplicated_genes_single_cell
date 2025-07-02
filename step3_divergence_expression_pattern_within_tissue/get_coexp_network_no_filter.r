# Script to generate gene-gene correlation network from 
# gene expression x tissue samples data

# Function to build rank-standardized coexpression network from tissue replicates
build_coexp_network <- function(net, method = "spearman", flag = "rank") {
  # Calculate correlation coefficients
  genes = rownames(net)
  net = net[rowSums(net) > 0, ]
  
  # Calculate correlation matrix
  net = cor(t(net), method = method)
  
  # Create network
  temp = net[upper.tri(net, diag = TRUE)]
  if (flag == "abs") {
    temp = abs(temp)
  }
  
  temp = rank(temp, ties.method = "average")
  net[upper.tri(net, diag = TRUE)] = temp
  net = t(net)
  net[upper.tri(net, diag = TRUE)] = temp
  net = net / max(net, na.rm = TRUE)
  
  # Fill missing genes with median values
  med = median(net, na.rm = TRUE)
  ind = setdiff(genes, rownames(net))
  temp = matrix(med, length(ind), dim(net)[2])
  rownames(temp) = ind
  net = rbind(net, temp)
  temp = matrix(med, dim(net)[1], length(ind))
  colnames(temp) = ind
  net = cbind(net, temp)
  
  # Reorder to original
  net = net[genes, genes]
  diag(net) = 1
  
  return(net)
}

# Function to get median expression
get_median_exp <- function(tissues) {
  med_exp = unlist(lapply(1:dim(tissues)[2], function(ii) (median(tissues[, ii], na.rm = TRUE))))
  med_mat = matrix(rep(med_exp, each = dim(tissues)[1]), nrow = dim(tissues)[1])
  med_NA = (tissues > med_mat)
  return(med_NA)
}

# Capture command line arguments
args <- commandArgs(trailingOnly = TRUE)

# Check if the input file argument is provided
if (length(args) < 1) {
  stop("Please provide the input file as the first argument.")
}

# The input file path
input_file <- args[1]

# List of species
spename = c('early_nodule')

# Load expression data from the input file
exp1 = read.csv(input_file, row.names = 1)
exp1 <- as.matrix(exp1)
print(dim(exp1))

# Get expression matrix with 1 indicating above-median expression
#med_atlas <- get_median_exp(exp1)
#exp1 <- exp1[which(rowSums(med_atlas) > 0), ]
#print(dim(exp1))

# Build coexpression network for all genes with above-median expression
prionet_atlas = build_coexp_network(exp1, method = 'pearson')

# Save the network
save(prionet_atlas, file = paste0(spename, '_coexp_network.Rdata'))

