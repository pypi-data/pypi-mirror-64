rule count:
    input: 
        r1 = wc_config['fastq_gz_file_wc']
    output: 
        r1 = wc_config['count_wc']
    wildcard_constraints:    
        df="[\w\d_-]+"
    run:
        exec_loc = os.path.join(config['assnake-core-preprocessing'],'count/count_bp.sh')
        shell('''bash {exec_loc} {input.r1} > {output.r1}''')