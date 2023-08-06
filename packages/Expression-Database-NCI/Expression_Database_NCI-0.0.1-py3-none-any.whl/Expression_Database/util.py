import os, sys, re, numpy, pandas
from sklearn.impute import KNNImputer

script_path = os.path.join(sys.prefix, 'bin')

space_char = re.compile('\t|\r|\n')


def split_head_fields(arr):
    # split non regular characters and get the top fields
    spliter_nondigit = re.compile('[^0-9]')
    return map(lambda v: v[:3] + spliter_nondigit.split(v[3:])[0], arr)


def matrix_merge_gene_probe(f, output, flag_split_header = False):
    # merge gene probes to unique genes
    data = pandas.read_csv(f, index_col=0, sep='\t')
    
    # this should never be possible, but I still add it in case
    data = data.loc[map(lambda v:v.find('@') >= 0, data.index)]
    if data.shape[0] == 0: return None
    
    data.index = [v.split('@')[1].strip() for v in data.index]
    
    data = data.loc[[v not in ['', 'NA'] for v in data.index]]
    data = data.groupby(data.index).median()
    
    if flag_split_header: data.columns = split_head_fields(data.columns)
    
    if output is not None:
        if output.split('.').pop() == 'gz':
            data.to_csv(output, sep='\t', index_label=False, compression='gzip')
        else:
            data.to_csv(output, sep='\t', index_label=False)
    
    return data



def meta_merge_info_index(meta_info, sep = '|'):
    # merge meta information index to unique index
    if type(meta_info) == pandas.DataFrame:
        meta_info = meta_info.groupby(meta_info.index).apply(
            lambda meta: meta.apply(
                lambda v: sep.join(set(map(str,v)))
                )
            )
    
    elif type(meta_info) == pandas.Series:
        meta_info = meta_info.groupby(meta_info.index).apply(
            lambda v: sep.join(set(map(str,v)))
            )
    
    return meta_info



def remap_ArrayExpress_columns(meta, data):
    # ArrayExpress data columns and meta IDs could mismatch
    
    # perfect match
    if data.columns.intersection(meta.index).shape[0] == data.columns.shape[0]:
        return True
    
    match_counts = meta.apply(
        lambda v: len(set(data.columns.intersection(v)))
        )
    
    best_inx = match_counts.idxmax()
    
    reverse_map = pandas.Series(meta.index, index=meta[best_inx])
    
    # if duplicated index exists, this step may cause mismatches between data columns and meta index, due to multiple IDs
    if reverse_map.index.value_counts().max() > 1: reverse_map = meta_merge_info_index(reverse_map)
        
    data.columns = reverse_map.reindex(data.columns)
    
    return data.columns.isnull().sum() == 0




def translate_matrix_names(field_name_map, f, output, ratio_null = 0.333, ratio_transform=10):
    # do not assume data is all numerical
    data = pandas.read_csv(f, sep='\t', index_col=0, low_memory=False)
    
    # for AE microarray
    if str(data.index[0]).find(' REF') > 0: data.drop(data.index[0], inplace=True)
    
    spliter = re.compile('[^0-9a-zA-Z-_]')

    included = set()
    list(map(lambda v: included.update(spliter.split(str(v))), data.index))

    if '' in included: included.remove('')
    
    if len(included) < 3:
        sys.stderr.write('Error %s : name diversity too low\n' % os.path.basename(f))
        return False
    
    max_ratio = 0
    max_field = None

    for field, name_map in field_name_map.items():
        symbols = name_map.reindex(included)
        ratio = float(sum(~symbols.isnull())) / len(included)
        
        print(field, ratio)
        
        if ratio > max_ratio:
            max_field = field
            max_ratio = ratio
    
    if max_field is None:
        sys.stderr.write('Error %s : cannot find field for name translation\n' % os.path.basename(f))
        return False
    
    # current best map
    name_map = field_name_map[max_field]
    
    #fout = open(output + '.guess', 'w')
    #fout.write('\t'.join(map(str, [max_field, max_ratio])) + '\n')
    #fout.close()
    
    flag_entrez = max_field.lower().find('entrez') >= 0
    
    merge = []

    # a common pattern for entrez gene ID with pandas auto fix
    post_zero = re.compile('[.]0$')

    for gid, arr in data.iterrows():
        gid = str(gid)
        if flag_entrez: gid = post_zero.sub('', gid)
        
        gid_set = spliter.split(gid)
        
        # try 1: first element: directly search on the relevant field
        symbol = name_map.get(gid_set[0])
        
        # try 2: first element: search all maps
        for field, name_map_temp in field_name_map.items():
            symbol = name_map_temp.get(gid_set[0])
            if symbol is not None: break
        
        # try 3: search all fields and majority vote
        if symbol is None:
            gid_set = set(gid_set)
            if '' in gid_set: gid_set.remove('')
    
            gid_set = name_map.reindex(gid_set).dropna()
            
            if len(gid_set) == 0:
                sys.stdout.write('Warning %s : cannot find %s with %s\n' %(os.path.basename(f), gid, max_field))
                continue
            
            gid_set = gid_set.value_counts(sort=True, ascending=False)
            
            if gid_set.shape[0] == 1 or gid_set.iloc[0] > gid_set.iloc[1]:
                symbol = gid_set.idxmax()
            else:
                sys.stdout.write('Warning %s : ambiguous name %s with %s\n' %(os.path.basename(f), gid, max_field))
                continue

        arr.name = symbol
        merge.append(arr)
    
    if len(merge) < 3:
        sys.stderr.write('Error %s : low effective names\n' % os.path.basename(f))
        return False
    
    data = pandas.concat(merge, axis=1, join='inner').transpose()
    
    try:
        data_merge = data.astype(float).groupby(data.index).median()
    except:
        data_merge = None
        sys.stderr.write('Warning %s : Cannot merge genes\n' % os.path.basename(f))
    
    # only auto transform if the matrix is numerical mergable, (ArrayExpress matrix may violate)
    if data_merge is not None:
        data = data_merge
    
        # if has some NA values
        if data.isnull().sum().sum() > 0:
            data = data.loc[data.isnull().mean(axis=1) < ratio_null, :]
            data = data.loc[:, data.isnull().mean(axis=0) < ratio_null]
            
            imputer = KNNImputer()
        
            try:
                data = pandas.DataFrame(imputer.fit_transform(data), index=data.index, columns=data.columns)
            except: 
                sys.stderr.write('Error %s : KNN impute failure\n' % os.path.basename(f))
                return False
        
        if data.shape[0] < 10 or data.shape[1] < 2:
            sys.stderr.write('Error %s : low effective names\n' % os.path.basename(f))
            return False
    
        # if need log2 transformation (or Z-norm if negative value exists)
        data_arr = pandas.Series(data.values.flatten())
        data_top, data_med = data_arr.abs().quantile(0.99), data_arr.abs().median()
        
        # the current criterion is not perfect, post processing supervision is still necessary
        if data_top > ratio_transform * ratio_transform and data_top > ratio_transform * data_med:
            if data_arr.min() >= 0:
                data = numpy.log2(data + 1)
            else:
                data = data.subtract(data.mean(axis=1), axis=0).divide(data.std(axis=1), axis=0)
    
    if output.split('.').pop() == 'gz':
        data.to_csv(output, sep='\t', index_label=False, compression='gzip')
    else:
        data.to_csv(output, sep='\t', index_label=False)
    
    return True
