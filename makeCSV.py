#!/usr/bin/python3
import os
import ausmic

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



def readblastOutput(filename):
    f = open(filename, "r")
    data = f.readline()
    data = data.strip("\n")
    data = data.split("\t")
    return data[0],data[1],data[2]

def main():
    stats = {}
    path = os.getcwd()
    comp_threshold = 95
    cont_threshold = 0.5
    sim_threshold = 99
    overlap_threshold = 80
    os.chdir(path=path + "/checkmOut")
    checkMfiles = os.listdir(path=path + "/checkmOut")
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

    for i in blastfiles:
        overlap, sim, total_len = readblastOutput(i)
        stats[i.strip("_blastinfo")][1] = sim#similarity
        stats[i.strip("_blastinfo")][2] = float(overlap) / float(total_len)#%overlap
        if float(sim) < sim_threshold or float(overlap) < overlap_threshold:
            stats[i.strip("_blastinfo")][0] = "N"
    outfile = open(path + "/pipelineStats.csv", "w")

    # set up connection to dc b
    connection = ausmic.db_connection()
    cursor = connection.cursor()
    # file location = path+"spadesOut"+stats[i][0]
    for i in stats:
        cursor.execute(
            "INSERT INTO genome (genomeID,overlap,cont,completness,pass,similarity) values ({},{},{},{},{},{});".format("'stats[i][0]'",stats[i][2],stats[i][4],stats[i][3],stats[i][5],stats[i][1]))
        outfile.write(
            "{},{},{},{},{},{}\n".format(stats[i][0], stats[i][1], stats[i][2], stats[i][3], stats[i][4], stats[i][5]))
    outfile.close()
    # print(stats)




