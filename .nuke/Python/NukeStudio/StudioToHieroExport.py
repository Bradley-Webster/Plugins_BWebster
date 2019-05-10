def process(self, data):
 '''Process *data* and assetise related track item.'''

 session = ftrack_api.Session()

 assetVersion = session.get('AssetVersion', data['asset_version_id'])
 project = assetVersion.getProject()
 storage = networkFunctions.getStorageNameFromProject(project)
 assetVersionPublishPath = networkFunctions.getPathFromAssetVersion(assetVersion)
 assetVersionPathAbs = pathFunctions.prependProjectsStoragePath(
 storage, assetVersionPublishPath
 )
 pathExtra.createDir(assetVersionPathAbs)

 # The component has to be created before the render renderJob is kicked off
 # in order to assetise the track_item. This is required since the render
 # renderJob is asynchronous and will be offloaded to another machine
 component = ftrack.createComponent(
 name=environment.PLATE_COMPONENT_NAME,
 versionId=data['asset_version_id'],
 systemType='sequence'
 )
 component.setMeta('img_main', True)

 track_item = data['application_object']

 ftrack_connect_nuke_studio.entity_reference.set(
 track_item, component
 )

 # Copied from ftrack_connect_nuke_studio.processor.ProcessorPlugin.process
 # Could not call super(DeadlineSubmitPlugin).process(data) because
 # it would start the Nuke render, but we don't want that
 nuke.scriptClear()
 nuke.nodePaste(os.path.expandvars(self.script))
 read_node = nuke.toNode('IN')
 write_node = nuke.toNode('OUT')

 if not all([read_node, write_node]):
 raise ValueError(
 'Missing required IN and OUT nodes.'
 )

 self.logger.debug('Raw data: {0}'.format(data))
 data = self.prepare_data(data)
 self.logger.debug('Prepared data: {0}'.format(data))

 self._ensure_attributes(write_node)
 self._apply_options_to_nuke_script(data)

 start = write_node['first'].value()
 end = write_node['last'].value()

 temporary_script_name = os.path.join(
 tempfile.gettempdir(),
 '{prefix}-{random}.nk'.format(
 prefix=self.getName(),
 random=uuid.uuid4().hex
 )
 )

 self.logger.info(
 'Saving temporary script to "{0}"'.format(temporary_script_name)
 )
 nuke.scriptSaveAs(temporary_script_name)

# nuke.executeBackgroundNuke(
# nuke.EXE_PATH,
# [write_node],
# nuke.FrameRanges([
# nuke.FrameRange('{0}-{1}'.format(int(start), int(end)))
# ]),
# nuke.views(),
# {}
# )

 nuke.scriptClear()
 # End of copy from ftrack_connect_nuke_studio.processor.ProcessorPlugin.process


 project = track_item.project()
 renderPath = pathFunctions.appendFilenameToAssetVersionPath(
 assetVersionPublishPath,
 'exr',
 component='master',
 padding='%04d',
 ranges='{0}-{1}'.format(int(start), int(end))
 )
 # Only get the version number
 versionNumber = os.path.basename(track_item.currentVersion().name())
 jobName = '{shot}-{version}'.format(
 shot=track_item.name(),
 version=versionNumber
 )
 pool = deadlineUtils.findPool(project.path())
 fromScene = pathFunctions.removeProjectsStoragePath(project.path())

 inData = data['IN']
 inFilePath = '{0} [{1}-{2}]'.format(
 inData['file'], inData['first'], inData['last']
 )

 args = (
 nuke.NUKE_VERSION_STRING,
 temporary_script_name,
 inFilePath,
 renderPath,
 assetVersion,
 jobName,
 project.framerate().toFloat(),
 pool,
 project.path()
 )
 _THREAD_POOL.apply_async(submitJobs, args)
