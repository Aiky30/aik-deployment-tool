import warnings

from fabric.api import local, lcd


from aik_deployment_tool.enviroment import Environment


class LocalService(object):

    service_list = {}

    def __init__(self, Environment):

        print("service init: ", self, Environment.environment)

    def find_service_from_label(self, label):
    #TODO: Should
        pass

    def register_services(self, services):

        warnings.warn(
            "Services should now be registered when initialised",
            PendingDeprecationWarning
        )

        self.service_list = services

    def register_plugin_services(self, plugin):

        if 'services' in plugin:
            self.service_list.append(plugin['services'])

    def restart_service(self, service_label):

        local(self.service_list[service_label]['restart_cmd'])

    def start_service(self, service_label):

        local(self.service_list[service_label]['start_cmd'])

    def run_service(self, service_label):

        local(self.service_list[service_label]['run_cmd'])

    def run_from_directory(self, service_label):

        with lcd(self.service_list[service_label]['run_from']):

            local(self.service_list[service_label]['run_cmd'])
