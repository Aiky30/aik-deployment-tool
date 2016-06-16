from fabric.api import local, lcd


class LocalOperation(object):

    def __init__(self, environment):

        self.environment = environment

    def run(self, command):

        local(command)

    def run_from_directory(self, directory, command):

        with lcd(directory):

            local(command)
