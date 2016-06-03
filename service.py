from fabric.api import local

from aik_deployment_tool.enviroment import Environment


class Service(Environment):

    service_list = {}

    def __init__(self, Environment):

        print("service init: ", self, Environment.environment)

    def find_service_from_label(self, label):
    #TODO: Should
        pass

    def register_services(self, services):

        self.service_list = services

    def restart_service(self, service_label):

        local(self.service_list[service_label]['restart_cmd'])

    def start_service(self, service_label):

        local(self.service_list[service_label]['start_cmd'])
