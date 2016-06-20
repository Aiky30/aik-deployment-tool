from fabric.api import local, lcd


class LocalOperation(object):

    def __init__(self, environment):

        self.environment = environment

    def run(self, command):

        local(command)

    def run_from_directory(self, directory, command):

        with lcd(directory):

            local(command)

    def copy_file(self, from_location, to_location):
        local("cp %s %s" % (from_location, to_location))

    def link_file(self, from_location, to_location):
        local("sudo ln -s %s %s" % (from_location, to_location))

    def copy_all(self, from_location, to_location):
        local("cp -r %s. %s" % (from_location, to_location))