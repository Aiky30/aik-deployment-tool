from fabric.api import prompt

from aik_deployment_tool.directory import LocalDirectory
from aik_deployment_tool.file import LocalFile
from aik_deployment_tool.service import LocalService
from aik_deployment_tool.operation import LocalOperation

class Environment(object):

    # FIXME: May be bad to set in init as it gets called on inheritance
    def __init__(self, config, app_config):

        print("Environment init", config)

        self.environment = config['environment']

        self.app_config = app_config

        self.remote_environment = False
        self.local_environment = False


    def set_enviroment(self):
        # TODO: If remote select specific remote enviroment
        return prompt("Which environment do you want to use? options: local | remote")

# FIXME: Wording of environment here is old, needs a new name as environment takes a new meaning
    def get_enviroment(self):
        return self.environment;

    #def set_operating_system(self):


class LocalEnvironment(Environment):

    def __init__(self, config, app_config):

        super(self.__class__, self).__init__(config, app_config)

        self.local_config = config

        self.local_environment = True

        self.service = LocalService(self)
        self.directory = LocalDirectory(self)
        self.file = LocalFile(self)
        self.operation = LocalOperation(self)

    def register_services(self):

        # for each app
        for app_label, app in self.app_config.items():

            # if the current app has a service config, register it
            if 'services' in app:
                self.service.register_service(app['services'])

class RemoteEnvironment(Environment):

    """
        def __init__(self, config):

        Environment.__init__(self, config)
    """

    def __init__(self, config):

        super(self.__class__, self).__init__(config)

    # Set the environment to work on
    def set_remote_environment(self, available_environments):

        environment_list = available_environments.keys()

        # ask the user to set the remote environment they wish to use
        while self.remote_environment is False:

            answer = prompt("Which environment do you want to use: %s" % environment_list)

            if answer in environment_list:
                self.remote_environment = answer
            else:
                print("Wrong answer, please try again.")
