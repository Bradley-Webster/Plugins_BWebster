'''
Created on 07 March 2016

@author: sean-f
'''
import subprocess as sub
import PyOpenColorIO as OCIO

def getAllCS():
	# env=os.environ
	# env['OCIO_MODE']='standard'
	# process =sub.Popen(os.path.join(os.environ['HIERO_BUNDLE_TOOLS_SCRIPTS'],'listCS'),stdout=sub.PIPE, env=env)
	# out, err = process.communicate()
	# cs=out.split("\n")
	# rtn= filter(lambda k: k and "PATH#" not in k and not k.startswith("/"),cs)    
	# rtn.insert(0,"")
	# return rtn	

	config = OCIO.GetCurrentConfig()
	colorspaces = []
	for cs in config.getColorSpaces():
		colorspaces.append(cs.getName())
	return colorspaces

global batch_config


batch_config={'default':"turnover/frames",
              'definitions':{

                             'turnover':{
                                      'frames':{
                                                    'widgets':[
															
															{
															'name':'bundleName',
															'label':'Bundle Name',
															'type':'text',
															'value':"<bundleName>",
															},
															{
															'name':'in_colorSpace',
															'label':'Colorspace',
															'type':'combobox',
															'value':"<in_colorSpace>",
															'values':getAllCS(),
																			},
															
	
															
															{
															'name':'createPlate',
															'label':'Create Plate',
															'type':'checkbox',
															'value':True,
															},
															{
															'name':'autoOverwrite',
															'label':'Auto Overwrite Versions',
															'type':'checkbox',
															'value':True,
															},
                                                    
															{
															'name':'anamorphic',
															'label':'Anamorphic',
															'type':'checkbox',
															'value':False,
															},
															{
															'name':'publish_this',
															'label':'Publish',
															'type':'checkbox',
															'value':True
															},
															

                                                    ]
                                                    },
                                                },
                             'plate':{
                                      'input_plate':{
                                                    'widgets':[
															
															{
															'name':'bundleName',
															'label':'Bundle Name',
															'type':'text',
															'value':"<bundleName>",
															},
															{
															'name':'firstFrameNumber',
															'label':'Renumber From',
															'type':'text',
															'value':"1001",
															},
															{
															'name':'in_colorSpace',
															'label':'Colorspace',
															'type':'combobox',
															'value':"<in_colorSpace>",
															'values':getAllCS(),
																			},
															
															{
															'name':'changeFrameRange',
															'label':'Renumber',
															'type':'checkbox',
															'value':"<$RENUMBER_PLATE_FRAMES>",
															},
															
															{
															'name':'anamorphic',
															'label':'Anamorphic',
															'type':'checkbox',
															'value':False,
															},
															{
															'name':'publish_this',
															'label':'Publish',
															'type':'checkbox',
															'value':True
															},
                                                    ]
                                                    },
                            },

                            }
                   }
