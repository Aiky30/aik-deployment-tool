

class Plugin(object):

    def __init__(self, environment, plugin_config):

        self.environment = environment
        self.plugin_config = plugin_config

    def install(self):

        if 'directories' in self.plugin_config:
            directory_instance = self.environment.directory
            directory_instance.build_directories(self.plugin_config['directories'])

    def remove(self):

        if 'directories' in self.plugin_config:
            directory_instance = self.environment.directory
            directory_instance.destroy_directories(self.plugin_config['directories'])

        if 'files' in self.plugin_config:
            file_instance = self.environment.file
            file_instance.destroy_files(self.plugin_config['files'])


class ApachePlugin(Plugin):

    def configure(self):

        file_instance = self.environment.file
        config = self.plugin_config['config']

        file_instance.copy_file(
            config['copy_from'],
            config['copy_to'],
        )

        file_instance.link_file(
            config['copy_to'],
            config['symlink'],
        )


class PythonPlugin(Plugin):

    def install(self):

        super(self.__class__, self).install()

        # Configure virtual environment
        self.configure_virtual_environment()

        # Get the source from the repository
        self.get_from_repository()

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


class DjangoPlugin(Plugin):

    def collect_static_files(self):

        self.environment.operation.run(self.plugin_config['utilities']['collect_static']['run_cmd'])

    def run_migrations(self):

        self.environment.operation.run(self.plugin_config['utilities']['migrate']['run_cmd'])

    def run_development_server(self):

        self.environment.operation.run(self.plugin_config['utilities']['django_server']['start_cmd'])

class GismohBackEndPlugin(Plugin):

    def copy_data(self):

        gismoh_data = self.plugin_config['gismoh_data']
        file_instance = self.environment.file

        file_instance.copy_all(gismoh_data['copy_from'], gismoh_data['copy_to'])

    def import_data(self):

        utilities = self.plugin_config['utilities']

        # Clean any previous imported data
        self.environment.operation.run(utilities['migrate-mrsa001_api-zero']['run_cmd'])

        # re-apply any migrations
        self.environment.operation.run(utilities['migrate-mrsa001_api']['run_cmd'])

        # Import the data
        self.environment.operation.run(utilities['data-import']['run_cmd'])


# Front end specific

class JavascriptPlugin(Plugin):

    def install(self):

        super(self.__class__, self).install()

        # Get the source from the repository
        self.get_from_repository()

        # Install libraries
        self.install_libraries()

    def install_libraries(self):

        packages = self.plugin_config['js_packages']

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


class NodePlugin(Plugin):

    def run_development_server(self):

        server = self.plugin_config['utilities']['node_development_server']

        self.environment.operation.run_from_directory(
            server['run_from'], server['run_cmd']
        )

class GismohFrontEndPlugin(Plugin):

    def copy_config(self):

        gismoh_config = self.plugin_config['gismoh_config']
        file_instance = self.environment.file

        file_instance.copy_file(gismoh_config['copy_from'], gismoh_config['copy_to'])