import click, glob, os
from assnake.cli.cli_utils import sample_set_construction_options, add_options, generic_command_individual_samples, generate_result_list
from assnake.core.result import Result

parameters = [p.split('/')[-1].replace('.json', '') for p in glob.glob('/data11/bio/databases/ASSNAKE/params/tmtic/*.json')]

@click.command('remove-human-bbmap', short_help='Quality based trimming')
@add_options(sample_set_construction_options)
@click.pass_obj
def rmhumbbmap_invocation(config, **kwargs):
    wc_str = '{fs_prefix}/{df}/reads/{preproc}__rmhum_bbmap/{sample}_R1.fastq.gz'
    sample_set, sample_set_name = generic_command_individual_samples(config,  **kwargs)
    config['requests'] += generate_result_list(sample_set, wc_str, **kwargs)

this_dir = os.path.dirname(os.path.abspath(__file__))
result = Result.from_location(name = 'remove-human-bbmap', location = this_dir, input_type = 'illumina_sample', additional_inputs = None, invocation_command = rmhumbbmap_invocation)
