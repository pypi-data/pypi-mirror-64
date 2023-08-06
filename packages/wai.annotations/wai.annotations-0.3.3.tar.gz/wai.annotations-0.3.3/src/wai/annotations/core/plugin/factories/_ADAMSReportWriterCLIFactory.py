"""
Automatically generated.
"""
from argparse import Namespace
from typing import Type

from wai.common.cli import CLIFactory, CLIInstantiable
from wai.common.meta.typing import VAR_ARGS_TYPE

from wai.common.cli.options._FlagOption import FlagOption
from wai.common.cli.options._TypedOption import TypedOption
from builtins import str
from builtins import int


class ADAMSReportWriterCLIFactory(CLIFactory):
    """
    Factory which instantiates the ADAMSReportWriter class.
    """
    # Options
    no_images = FlagOption('--no-images', help='skip the writing of images, outputting only the annotation files')
    output = TypedOption('-o', '--output', type=str, required=True, metavar='dir_or_file')
    split_names = TypedOption('--split-names', type=str, nargs='+', help='the names to use for the splits', metavar='SPLIT NAME')
    split_ratios = TypedOption('--split-ratios', type=int, nargs='+', help='the ratios to use for the splits', metavar='RATIO')

    @classmethod
    def production_class(self, namespace: Namespace) -> Type[CLIInstantiable]:
        from wai.annotations.adams.io._ADAMSReportWriter import ADAMSReportWriter
        return ADAMSReportWriter

    @classmethod
    def init_args(self, namespace: Namespace) -> VAR_ARGS_TYPE:
        return (namespace,), dict()
