import pandas
import numpy
import sqlite3 as lite
from pandas.io import sql
import os


# Open connect to database
con = lite.connect('geneSequenceResults.db');
cur = con.cursor() 
# Create isoform table to which we will write in the MAIN LOOP below
cur.execute("DROP TABLE IF EXISTS isoforms");
cur.execute("CREATE TABLE isoforms (geneid text, isoformid text, normcount real, barcode text, tissuetype text)")



# Read in the file_manifest.txt
file_manifest = pandas.read_csv('file_manifest.txt', sep='\t').shift(-2)
# Only need one entry for each sample....can find all files based on prefix of 'File Name' 
subset_manifest = file_manifest.drop_duplicates(['Sample','Barcode']).dropna().reset_index(drop=True)


## MAIN LOOP
# Loops through the samples
for i in subset_manifest.index:
    # Get the i^th sample and its barcode
    sample, barcode = subset_manifest.loc[i,['Sample','Barcode']]

    # Specify the directory path, and the prefix that is unique to the 6 files associated with this sample
    path = subset_manifest.loc[i,'Platform Type'] + "/" + subset_manifest.loc[i,'Center'] + '__' + subset_manifest.loc[i,'Platform'] + "/Level_" + subset_manifest.loc[i,'Level'] + "/"
    file_prefix = '.'.join( str.split(subset_manifest.loc[i,'File Name'], '.')[:3] )

    # Read in sample's relevant file on isoform.normalized_results
    file = os.popen('ls ' + path + file_prefix + '*genes.results*').read()[:-1]
    genes_results = pandas.read_csv(file, '\t')

    # There are multiple transcript_ids for each gene_id
    # These lines unpack the transcript_ids into a long array
    list_transcript_ids = ','.join( genes_results['transcript_id'].as_matrix() )
    expanded_genes_results = pandas.DataFrame( str.split(list_transcript_ids, ',')).rename(columns={0:'transcript_id'})
    # Count how many transcript_ids per gene_id
    count_transcript_ids = genes_results['transcript_id'].apply(lambda x: len( x.split(',') ) )
    cum_count = count_transcript_ids.cumsum() - 1
    # Use the cumulative count of transcript_ids per gene_id, to match each transcript_id to its gene_id
    expanded_genes_results.loc[cum_count,'original_index'] = cum_count.index
    expanded_genes_results.fillna(method='bfill', inplace=True)
    g_ids = pandas.DataFrame(genes_results.loc[ expanded_genes_results['original_index'], 'gene_id' ]).set_index(expanded_genes_results.index)
    expanded_genes_results['gene_id'] = g_ids


    # Read in sample's relevant file on isoform.normalized_results
    file = os.popen('ls ' + path + file_prefix + '*isoforms.normalized_results*').read()[:-1]
    isoforms_normalized_results = pandas.read_csv(file, '\t')

    # Merge the expanded_genes_results and isoform_normalized_results, according to transcript_id=isoform_id
    merged_genes_isoforms = pandas.merge( expanded_genes_results.drop(['original_index'],axis=1), isoforms_normalized_results, left_on='transcript_id', right_on='isoform_id').drop(['transcript_id'],axis=1)

    # Add the barcode as a column to the dataframe
    merged_genes_isoforms['barcode'] = barcode
    # Add tissue_type as a column to the dataframe
    if barcode[13]=='0':
        tissue_type = 'TN'
    else:
        tissue_type = 'NT'
    merged_genes_isoforms['tissuetype'] = tissue_type


    # Append the dataframe tothe isoform table in the geneSequenceResults database
    merged_genes_isoforms.rename(columns={'gene_id':'geneid','isoform_id':'isoformid','normalized_count':'normcount'}, inplace=True)
    sql.to_sql(merged_genes_isoforms, name='isoforms', con=con, flavor='sqlite', if_exists='append', index=False)
    print("Completed sample: ",i)
    ## END OF LOOP

# Commit to the changes and close connection to geneSequenceResults.db
con.commit()
con.close()



#####################################
# END OF FILE
#####################################
