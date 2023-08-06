"""
Automatically generated.
"""
from argparse import Namespace
from typing import Type

from wai.common.cli import CLIFactory, CLIInstantiable
from wai.common.meta.typing import VAR_ARGS_TYPE

from wai.common.cli.options._TypedOption import TypedOption
from builtins import str
from wai.common.cli.options._FlagOption import FlagOption
from builtins import int


class ROIWriterCLIFactory(CLIFactory):
    """
    Factory which instantiates the ROIWriter class.
    """
    # Options
    comments = TypedOption('--comments', type=str, nargs='+', help='comments to write to the beginning of the ROI file')
    no_images = FlagOption('--no-images', help='skip the writing of images, outputting only the annotation files')
    output = TypedOption('-o', '--output', type=str, required=True, metavar='dir_or_file')
    size_mode = FlagOption('--size-mode', help='writes the ROI files with x,y,w,h headers instead of x0,y0,x1,y1')
    split_names = TypedOption('--split-names', type=str, nargs='+', help='the names to use for the splits', metavar='SPLIT NAME')
    split_ratios = TypedOption('--split-ratios', type=int, nargs='+', help='the ratios to use for the splits', metavar='RATIO')
    writer_prefix = TypedOption('--prefix', type=str, help="the prefix for output filenames (default = '')")
    writer_suffix = TypedOption('--suffix', type=str, help="the suffix for output filenames (default = '-rois.csv')")

    @classmethod
    def production_class(self, namespace: Namespace) -> Type[CLIInstantiable]:
        from wai.annotations.roi.io._ROIWriter import ROIWriter
        return ROIWriter

    @classmethod
    def init_args(self, namespace: Namespace) -> VAR_ARGS_TYPE:
        return (namespace,), dict()
