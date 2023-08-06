#!/usr/bin/env Rscript
library(recount)

commands = commandArgs(trailingOnly=T)
fpath = commands[1]

files = list.files(fpath, pattern = "*.Rdata")

for (f in files)
{
  load(file.path(fpath, f))
  rse_gene = assay(scale_counts(rse_gene))
  rse_gene = rse_gene[rowMeans(rse_gene == 0) < 1,]
  write.table(rse_gene, file=file.path(fpath, gsub(".Rdata", ".Count", f)), sep='\t', quote=F)
  rm(rse_gene)
}
