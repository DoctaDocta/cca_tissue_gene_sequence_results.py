#####################################
######  	 ABOUT THIS SCRIPT 	    #
#####################################
# This script reads a txt/csv file and imports it as a table in a database
# It also merges two tables on a common column, and writes the resulting merge as a new table in the database


#####################################
######  INSTRUCTIONS FOR USE:		#
#####################################
#In the shell go to this directory and type 'python script_add_table_to_database.py' to run the script.


#####################################
# Import necessary libraries
import numpy
import pandas
from pandas.io import sql
import sqlite3 as lite

# Open connection to the geneSequenceResults.db
con = lite.connect('geneSequenceResults.db');
cur = con.cursor()

# Read in the file as a dataframe
patients_table = pandas.read_csv('nationwidechildrens.org_clinical_patient_chol.txt', sep='\t')

# This particular file needs to be clean (the first two rows are header descriptions, not actual data
if patients_table.columns[0] == patients_table.iloc[0][patients_table.columns[0]]:
    patients_table = patients_table.shift(-2)    

# Write the dataframe to the database as a table
cur.execute('DROP TABLE IF EXISTS patients')
sql.to_sql(patients_table, name='patients', con=con)

# Read in database table as a dataframe
gene_pairs = pandas.read_sql_query('select * from gene_pairs', con)

# Merge the two dataframes on a common column
patients_table.rename(columns={'bcr_patient_barcode':'sample'}, inplace=True)
merged = pandas.merge(gene_pairs, patients_table, on=['sample'], how='inner')
gene_pairs_patient = merged[ numpy.concatenate([gene_pairs.columns, ['tumor_grade']]) ]

# Write the resulting dataframe to the database as a table
cur.execute('DROP TABLE IF EXISTS gene_pairs_patient')
sql.to_sql(gene_pairs_patient, name='gene_pairs_patient', con=con)

# Commit to the changes and close connection to geneSequenceResults.db
con.commit()
con.close()

print("...successfully completed !")

#####################################
# END OF FILE
#####################################
