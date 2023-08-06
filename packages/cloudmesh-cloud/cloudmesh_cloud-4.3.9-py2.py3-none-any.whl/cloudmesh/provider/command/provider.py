from pprint import pprint

from cloudmesh.common.util import banner
from cloudmesh.provider import ComputeProviderPlugin
from cloudmesh.provider import Provider as ProviderList
from cloudmesh.shell.command import PluginCommand
from cloudmesh.shell.command import command, map_parameters


class ProviderCommand(PluginCommand):

    # see https://github.com/cloudmesh/client/blob/master/cloudmesh_client/shell/plugins/KeyCommand.py
    # see https://github.com/cloudmesh/client/blob/master/cloudmesh_client/shell/plugins/AkeyCommand.py

    # noinspection PyUnusedLocal
    @command
    def do_provider(self, args, arguments):
        """
        ::

           Usage:
             provider list [--output=OUTPUT]
             provider delete NAME
             provider add NAME

           Arguments:
             NAME           The name of the key.

           Options:
              --output=OUTPUT               the format of the output [default: table]


           Description:

                THIS IS NOT YET IMPLEMENTED

                Managing the providers
        """

        map_parameters(arguments, 'output')

        if arguments.list:

            banner("Loaded Compute Providers")

            providers = ComputeProviderPlugin.__subclasses__()

            for provider in providers:
                print(provider.kind)
                pprint(provider)

            banner("Available Compute Providers")

            providers = ProviderList()

            for name in ["openstack",
                         "azure"]:
                try:
                    provider = providers[name]
                    print(name)
                except Exception as e:
                    print(e)
        elif arguments.delete:
            raise NotImplementedError

        elif arguments.add:
            raise NotImplementedError

        return ""
