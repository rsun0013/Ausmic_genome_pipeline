import os
import makeCSV
# need to specify the input names of the fasta files to analyse in the input list
input = ["CC513_S55","CC514_S56","CC516_S57"]
output = "snakemake -p --cores 8 "
for i in input:
    output += "blastData/{}_blastinfo ".format(i)
os.system(output)

makeCSV.main()
