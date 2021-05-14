#!/usr/bin/python3.7
import os
import makeCSV
import argparse
import json
import path_structure
# need to specify the input names of the fasta files to analyse in the input list
parser = argparse.ArgumentParser()
parser.add_argument("-f" ,action="store",dest="input_folder",help = "enter the folder where your fastq input files are",required = True)
parser.add_argument("--names",action="store",dest="name",nargs="*", help = " specify specific fastq samples for which script should run, optional",required=False)
parser.add_argument("-16s",action="store",dest="s16s", help = " specify folder which has all the 16s files for each sample",required = True)
args = parser.parse_args()

input_f = args.name
input_folder = args.input_folder
s16s = args.s16s
os.chdir(input_folder)
# choose the input files by scanning those in folder if not specified by the user
if input_f is None:
    input_f = []
    input_files = os.listdir()
    for i in input_files:
        if i.endswith("_R1_001.fastq.gz") or i.endswith("_R2_001.fastq.gz"):
            i = i.strip("_R1_001.fastq.gz")
            i = i.strip("_R2_001.fastq.gz")
            input_f.append(i)
    input_f = list(set(input_f))

for i in input_f:
    if not os.path.isfile(input_folder+"/"+i+"_R1_001.fastq.gz") or not os.path.isfile(input_folder+"/"+i+"_R2_001.fastq.gz"):
        print("fast q file for sample {} is missing, please ensure that both files exist in given folder, or remove the sample from folder".format(i))
        exit()
    if not os.path.isfile("{}/{}_16s".format(s16s,i)):
        print(" the 16s file for sample {} is not in the specified folder for 16s files")
        exit()
def addPathsToConfig(config_dict):
    paths = path_structure.genome_paths()
    os.system("cp ")
    config_dict["contigStore"] = paths.contigs
    config_dict["rawStore"] = paths.raw_reads
    config_dict["pairedStore"] = paths.paired
"""os.system("echo 'export PATH=$PATH:/usr/bin/SPAdes-3.15.2-Linux/bin' >> ~/.bashrc")
os.system("echo 'export PATH=$PATH:/home/vmar0011/anaconda3/bin/checkm' >> ~/.bashrc")
os.system("echo 'export PATH=$PATH:/home/rsun0013/TrimGalore-0.6.6/' >> ~/.bashrc")
os.system("echo 'export PATH=$PATH:/home/rsun0013/.local/bin' >> ~/.bashrc")
os.system(". ~/.bashrc")
os.system("cat ~/.bashrc")
os.system("echo $PATH")"""
config_dict = {}
config_dict["16s"] = s16s
addPathsToConfig(config_dict)
with open("config.json","w") as json_file:
    json.dump(config_dict,json_file)
snakefileLocation = "/usr/bin/pipeline/Ausmic_genome_pipeline/Snakefile"
output = "snakemake -s "+snakefileLocation+" -p --cores 8 "
for i in input_f:
    output += "blastData/{}_blastinfo ".format(i)
    output += "checkmOut/{}_checkm_out ".format(i)

os.system(output)


makeCSV.main()
