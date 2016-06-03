from fabric.api import local, prompt, sudo

from aik_deployment_tool.enviroment import Environment

#TODO: Need a way to delete a file????

class Directory(Environment):
    # TODO: If the directory has permissions, register them etc so the config becomes native and an attribute of the class

    def __init__(self, Enviroment):
        print("Directory init", self, Enviroment)

    def register_directory(self):
        pass

    def destroy_directories(self, directory_dict):
        for label, directory in directory_dict.iteritems():

            if 'destroy' in directory:
                self.destroy_directory(directory)

    def build_directories(self, directory_dict):

        for label, directory in directory_dict.items():

            if 'creation' in directory:
                self.create_directory(directory)

        # FYI: This loop is duplicated because setting the privileges that are recursive
        for label, directory in directory_dict.iteritems():

            if 'permissions' in directory:
                self.set_directory_privileges(directory)

    def set_directory_privileges(self, directory):

        # If a level is set
        if 'level' in directory['permissions']:
            self.set_directory_level(directory)

        # If an owner and group is set
        if 'owner' in directory['permissions'] and 'group' in directory['permissions']:
            self.set_directory_owner(directory)


class LocalDirectory(Directory):
    def create_directory(self, directory):

        if 'parents' in directory['creation'] and directory['creation']['parents']:
            local("sudo mkdir -p %s" % (directory['path']))
        else:
            local("sudo mkdir %s" % directory['path'])

    # Delete any directories
    def destroy_directory(self, directory):

        answer = prompt('Are you sure you want to delete: %s (y/n)' % directory['path'])

        print("You answered: %s" % answer)

        if answer == 'y':
            local("sudo rm -R %s" % directory['path'])

    def set_directory_level(self, directory):

        if 'recursive' in directory['permissions'] and directory['permissions']['recursive']:
            local("sudo chmod 775 -R %s" % directory['path'])
        else:
            local("sudo chmod 775 %s" % directory['path'])

    def set_directory_owner(self, directory):

        if 'recursive' in directory['permissions'] and directory['permissions']['recursive']:
            local("sudo chown %s:%s -R %s" % (
                directory['permissions']['owner'], directory['permissions']['group'], directory['path']))
        else:
            local("sudo chown %s:%s %s" % (
                directory['permissions']['owner'], directory['permissions']['group'], directory['path']))

class RemoteDirectory(Directory):

    def create_directory(self, directory):

        if 'parents' in directory['creation'] and directory['creation']['parents']:
            sudo("sudo mkdir -p %s" % (directory['path']))
        else:
            sudo("sudo mkdir %s" % directory['path'])

    # Delete any directories
    def destroy_directory(self, directory):

        answer = prompt('Are you sure you want to delete: %s (y/n)' % directory['path'])

        print("You answered: %s" % answer)

        if answer == 'y':
            sudo("sudo rm -R %s" % directory['path'])

    def set_directory_level(self, directory):

        if 'recursive' in directory['permissions'] and directory['permissions']['recursive']:
            sudo("sudo chmod 775 -R %s" % directory['path'])
        else:
            sudo("sudo chmod 775 %s" % directory['path'])

    def set_directory_owner(self, directory):

        if 'recursive' in directory['permissions'] and directory['permissions']['recursive']:
            sudo("sudo chown %s:%s -R %s" % (
                directory['permissions']['owner'], directory['permissions']['group'], directory['path']))
        else:
            sudo("sudo chown %s:%s %s" % (
                directory['permissions']['owner'], directory['permissions']['group'], directory['path']))
