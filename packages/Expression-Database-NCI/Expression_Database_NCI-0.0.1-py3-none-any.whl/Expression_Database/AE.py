import os
import sys
import shutil
import re
import glob
import pandas
import numpy
import urllib
from orangecontrib.bio import arrayexpress
from zipfile import ZipFile
from bioservices import RNASEQ_EBI

from Expression_Database.util import script_path, meta_merge_info_index, remap_ArrayExpress_columns, space_char


def AE_meta(AE_ID, AE_Path, flag_enforce = False):

    meta = os.path.join(AE_Path, AE_ID + '.meta')
    
    if not flag_enforce and os.path.exists(meta + '.summary'):
        return pandas.read_csv(meta + '.summary', sep='\t', index_col=0, header=None).iloc[:,0]
    
    if not os.path.exists(AE_Path): os.mkdir(AE_Path)
        
    try:
        experiment = arrayexpress.ArrayExpressExperiment(AE_ID)
    except:
        sys.stderr.write('Error %s : ArrayExpress failure\n' % AE_ID)
        return None
    
    # identify the experiment meta information
    title = experiment.name

    merge = []
    for description in experiment.description:
        description = description.get('text')
        if description is not None: merge.append(description)
    
    description = ' '.join(merge)

    design = ' '.join(experiment.experimentdesign)
    
    # experimental platform
    merge = []

    for array in experiment.arraydesign:
        merge.append(str(array.get('name')).replace(',', '-'))
    
    if len(merge) > 0:
        experiment_platform = ','.join(merge)
    else:
        experiment_platform = experiment.experimenttype.replace(',', '-')
    
    technology = experiment.experimenttype
    
    title = space_char.sub(' ', title).strip()
    description = space_char.sub(' ', description).strip()
    design = space_char.sub(' ', design).strip()
    technology = space_char.sub(' ', technology).strip()
    experiment_platform = space_char.sub(' ', experiment_platform).strip()
    
    # identify the sample meta information
    url = meta_info = meta_info_full = None
    
    for fmap in experiment.files:
        if fmap.get('kind') == 'sdrf':
            url = fmap.get('url')
            break
    
    if url is None:
        sys.stderr.write('Error %s : No sdrf meta information\n' % AE_ID)
        return None
    
    try:
        meta_info_full = pandas.read_csv(url, sep='\t', index_col=0)
    except:
        sys.stderr.write('Error %s : sdrf meta information download and parse failure\n' % AE_ID)
        return None
    
    meta_info_full.to_csv(meta + '.full.gz', sep='\t', index_label = 'ID', compression = 'gzip')
    
    flag = [len(v.strip()) > 0 and v.lower().find('comment') < 0 for v in meta_info_full.columns]
    
    if sum(flag) > 0:
        meta_info = meta_info_full.loc[:, flag]
        
        # if the index has duplicated keys
        if meta_info.index.value_counts().max() > 1: meta_info = meta_merge_info_index(meta_info)
        
        meta_info.to_csv(meta, sep='\t', index_label = 'ID')    
    else:
        sys.stderr.write('Error %s : sdrf meta information has no informative columns\n' % AE_ID)
        return None    
    
    # assign super series by experience
    status = 'Regular'
    if AE_ID in ['E-MTAB-3732', 'E-MTAB-1788', 'E-MTAB-62']: status = 'Super'
    
    meta_summary = pandas.Series(
        [title, description, design, experiment_platform, technology, status, meta_info.shape[0]],
        index=['title', 'summary', 'design', 'platform', 'technology', 'status', 'count'])
    
    meta_summary.to_csv(meta + '.summary', sep='\t', header=False)
    
    return meta_summary




def AE_MicroArray(AE_ID, AE_Path, flag_enforce=False):
    
    # gene name columns to search
    name_fields = ['hugo', 'refseq', 'ensembl', 'entrez', 'unigene']

    # output prefix
    output = os.path.join(AE_Path, AE_ID + '.MicroArray')
    
    if not flag_enforce and os.path.exists(output):
        return pandas.read_csv(output, sep='\t', header=None).iloc[:,0].tolist()
    
    # clear existing file
    os.system('rm -rf ' + output + '*')
    
    processed_path = output +  '.processed'
    raw_path = output + '.raw'
    platform_path = output + '.platform'
    
    for fpath in [AE_Path, raw_path, processed_path, platform_path]:
        if not os.path.exists(fpath): os.mkdir(fpath)
    
    # return matrix, ranked by preference order
    matrix_list = []
    
    # probe maps list to map gene names
    probe_map_list = []
    
    # start reading data from the ArrayExpress database
    try:
        experiment = arrayexpress.ArrayExpressExperiment(AE_ID)
    except:
        sys.stderr.write('Error %s : ArrayExpress failure\n' % AE_ID)
        return None
    
    # Detect Affymetrix platform
    flag_Affymetrix = False

    for array in experiment.arraydesign:
        array_name = array.get('name')
        if(array_name.lower().find('affymetrix') >= 0):
            flag_Affymetrix = True
            break

    # any type of processed data?
    flag_processed_data = False
    
    # go over all files
    for fmap in experiment.files:
        file_name, file_type, url = fmap.get('name'), fmap.get('kind'), fmap.get('url')
        
        # jump files without complete information
        if file_name is None or file_type is None or url is None: continue

        if file_type == 'fgem':
            # final gene expression matrix
            if file_name.split('.')[-1] != 'zip': continue
        
            f = os.path.join(AE_Path, file_name)
            
            try:
                urllib.request.urlretrieve(url, f)
            except:
                sys.stderr.write('Error %s : download %s failure\n' % (AE_ID, file_name))
                continue

            # only unzip it, we will analyze it later
            try:
                zf = ZipFile(f, 'r')
                zf.extractall(processed_path)
                zf.close()
            except:
                sys.stderr.write('Error %s : unzip %s failure\n' % (AE_ID, file_name))
                os.remove(f)
                continue
            
            os.remove(f)

            flag_processed_data = True

        elif file_type == 'raw' and flag_Affymetrix:     
            # download Affymetrix CEL files
            
            f = os.path.join(AE_Path, file_name)
            
            try:
                urllib.request.urlretrieve(url, f)
            except:
                sys.stderr.write('Error %s : download %s failure\n' % (AE_ID, file_name))
                continue

            # only unzip it, we will analyze it later
            try:
                zf = ZipFile(f, 'r')
                zf.extractall(raw_path)
                zf.close()
            except:
                sys.stderr.write('Error %s : unzip %s failure\n' % (AE_ID, file_name))
                os.remove(f)
                continue
            
            os.remove(f)

        elif file_type == 'adf' and url.find('.adf.txt') > 0:
            # gene probe map
            
            f = os.path.join(platform_path, file_name)

            # process a simplified gene map from scratch
            try:
                urllib.request.urlretrieve(url, f)
            except:
                sys.stderr.write('Error %s : download %s failure\n' % (AE_ID, file_name))
                continue

            # get the number of jump count
            jump_count = 0

            fin = open(f, encoding = "ISO-8859-1")
            for l in fin:
                jump_count += 1
                if l.find('[main]')  == 0: break
            fin.close()

            if l.find('[main]') != 0:
                sys.stderr.write('Error %s : Cannot find start location in ADF file %s\n' % (AE_ID, file_name))
                os.remove(f)
                continue
            
            try:
                probe_map = pandas.read_csv(f, sep='\t', index_col=0, low_memory=False, skiprows=jump_count, encoding = "ISO-8859-1")
            except:
                sys.stderr.write('Error %s : Cannot read ADF file %s\n' % (AE_ID, file_name))
                continue

            # test if other probe columns
            if 'Reporter Name' in probe_map.columns: probe_map.index = probe_map['Reporter Name']
            
            # guess the gene fields
            gene_name_col = None
            
            for pivot in name_fields:
                fields = [v.lower().find('[' + pivot + ']') >= 0 for v in probe_map.columns]
                fields = probe_map.columns[fields]
                if len(fields) > 0:
                    gene_name_col = fields[0]
                    break

            if gene_name_col is None:
                sys.stderr.write('Error %s : Cannot find gene name column in ADF file %s\n' % (AE_ID, file_name))
                continue

            probe_map = probe_map[gene_name_col].dropna().apply(lambda v:str(v).strip())
            
            # get unique index
            if probe_map.index.value_counts().max() > 1: probe_map = meta_merge_info_index(probe_map)
            
            if probe_map.shape[0] < 3:
                sys.stderr.write('Error %s : Gene name column %s in ADF file %s does not have sufficient values\n' % (AE_ID, gene_name_col, file_name))
                continue
            
            probe_map_list.append(probe_map)


    # AE Patch: rename the cel to upper
    cel_postfix = re.compile('[.]cel$', re.IGNORECASE)   # @UndefinedVariable
    
    file_lst = glob.glob(os.path.join(raw_path, '**', '*.cel'), recursive=True)
    
    for f in file_lst: shutil.move(f, cel_postfix.sub('.CEL', f))
    
    file_lst = glob.glob(os.path.join(raw_path, '**', '*.CEL*'), recursive=True)
    
    if flag_Affymetrix and len(file_lst) > 0:
        # adjust all files to the first level (if any files located in subdirs)
        for i in range(len(file_lst)):
            f = file_lst[i]    
            dst = os.path.join(raw_path, os.path.basename(f))
            
            if dst != f:
                shutil.move(f, dst)
                file_lst[i] = dst
        
        # RMA processing
        os.system(' '.join([os.path.join(script_path, 'rma_oligo.R'), raw_path, output]))
        
        if os.path.exists(output + '.log'):
            fin = open(output + '.log')
            for l in fin:
                fields = l.strip().split()
                
                if len(fields) > 0 and fields[0] == 'Output':
                    out = output + '.' + fields[1] + '.rma'
                    assert os.path.exists(out)
                    os.system('gzip ' + out)
                    
                    matrix_list.append(out + '.gz')
            fin.close()
        else:
            sys.stderr.write('Error %s : rma_oligo failure\n' % AE_ID)
    
    
    # for processed data, the goal is not to make it ready, but to make it as processed as possible
    if flag_processed_data:
        processed_files = glob.glob(os.path.join(processed_path, '*'))

        for f in processed_files:
            
            fname = os.path.basename(f).replace('.txt', '').replace('processedData', '').strip('-').strip()
            out = output + '.' + fname + '.AE'
            
            # round 1: search for start position
            count_lst = []
            
            fin = open(f, encoding = "ISO-8859-1")
            for l in fin:
                fields = l.rstrip().split('\t')
                count_lst.append(len(fields))
            fin.close()
            
            count_lst = pandas.Series(count_lst)
            jump_count = count_lst.index[count_lst == count_lst.median()]
            
            if len(jump_count) == 0: continue
            jump_count = jump_count[0]
            
            # round 2: read data
            try:
                data = pandas.read_csv(f, sep='\t', index_col=0, low_memory = False, skiprows = jump_count, encoding = "ISO-8859-1")
            except:
                sys.stderr.write('Error %s : Cannot read data file %s\n' % (AE_ID, fname))
                continue
            
            # search for type REF rows
            type_arr = None
            
            if str(data.index[0]).find(' REF') > 0:
                type_arr = data.iloc[0]
                data.drop(data.index[0], inplace=True)
            
            # guess which probe map is relevant by high probe overlap
            overlap_counts = [len(data.index.intersection(probe_map.index)) for probe_map in probe_map_list]
            if len(overlap_counts) == 0 or max(overlap_counts) < 100:
                sys.stderr.write('Error %s : Cannot find gene map for %s\n' % (AE_ID, fname))
                continue

            probe_map = probe_map_list[numpy.argmax(overlap_counts)]

            data = data.loc[probe_map.index.intersection(data.index)]
            data.index = probe_map[data.index]
            
            try:
                data_merge = data.astype(float).groupby(data.index).median()
            except:
                data_merge = None
                sys.stderr.write('Error %s : Cannot merge genes for %s\n' % (AE_ID, fname))
            
            if data_merge is not None: data = data_merge
            
            if type_arr is not None:
                data = pandas.concat([pandas.DataFrame(type_arr).transpose(), data])
            
            data.to_csv(out + '.gz', sep='\t', index_label=False)
            matrix_list.append(out + '.gz')
    
    # clear up all paths
    for fpath in [raw_path, processed_path, platform_path]: shutil.rmtree(fpath)
    
    # convert to relative path
    for i in range(len(matrix_list)):
        matrix_list[i] = os.path.relpath(matrix_list[i], AE_Path)
    
    
    if len(matrix_list) > 0:
        fout = open(output, 'w')
        for f in matrix_list: fout.write(f + '\n')
        fout.close()
    else:
        sys.stderr.write('Warning %s : Cannot find any MicroArray matrix\n' % AE_ID)

    return matrix_list





def AE_RNASeq(AE_ID, AE_Path, flag_enforce = False, flag_translate = True):
    # Get a data matrix if it is RNASeq
    # Return matrix list, None if failed
    
    # output prefix    
    output = os.path.join(AE_Path, AE_ID + '.RNASeq')
     
    if not flag_enforce and os.path.exists(output):
        return pandas.read_csv(output, sep='\t', header=None).iloc[:,0].tolist()
    
    # clear existing file
    os.system('rm -rf ' + output + '*')
    
    if not os.path.exists(AE_Path): os.mkdir(AE_Path)
    
    meta = os.path.join(AE_Path, AE_ID + '.meta.full.gz')
    
    if not os.path.exists(meta):
        sys.stderr.write('Warning %s : meta information does not exist. Skip.\n' % AE_ID)
        return None
    
    meta = pandas.read_csv(meta, sep='\t', index_col=0)
    
    try:
        experiment = arrayexpress.ArrayExpressExperiment(AE_ID)
    except:
        sys.stderr.write('Error %s : ArrayExpress failure\n' % AE_ID)
        return None
    
    r = RNASEQ_EBI()
    
    ENA_ID = experiment.secondaryaccession
    
    try:
        results = r.get_study(ENA_ID, frmt='tsv')
    except:
        sys.stderr.write('Error %s : ENA %s RNASEQ_EBI get_study failure\n' % (AE_ID, ENA_ID))
        return None
    
    if results.shape[0] == 0:
        sys.stderr.write('Warning %s : ENA %s is not processed\n' % (AE_ID, ENA_ID))
        return None
    
    matrix_list = []
    
    result_group = results.groupby('ASSEMBLY_USED')

    for assembly, result in result_group:
        out = output + '.' + ENA_ID + '_' + assembly + '.FPKM'
        
        if 'GENES_FPKM_COUNTS_FTP_LOCATION' not in result.columns:
            sys.stderr.write('Error %s : ENA %s FPKM column does not exist\n' % (AE_ID, ENA_ID))
            continue
        
        s = set(result['GENES_FPKM_COUNTS_FTP_LOCATION'].dropna())
        
        if len(s) == 0:
            sys.stderr.write('Error %s : ENA %s FPKM location is all empty\n' % (AE_ID, ENA_ID))
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
                    sys.stderr.write('Attemp %s, but %s, %s, %s FPKM download failure\n' % (program, AE_ID, assembly, ENA_ID))
                    
            if flag_attempt:
                sys.stderr.write('Error %s : SRA %s assembly %s FPKM download failure\n' % (AE_ID, ENA_ID, assembly))
                continue
        
        data = pandas.read_csv(out, sep='\t', index_col=0)
        os.remove(out)
        
        data = data.loc[(data == 0).mean(axis=1) < 1]
        
        if flag_translate:
            # remap data columns to match meta IDs
            data = remap_ArrayExpress_columns(meta, data)
        
            if data is None:
                sys.stderr.write('Error %s : ENA %s assembly %s sample name remap failure\n' % (AE_ID, ENA_ID, assembly))
                continue
        
        data.to_csv(out + '.gz', sep='\t', index_label=False, compression='gzip')
        matrix_list.append(os.path.relpath(out + '.gz', AE_Path))
    
    
    if len(matrix_list) > 0:
        fout = open(output, 'w')
        for f in matrix_list: fout.write(f + '\n')
        fout.close()
    else:
        sys.stderr.write('Warning %s : Cannot find any read matrix\n' % AE_ID)
    
    return matrix_list
