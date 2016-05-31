#####################################
######  	 ABOUT THIS SCRIPT 	    #
#####################################
# This script does a 2-tailed paired t-test on the samples of each gene


#####################################
######  INSTRUCTIONS FOR USE:		#
#####################################
#In the shell go to this directory and type 'python paired_t_test.py' to run the script.


#####################################
# Import necessary libraries
import pandas
from pandas.io import sql
import sqlite3 as lite
from scipy import stats
import numpy


# Open connection to the geneSequenceResults.db
con = lite.connect('geneSequenceResults.db');
cur = con.cursor()
cur.execute('DROP TABLE IF EXISTS gene_paired_ttest')
cur.execute('CREATE TABLE gene_paired_ttest (geneid TEXT, tvalue REAL, pvalue REAL)')


# Get list of distinct gene id's
gene_ids = pandas.read_sql_query("select distinct geneid from gene_pairs", con)

# Loop through each gene id
for i in gene_ids.index:
    g = gene_ids.loc[i][0] 
    g_samples = pandas.read_sql_query("select * from gene_pairs where geneid like '" + g + "'", con) #get all samples of the gene
    g_samples[['normcount_TN','normcount_NT']] = g_samples[['normcount_TN','normcount_NT']].applymap(lambda x: float(x)) #convert the count from strings to floats
    t_value, p_value = stats.ttest_rel(g_samples['normcount_TN'], g_samples['normcount_NT']) #calculate the t-value and p-value
    tmpList = []                                                                            
    tmpList.extend([g, t_value, p_value])
    cur.execute('INSERT INTO gene_paired_ttest VALUES (?,?,?)', tmpList) #write the geneid, tvalue, pvalue into the database

# Commit to the changes and close connection to geneSequenceResults.db
con.commit()
con.close()


#####################################
# END OF FILE
#####################################
