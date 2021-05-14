NUM=[1,2]
THREADS = 16
SPADES_MEM = 72
configfile: "config.json"

rule trimming:
    input:
        r1=config["rawStore"] + "/{sample}_R1_001.fastq.gz",
        r2=config["rawStore"] + "/{sample}_R2_001.fastq.gz"
    output:
        "trimmed/{sample}_R1_001_val_1.fq.gz",
        "trimmed/{sample}_R2_001_val_2.fq.gz"
    shell:
        "trim_galore --paired --length 80 --output_dir ./trimmed --fastqc {input.r1} {input.r2}"

rule storeRaw:# puts the input genome in correct location in storage server
    input:
        r1="{sample}_R1_001.fastq.gz",
        r2="{sample}_R2_001.fastq.gz"
    output:
        r1=config["rawStore"]+"/{sample}_R1_001.fastq.gz",
        r2=config["rawStore"]+"/{sample}_R2_001.fastq.gz"
    shell:
        "cp {input.r1} {output.r1};cp {input.r2} {output.r2}"

rule storePaired:# puts the trimmed paired output in correct location in storage server
    input:
        r1="trimmed/{sample}_R1_001_val_1.fq.gz",
        r2="trimmed/{sample}_R2_001_val_2.fq.gz"
    output:
        r1=config["pairedStore"]+"/{sample}_R1_001_val_1.fq.gz",
        r2=config["pairedStore"]+"/{sample}_R2_001_val_2.fq.gz"
    shell:
        "cp {input.r1} {output.r1};cp {input.r2} {output.r2}"

rule spades:
    input:
        r1=config["pairedStore"]+"/{sample}_R1_001_val_1.fq.gz",
        r2=config["pairedStore"]+"/{sample}_R2_001_val_2.fq.gz"
    output:
        output="spadesOut{sample}/contigs.fasta"
    shell:
        "spades.py -1 {input.r1} -2 {input.r2} --cov-cutoff 10 --careful -t {THREADS} -m {SPADES_MEM} -o spadesOut{wildcards.sample}"

rule storeSpades:
    input:
        r1="spadesOut{sample}/contigs.fasta"
    output:
        r1 = config["contigStore"]+"/{sample}contig.fasta"
    shell:
        "cp {input.r1} {output.r1}"

rule rename:
    input:
        "spadesOut{sample}/contigs.fasta",config["contigStore"]+"/{sample}contig.fasta"
    output:
        "spadesOut{sample}/contigs.fna"
    shell:
        "mv spadesOut{wildcards.sample}/contigs.fasta spadesOut{wildcards.sample}/contigs.fna"

rule checkm:
    input:
        "spadesOut{sample}/contigs.fna"
    output:
        "checkmOut/{sample}_checkm_out",
        directory("{sample}_checkmOut/")
    shell:
        "checkm lineage_wf -f checkmOut/{wildcards.sample}_checkm_out -t 1 -x fna spadesOut{wildcards.sample} {wildcards.sample}_checkmOut --"

rule get16s:
    input:
        "spadesOut{sample}/contigs.fna"
    output:
        "genome16calculated/{sample}_calculated_16s"
    shell:
        "genome_get16s -g {input} > {output}"

rule blastdata:
    input:
        "genome16calculated/{sample}_calculated_16s",
        config["16s"]+"/{sample}_16s"
    output:
        "blastData/{sample}_blastinfo"
    shell:
        "blastn -subject {input[1]} -query {input[0]} -out {output} -outfmt '6 length pident slen'"

rule annotate:
    input:
        "spadesOut{sample}/contigs.fna"
    output:
        "annotation/{sample}"
    shell:
        "prokka 1_CC00064_assembly/assembly.fasta --outdir 2_annotation/CC00064 --centre Hudson —compliant"
"""rule csv:
    input:
        "blastData/{sample}_bltinfo",
        "checkmOut/{sample}_checkm_out"
    output:
        "pipelineStats.csv"
    script:
        makeCSV.main()"""