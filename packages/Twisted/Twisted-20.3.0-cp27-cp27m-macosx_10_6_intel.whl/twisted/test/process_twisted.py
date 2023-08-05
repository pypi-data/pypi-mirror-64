"""A process that reads from stdin and out using Twisted."""

from __future__ import division, absolute_import, print_function

### Twisted Preamble
# This makes sure that users don't have to set up their environment
# specially in order to run these programs from bin/.
import sys, os
pos = os.path.abspath(sys.argv[0]).find(os.sep+'Twisted')
if pos != -1:
    sys.path.insert(0, os.path.abspath(sys.argv[0])[:pos+8])
sys.path.insert(0, os.curdir)
### end of preamble


from twisted.python import log
from zope.interface import implementer
from twisted.internet import interfaces

log.startLogging(sys.stderr)

from twisted.internet import protocol, reactor, stdio


@implementer(interfaces.IHalfCloseableProtocol)
class Echo(protocol.Protocol):

    def connectionMade(self):
        print("connection made")

    def dataReceived(self, data):
        self.transport.write(data)

    def readConnectionLost(self):
        print("readConnectionLost")
        self.transport.loseConnection()
    def writeConnectionLost(self):
        print("writeConnectionLost")

    def connectionLost(self, reason):
        print("connectionLost", reason)
        reactor.stop()

stdio.StandardIO(Echo())
reactor.run()
