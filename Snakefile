NUM=[1,2]
THREADS = 16
SPADES_MEM = 72


rule trimming:
    input:
        r1="{sample}_R1_001.fastq.gz",
        r2="{sample}_R2_001.fastq.gz"
    output:
        "trimmed/{sample}_R1_001_val_1.fq.gz",
        "trimmed/{sample}_R2_001_val_2.fq.gz"
    shell:
        "TrimGalore-0.6.6/trim_galore --paired --length 80 --output_dir ~/trimmed --fastqc {input.r1} {input.r2}"

rule spades:
    input:
        "trimmed/{sample}_R1_001_val_1.fq.gz",
        "trimmed/{sample}_R2_001_val_2.fq.gz"
    output:
        output="spadesOut{sample}/contigs.fasta"
    shell:
        "spades.py -1 {input[0]} -2 {input[1]} --cov-cutoff 10 --careful -t {THREADS} -m {SPADES_MEM} -o spadesOut{wildcards.sample}"

rule rename:
    input:
        "spadesOut{sample}/contigs.fasta"
    output:
        "spadesOut{sample}/contigs.fna"
    shell:
        "mv spadesOut{wildcards.sample}/contigs.fasta spadesOut{wildcards.sample}/contigs.fna"

rule checkm:
    input:
        "spadesOut{sample}/contigs.fna"
    output:
        "checkmOut/{sample}_checkm_out",
        "{sample}_checkmOut/"
    shell:
        "checkm lineage_wf -f checkmOut/{wildcards.sample}_checkm_out -t 8 -x fna spadesOut{wildcards.sample} {wildcards.sample}_checkmOut"

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
        "16sgiven/{sample}_16s"
    output:
        "blastData/{sample}_blastinfo"
    shell:
        "blastn -subject {input[1]} -query {input[0]} -out {output} -outfmt '6 length pident slen'"
rule csv:
    input:
        "blastData/{sample}_blastinfo",
        "checkmOut/{sample}_checkm_out"
    output: