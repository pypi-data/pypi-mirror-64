# -*- test-case-name: twisted.application.twist.test.test_twist -*-
# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.

"""
Run a Twisted application.
"""

import sys

from twisted.python.usage import UsageError
from ..service import Application, IService
from ..runner._exit import exit, ExitStatus
from ..runner._runner import Runner
from ._options import TwistOptions
from twisted.application.app import _exitWithSignal
from twisted.internet.interfaces import _ISupportsExitSignalCapturing



class Twist(object):
    """
    Run a Twisted application.
    """

    @staticmethod
    def options(argv):
        """
        Parse command line options.

        @param argv: Command line arguments.
        @type argv: L{list}

        @return: The parsed options.
        @rtype: L{TwistOptions}
        """
        options = TwistOptions()

        try:
            options.parseOptions(argv[1:])
        except UsageError as e:
            exit(ExitStatus.EX_USAGE, "Error: {}\n\n{}".format(e, options))

        return options


    @staticmethod
    def service(plugin, options):
        """
        Create the application service.

        @param plugin: The name of the plugin that implements the service
            application to run.
        @type plugin: L{str}

        @param options: Options to pass to the application.
        @type options: L{twisted.python.usage.Options}

        @return: The created application service.
        @rtype: L{IService}
        """
        service = plugin.makeService(options)
        application = Application(plugin.tapname)
        service.setServiceParent(application)

        return IService(application)


    @staticmethod
    def startService(reactor, service):
        """
        Start the application service.

        @param reactor: The reactor to run the service with.
        @type reactor: L{twisted.internet.interfaces.IReactorCore}

        @param service: The application service to run.
        @type service: L{IService}
        """
        service.startService()

        # Ask the reactor to stop the service before shutting down
        reactor.addSystemEventTrigger(
            "before", "shutdown", service.stopService
        )


    @staticmethod
    def run(twistOptions):
        """
        Run the application service.

        @param twistOptions: Command line options to convert to runner
            arguments.
        @type twistOptions: L{TwistOptions}
        """
        runner = Runner(
            reactor=twistOptions["reactor"],
            defaultLogLevel=twistOptions["logLevel"],
            logFile=twistOptions["logFile"],
            fileLogObserverFactory=twistOptions["fileLogObserverFactory"],
        )
        runner.run()
        reactor = twistOptions["reactor"]
        if _ISupportsExitSignalCapturing.providedBy(reactor):
            if reactor._exitSignal is not None:
                _exitWithSignal(reactor._exitSignal)


    @classmethod
    def main(cls, argv=sys.argv):
        """
        Executable entry point for L{Twist}.
        Processes options and run a twisted reactor with a service.

        @param argv: Command line arguments.
        @type argv: L{list}
        """
        options = cls.options(argv)

        reactor = options["reactor"]
        service = cls.service(
            plugin=options.plugins[options.subCommand],
            options=options.subOptions,
        )

        cls.startService(reactor, service)
        cls.run(options)
