def get_fastqc_files_for_multiqc(wildcards):
    fastqc_files = []
    with open('{fs_prefix}/{df}/profile/multiqc/{sample_set}/{strand}/samples.list'.format(**wildcards), 'r') as sample_list:
        fastqc_files = [s.strip() for s in sample_list.readlines()]
    return fastqc_files

rule multiqc_fastqc:
    input:
        sample_list = wc_config['sample_list_wc'],
        samples = get_fastqc_files_for_multiqc
    output:
        multiqc_report = wc_config['multiqc_report_wc']
    params:
        wd = wc_config['work_dir_wc']
    conda: "multiqc.yaml"
    shell: ("export LC_ALL=en_US.UTF-8; export LANG=en_US.UTF-8; multiqc --file-list {input.sample_list} -o {params.wd}")


