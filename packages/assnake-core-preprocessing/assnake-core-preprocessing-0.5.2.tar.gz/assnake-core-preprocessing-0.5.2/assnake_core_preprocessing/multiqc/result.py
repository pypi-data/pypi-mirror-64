import click
from assnake.utils import read_yaml, pathizer
import datetime
# from assnake_core_preprocessing.utils import format_cmdinp2obj, prepare_fastqc_list_multiqc
import click, glob, os
from assnake.cli.cli_utils import sample_set_construction_options, add_options, generic_command_individual_samples, generate_result_list, generic_command_dict_of_sample_sets, prepare_sample_set_tsv_and_get_results
from assnake.core.result import Result
import os
from pathlib import Path

@click.command('multiqc', short_help='Forming the multiqc report')
@add_options(sample_set_construction_options)
@click.option('--strand', help='Strand to profile', default='R1', type=click.STRING )

# @click.option('--set-name', '-n', help='Name of the set', default='', type=click.STRING )
@click.pass_obj


def multiqc_invocation(config, strand, **kwargs):
    sample_sets = generic_command_dict_of_sample_sets(config,  **kwargs)
    sample_set_dir_wc = '{fs_prefix}/{df}/profile/multiqc/{sample_set}/'
    result_wc = '{fs_prefix}/{df}/profile/multiqc/{sample_set}/multiqc_report_{strand}.html'
    res_list = prepare_sample_set_tsv_and_get_results(sample_set_dir_wc, result_wc, df = kwargs['df'], sample_sets = sample_sets, strand = strand, overwrite = False)
    config['requests'] += res_list



this_dir = os.path.dirname(os.path.abspath(__file__))
result = Result.from_location(name = 'multiqc', location = this_dir, input_type = 'illumina_sample_set', additional_inputs = None, invocation_command = multiqc_invocation)
