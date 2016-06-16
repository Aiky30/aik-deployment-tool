import warnings

from fabric.api import local, lcd

class LocalService(object):

    def __init__(self, environment):

        self.service_list = {}
        self.environment = environment

    def find_service_from_label(self, label):
    #TODO: Should
        pass

    def register_service(self, service):

        self.service_list.update(service)

    def restart_service(self, service_label):

        local(self.service_list[service_label]['restart_cmd'])

    def start_service(self, service_label):

        local(self.service_list[service_label]['start_cmd'])

