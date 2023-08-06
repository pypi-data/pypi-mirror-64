"""
Automatically generated.
"""
from argparse import Namespace
from typing import Type

from wai.common.cli import CLIFactory, CLIInstantiable
from wai.common.meta.typing import VAR_ARGS_TYPE

from wai.common.cli.options._TypedOption import TypedOption
from wai.annotations.core._ImageFormat import ImageFormat
from builtins import str


class FromADAMSReportCLIFactory(CLIFactory):
    """
    Factory which instantiates the FromADAMSReport class.
    """
    # Options
    image_conversion_format = TypedOption('--convert-image', type=ImageFormat, help='format to convert images to', metavar='FORMAT')
    label_mapping = TypedOption('-m', '--mapping', type=str, action='append', help='mapping for labels, for replacing one label string with another (eg when fixing/collapsing labels)', metavar='old=new')
    prefixes = TypedOption('-p', '--prefixes', type=str, nargs='+', help='prefixes to parse')

    @classmethod
    def production_class(self, namespace: Namespace) -> Type[CLIInstantiable]:
        from wai.annotations.adams.convert._FromADAMSReport import FromADAMSReport
        return FromADAMSReport

    @classmethod
    def init_args(self, namespace: Namespace) -> VAR_ARGS_TYPE:
        return (namespace,), dict()
