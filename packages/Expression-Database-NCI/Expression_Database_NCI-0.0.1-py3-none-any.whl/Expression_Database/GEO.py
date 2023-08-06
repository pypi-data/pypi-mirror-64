import os
import sys
import numpy
import shutil
import re
import glob
import pandas
import urllib
import GEOparse

from bioservices import RNASEQ_EBI
from Expression_Database.util import script_path, space_char


#######################################################################################################################################
# Tool functions

def create_SRA_maps(f):
    # create SRR ID map to GSM, SRX (Experiment), and SAM (BioSample)
    data = pandas.read_csv(f + '.tab.gz', sep='\t', index_col=0, low_memory=False)
    data = data.loc[map(lambda v: v[:3] == 'SRR', data.index)]

    spliter_nondigit = re.compile('[^0-9a-zA-Z]')

    for field, keyword in [
        ['Alias', 'GSM'],
        ['Experiment', 'SRX'],
        ['BioSample', 'SAM'],
        ]:
        print(field, keyword)

        data_sub = data.loc[:, field]
        data_sub = data_sub.loc[data_sub.apply(lambda v: str(v).find(keyword) == 0)]
        data_sub = data_sub.apply(lambda v: spliter_nondigit.split(v)[0])
        
        # unique key map
        assert data_sub.index.value_counts().max() == 1
        data_sub.to_csv(f + '.' + keyword + '.gz', sep='\t', header=False, compression='gzip')



def load_SRR_maps(fprefix):
    lst = []
    
    for title in ['GSM', 'SAM']:
        lst.append(pandas.read_csv(fprefix + '.' + title + '.gz', sep='\t', index_col=0, header=None).iloc[:,0])
    
    return lst


def load_SAM_GSM_map(fprefix):
    # create SRX to GSM from meta relations
    meta = pandas.read_csv(fprefix + '.meta.full.gz', sep='\t', index_col=0)
    map_SAM_GSM = {}

    for ID, arr in meta.iterrows():
        relations = str(arr['relation']).split('BioSample:',1)
        
        if len(relations) > 1:
            ID_SAM = relations[-1].strip().split()[0]
            map_SAM_GSM[os.path.basename(ID_SAM).strip()] = ID.strip()
    
    return pandas.Series(map_SAM_GSM, name='SAM_GSM')



def translate_SRA_columns(GSE_ID, SRA_ID, data, map_SAM_GSM, map_SRR_GSM, map_SRR_SAM, API_key):
    lst_candidate = []
    
    # stage 1: direct translation
    lst_SRR_GSM = map_SRR_GSM.reindex(data.columns)

    if sum(lst_SRR_GSM.isnull()) == 0:
        data.columns = lst_SRR_GSM
        return True
    else:
        lst_candidate.append(lst_SRR_GSM)
    
    # stage 2: indirect translation
    lst_SRR_SAM = map_SRR_SAM.reindex(data.columns)
    lst_SAM_GSM = map_SAM_GSM.reindex(lst_SRR_SAM)

    if sum(lst_SAM_GSM.isnull()) == 0:
        data.columns = lst_SAM_GSM
        return True
    else:
        lst_candidate.append(lst_SAM_GSM)
    
    # stage 3: online translation
    # URL for SRA run information
    SRA_info = 'https://trace.ncbi.nlm.nih.gov/Traces/sra/sra.cgi?save=efetch&db=sra&rettype=runinfo&term=%s'
    
    # the NCBI eutil has access limitation, API key can increase to 10 per seconds
    if API_key is not None: SRA_info += ('&api_key=%s' % API_key)
    
    # translate column names
    try:
        run_info = pandas.read_csv(SRA_info % SRA_ID)
        run_info.index = run_info['Run']
        run_info = run_info['SampleName']
        
        lst_efetch = run_info.reindex(data.columns)
        flag = lst_efetch.apply(lambda v: str(v).find('GSM') != 0)
        lst_efetch.loc[flag] = None
        
        if sum(lst_efetch.isnull()) == 0:
            data.columns = lst_efetch
            return True
        else:        
            lst_candidate.append(lst_efetch)
    except:
        sys.stderr.write('Error %s : SRA %s read runinfo failure\n' % (GSE_ID, SRA_ID))
    
    inx = numpy.argmin([sum(lst.isnull()) for lst in lst_candidate])
    data.columns = lst_candidate[inx]
    
    return False


#######################################################################################################################################
# Main functions

def GEO_meta(GSE_ID, GSE_Path, flag_enforce = False):
    # get the meta information of GEO entry, store the processed data in GSE_Path
    # Return : None, if failed. otherwise information
    
    meta = os.path.join(GSE_Path, GSE_ID + '.meta')
    
    if not flag_enforce and os.path.exists(meta + '.summary'):
        return pandas.read_csv(meta + '.summary', sep='\t', index_col=0, header=None).iloc[:,0]
    
    # parse GEO meta data from the database
    try:
        gse = GEOparse.get_GEO(geo = GSE_ID, destdir = GSE_Path, silent=True)
    except:
        sys.stderr.write('Error %s : GEOparse failure\n' % GSE_ID)
        return None
    
    # test if all fields exists
    for v in ['title', 'summary']:
        if v not in gse.metadata:
            sys.stderr.write('Error %s : missing title or summary\n' % GSE_ID)
            return None
    
    # no platform information
    if gse.gpls is None or len(gse.gpls) == 0:
        sys.stderr.write('Error %s : missing platform information\n' % GSE_ID)
        return None
    
    
    
    # assemble technology list
    merge = []
    
    for _, platform in gse.gpls.items():
        assert len(platform.metadata['technology']) == 1    
        technology = platform.metadata['technology'][0]
        if technology.lower() == 'other': technology = platform.metadata['title'][0]
        
        technology = space_char.sub(' ', technology).strip()
        merge.append(technology.replace(',', '-'))
    
    technology = ','.join(merge)
    
    status = 'Regular'
    
    # test is super series first
    for v, lst in gse.relations.items():
        if v.find('SuperSeries') >= 0: status = 'Super ' + ','.join(lst)
    
    # individual series with all basic information
    title = ' '.join(gse.metadata['title'])
    summary = ' '.join(gse.metadata['summary'])
    
    
    # design may not be available
    design = gse.metadata.get('overall_design')
    
    if design is None:
        design = ''
    else:
        design = ' '.join(design)
    
    # remove potential trouble chars
    title = space_char.sub(' ', title).strip()
    summary = space_char.sub(' ', summary).strip()
    design = space_char.sub(' ', design).strip()
    
    
    # assemble experimental platforms information
    merge = []
    for _, gpl in gse.gpls.items():
        platform = ' '.join(gpl.metadata.get('title'))
        
        # simply the previous bracket
        if platform[0] == '[': platform = platform.split(']',1)[1]
        
        platform = space_char.sub(' ', platform).strip()
        merge.append(platform.replace(',', '-'))
    
    experiment_platform = ','.join(merge)
    
    
    # merge sample meta information
    merge = []
    merge_full = []
    
    for gsm_name, gsm in gse.gsms.items():    
        vmap = {}
        vmap_full = {}
        
        for key, value_lst in gsm.metadata.items():
            v = vmap_full[key] = ' '.join(value_lst).strip()
            
            if key.lower() in ['title', 'source_name_ch1', 'organism_ch1', 'description']:
                vmap[key] = v
            
            elif key.lower().find('characteristics') == 0:
                for value in value_lst:
                    if value.find(':') > 0:
                        t, value = value.split(':', 1)
                        vmap[t.strip()] = value.strip()
        
        if len(vmap) > 0:
            merge.append(pandas.Series(vmap, name=gsm_name))
        
        if len(vmap_full) > 0:
            merge_full.append(pandas.Series(vmap_full, name=gsm_name))
    
    
    if len(merge) == 0:
        sys.stderr.write('Error %s : No meta information\n' % GSE_ID)
        return None
    
    meta_info = pandas.concat(merge, axis=1, join='outer', sort=False).transpose()
    
    meta_info.rename(columns={
        'source_name_ch1': 'source name',
        'organism_ch1': 'organism',
        }, inplace=True)
    
    meta_info.to_csv(meta, sep='\t', index_label = 'ID')
    
    meta_info_full = pandas.concat(merge_full, axis=1, join='outer', sort=False).transpose()
    meta_info_full.to_csv(meta + '.full.gz', sep='\t', index_label = 'ID', compression = 'gzip')
    
    meta_summary = pandas.Series(
        [title, summary, design, experiment_platform, technology, status, meta_info.shape[0]],
        index=['title', 'summary', 'design', 'platform', 'technology', 'status', 'count'])
    
    meta_summary.to_csv(meta + '.summary', sep='\t', header=False)
    
    return meta_summary




def GEO_MicroArray(GSE_ID, GSE_Path, flag_enforce = False):
    # Get a data matrix if it is MicroArray
    # Return matrix list, None if failed

    # output prefix
    output = os.path.join(GSE_Path, GSE_ID + '.MicroArray')
    
    if not flag_enforce and os.path.exists(output):
        return pandas.read_csv(output, sep='\t', header=None).iloc[:,0].tolist()
    
    # clear existing file
    os.system('rm -rf ' + output + '*')
    os.system('rm -rf ' + os.path.join(GSE_Path, 'Supp*'))

    # parse GEO meta data from the database
    try:
        gse = GEOparse.get_GEO(geo = GSE_ID, destdir = GSE_Path, silent=True)
    except:
        sys.stderr.write('Error %s : GEOparse failure\n' % GSE_ID)
        return None
        
    # no platform information
    if gse.gpls is None or len(gse.gpls) == 0:
        sys.stderr.write('Error %s : missing platform information\n' % GSE_ID)
        return None

    # potential names for gene symbol columns
    symbol_column_lst = [
        '^gene.symbol',
        'gene.symbol',
        
        '^symbol',
        '^entrez',
        
        'gene.assignment',
        '^gb_acc',
        '^gene$',
        '^GB_LIST$',
        '^orf$',
        ]
    
    for i in range(len(symbol_column_lst)):
        symbol_column_lst[i] = re.compile(symbol_column_lst[i], re.IGNORECASE)  # @UndefinedVariable
    
    matrix_list = []
    platform_map = {}

    # test whether Affymetrix CEL data exists
    flag_Affymetrix = False
    
    for platform_ID, platform in gse.gpls.items():
        if ' '.join(platform.metadata.get('title')).lower().find('affymetrix') >= 0:
            flag_Affymetrix = True

        annotation = platform.table
        if annotation.shape[0] == 0: continue
        
        # very unlikely
        if 'ID' not in annotation.columns:
            sys.stderr.write('Error %s : platform %s has no ID column\n' % (GSE_ID, platform_ID))
            continue
        
        annotation.index = annotation['ID']

        if annotation.index.value_counts().max() > 1:
            sys.stderr.write('Error %s : platform %s has duplicated index\n' % (GSE_ID, platform_ID))
            continue
        
        # search the fields for gene names
        for pattern in symbol_column_lst:
            flag = [pattern.search(v) is not None for v in annotation.columns]
            if sum(flag):
                annotation = annotation.loc[:, annotation.columns[flag][0]]
                break

        # if cannot find gene symbol columns, ignore such platform
        if type(annotation) == pandas.DataFrame:
            sys.stderr.write('Error %s : platform %s has no gene name column\n' % (GSE_ID, platform_ID))
            continue

        platform_map[platform.name] = annotation.dropna()
    
    ################################################################################
    # First, unified processing for Affymetrix platform
    if flag_Affymetrix:
        gse.download_supplementary_files(directory=GSE_Path, download_sra = False)
    
        CEL_lst = glob.glob(os.path.join(GSE_Path, 'Supp*', '**', '*.CEL*'), recursive = True)
    
        if len(CEL_lst) > 0:
            if not os.path.exists(output): os.mkdir(output)
            
            for f in CEL_lst: shutil.move(f, os.path.join(output, os.path.basename(f)))
            
            os.system(' '.join([os.path.join(script_path, 'rma_oligo.R'), output, output]))
            shutil.rmtree(output)
            
            if os.path.exists(output + '.log'):
                fin = open(output + '.log')
                for l in fin:
                    fields = l.strip().split()
    
                    if len(fields) > 0 and fields[0] == 'Output':
                        out = output + '.' + fields[1] + '.rma'
                        assert os.path.exists(out) # if log file write it, it must exist
                        os.system('gzip ' + out)
                        
                        matrix_list.append(out + '.gz')
                fin.close()
            else:
                sys.stderr.write('Error %s : rma_oligo failure\n' % GSE_ID)


        Supp_lst = glob.glob(os.path.join(GSE_Path, 'Supp*'))
        for f in Supp_lst: shutil.rmtree(f)

    ################################################################################
    # Second, split GSM profiles to different platforms
    if len(platform_map) > 0:
        merge_map = {}

        for gsm_ID, gsm in gse.gsms.items():
            data = gsm.table
            if data.shape[0] == 0: continue

            if 'ID_REF' not in data.columns or 'VALUE' not in data.columns:
                sys.stderr.write('Error %s : sample %s has no ID_REF or VALUE columns\n' % (GSE_ID, gsm_ID))
                continue

            data.index = data['ID_REF']
            data = data['VALUE']
            data.name = gsm_ID

            platform = gsm.metadata['platform_id']
            assert len(platform) == 1
            platform = platform[0]

            annotation = platform_map.get(platform)
            if annotation is None:
                sys.stderr.write('Error %s : sample %s has no platform annotation\n' % (GSE_ID, gsm_ID))
                continue

            data = data.loc[data.index.intersection(annotation.index)]
            data = data.groupby(annotation.loc[data.index]).median()

            merge = merge_map.get(platform)
            if merge is None:
                merge = merge_map[platform] = []

            merge.append(data)

        for platform, merge in merge_map.items():
            data = pandas.concat(merge, axis=1, join='inner')

            out = output + '.' + platform + '.GEO.gz'
            data.to_csv(out, sep='\t', index_label=False, compression='gzip')
            
            matrix_list.append(out)


    for i in range(len(matrix_list)):
        matrix_list[i] = os.path.relpath(matrix_list[i], GSE_Path)
    
    if len(matrix_list) > 0:
        fout = open(output, 'w')
        for f in matrix_list: fout.write(f + '\n')
        fout.close()
    
    return matrix_list




def GEO_RNASeq(GSE_ID, GSE_Path, flag_enforce = False, flag_translate = True, API_key=None):
    # Get a data matrix if it is RNASeq
    # Return matrix list, None if failed
    # flag_enforce: enforce download from scratch, ignore previous results
    # flag_translate: translate SRA names to GSM
    # API_Key: for e-utils to increase to 10 per seconds

    # output prefix
    output = os.path.join(GSE_Path, GSE_ID + '.RNASeq')
    
    if not flag_enforce and os.path.exists(output):
        return pandas.read_csv(output, sep='\t', header=None).iloc[:,0].tolist()
    
    # clear existing files
    os.system('rm -rf ' + output + '*')
    
    try:
        gse = GEOparse.get_GEO(geo = GSE_ID, destdir = GSE_Path, silent=True)
    except:
        sys.stderr.write('Error %s : GEOparse failure\n' % GSE_ID)
        return None

    # search SRA
    r = RNASEQ_EBI()
    
    # URL for SRA run information
    SRA_info = 'https://trace.ncbi.nlm.nih.gov/Traces/sra/sra.cgi?save=efetch&db=sra&rettype=runinfo&term=%s'
    
    # the NCBI eutil has access limitation, API key can increase to 10 per seconds
    if API_key is not None: SRA_info += ('&api_key=%s' % API_key)
    
    
    relations = gse.metadata.get('relation')
    if relations is None:
        sys.stderr.write('Warning %s : Cannot find any SRA relation information\n' % GSE_ID)
        return None
    
    matrix_list = []
    
    fout = open(output + '.external_ID', 'w')
    
    for relation in relations:
        if relation.find('SRA') == 0:
            SRA_ID = relation.split('=')[-1]
            
            # processed data
            try:
                results = r.get_study(SRA_ID, frmt='tsv')
            except:
                sys.stderr.write('Error %s : SRA %s RNASEQ_EBI get_study failure\n' % (GSE_ID, SRA_ID))
                continue
            
            if results is None or results.shape[0] == 0:
                sys.stderr.write('Warning %s : SRA %s is not processed\n' % (GSE_ID, SRA_ID))
                continue
            
            # SRA run information
            runinfo = None
            
            if flag_translate:
                # load run info for sample name translation
                try:
                    runinfo = pandas.read_csv(SRA_info % SRA_ID)
                except:
                    sys.stderr.write('Error %s : SRA %s read runinfo failure\n' % (GSE_ID, SRA_ID))
                    continue
                
                runinfo.index = runinfo['Run']
                runinfo = runinfo['SampleName']

            result_group = results.groupby('ASSEMBLY_USED')

            for assembly, result in result_group:
                out = output + '.' + SRA_ID + '_' + assembly + '.FPKM'
                
                fout.write(GSE_ID + '\t' + SRA_ID + '\t' + assembly + '\n')
                
                if 'GENES_FPKM_COUNTS_FTP_LOCATION' not in result.columns:
                    sys.stderr.write('Error %s : SRA %s FPKM column does not exist\n' % (GSE_ID, SRA_ID))
                    continue
                
                s = set(result['GENES_FPKM_COUNTS_FTP_LOCATION'].dropna())
                
                if len(s) == 0:
                    sys.stderr.write('Error %s : SRA %s FPKM location is all empty\n' % (GSE_ID, SRA_ID))
                    continue
                
                assert len(s) == 1
                url = s.pop()
                
                try:
                    urllib.request.urlretrieve(url, out)
                except:
                    flag_attempt = True
                    
                    # Bug fix for the RNASeq-ER API from my side
                    for program in ['htseq2', 'kallisto']:
                        try:
                            urllib.request.urlretrieve(url.replace('.featurecounts.', '.' + program + '.'), out)
                            flag_attempt = False
                            break
                        except:
                            sys.stderr.write('Attemp %s, but %s, %s, %s FPKM download failure\n' % (program, GSE_ID, assembly, SRA_ID))
                    
                    if flag_attempt:
                        sys.stderr.write('Error %s : SRA %s assembly %s FPKM download failure\n' % (GSE_ID, SRA_ID, assembly))
                        continue
                
                data = pandas.read_csv(out, sep='\t', index_col=0)
                os.remove(out)
                
                # has something to translate
                if runinfo is not None:
                    data.columns = runinfo.reindex(data.columns)
                    
                    flag_null = data.columns.isnull()
                    cnt_null = flag_null.sum()
                    
                    if cnt_null > 0:
                        sys.stderr.write('Error %s : SRA %s assembly %s runinfo column mismatch. %d out of %d missing\n' % (GSE_ID, SRA_ID, assembly, cnt_null, data.shape[1]))
                        
                        if cnt_null < data.shape[1]:
                            data = data.iloc[:, ~flag_null]
                        else:
                            # completely empty
                            continue
                
                data = data.loc[(data == 0).mean(axis=1) < 1]
                data.to_csv(out + '.gz', sep='\t', index_label=False, compression='gzip')
                
                matrix_list.append(os.path.relpath(out + '.gz', GSE_Path))
    
    fout.close()
    
    
    if len(matrix_list) > 0:
        fout = open(output, 'w')
        for f in matrix_list: fout.write(f + '\n')
        fout.close()
    else:
        sys.stderr.write('Warning %s : Cannot find any read matrix\n' % GSE_ID)
    
    return matrix_list




def download_Recount2_RNASeq(fail_log, output_path):
    # try download RNASeq failed on RNASeq-ER from Recount2
    # fail_log: failure log from RNASeq-ER
    # output_path: location path of output files
    
    url = 'http://duffel.rail.bio/recount/v2/%s/rse_gene.Rdata'
        
    fin = open(fail_log)
    
    for l in fin:
        fields = l.strip().split()
        
        SRP_ID = None
        
        for v in fields:
            if v[:3] == 'SRP':
                SRP_ID = v
                break
        
        if SRP_ID is None: continue
        
        output = os.path.join(output_path, SRP_ID)
        
        try:
            urllib.request.urlretrieve(url % SRP_ID, output + '.Rdata')
        except:
            sys.stderr.write('Error Recount2 %s download failure\n' % SRP_ID)
    
    fin.close()
    
    os.system(' '.join([os.path.join(script_path, 'Rdata_Matrix.R'), output_path]))
