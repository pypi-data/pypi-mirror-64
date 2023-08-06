#!/usr/bin/env Rscript
suppressPackageStartupMessages(library(annotate))
suppressPackageStartupMessages(library(affyio))
suppressPackageStartupMessages(library(oligo))
suppressPackageStartupMessages(library(funr))

cmd_old = file.path(dirname(sys.script()), "rma_affy.R")

split_names = function(arr)
{
  # isolate the top most part of CEL file names
  for(i in 1:length(arr)){
    arr[i] = unlist(strsplit(arr[i], '[.]CEL'))[1]
  }
  
  return (arr)
}


platform_map = list(
  "pd.ht.hg.u133.plus.pm.db" = "hgu133plus2.db",
  "pd.hg.u133.plus.2.db" = "hgu133plus2.db",
  
  "pd.ht.hg.u133a.db" = "hgu133a.db",
  "pd.hg.u133a.db" = "hgu133a.db",
  "pd.hg.u133a.2.db" = "hgu133a2.db",
  
  "pd.hg.u133b.db" = "hgu133b.db",
  
  "pd.hugene.1.0.st.v1.db" = "hugene10sttranscriptcluster.db",
  "pd.hugene.1.1.st.v1.db" = "hugene11sttranscriptcluster.db",
  
  "pd.hugene.2.0.st.db" = "hugene20sttranscriptcluster.db",
  "pd.hugene.2.1.st.db" = "hugene21sttranscriptcluster.db",
  
  "pd.huex.1.0.st.v1.db" = "huex10sttranscriptcluster.db",
  "pd.huex.1.0.st.v2.db" = "huex10sttranscriptcluster.db",
  
  "pd.hta.2.0.db" = "hta20transcriptcluster.db",
  "pd.hg.focus.db" = "hgfocus.db",
  "pd.hg.u95av2.db" = "hgu95av2.db",
  "pd.hg.u219.db" = "hgu219.db",
  
  "pd.hg.u95c.db" = "hgu95c.db",
  "pd.hg.u95d.db" = "hgu95d.db",
  "pd.hg.u95e.db" = "hgu95e.db",
  "pd.chicken.db" = "chicken.db",
  "pd.porcine.db" = "porcine.db",
  "pd.rg.u34a.db" = "rgu34a.db",
  
  "pd.moe430b.db" = "moe430b.db",
  "pd.raex.1.0.st.v1.db" = "raex10sttranscriptcluster.db",
  
  "pd.clariom.d.human.db" = "clariomdhumantranscriptcluster.db",
  "pd.clariom.s.human.db" = "clariomshumantranscriptcluster.db",
  "pd.clariom.s.human.ht.db" = "clariomshumanhttranscriptcluster.db",
  "pd.hu6800.db" = "hu6800.db",
  "pd.bovine.db" = "bovine.db",
  "pd.moe430a.db" = "moe430a.db",
  
  "pd.mg.u74av2.db" = "mgu74av2.db",
  "pd.mg.u74bv2.db" = "mgu74bv2.db",
  "pd.mg.u74cv2.db" = "mgu74cv2.db",
  
  "pd.u133.x3p.db" = "u133x3p.db",
  "pd.hc.g110.db" = "hcg110.db",
  "pd.hg.u95a.db" = "hgu95a.db",
  
  "pd.nugo.hs1a520180.db" = "nugohs1a520180.db",
  
  "pd.mogene.2.0.st.db" = "mogene20sttranscriptcluster.db",
  "pd.mogene.1.0.st.v1.db" = "mogene10sttranscriptcluster.db",
  "pd.mogene.1.1.st.v1.db" = "mogene11sttranscriptcluster.db",
  
  "pd.moex.1.0.st.v1.db" = "moex10sttranscriptcluster.db",
  
  "pd.mouse430.2.db" = "mouse4302.db",
  "pd.mouse430a.2.db" = "mouse4302.db",
  
  "pd.rat230.2.db" = "rat2302.db",
  
  
  ###########################
  # second session for annotation remap
  "HuGene-2_0-st-v1" = "pd.hugene.2.0.st",
  "HuGene-2_0-st-v2" = "pd.hugene.2.0.st",
  "HuEx-1_0-st-ta1" = "pd.huex.1.0.st.v2",
  "HT_HG-U133B" = "pd.hg.u133b",
  "U133AAofAv2" = "pd.hg.u133a.2",
  "HuGeneFL" = "pd.hu6800"
)


process_path = function(input, output, platform)
{
  # read cel files from the same platform in a directory, and convert to probe@gene matrix
  cel_list = list.celfiles(input, full.names=T, listGzipped=T)
  
  # first of all, try to see any standardize platform name
  platform_std = platform_map[[platform]]
  
  if(!is.null(platform_std)){
    cel_list = read.celfiles(cel_list, pkgname=platform_std)
  }else{
    cel_list = read.celfiles(cel_list)
  }
  
  # start rma
  eset = rma(cel_list)
  
  # simplify the column names
  colnames(eset) = split_names(colnames(eset))
  
  # load the annotation file to convert gene symbols
  db = paste(annotation(eset), "db", sep='.')
  
  if(db == "pd.ht.hg.u133.plus.pm.db"){
    featureNames(eset) <- gsub("_PM", "", featureNames(eset))
  }
  
  print(db)
  
  db_std = platform_map[[db]]
  if(!is.null(db_std)){db = db_std}
  
  suppressPackageStartupMessages(library(db, character.only=T))
  
  ID = featureNames(eset)
  Symbol = getSYMBOL(ID, db)
  
  fData(eset) = data.frame(ID=ID, Symbol=Symbol)
  
  # write the rma normalized file to output
  write.exprs(eset, file=output, row.names=paste(ID, Symbol, sep='@'))
  #save(eset, file=paste(output, "rda", sep='.'))
}

# read parameters
commands = commandArgs(trailingOnly=T)
input = commands[1]
output = commands[2]

# analyze the platform first, split if multiple platforms
file_lst = list.files(input, pattern = "CEL")

platform_lst = sapply(file_lst, function(x) read.celfile.header(file.path(input, x))$cdfName)
cnt_map = table(platform_lst)

# for each platform, create a sub path for analysis
N = length(cnt_map)

fout = file(paste(output, "log", sep='.'), "w")

for(i in 1:N)
{
  platform = names(cnt_map)[i]
  
  out_path = paste(output, platform, sep='.')
  if(!dir.exists(out_path)) dir.create(out_path)
  
  sub_lst = names(platform_lst)[platform_lst == platform]
  file.copy(file.path(input, sub_lst), out_path)
  
  out = paste(out_path, 'rma', sep='.')
  
  tryCatch({
    process_path(out_path, out, platform)
    write(paste('Output', platform, sep='\t'), file=fout)
    
  }, warning = function(w) {
    write(paste('Warning', platform, w, sep='\t'), file=fout)
    
  }, error = function(e) {
    # try the old affy package first
    system(paste(cmd_old, out_path, out, sep=' '))
    
    if(file.exists(out)){
      write(paste('Output', platform, 'old', sep='\t'), file=fout)
    }else{
      write(paste('Error', platform, e, sep='\t'), file=fout)
    }
  })
  
  unlink(out_path, recursive=T)
}

close(fout)
