from fabric.api import local, lcd

from file import LocalFile
from directory import LocalDirectory


class Project(object):

    def __init__(self, environment, project_config):

        self.environment = environment
        self.project_config = project_config


class LocalProject(Project):

    """
    def __init__(self, Environment):
        super(self.__class__, self).__init__(Environment)
    """

    def install(self):

        if 'directories' in self.project_config:
            # Create directories
            directory_instance = LocalDirectory(self.environment)
            directory_instance.build_directories(self.project_config['directories'])

    def remove(self):

        if 'directories' in self.project_config:
            # Remove directories
            directory_instance = LocalDirectory(self.environment)
            directory_instance.destroy_directories(self.project_config['directories'])

        if 'files' in self.project_config:
            # Remove files
            file_instance = LocalFile(self.environment)
            file_instance.destroy_files(self.project_config['files'])