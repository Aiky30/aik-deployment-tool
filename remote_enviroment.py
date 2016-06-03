from fabric.api import cd, run, sudo, abort

from config import *

class RemoteEnviroment():

    #def __init__(self, config):
     #   self.config = config

    def build_directories(self, directory_dict):
        for directory in directory_dict:
           self.create_directory(directory)
           self.set_directory_privileges(directory)

    def create_directory(self, directory):
        if 'parents' in directory.creation and directory.creation.parents:
            sudo("sudo mkdir -p %s" % (directory.path))
        else:
            sudo("sudo mkdir %s" % directory.path)

    def set_directory_privileges(self, directory):

        if 'permissions' in directory:

            # If a level is set
            if 'level' in directory.permissions:
                self.set_directory_level(directory)

            # If an owner and group is set
            if 'owner' in directory.permissions and 'group' in directory.permissions:
                self.set_directory_owner(directory)

    def set_directory_level(self, directory):

        if 'recursive' in directory.permissions and directory.permissions.recursive
            sudo("sudo chmod 775 -R %s" % directory.path)
        else:
            sudo("sudo chmod 775 %s" % directory.path)


    def set_directory_owner(self, directory):
        if 'recursive' in directory.permissions and directory.permissions.recursive
            sudo("sudo chown %s:%s -R %s" % (
                directory.permissions.owner, directory.permissions.group, directory.path))
        else:
            sudo("sudo chown %s:%s %s" % (
                directory.permissions.owner, directory.permissions.group, directory.path))