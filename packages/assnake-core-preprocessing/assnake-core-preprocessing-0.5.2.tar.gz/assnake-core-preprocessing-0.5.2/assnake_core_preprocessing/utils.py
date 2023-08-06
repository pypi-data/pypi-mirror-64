import assnake.api.loaders
import assnake
from tabulate import tabulate
import click
import os
import pandas as pd

# DONE self to ss
def prepare_fastqc_list_multiqc(sample_setObj, strand, set_name):
    fastqc_list = []

    for s in sample_setObj.samples_pd.to_dict(orient='records'):
        fastqc_list.append(sample_setObj.wc_config['fastqc_data_wc'].format(**s, strand=strand))

    dfs = list(set(sample_setObj.samples_pd['df']))

    if len(dfs) == 1:
        fs_prefix = list(set(sample_setObj.samples_pd['fs_prefix']))[0]
        sample_list = sample_setObj.wc_config['multiqc_fastqc_wc'].format(
            df=dfs[0],
            fs_prefix=fs_prefix,
            strand=strand,
            sample_set=set_name)
        # print(sample_list)

        multiqc_dir = os.path.dirname(sample_list)
        if not os.path.isdir(multiqc_dir):
            os.makedirs(multiqc_dir)
        try:
            with open(sample_list, 'x') as file:
                file.writelines('\n'.join(fastqc_list))
        except FileExistsError:
            print('List already exists')

    return fastqc_list
