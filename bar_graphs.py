import sys
import pandas
import numpy
import sqlite3 as lite
from pandas.io import sql
import os
import matplotlib.pyplot as plt


# Open connect to database
con = lite.connect('geneSequenceResults.db');
cur = con.cursor() 


gene_pairs = pandas.read_sql("select * from gene_pairs", con=con)
geneid = 'ZYX|7791'
# geneid = sys.argv[1]
samples_of_geneid = gene_pairs[gene_pairs['geneid']==geneid].set_index('sample').drop('geneid',axis=1).astype(float)

# Bar graph of NT and TN normcounts for specified Gene ID
plt.figure()
samples_of_geneid[['normcount_NT','normcount_TN']].plot(kind='bar')
plt.savefig("/Users/ehrlich/Syncplicity/bioinformatics_folder/cca_tissue_gene_sequence_results/figures_geneidBarGraphs/" + geneid + ".png")

# Commit to the changes and close connection to geneSequenceResults.db
#con.commit()
con.close()



#####################################
# END OF FILE
#####################################

