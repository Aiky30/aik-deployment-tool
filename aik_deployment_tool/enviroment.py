import warnings

from fabric.api import prompt

from aik_deployment_tool.directory import LocalDirectory
from aik_deployment_tool.file import LocalFile
from aik_deployment_tool.service import LocalService
from aik_deployment_tool.operation import LocalOperation

from aik_deployment_tool.directory import RemoteDirectory
from aik_deployment_tool.file import RemoteFile
from aik_deployment_tool.service import RemoteService
from aik_deployment_tool.operation import RemoteOperation

class Environment(object):

    # FIXME: May be bad to set in init as it gets called on inheritance
    def __init__(self, config, app_config):

        print("Environment init", config)

        self.environment = config['environment']

        self.config = config
        self.app_config = app_config

        self.remote_environment = False
        self.local_environment = False
    """
    def set_enviroment(self):
        # TODO: If remote select specific remote enviroment
        return prompt("Which environment do you want to use? options: local | remote")

        # FIXME: Wording of environment here is old, needs a new name as environment takes a new meaning

    def get_enviroment(self):
        return self.environment;
    """

    def register_services(self):
        # for each app
        for app_label, app in self.app_config.items():

            # if the current app has a service config, register it
            if 'services' in app:
                self.service.register_service(app['services'])

class LocalEnvironment(Environment):

    def __init__(self, config, app_config):

        super(self.__class__, self).__init__(config, app_config)

        self.local_environment = True

        self.service = LocalService(self)
        self.directory = LocalDirectory(self)
        self.file = LocalFile(self)
        self.operation = LocalOperation(self)

        # Register services
        self.register_services()


class RemoteEnvironment(Environment):
#TODO: Prompt the user what directory they are working with before starting any commands when working with the server
    def __init__(self, config, app_config):

        super(self.__class__, self).__init__(config, app_config)

        self.remote_environment = True

        self.service = RemoteService(self)
        self.directory = RemoteDirectory(self)
        self.file = RemoteFile(self)
        self.operation = RemoteOperation(self)

        # Register services
        self.register_services()

# TODO: Fidn app in config, error if doesn't exist!!!

    # Set the environment to work on
    def set_remote_environment(self, available_environments):

        warnings.warn("Environment is set on command execution, deprecated feature", DeprecationWarning)

        environment_list = available_environments.keys()

        # ask the user to set the remote environment they wish to use
        while self.remote_environment is False:

            answer = prompt("Which environment do you want to use: %s" % environment_list)

            if answer in environment_list:
                self.remote_environment = answer
            else:
                print("Wrong answer, please try again.")
