import assnake.api.loaders
import assnake
from tabulate import tabulate
import click

@click.command('remove_human_bbmap', short_help='Count number of reads and basepairs in fastq file')

@click.pass_obj

def init_remove_human_bbmap(config, ):
    """
    Will download masked human genome and save it fasta directory.
    """
    # TODO upload masked genome on RCPCM server, download it here
    pass