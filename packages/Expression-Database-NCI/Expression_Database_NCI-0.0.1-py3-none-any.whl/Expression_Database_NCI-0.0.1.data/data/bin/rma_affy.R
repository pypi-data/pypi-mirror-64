#!/usr/bin/env Rscript
suppressPackageStartupMessages(library(annotate))
suppressPackageStartupMessages(library(affy))

split_names = function(arr)
{
  # isolate the top most part of CEL file names
  for(i in 1:length(arr)){arr[i] = unlist(strsplit(arr[i], '[.]CEL'))[1]}
  return (arr)
}

platform_map = list()

# read parameters
commands = commandArgs(trailingOnly=T)

input = commands[1]
output = commands[2]

eset = justRMA(celfile.path=input)
colnames(eset) = split_names(colnames(eset))

db = paste(annotation(eset), "db", sep='.')
db_std = platform_map[[db]]
if(!is.null(db_std)){db = db_std}

suppressPackageStartupMessages(library(db, character.only=T))

ID = featureNames(eset)
Symbol = getSYMBOL(ID, db)

fData(eset) = data.frame(ID=ID, Symbol=Symbol)

write.exprs(eset, file=output, row.names=paste(ID, Symbol, sep='@'))
#save(eset, file=paste(output, "rda", sep='.'))
