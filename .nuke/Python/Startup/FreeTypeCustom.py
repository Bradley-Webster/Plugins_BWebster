import nuke

nuke.toNode('root').knob('free_type_font_path').setValue('C:\\temp\\MY_FONTS')
nuke.toNode('root').knob('free_type_system_fonts').setValue(False)