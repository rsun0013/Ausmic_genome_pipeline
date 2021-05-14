#!/usr/bin/python3.7
import argparse
import os
import ausmicc_f_db_connection


# process output from checkm
def readcheckmOutput(filename):
    f = open(filename, "r")
    f.readline()
    f.readline()
    f.readline()
    data = f.readline()
    data = data.strip("\n")
    data = data.split(" ")
    data = [x for x in data if x != ""]
    comp = data[-3]
    cont = data[-2]
    return comp,cont


# read the output produced by blast
def readblastOutput(filename):
    f = open(filename, "r")
    data = f.readline()
    data = data.strip("\n")
    data = data.split("\t")
    return data[0],data[1],data[2]

#parse the arguments and set thresholds
def parseInputs():
    parser = argparse.ArgumentParser()
    parser.add_argument("--comp", action="store", dest="comp",default = 95,
                        help="enter a value for the comp threshold if dont want default", required=False)
    parser.add_argument("--cont", action="store", dest="cont",default = 0.5,
                        help="enter a value for the cont threshold if dont want default", required=False)
    parser.add_argument("--sim", action="store", dest="sim",default=99,
                        help="enter a value for the similarity threshold if dont want default", required=False)
    parser.add_argument("--overlap", action="store", dest="overlap",default=80,
                        help="enter a value for the overlap threshold if dont want default", required=False)

    args = parser.parse_args()

    return args.comp,args.cont,args.sim,args.overlap

def main():
    stats = {}
    path = os.getcwd()
    # set the thresholds
    comp_threshold,cont_threshold,sim_threshold,overlap_threshold = parseInputs()
    os.chdir(path=path + "/checkmOut")
    checkMfiles = os.listdir(path=path + "/checkmOut")

    # process output from each checkm file
    for i in checkMfiles:
        comp, cont = readcheckmOutput(i)
        stats[i.strip("_checkm_out")] = [0 for j in range(6)]
        stats[i.strip("_checkm_out")][0] = i.strip("_checkm_out")#name
        stats[i.strip("_checkm_out")][5] = "Y"#pass
        stats[i.strip("_checkm_out")][3] = comp#completness
        stats[i.strip("_checkm_out")][4] = cont#cont
        if float(comp) < comp_threshold or float(cont) > cont_threshold:
            stats[i.strip("_checkm_out")][5] = "N"



    os.chdir(path=path + "/blastData")
    blastfiles = os.listdir(path=path + "/blastData")
    # process each of the blast files output
    for i in blastfiles:
        overlap, sim, total_len = readblastOutput(i)
        stats[i.strip("_blastinfo")][1] = sim#similarity
        stats[i.strip("_blastinfo")][2] = float(overlap) / float(total_len)#%overlap
        if float(sim) < sim_threshold or float(overlap) < overlap_threshold:
            stats[i.strip("_blastinfo")][5] = "N"
    outfile = open(path + "/pipelineStats.csv", "w")
    outfile.write("Genome name,similarity,overlap,completness,contigcount,pass")

    # print num of passed samples and names of failed samples
    passed=0
    failed = 0
    failedSamples = []
    for i in stats.keys():
        sample = stats[i]
        if sample[5] == "Y":
            passed += 1
        else:
            failed += 1
            failedSamples.append(stats[0])

    # print the number of samples that pass and names of failed samples
    if len(failedSamples) >0:
        print("Samples that failed qc:")
        for i in failedSamples:
            print(i)
        print("")
    print("num of samples passing qc: {}".format(passed))


    # set up connection to dc b
    connection = ausmicc_f_db_connection.db_connection()
    cursor = connection.cursor()
    # file location = path+"spadesOut"+stats[i][0]
    for i in stats:
        cursor.execute(
            "INSERT INTO genome (genomeID,overlap,cont,completness,pass,similarity) values ({},{},{},{},{},{});".format("'stats[i][0]'",stats[i][2],stats[i][4],stats[i][3],stats[i][5],stats[i][1]))
        outfile.write(
            "{},{},{},{},{},{}\n".format(stats[i][0], stats[i][1], stats[i][2], stats[i][3], stats[i][4], stats[i][5]))
    outfile.close()
    # print(stats)



