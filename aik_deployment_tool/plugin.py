from fabric.api import local, lcd, cd, run, sudo

from directory import LocalDirectory
from file import LocalFile

class Plugin(object):

    def __init__(self, Environment):

        self.environment = Environment

        print("plugin init: ", self, Environment.environment)

class LocalPlugin(Plugin):

    def __init__(self, Environment):
        super(self.__class__, self).__init__(Environment)

    def install(self, plugin):

        directory_instance = LocalDirectory(self.environment)
        directory_instance.build_directories(plugin['directories'])

    def remove(self, plugin):

        directory_instance = LocalDirectory(self.environment)
        directory_instance.destroy_directories(plugin['directories'])

        file_instance = LocalFile(self.environment)
        file_instance.destroy_files(plugin['files'])

    def configure(self, plugin):

        file_instance = LocalFile(self.environment)

        file_instance.copy_file(
            plugin['config']['copy_from'],
            plugin['config']['copy_to'],
        )

        file_instance.link_file(
            plugin['config']['copy_to'],
            plugin['config']['symlink'],
        )
"""
LOCAL_BACKEND_APPS['apache'] = {
    'dependencies': [
        'project',
        'logs',
        'config'
    ],
    'directories': {
        'logs': {
            'path': os.path.join(LOCAL_PROJECT['backend_root'], "logs/apache"),
            'create': True,
            'parents': True
        },
        'config': {
            'path': os.path.join(LOCAL_PROJECT['backend_root'], "config/apache"),
            'creation': {}
        }
    },
    'files': {
        'config': {
            'path': os.path.join(LOCAL_SYSTEM['apache_config_root'], "gismoh-dev-backend.conf"),
            'destroy': True
        }
    },
    'services': {
        'apache': {
            'restart_cmd': "sudo service apache2 restart"
        }
    },
    'config': {
        'symlink': os.path.join(LOCAL_SYSTEM['apache_config_root'], "gismoh-dev-backend.conf"),
        'copy_from': os.path.join(LOCAL_PROJECT['build_resources'], "backend/development.conf"),
        'copy_to': os.path.join(LOCAL_PROJECT['backend_root'], 'logs/apache/dev-backend.conf')
    }
}

"""