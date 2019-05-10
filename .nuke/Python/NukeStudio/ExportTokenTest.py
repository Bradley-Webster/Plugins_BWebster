class FtrackBasePreset(FtrackBase):
    def __init__(self, name, properties, **kwargs):

        super(FtrackBasePreset, self).__init__(name, properties)
        self.set_export_root()
        self.set_ftrack_properties(properties)

    def set_ftrack_properties(self, properties):

        properties = self.properties()
        properties.setdefault('ftrack', {})

        # add placeholders for default ftrack defaults
        self.properties()['ftrack']['component_name'] = 'main'
        self.properties()['ftrack']['component_pattern'] = '.{ext}'
        self.properties()['ftrack']['project_schema'] = 'Film Pipeline'
        self.properties()['ftrack']['task_type'] = 'Generic'
        self.properties()['ftrack']['task_status'] = 'Not Started'
        self.properties()['ftrack']['shot_status'] = 'In progress'
        self.properties()['ftrack']['asset_version_status'] = 'WIP'
        self.properties()['ftrack']['processor_id'] = hash(self.__class__.__name__)

        # options
        self.properties()['ftrack']['opt_publish_thumbnail'] = True

    def set_export_root(self):

        self.properties()['exportRoot'] = self.ftrack_location.accessor.prefix

    def resolve_ftrack_project(self, task):

        return task.projectName()

    def resolve_ftrack_sequence(self, task):

        trackItem = task._item
        return trackItem.name().split('_')[0]

    def resolve_ftrack_shot(self, task):
        trackItem = task._item
        if not isinstance(trackItem, hiero.core.Sequence):
            return trackItem.name().split('_')[1]
        else:
            return trackItem.name()

    def resolve_ftrack_task(self, task):
        return self.properties()['ftrack']['task_type']

    def resolve_ftrack_asset(self, task):

        return task._preset.name()

    def resolve_ftrack_component(self, task):

        component_name = self.properties(['ftrack']['component_name'])
        extension = self.properties(['ftrack']['component_pattern'])
        component_full_name = '{0}{1}'.format(component_name, extension)
        return component_full_name

    def addFtrackResolveEntries(self, resolver):
        resolver.addResolver(
            '{ftrack_project}',
            'Ftrack project name.',
            lambda keyword, task: self.resolve_ftrack_project(task)
        )

        resolver.addResolver(
            '{ftrack_sequence}',
            'Ftrack sequence name.',
            lambda keyword, task: self.resolve_ftrack_sequence(task)
        )

        resolver.addResolver(
            '{ftrack_shot}',
            'Ftrack shot name.',
            lambda keyword, task: self.resolve_ftrack_shot(task)
        )

        resolver.addResolver(
            '{ftrack_task}',
            'Ftrack task name.',
            lambda keyword, task: self.resolve_ftrack_task(task)
        )

        resolver.addResolver(
            '{ftrack_asset}',
            'Ftrack asset name.',
            lambda keyword, task: self.resolve_ftrack_asset(task)
        )

        resolver.addResolver(
            '{ftrack_component}',
            'Ftrack component name.',
            lambda keyword, task: self.resolve_ftrack_component(task)
        )
