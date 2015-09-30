# searching CCA gene sequence results

import csv		#this is a library used to read files in
import sqlite3 as lite	# these libraries will help us write our info to a database. easiest to read in.

#setting up the outfile for out results!
con = lite.connect('../larry_CCA_analysis/geneSequenceResults.db'); #initilazing output file
cur = con.cursor() #save cursor to var
cur.execute("DROP TABLE IF EXISTS genes") #if this table doesn't exist, create it. SQLITE3

cur.execute("DROP TABLE IF EXISTS isoforms"); # a second table


#This function allows you to query the 45 sample for a certain gene.
# Will output all of it's isoforms and their expressions in cancerous and non cancerous tissues.
def search_isoform_expressions_by_gene(genename):
	data = genename

	cur.execute("SELECT * FROM genes") # you can also select from genes to see the other table!
	for row in cur:
		print row

search_isoform_expressions_by_gene('babel')