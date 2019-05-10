import hiero.core
from hiero.core import log, taskRegistry, TaskPresetBase
from hiero.core.events import EventType, registerInterest
from hiero.exporters.FnShotProcessor import ShotProcessorPreset
from hiero.exporters.FnTranscodeExporter import TranscodePreset, TranscodeExporter
###################################################################The latest Foundry Edit
from hiero.ui import taskUIRegistry
from hiero.exporters.FnExternalRenderUI import NukeRenderTaskUI
###################################################################
EXPORT_PRESET_NAME = 'Export Footage with Custom Presets'

# =============================================================================
class CustomTranscodeExporter(TranscodeExporter):
    """Custom Task that pre-creates elements for outputs.

    """

    def startTask(self, *args, **kwargs):
        log.debug('running startTask() for shot: {0}'.format(self.shotName()))
        super(CustomTranscodeExporter, self).startTask(*args, **kwargs)

# =============================================================================
class CustomTranscodePreset(TranscodePreset):
    """Custom preset for implementing a custom TranscodeExporter.

    """

    def __init__(self, name, properties):
        hiero.core.RenderTaskPreset.__init__(self, CustomTranscodeExporter, name, properties)


        # Set any preset defaults here
        self.properties()["keepNukeScript"] = False
        self.properties()["burninDataEnabled"] = False
        self.properties()["burninData"] = {}
        self.properties()["additionalNodesEnabled"] = False
        self.properties()["additionalNodesData"] = []
        self.properties()["method"] = "Blend"

        # Give the Write node a name, so it can be referenced elsewhere
        if "writeNodeName" not in self.properties():
            self.properties()["writeNodeName"] = "Write_{ext}"

        self.properties().update(properties)


# =============================================================================
# Build custom preset.

def registerPresets(event=None):
    """Function for creating custom export presets.

    Can be called standalone, or used as an event handler.  See:
    https://learn.foundry.com/hiero/developers/11.1/HieroPythonDevGuide/events.html#registering-interest-in-an-event

    """

    log.debug('registerPresets() called for event: {0}'.format(event))

    if EXPORT_PRESET_NAME in taskRegistry.processorPresetNames():
        log.debug("preset '{}' already in registry; skipping registration".format(EXPORT_PRESET_NAME))
        preset = taskRegistry.processorPresetByName(EXPORT_PRESET_NAME)
    else:
        properties = {
            'exportTemplate' : (
                (
                    "shot/element/footage/cc/{version}/default/rgba/NukeShotPreset.{ext}",
                    hiero.exporters.FnNukeShotExporter.NukeShotPreset("NukeShotPreset", {'writePaths': ["shot/{shotnum}/element/footage/cc/{version}/default/{res}/rgba/NukeRenderPreset.####.{ext}"]})
                ),
                (
                    "shot/element/footage/cc/{version}/default/rgba/NukeRenderPreset.####.{ext}",
                    hiero.exporters.FnExternalRender.NukeRenderPreset("NukeRenderPreset", {'file_type' : 'exr', 'exr' : {'datatype' : '16 bit half'}} )
                ),
                (
                    "shot/element/footage/cc/{version}/TranscodedFiles/rgba/{filehead}.####.{fileext}"
                ),
            )
        }

        preset = ShotProcessorPreset(EXPORT_PRESET_NAME, properties)
        taskRegistry.addProcessorPreset(EXPORT_PRESET_NAME, preset)

    # Update version padding to 4.
    preset.properties()['versionPadding'] = 4

# =============================================================================
# Add custom tokens per instructions here:
# https://www.thefoundry.co.uk/products/hiero/developers/11.1/hieropythondevguide/export.html

def GlobalAddUserResolveEntries(_, resolver):
    """Function for adding custom tokens to the export string resolver.

    See:
    https://www.thefoundry.co.uk/products/hiero/developers/1.8/hieropythondevguide/export.html#export-tokens

    """

    # these are just stubs for now
    resolver.addResolver('{file}', 'output footage base name.', lambda _, task: 'file')
    resolver.addResolver('{res}', 'image resolution alias.', lambda _, task: 'res')
    resolver.addResolver('{shotnum}', 'shot number.', lambda _, task: 'shotnum')

# =============================================================================
# From an init script in a location that is added to $HIERO_PLUGIN_PATH
TaskPresetBase.addUserResolveEntries = GlobalAddUserResolveEntries

registerInterest(EventType.kAfterProjectLoad, registerPresets)
registerInterest(EventType.kAfterNewProjectCreated, registerPresets)

taskRegistry.registerTask(CustomTranscodePreset, CustomTranscodeExporter)

# Register the new task to appear in the export settings column
taskUIRegistry.registerTaskUI(CustomTranscodePreset, NukeRenderTaskUI)

