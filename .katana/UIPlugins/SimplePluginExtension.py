from Katana import FnAttribute
from Katana import FnGeolibServices

from PluginAPI.BaseViewerPluginExtension import BaseViewerPluginExtension


_OPSCRIPT_SOURCE = """
local txtAttr = Interface.GetAttr('viewer.texture.path')
if Attribute.IsString(txtAttr) then
  gb = GroupBuilder()
  gb:set('hydraSurfaceShader', StringAttribute('simple_shader'))
  gb:set('hydraSurfaceParams.flipT', IntAttribute(1))
  gb:set('hydraSurfaceParams.texture', txtAttr)
  Interface.SetAttr('material', gb:build())
end
"""

class SimplePluginExtension(BaseViewerPluginExtension):
    """Simple VPE plug-in."""

    def onApplyTerminalOps(self, txn, inputOp, viewerDelegate):
        """..."""

        # Turn facesets into geometry locations.
        argsBuilder = FnGeolibServices.OpArgsBuilders.AttributeSet()
        argsBuilder.setCEL([
            '/root/world//*{@type == "faceset"}'])
        argsBuilder.setAttr('type',
            FnAttribute.StringAttribute('polymesh'))

        setAttrOp = txn.createOp()
        txn.setOpArgs(setAttrOp, 'AttributeSet', argsBuilder.build())
        txn.setOpInputs(setAttrOp, [inputOp])

        # Apply material.
        asgb = FnAttribute.GroupBuilder()
        asgb.set('script', _OPSCRIPT_SOURCE)
        argsBuilder = FnGeolibServices.OpArgsBuilders.AttributeSet()
        argsBuilder.setCEL(['/root/world/geo//*{@type == "polymesh" '
                            'or @type == "subdmesh"}'])
        argsBuilder.addSubOp('OpScript.Lua', asgb.build())

        setMaterialOp = txn.createOp()
        txn.setOpArgs(setMaterialOp, 'AttributeSet', argsBuilder.build())
        txn.setOpInputs(setMaterialOp, [setAttrOp])
        return setMaterialOp

PluginRegistry = [
    ('ViewerPluginExtension', 1,
     'SimplePluginExtension', SimplePluginExtension),
]
