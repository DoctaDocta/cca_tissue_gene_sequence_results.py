# cca_tissue_gene_sequence_results.py
You must download the gene sequence results from:
https://tcga-data.nci.nih.gov/tcga/tcgaCancerDetails.jsp?diseaseType=CHOL&diseaseName=Cholangiocarcinoma

There are variables within the first twenty lines of code that have file paths in them. You must update these to locate the data.

To run the script, run it through a text editor like Sublime Text 2. If you have a mac, the command line seems to be faster. Open the terminal and go to the directory with the analize.py script, and type python analyze.py to build a database.


-------------------------------------------------------------------------------------------------------------------------------
This script is just reading expressions of RNA from the link above. it should be able to intepret other sets of data from the site.

ideally this will be a command line tool...
http://www.diveintopython.net/scripts_and_streams/command_line_arguments.html