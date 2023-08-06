"""
Automatically generated.
"""
from wai.annotations.core.plugin.registry._PluginRegistry import PluginRegistry
from wai.annotations.core.plugin.registry._RegistryEntry import RegistryEntry

registry = PluginRegistry(adams=RegistryEntry('wai.annotations.adams.ADAMSFormatSpecifier', 'wai.annotations 0.3.2', 'ADAMSReportReaderCLIFactory', 'FromADAMSReportCLIFactory', 'ToADAMSReportCLIFactory', 'ADAMSReportWriterCLIFactory'), coco=RegistryEntry('wai.annotations.coco.COCOFormatSpecifier', 'wai.annotations 0.3.2', 'COCOReaderCLIFactory', 'FromCOCOCLIFactory', 'ToCOCOCLIFactory', 'COCOWriterCLIFactory'), roi=RegistryEntry('wai.annotations.roi.ROIFormatSpecifier', 'wai.annotations 0.3.2', 'ROIReaderCLIFactory', 'FromROICLIFactory', 'ToROICLIFactory', 'ROIWriterCLIFactory'), tfrecords=RegistryEntry('wai.annotations.tf.TFFormatSpecifier', 'wai.annotations 0.3.2', 'TensorflowExampleReaderCLIFactory', 'FromTensorflowExampleCLIFactory', 'ToTensorflowExampleCLIFactory', 'TensorflowExampleWriterCLIFactory'), vgg=RegistryEntry('wai.annotations.vgg.VGGFormatSpecifier', 'wai.annotations 0.3.2', 'VGGReaderCLIFactory', 'FromVGGCLIFactory', 'ToVGGCLIFactory', 'VGGWriterCLIFactory'))
