# Copyright (c) 2018 The Foundry Visionmongers Ltd. All Rights Reserved.
"""
This is a plug-in for Katana which executes a user specified script on 
start-up - like when  launching in script mode - in UI mode. 

To use it, simply launch Katana in UI mode with a python file on the command line.
"""
from Katana import (Callbacks, Configuration)
import logging, os, sys


if not Configuration.get('KATANA_SCRIPT_MODE'):
	log = logging.getLogger("UIStartupScript")
	
	def onStartupComplete(**kwargs):
		for arg in sys.argv:
			if not arg.endswith('.py'):
				continue
				
			path = os.path.abspath(arg)
			if os.path.exists(path):
				log.info("Excuting commandline script %s" % path)
				execfile(path)

	Callbacks.addCallback(Callbacks.Type.onStartupComplete, onStartupComplete)
