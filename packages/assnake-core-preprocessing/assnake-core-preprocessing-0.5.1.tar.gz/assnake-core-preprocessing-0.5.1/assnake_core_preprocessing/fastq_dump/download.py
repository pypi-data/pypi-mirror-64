rule fastq_dump:
    input: 
        sample     = '{fs_prefix}/{df}/reads/sra/{sample}.download'
    output:
        r1         = '{fs_prefix}/{df}/reads/sra/{sample}_R1.fastq.gz',
        r2         = '{fs_prefix}/{df}/reads/sra/{sample}_R2.fastq.gz'
    params: 
        out_folder = '{fs_prefix}/{df}/reads/sra/',
        tmp_dir = '{fs_prefix}/{df}/reads/sra/',
        r1         = '{fs_prefix}/{df}/reads/sra/{sample}_1.fastq.gz',
        r2         = '{fs_prefix}/{df}/reads/sra/{sample}_2.fastq.gz'
    log:             '{fs_prefix}/{df}/reads/sra/{sample}.download.log'
    conda: 'env.yaml'
    threads: 4
    shell: '''fastq-dump  --tmpdir {params.tmp_dir} --threads {threads} --split-files --gzip --dumpbase --skip-technical --outdir {params.out_folder} --sra-id {wildcards.sample} >{log} 2>&1;\
        mv {params.r1} {output.r1};\
        mv {params.r2} {output.r2}'''