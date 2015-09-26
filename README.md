# cca_tissue_gene_sequence_results.py
This repo does not contain the actual data because it is too large.
You can download it from here: https://tcga-data.nci.nih.gov/tcga/tcgaCancerDetails.jsp?diseaseType=CHOL&amp;diseaseName=Cholangiocarcinoma

To run the program, download this repository and save it in the same folder that contains the TCGA Data from the link above.
example: pwd --> users/documents/CCA_analysis
                  --> TCGA_data (results folder)
                  --> cca_tissue_gene_sequence_results.py (this repository)

IF THE SCRIPT HAS ISSUES FINDING THE FILES, YOU WILL HAVE TO EDIT THE SOME VARIABLES IN THE FIRST 20 LINES OF ANALIZE.PY TO THE
APPROPRIATE WORKING DIRECTORY PATH'S.


-------------------------------------------------------------------------------------------------------------------------------
This script is just reading expressions of RNA from the link above. it should be able to intepret other sets of data from the site.

ideally this will be a command line tool...
http://www.diveintopython.net/scripts_and_streams/command_line_arguments.html