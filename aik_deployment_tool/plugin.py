from fabric.api import prompt

#FIXME: Teh python and javascript sections contain project specific instructions, this is very bad

class Plugin(object):

    def __init__(self, environment, plugin_config):

        self.environment = environment
        self.plugin_config = plugin_config

    def install(self):

        if 'directories' in self.plugin_config:
            directory_instance = self.environment.directory
            directory_instance.build_directories(self.plugin_config['directories'])

    def process_actions(self):

        operation_instance = self.environment.operation

        actions = self.plugin_config['actions']

        if 'copy_file' in actions:
            for action in actions['copy_file']:
                operation_instance.copy_file(action['source'], action['destination'])

        if 'copy_all' in actions:
            for action in actions['copy_all']:
                operation_instance.copy_all(action['source'], action['destination'])

        if 'sym_link' in actions:
            for action in actions['sym_link']:
                operation_instance.link_file(action['source'], action['destination'])

    def remove(self):

        if 'directories' in self.plugin_config:
            directory_instance = self.environment.directory
            directory_instance.destroy_directories(self.plugin_config['directories'])

        if 'files' in self.plugin_config:
            file_instance = self.environment.file
            file_instance.destroy_files(self.plugin_config['files'])


class ApachePlugin(Plugin):

    def install(self):

        super(self.__class__, self).install()

class PythonPlugin(Plugin):

    def install(self):

        super(self.__class__, self).install()

        # Configure virtual environment
        self.configure_virtual_environment()

        # Get the source from the repository
        self.get_from_repository()

        # Install libraries
        self.install_libraries()

    def update(self):

        # Get the updated source from the repository
        self.update_from_repository()

        # Install libraries
        self.install_libraries()

    def configure_virtual_environment(self):

        virtual_environment = self.plugin_config['virtual_environment']

        self.environment.operation.run(
            virtual_environment['create_cmd'] + " " + virtual_environment['library_container']
        )

    def install_libraries(self):

        packages = self.plugin_config['pip_packages']

        self.environment.operation.run_from_directory(packages['run_from'], packages['run_cmd'])

    def get_from_repository(self):

        # If a source exists copy from that
        if 'source' in self.plugin_config:

            source = self.plugin_config['source']

            file_instance = self.environment.file
            file_instance.copy_all(source['location'], source['destination'])

        # Otherwise use our cached version
        else:

            repository = self.plugin_config['repository']
            branch = repository['branch']

            self.environment.operation.run(
                "git clone %s %s" % (repository['url'], repository['destination'])
            )

            if branch is not False:
                self.environment.operation.run_from_directory(
                    repository['destination'], "git checkout %s" % branch
                )

    def update_from_repository(self):

        repository = self.plugin_config['repository']

        self.environment.operation.run_from_directory(
            repository['destination'], "git pull"
        )


class DjangoPlugin(Plugin):

    def collect_static_files(self):
        self.environment.operation.sudo_run(self.plugin_config['utilities']['collect_static']['run_cmd'])

    def make_migrations(self):
        self.environment.operation.sudo_run(self.plugin_config['utilities']['makemigrations']['run_cmd'])

    def run_migrations(self):
        self.environment.operation.sudo_run(self.plugin_config['utilities']['migrate']['run_cmd'])

    def run_development_server(self):
        self.environment.operation.sudo_run(self.plugin_config['utilities']['django_server']['run_cmd'])

    def run_management_command(self):

        command = self.plugin_config['utilities']['run_management_command']['run_cmd']

        answer = prompt('Enter a management command to execute')

        command = command.replace('PLACEHOLDER', answer)

        self.environment.operation.sudo_run(command)

    def test(self):
        self.environment.operation.sudo_run_from_directory(self.plugin_config['utilities']['test']['run_from'], self.plugin_config['utilities']['test']['run_cmd'])

    def generate_pip_package_list(self):
        self.environment.operation.sudo_run_from_directory(self.plugin_config['utilities']['generate_pip_package_list']['run_from'],
                                                           self.plugin_config['utilities']['generate_pip_package_list']['run_cmd'])

class GismohBackEndPlugin(Plugin):

    def import_data(self):

        utilities = self.plugin_config['utilities']

# FIXME: Too generic!!

        # Clean any previous imported data
        self.environment.operation.sudo_run(utilities['migrate-mrsa001_api-zero']['run_cmd'])

        # re-apply any migrations
        self.environment.operation.sudo_run(utilities['migrate-mrsa001_api']['run_cmd'])

        # Import the data
        self.environment.operation.sudo_run(utilities['data-import']['run_cmd'])


# Front end specific

class JavascriptPlugin(Plugin):

    def install(self):

        super(self.__class__, self).install()

        # Get the source from the repository
        self.get_from_repository()

    def update(self):

        # Get the updated source from the repository
        self.update_from_repository()

    def update_from_repository(self):

        repository = self.plugin_config['repository']

        self.environment.operation.run_from_directory(
            repository['destination'], "git pull"
        )

    def get_from_repository(self):

        # If a source exists copy from that
        if 'source' in self.plugin_config:

            source = self.plugin_config['source']

            file_instance = self.environment.file
            file_instance.copy_all(source['location'], source['destination'])

        # Otherwise use our cached version
        else:

            repository = self.plugin_config['repository']
            branch = repository['branch']

            self.environment.operation.run(
                "git clone %s %s" % (repository['url'], repository['destination'])
            )

            if branch is not False:
                self.environment.operation.run_from_directory(
                    repository['destination'], "git checkout %s" % branch
                )

class NodePlugin(Plugin):

    def install(self):

        super(self.__class__, self).install()

        # Install libraries
        self.install_libraries()

    def install_libraries(self):

        packages = self.plugin_config['utilities']['js_packages']

        self.environment.operation.run_from_directory(packages['run_from'], packages['run_cmd'])

    def run_development_server(self):

        server = self.plugin_config['utilities']['node_development_server']

        self.environment.operation.run_from_directory(
            server['run_from'], server['run_cmd']
        )

class GismohFrontEndPlugin(Plugin):

    def install(self):

        super(self.__class__, self).install()


class GismohFrontEndDistributionPlugin(Plugin):

    def prepare_distribution(self):

        packages = self.plugin_config['utilities']['create_distribution']

        self.environment.operation.run_from_directory(packages['run_from'], packages['run_cmd'])




