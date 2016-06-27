

class Project(object):

    def __init__(self, environment, project_config):

        self.environment = environment
        self.project_config = project_config

    def install(self):

        if 'directories' in self.project_config:
            # Create directories
            directory_instance = self.environment.directory
            directory_instance.build_directories(self.project_config['directories'])

    def remove(self):

        if 'directories' in self.project_config:
            # Remove directories
            directory_instance = self.environment.directory
            directory_instance.destroy_directories(self.project_config['directories'])

        if 'files' in self.project_config:
            # Remove files
            file_instance = self.environment.file
            file_instance.destroy_files(self.project_config['files'])


class LocalProject(Project):

    def __init__(self, environment, project_config):
        super(self.__class__, self).__init__(environment, project_config)


class RemoteProject(Project):

    def __init__(self, environment, project_config):
        super(self.__class__, self).__init__(environment, project_config)
