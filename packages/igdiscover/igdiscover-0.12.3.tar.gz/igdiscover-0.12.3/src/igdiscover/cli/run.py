"""
Run IgDiscover

Calls Snakemake to produce all the output files.
"""
import sys
import logging
import resource
import platform
import pkg_resources
from snakemake import snakemake

from .config import Config
from . import CommandLineError
from ..utils import available_cpu_count
from .. import __version__


logger = logging.getLogger(__name__)


def add_arguments(parser):
    arg = parser.add_argument
    arg('--dryrun', '-n', default=False, action='store_true',
        help='Do not execute anything')
    arg('--cores', '--jobs', '-j', metavar='N', type=int, default=available_cpu_count(),
        help='Run on at most N CPU cores in parallel. '
        'Default: Use as many cores as available (%(default)s)')
    arg('--keepgoing', '-k', default=False, action='store_true',
        help='If one job fails, finish the others.')
    arg('targets', nargs='*', default=[],
        help='File(s) to create. If omitted, the full pipeline is run.')


def main(args):
    run_snakemake(**vars(args))


def run_snakemake(
    dryrun=False,
    cores=available_cpu_count(),
    keepgoing=False,
    targets=None,
):
    try:
        config = Config.from_default_path()
    except FileNotFoundError as e:
        sys.exit("Pipeline configuration file {!r} not found. Please create it!".format(e.filename))

    print('IgDiscover version {} with Python {}. Configuration:'.format(__version__,
        platform.python_version()))
    for k, v in sorted(vars(config).items()):
        # TODO the following line is only necessary for non-YAML configurations
        if k.startswith('_'):
            continue
        print('   ', k, ': ', repr(v), sep='')
    sys.stdout.flush()

    old_root_handlers = logger.root.handlers
    root = logging.getLogger()
    root.handlers = []
    file_handler = logging.FileHandler("log.txt")
    root.addHandler(file_handler)

    snakefile_path = pkg_resources.resource_filename('igdiscover', 'Snakefile')
    success = snakemake(
        snakefile_path,
        snakemakepath='snakemake',  # Needed in snakemake 3.9.0
        dryrun=dryrun,
        cores=cores,
        keepgoing=keepgoing,
        printshellcmds=True,
        targets=targets,
    )
    logger.root.handlers = old_root_handlers

    if sys.platform == 'linux' and not dryrun:
        cputime = resource.getrusage(resource.RUSAGE_SELF).ru_utime
        cputime += resource.getrusage(resource.RUSAGE_CHILDREN).ru_utime
        h = int(cputime // 3600)
        m = (cputime - h * 3600) / 60
        print('Total CPU time: {}h {:.2f}m'.format(h, m))

    if not success:
        raise CommandLineError()
