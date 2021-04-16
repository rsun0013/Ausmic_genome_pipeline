import os
import makeCSV
import argparse
import json
# need to specify the input names of the fasta files to analyse in the input list
parser = argparse.ArgumentParser()
parser.add_argument("-f" ,action="store",dest="input_folder")
parser.add_argument("--names",action="store",dest="name",nargs="*")
parser.add_argument("-16s",action="store",dest="s16s")
args = parser.parse_args()
input_f = args.name
input_folder = args.input_folder
s16s = args.s16s
os.chdir(input_folder)
if input_f is None:
    input_f = os.listdir()
    for i in input_f:
        i.strip("_R1_001.fastq.gz")
        i.strip("_R2_001.fastq.gz")
    list(set(input_f))


config_dict = {}
config_dict["16s"] = s16s
with open("config.json","w") as json_file:
    json.dump(config_dict,json_file)

output = "snakemake -p --cores 8 "
for i in input_f:
    output += "blastData/{}_blastinfo ".format(i)
os.system(output)

makeCSV.main()
