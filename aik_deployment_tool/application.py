from fabric.api import local, lcd, cd, run, sudo

import warnings

class Application(object):

    def __init__(self, Environment):
        self.environment = Environment

    def configure_virtual_environment(self, application):
        print("\n## Virtual environment setup\n")

    def install_application_from_repo(self, application, directories):
        print("\n## Application install\n")

class LocalApplication(Application):

    def __init__(self, Environment):
        super(self.__class__, self).__init__(Environment)

    def configure_virtual_environment(self, application):

        super(self.__class__, self).configure_virtual_environment(application)

        local(application['virtual_environment']['create_cmd'] + " " + application['virtual_environment']['library_container'])

    def install_application_from_repo(self, application, directories):

        super(self.__class__, self).install_application_from_repo(application, directories)

        warnings.warn(
            "Should be handled in project!!",
            DeprecationWarning
        )

        branch = application['repository']['branch']

        # Pull the code
        local("git clone %s %s" % (application['repository']['url'], directories['application']['path']))

        if branch is not False:

            with lcd(directories['application']['path']):
                local("git checkout %s" % branch)

    def update_application_from_repo(self, directories):

#TODO: May be better to have a pull commit, from branhc, checkout etc!!!
        with lcd(directories['application']['path']):
            # Pull the code
            local("git pull")

    def copy_file(self, from_location, to_location):

        warnings.warn(
            "Should be handled in file",
            DeprecationWarning
        )

        local("cp %s %s" % (from_location, to_location))

    def link_file(self, from_location, to_location):

        warnings.warn(
            "Should be handled in file",
            DeprecationWarning
        )

        local("sudo ln -s %s %s" % (from_location, to_location))

    def copy_all(self, from_location, to_location):

        warnings.warn(
            "Should be handled in file",
            DeprecationWarning
        )

        local("cp -r %s. %s" % (from_location, to_location))

    def configure_apache(self, application):

        warnings.warn(
            "Should be handled in plugins",
            DeprecationWarning
        )

        self.copy_file(
            application['apache_config']['copy_from'],
            application['apache_config']['copy_to'],
        )

        self.link_file(
            application['apache_config']['copy_to'],
            application['apache_config']['symlink'],
        )

class RemoteApplication(Application):

    def __init__(self, Environment):

        super(self.__class__, self).__init__(Environment)

    def configure_virtual_environment(self, application):

        super(self.__class__, self).configure_virtual_environment(application)

        run(application['virtual_environment']['create_cmd'] + " " + application['virtual_environment']['library_container'])

    def install_application_from_repo(self, application, directories):

        super(self.__class__, self).install_application_from_repo(application, directories)

        branch = application['repository']['branch']

        # Pull the code
        run("git clone %s %s" % (application['repository']['url'], directories['application']['path']))

        if branch is not False:

            with cd(directories['application']['path']):
                run("git checkout %s" % branch)

    def install_libraries(self, application, directories):
        super(self.__class__, self).install_libraries(application, directories)

        with cd(directories['application']['path']):
            run("%s install -r %s" % (application['package_manager']['install_cmd'], application['package_manager']['package_list_file']))

    def apache_server_setup(self, files):

        print("\n## Apache setup\n")

        run("cp %s %s" % (files['config_copy_from'], files['config_copy_to']))

        sudo("sudo ln -s %s %s" % (files['config_copy_to'], files['config_symlink']))

        # TODO: Restart apache here