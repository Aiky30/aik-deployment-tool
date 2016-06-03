from fabric.api import local, lcd, cd, run, sudo


class Application(object):

    def __init__(self, Environment):

        print("application init: ", self, Environment.environment)


class LocalApplication(Application):

    def __init__(self, Environment):
        self.super(self, Environment)

    def configure_virtual_environment(self, application):

        local(application['virtual_environment']['create_cmd'] + " " + application['virtual_environment']['library_container'])

    def install_application_from_repo(self, application, directories):

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

    def install_libraries(self, application, directories):

        with lcd(directories['application']['path']):
            local("%s install -r %s" % (application['package_manager']['install_cmd'], application['package_manager']['package_list_file']))

class RemoteApplication(Application):

    def __init__(self, Environment):

        super(self.__class__, self).__init__(Environment)

    def configure_virtual_environment(self, application):

        run(application['virtual_environment']['create_cmd'] + " " + application['virtual_environment']['library_container'])

    def install_application_from_repo(self, application, directories):

        branch = application['repository']['branch']

        # Pull the code
        run("git clone %s %s" % (application['repository']['url'], directories['application']['path']))

        if branch is not False:

            with cd(directories['application']['path']):
                run("git checkout %s" % branch)

    def install_libraries(self, application, directories):

        with cd(directories['application']['path']):
            run("%s install -r %s" % (application['package_manager']['install_cmd'], application['package_manager']['package_list_file']))

    def apache_server_setup(self, files):

        print("\n## Apache setup\n")

        run("cp %s %s" % (files['config_copy_from'], files['config_copy_to']))

        sudo("sudo ln -s %s %s" % (files['config_copy_to'], files['config_symlink']))

        # TODO: Restart apache here