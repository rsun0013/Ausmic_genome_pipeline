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
    input_f = []
    input_files = os.listdir()
    for i in input_files:
        if i.endswith("_R1_001.fastq.gz") or i.endswith("_R2_001.fastq.gz"):
            i = i.strip("_R1_001.fastq.gz")
            i = i.strip("_R2_001.fastq.gz")
            input_f.append(i)
    input_f = list(set(input_f))

"""os.system("echo 'export PATH=$PATH:/usr/bin/SPAdes-3.15.2-Linux/bin' >> ~/.bashrc")
os.system("echo 'export PATH=$PATH:/home/vmar0011/anaconda3/bin/checkm' >> ~/.bashrc")
os.system("echo 'export PATH=$PATH:/home/rsun0013/TrimGalore-0.6.6/' >> ~/.bashrc")
os.system("echo 'export PATH=$PATH:/home/rsun0013/.local/bin' >> ~/.bashrc")
os.system(". ~/.bashrc")
os.system("cat ~/.bashrc")
os.system("echo $PATH")"""
config_dict = {}
config_dict["16s"] = s16s
with open("config.json","w") as json_file:
    json.dump(config_dict,json_file)

output = "snakemake -p --cores 8 "
for i in input_f:
    output += "blastData/{}_blastinfo ".format(i)
os.system(output)

makeCSV.main()
