import os
import pandas as pd

def get_fastqc_files_for_multiqc(wildcards):
    fastqc_list = []
    sample_set_loc = '{fs_prefix}/{df}/profile/multiqc/{sample_set}/sample_set.tsv'.format(**wildcards)
    sample_set = pd.read_csv(sample_set_loc, sep = '\t')
    for s in sample_set.to_dict(orient='records'):
        fastqc_list.append(wc_config['fastqc_data_wc'].format(df = s['df'], fs_prefix = s['fs_prefix'], fs_name = s['fs_name'], preproc = s['preproc'], strand = 'R1'))
        fastqc_list.append(wc_config['fastqc_data_wc'].format(df = s['df'], fs_prefix = s['fs_prefix'], fs_name = s['fs_name'], preproc = s['preproc'], strand = 'R2'))
    return fastqc_list

rule multiqc_list_from_sample_set:
    input:  
        sample_set_loc = '{fs_prefix}/{df}/profile/multiqc/{sample_set}/sample_set.tsv',
        fastqc_data = get_fastqc_files_for_multiqc
    output: sample_list = wc_config['sample_list_wc'],
    run: 
        fastqc_list = []
        sample_set = pd.read_csv(input.sample_set_loc, sep = '\t')
        for s in sample_set.to_dict(orient='records'):
            fastqc_list.append(wc_config['fastqc_data_wc'].format(df = s['df'], fs_prefix = s['fs_prefix'], fs_name = s['fs_name'], preproc = s['preproc'], strand = wildcards.strand))

        multiqc_dir = os.path.dirname(output.sample_list)
        os.makedirs(os.path.join(multiqc_dir), exist_ok = True)
        try:
            with open(output.sample_list, 'x') as file:
                file.writelines('\n'.join(fastqc_list))
        except FileExistsError:
            print('List already exists')

rule multiqc_fastqc:
    input:
        sample_list = wc_config['sample_list_wc'],
        # samples = get_fastqc_files_for_multiqc
    output:
        multiqc_report = '{fs_prefix}/{df}/profile/multiqc/{sample_set}/multiqc_report_{strand}.html'
    params:
        wd = wc_config['work_dir_wc'],
        prerep = '{fs_prefix}/{df}/profile/multiqc/{sample_set}/{strand}/multiqc_report.html'
    conda: "multiqc.yaml"
    shell: ("export LC_ALL=en_US.UTF-8; export LANG=en_US.UTF-8; multiqc --file-list {input.sample_list} -o {params.wd}; mv {params.prerep} {output.multiqc_report}")


