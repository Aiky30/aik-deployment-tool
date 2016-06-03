from fabric.api import prompt

class Environment(object):

    # FIXME: May be bad to set in init as it gets called on inheritance
    def __init__(self, config):

        print("Environment init", config)

        self.environment = config['environment']

        self.os = config['os']

        #self.environment = self.set_enviroment()

        print("environment set: ", self.environment)

    #   self.config = config  # Set the environment to work on

    def set_enviroment(self):
        # TODO: If remote select specific remote enviroment
        return prompt("Which environment do you want to use? options: local | remote")

    def get_enviroment(self):
        return self.environment;

    #def set_operating_system(self):


class RemoteEnvironment(Environment):

    """
        def __init__(self, config):

        Environment.__init__(self, config)
    """

    def __init__(self, config):

        super(self.__class__, self).__init__(config)

        self.remote_environment=False

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
