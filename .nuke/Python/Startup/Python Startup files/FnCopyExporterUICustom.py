import os.path

import hiero.ui
import FnCopyExporterCustom


class CopyExporterUI(hiero.ui.TaskUIBase):
  def __init__(self, preset):
    """Initialize"""
    hiero.ui.TaskUIBase.__init__(self, FnCopyExporterCustom.CopyExporter, preset, "Copy Exporter Custom")


hiero.ui.taskUIRegistry.registerTaskUI(FnCopyExporterCustom.CopyPreset, CopyExporterUI)
