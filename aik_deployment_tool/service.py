import warnings

from fabric.api import local, sudo

#FIXME: Should be once version that uses operations!!!


class Service(object):

    def __init__(self, environment):
        self.service_list = {}
        self.environment = environment

    def register_service(self, service):
        self.service_list.update(service)


class LocalService(Service):

    def restart_service(self, service_label):
        local(self.service_list[service_label]['restart_cmd'])

    def start_service(self, service_label):
        local(self.service_list[service_label]['start_cmd'])


class RemoteService(Service):

    def restart_service(self, service_label):
        sudo(self.service_list[service_label]['restart_cmd'])

    def start_service(self, service_label):
        sudo(self.service_list[service_label]['start_cmd'])