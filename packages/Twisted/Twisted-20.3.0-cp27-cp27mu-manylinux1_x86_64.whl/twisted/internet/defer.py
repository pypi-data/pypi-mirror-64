# -*- test-case-name: twisted.test.test_defer -*-
# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.

"""
Support for results that aren't immediately available.

Maintainer: Glyph Lefkowitz

@var _NO_RESULT: The result used to represent the fact that there is no
    result. B{Never ever ever use this as an actual result for a Deferred}.  You
    have been warned.

@var _CONTINUE: A marker left in L{Deferred.callback}s to indicate a Deferred
    chain.  Always accompanied by a Deferred instance in the args tuple pointing
    at the Deferred which is chained to the Deferred which has this marker.
"""

from __future__ import division, absolute_import, print_function

import attr
import traceback
import types
import warnings
from sys import exc_info, version_info
from functools import wraps
from incremental import Version

# Twisted imports
from twisted.python.compat import cmp, comparable
from twisted.python import lockfile, failure
from twisted.logger import Logger
from twisted.python.deprecate import warnAboutFunction, deprecated
from twisted.python._oldstyle import _oldStyle

log = Logger()


class AlreadyCalledError(Exception):
    pass



class CancelledError(Exception):
    """
    This error is raised by default when a L{Deferred} is cancelled.
    """


class TimeoutError(Exception):
    """
    This error is raised by default when a L{Deferred} times out.
    """



def logError(err):
    """
    Log and return failure.

    This method can be used as an errback that passes the failure on to the
    next errback unmodified. Note that if this is the last errback, and the
    deferred gets garbage collected after being this errback has been called,
    the clean up code logs it again.
    """
    log.failure(None, err)
    return err



def succeed(result):
    """
    Return a L{Deferred} that has already had C{.callback(result)} called.

    This is useful when you're writing synchronous code to an
    asynchronous interface: i.e., some code is calling you expecting a
    L{Deferred} result, but you don't actually need to do anything
    asynchronous. Just return C{defer.succeed(theResult)}.

    See L{fail} for a version of this function that uses a failing
    L{Deferred} rather than a successful one.

    @param result: The result to give to the Deferred's 'callback'
           method.

    @rtype: L{Deferred}
    """
    d = Deferred()
    d.callback(result)
    return d



def fail(result=None):
    """
    Return a L{Deferred} that has already had C{.errback(result)} called.

    See L{succeed}'s docstring for rationale.

    @param result: The same argument that L{Deferred.errback} takes.

    @raise NoCurrentExceptionError: If C{result} is L{None} but there is no
        current exception state.

    @rtype: L{Deferred}
    """
    d = Deferred()
    d.errback(result)
    return d



def execute(callable, *args, **kw):
    """
    Create a L{Deferred} from a callable and arguments.

    Call the given function with the given arguments.  Return a L{Deferred}
    which has been fired with its callback as the result of that invocation
    or its C{errback} with a L{Failure} for the exception thrown.
    """
    try:
        result = callable(*args, **kw)
    except:
        return fail()
    else:
        return succeed(result)



def maybeDeferred(f, *args, **kw):
    """
    Invoke a function that may or may not return a L{Deferred}.

    Call the given function with the given arguments.  If the returned
    object is a L{Deferred}, return it.  If the returned object is a L{Failure},
    wrap it with L{fail} and return it.  Otherwise, wrap it in L{succeed} and
    return it.  If an exception is raised, convert it to a L{Failure}, wrap it
    in L{fail}, and then return it.

    @type f: Any callable
    @param f: The callable to invoke

    @param args: The arguments to pass to C{f}
    @param kw: The keyword arguments to pass to C{f}

    @rtype: L{Deferred}
    @return: The result of the function call, wrapped in a L{Deferred} if
    necessary.
    """
    try:
        result = f(*args, **kw)
    except:
        return fail(failure.Failure(captureVars=Deferred.debug))

    if isinstance(result, Deferred):
        return result
    elif isinstance(result, failure.Failure):
        return fail(result)
    else:
        return succeed(result)



@deprecated(Version('Twisted', 17, 1, 0),
            replacement='twisted.internet.defer.Deferred.addTimeout')
def timeout(deferred):
    deferred.errback(failure.Failure(TimeoutError("Callback timed out")))



def passthru(arg):
    return arg



def setDebugging(on):
    """
    Enable or disable L{Deferred} debugging.

    When debugging is on, the call stacks from creation and invocation are
    recorded, and added to any L{AlreadyCalledError}s we raise.
    """
    Deferred.debug=bool(on)



def getDebugging():
    """
    Determine whether L{Deferred} debugging is enabled.
    """
    return Deferred.debug


# See module docstring.
_NO_RESULT = object()
_CONTINUE = object()



@_oldStyle
class Deferred:
    """
    This is a callback which will be put off until later.

    Why do we want this? Well, in cases where a function in a threaded
    program would block until it gets a result, for Twisted it should
    not block. Instead, it should return a L{Deferred}.

    This can be implemented for protocols that run over the network by
    writing an asynchronous protocol for L{twisted.internet}. For methods
    that come from outside packages that are not under our control, we use
    threads (see for example L{twisted.enterprise.adbapi}).

    For more information about Deferreds, see doc/core/howto/defer.html or
    U{http://twistedmatrix.com/documents/current/core/howto/defer.html}

    When creating a Deferred, you may provide a canceller function, which
    will be called by d.cancel() to let you do any clean-up necessary if the
    user decides not to wait for the deferred to complete.

    @ivar called: A flag which is C{False} until either C{callback} or
        C{errback} is called and afterwards always C{True}.
    @type called: L{bool}

    @ivar paused: A counter of how many unmatched C{pause} calls have been made
        on this instance.
    @type paused: L{int}

    @ivar _suppressAlreadyCalled: A flag used by the cancellation mechanism
        which is C{True} if the Deferred has no canceller and has been
        cancelled, C{False} otherwise.  If C{True}, it can be expected that
        C{callback} or C{errback} will eventually be called and the result
        should be silently discarded.
    @type _suppressAlreadyCalled: L{bool}

    @ivar _runningCallbacks: A flag which is C{True} while this instance is
        executing its callback chain, used to stop recursive execution of
        L{_runCallbacks}
    @type _runningCallbacks: L{bool}

    @ivar _chainedTo: If this L{Deferred} is waiting for the result of another
        L{Deferred}, this is a reference to the other Deferred.  Otherwise,
        L{None}.
    """

    called = False
    paused = False
    _debugInfo = None
    _suppressAlreadyCalled = False

    # Are we currently running a user-installed callback?  Meant to prevent
    # recursive running of callbacks when a reentrant call to add a callback is
    # used.
    _runningCallbacks = False

    # Keep this class attribute for now, for compatibility with code that
    # sets it directly.
    debug = False

    _chainedTo = None

    def __init__(self, canceller=None):
        """
        Initialize a L{Deferred}.

        @param canceller: a callable used to stop the pending operation
            scheduled by this L{Deferred} when L{Deferred.cancel} is
            invoked. The canceller will be passed the deferred whose
            cancelation is requested (i.e., self).

            If a canceller is not given, or does not invoke its argument's
            C{callback} or C{errback} method, L{Deferred.cancel} will
            invoke L{Deferred.errback} with a L{CancelledError}.

            Note that if a canceller is not given, C{callback} or
            C{errback} may still be invoked exactly once, even though
            defer.py will have already invoked C{errback}, as described
            above.  This allows clients of code which returns a L{Deferred}
            to cancel it without requiring the L{Deferred} instantiator to
            provide any specific implementation support for cancellation.
            New in 10.1.

        @type canceller: a 1-argument callable which takes a L{Deferred}. The
            return result is ignored.
        """
        self.callbacks = []
        self._canceller = canceller
        if self.debug:
            self._debugInfo = DebugInfo()
            self._debugInfo.creator = traceback.format_stack()[:-1]


    def addCallbacks(self, callback, errback=None,
                     callbackArgs=None, callbackKeywords=None,
                     errbackArgs=None, errbackKeywords=None):
        """
        Add a pair of callbacks (success and error) to this L{Deferred}.

        These will be executed when the 'master' callback is run.

        @return: C{self}.
        @rtype: a L{Deferred}
        """
        assert callable(callback)
        assert errback is None or callable(errback)
        cbs = ((callback, callbackArgs, callbackKeywords),
               (errback or (passthru), errbackArgs, errbackKeywords))
        self.callbacks.append(cbs)

        if self.called:
            self._runCallbacks()
        return self


    def addCallback(self, callback, *args, **kw):
        """
        Convenience method for adding just a callback.

        See L{addCallbacks}.
        """
        return self.addCallbacks(callback, callbackArgs=args,
                                 callbackKeywords=kw)


    def addErrback(self, errback, *args, **kw):
        """
        Convenience method for adding just an errback.

        See L{addCallbacks}.
        """
        return self.addCallbacks(passthru, errback,
                                 errbackArgs=args,
                                 errbackKeywords=kw)


    def addBoth(self, callback, *args, **kw):
        """
        Convenience method for adding a single callable as both a callback
        and an errback.

        See L{addCallbacks}.
        """
        return self.addCallbacks(callback, callback,
                                 callbackArgs=args, errbackArgs=args,
                                 callbackKeywords=kw, errbackKeywords=kw)


    def addTimeout(self, timeout, clock, onTimeoutCancel=None):
        """
        Time out this L{Deferred} by scheduling it to be cancelled after
        C{timeout} seconds.

        The timeout encompasses all the callbacks and errbacks added to this
        L{defer.Deferred} before the call to L{addTimeout}, and none added
        after the call.

        If this L{Deferred} gets timed out, it errbacks with a L{TimeoutError},
        unless a cancelable function was passed to its initialization or unless
        a different C{onTimeoutCancel} callable is provided.

        @param timeout: number of seconds to wait before timing out this
            L{Deferred}
        @type timeout: L{int}

        @param clock: The object which will be used to schedule the timeout.
        @type clock: L{twisted.internet.interfaces.IReactorTime}

        @param onTimeoutCancel: A callable which is called immediately after
            this L{Deferred} times out, and not if this L{Deferred} is
            otherwise cancelled before the timeout. It takes an arbitrary
            value, which is the value of this L{Deferred} at that exact point
            in time (probably a L{CancelledError} L{Failure}), and the
            C{timeout}.  The default callable (if none is provided) will
            translate a L{CancelledError} L{Failure} into a L{TimeoutError}.
        @type onTimeoutCancel: L{callable}

        @return: C{self}.
        @rtype: a L{Deferred}

        @since: 16.5
        """
        timedOut = [False]

        def timeItOut():
            timedOut[0] = True
            self.cancel()

        delayedCall = clock.callLater(timeout, timeItOut)

        def convertCancelled(value):
            # if C{deferred} was timed out, call the translation function,
            # if provdied, otherwise just use L{cancelledToTimedOutError}
            if timedOut[0]:
                toCall = onTimeoutCancel or _cancelledToTimedOutError
                return toCall(value, timeout)
            return value

        self.addBoth(convertCancelled)

        def cancelTimeout(result):
            # stop the pending call to cancel the deferred if it's been fired
            if delayedCall.active():
                delayedCall.cancel()
            return result

        self.addBoth(cancelTimeout)
        return self


    def chainDeferred(self, d):
        """
        Chain another L{Deferred} to this L{Deferred}.

        This method adds callbacks to this L{Deferred} to call C{d}'s callback
        or errback, as appropriate. It is merely a shorthand way of performing
        the following::

            self.addCallbacks(d.callback, d.errback)

        When you chain a deferred d2 to another deferred d1 with
        d1.chainDeferred(d2), you are making d2 participate in the callback
        chain of d1. Thus any event that fires d1 will also fire d2.
        However, the converse is B{not} true; if d2 is fired d1 will not be
        affected.

        Note that unlike the case where chaining is caused by a L{Deferred}
        being returned from a callback, it is possible to cause the call
        stack size limit to be exceeded by chaining many L{Deferred}s
        together with C{chainDeferred}.

        @return: C{self}.
        @rtype: a L{Deferred}
        """
        d._chainedTo = self
        return self.addCallbacks(d.callback, d.errback)


    def callback(self, result):
        """
        Run all success callbacks that have been added to this L{Deferred}.

        Each callback will have its result passed as the first argument to
        the next; this way, the callbacks act as a 'processing chain'.  If
        the success-callback returns a L{Failure} or raises an L{Exception},
        processing will continue on the *error* callback chain.  If a
        callback (or errback) returns another L{Deferred}, this L{Deferred}
        will be chained to it (and further callbacks will not run until that
        L{Deferred} has a result).

        An instance of L{Deferred} may only have either L{callback} or
        L{errback} called on it, and only once.

        @param result: The object which will be passed to the first callback
            added to this L{Deferred} (via L{addCallback}).

        @raise AlreadyCalledError: If L{callback} or L{errback} has already been
            called on this L{Deferred}.
        """
        assert not isinstance(result, Deferred)
        self._startRunCallbacks(result)


    def errback(self, fail=None):
        """
        Run all error callbacks that have been added to this L{Deferred}.

        Each callback will have its result passed as the first
        argument to the next; this way, the callbacks act as a
        'processing chain'. Also, if the error-callback returns a non-Failure
        or doesn't raise an L{Exception}, processing will continue on the
        *success*-callback chain.

        If the argument that's passed to me is not a L{failure.Failure} instance,
        it will be embedded in one. If no argument is passed, a
        L{failure.Failure} instance will be created based on the current
        traceback stack.

        Passing a string as `fail' is deprecated, and will be punished with
        a warning message.

        An instance of L{Deferred} may only have either L{callback} or
        L{errback} called on it, and only once.

        @param fail: The L{Failure} object which will be passed to the first
            errback added to this L{Deferred} (via L{addErrback}).
            Alternatively, a L{Exception} instance from which a L{Failure} will
            be constructed (with no traceback) or L{None} to create a L{Failure}
            instance from the current exception state (with a traceback).

        @raise AlreadyCalledError: If L{callback} or L{errback} has already been
            called on this L{Deferred}.

        @raise NoCurrentExceptionError: If C{fail} is L{None} but there is
            no current exception state.
        """
        if fail is None:
            fail = failure.Failure(captureVars=self.debug)
        elif not isinstance(fail, failure.Failure):
            fail = failure.Failure(fail)

        self._startRunCallbacks(fail)


    def pause(self):
        """
        Stop processing on a L{Deferred} until L{unpause}() is called.
        """
        self.paused = self.paused + 1


    def unpause(self):
        """
        Process all callbacks made since L{pause}() was called.
        """
        self.paused = self.paused - 1
        if self.paused:
            return
        if self.called:
            self._runCallbacks()


    def cancel(self):
        """
        Cancel this L{Deferred}.

        If the L{Deferred} has not yet had its C{errback} or C{callback} method
        invoked, call the canceller function provided to the constructor. If
        that function does not invoke C{callback} or C{errback}, or if no
        canceller function was provided, errback with L{CancelledError}.

        If this L{Deferred} is waiting on another L{Deferred}, forward the
        cancellation to the other L{Deferred}.
        """
        if not self.called:
            canceller = self._canceller
            if canceller:
                canceller(self)
            else:
                # Arrange to eat the callback that will eventually be fired
                # since there was no real canceller.
                self._suppressAlreadyCalled = True
            if not self.called:
                # There was no canceller, or the canceller didn't call
                # callback or errback.
                self.errback(failure.Failure(CancelledError()))
        elif isinstance(self.result, Deferred):
            # Waiting for another deferred -- cancel it instead.
            self.result.cancel()


    def _startRunCallbacks(self, result):
        if self.called:
            if self._suppressAlreadyCalled:
                self._suppressAlreadyCalled = False
                return
            if self.debug:
                if self._debugInfo is None:
                    self._debugInfo = DebugInfo()
                extra = "\n" + self._debugInfo._getDebugTracebacks()
                raise AlreadyCalledError(extra)
            raise AlreadyCalledError
        if self.debug:
            if self._debugInfo is None:
                self._debugInfo = DebugInfo()
            self._debugInfo.invoker = traceback.format_stack()[:-2]
        self.called = True
        self.result = result
        self._runCallbacks()


    def _continuation(self):
        """
        Build a tuple of callback and errback with L{_CONTINUE}.
        """
        return ((_CONTINUE, (self,), None),
                (_CONTINUE, (self,), None))


    def _runCallbacks(self):
        """
        Run the chain of callbacks once a result is available.

        This consists of a simple loop over all of the callbacks, calling each
        with the current result and making the current result equal to the
        return value (or raised exception) of that call.

        If L{_runningCallbacks} is true, this loop won't run at all, since
        it is already running above us on the call stack.  If C{self.paused} is
        true, the loop also won't run, because that's what it means to be
        paused.

        The loop will terminate before processing all of the callbacks if a
        L{Deferred} without a result is encountered.

        If a L{Deferred} I{with} a result is encountered, that result is taken
        and the loop proceeds.

        @note: The implementation is complicated slightly by the fact that
            chaining (associating two L{Deferred}s with each other such that one
            will wait for the result of the other, as happens when a Deferred is
            returned from a callback on another L{Deferred}) is supported
            iteratively rather than recursively, to avoid running out of stack
            frames when processing long chains.
        """
        if self._runningCallbacks:
            # Don't recursively run callbacks
            return

        # Keep track of all the Deferreds encountered while propagating results
        # up a chain.  The way a Deferred gets onto this stack is by having
        # added its _continuation() to the callbacks list of a second Deferred
        # and then that second Deferred being fired.  ie, if ever had _chainedTo
        # set to something other than None, you might end up on this stack.
        chain = [self]

        while chain:
            current = chain[-1]

            if current.paused:
                # This Deferred isn't going to produce a result at all.  All the
                # Deferreds up the chain waiting on it will just have to...
                # wait.
                return

            finished = True
            current._chainedTo = None
            while current.callbacks:
                item = current.callbacks.pop(0)
                callback, args, kw = item[
                    isinstance(current.result, failure.Failure)]
                args = args or ()
                kw = kw or {}

                # Avoid recursion if we can.
                if callback is _CONTINUE:
                    # Give the waiting Deferred our current result and then
                    # forget about that result ourselves.
                    chainee = args[0]
                    chainee.result = current.result
                    current.result = None
                    # Making sure to update _debugInfo
                    if current._debugInfo is not None:
                        current._debugInfo.failResult = None
                    chainee.paused -= 1
                    chain.append(chainee)
                    # Delay cleaning this Deferred and popping it from the chain
                    # until after we've dealt with chainee.
                    finished = False
                    break

                try:
                    current._runningCallbacks = True
                    try:
                        current.result = callback(current.result, *args, **kw)
                        if current.result is current:
                            warnAboutFunction(
                                callback,
                                "Callback returned the Deferred "
                                "it was attached to; this breaks the "
                                "callback chain and will raise an "
                                "exception in the future.")
                    finally:
                        current._runningCallbacks = False
                except:
                    # Including full frame information in the Failure is quite
                    # expensive, so we avoid it unless self.debug is set.
                    current.result = failure.Failure(captureVars=self.debug)
                else:
                    if isinstance(current.result, Deferred):
                        # The result is another Deferred.  If it has a result,
                        # we can take it and keep going.
                        resultResult = getattr(current.result, 'result', _NO_RESULT)
                        if resultResult is _NO_RESULT or isinstance(resultResult, Deferred) or current.result.paused:
                            # Nope, it didn't.  Pause and chain.
                            current.pause()
                            current._chainedTo = current.result
                            # Note: current.result has no result, so it's not
                            # running its callbacks right now.  Therefore we can
                            # append to the callbacks list directly instead of
                            # using addCallbacks.
                            current.result.callbacks.append(current._continuation())
                            break
                        else:
                            # Yep, it did.  Steal it.
                            current.result.result = None
                            # Make sure _debugInfo's failure state is updated.
                            if current.result._debugInfo is not None:
                                current.result._debugInfo.failResult = None
                            current.result = resultResult

            if finished:
                # As much of the callback chain - perhaps all of it - as can be
                # processed right now has been.  The current Deferred is waiting on
                # another Deferred or for more callbacks.  Before finishing with it,
                # make sure its _debugInfo is in the proper state.
                if isinstance(current.result, failure.Failure):
                    # Stash the Failure in the _debugInfo for unhandled error
                    # reporting.
                    current.result.cleanFailure()
                    if current._debugInfo is None:
                        current._debugInfo = DebugInfo()
                    current._debugInfo.failResult = current.result
                else:
                    # Clear out any Failure in the _debugInfo, since the result
                    # is no longer a Failure.
                    if current._debugInfo is not None:
                        current._debugInfo.failResult = None

                # This Deferred is done, pop it from the chain and move back up
                # to the Deferred which supplied us with our result.
                chain.pop()


    def __str__(self):
        """
        Return a string representation of this C{Deferred}.
        """
        cname = self.__class__.__name__
        result = getattr(self, 'result', _NO_RESULT)
        myID = id(self)
        if self._chainedTo is not None:
            result = ' waiting on Deferred at 0x%x' % (id(self._chainedTo),)
        elif result is _NO_RESULT:
            result = ''
        else:
            result = ' current result: %r' % (result,)
        return "<%s at 0x%x%s>" % (cname, myID, result)
    __repr__ = __str__


    def __iter__(self):
        return self


    @failure._extraneous
    def send(self, value=None):
        if self.paused:
            # If we're paused, we have no result to give
            return self

        result = getattr(self, 'result', _NO_RESULT)
        if result is _NO_RESULT:
            return self
        if isinstance(result, failure.Failure):
            # Clear the failure on debugInfo so it doesn't raise "unhandled
            # exception"
            self._debugInfo.failResult = None
            result.value.__failure__ = result
            raise result.value
        else:
            raise StopIteration(result)


    # For PEP-492 support (async/await)
    __await__ = __iter__
    __next__ = send


    def asFuture(self, loop):
        """
        Adapt a L{Deferred} into a L{asyncio.Future} which is bound to C{loop}.

        @note: converting a L{Deferred} to an L{asyncio.Future} consumes both
            its result and its errors, so this method implicitly converts
            C{self} into a L{Deferred} firing with L{None}, regardless of what
            its result previously would have been.

        @since: Twisted 17.5.0

        @param loop: The asyncio event loop to bind the L{asyncio.Future} to.
        @type loop: L{asyncio.AbstractEventLoop} or similar

        @param deferred: The Deferred to adapt.
        @type deferred: L{Deferred}

        @return: A Future which will fire when the Deferred fires.
        @rtype: L{asyncio.Future}
        """
        try:
            createFuture = loop.create_future
        except AttributeError:
            from asyncio import Future
            def createFuture():
                return Future(loop=loop)
        future = createFuture()
        def checkCancel(futureAgain):
            if futureAgain.cancelled():
                self.cancel()
        def maybeFail(failure):
            if not future.cancelled():
                future.set_exception(failure.value)
        def maybeSucceed(result):
            if not future.cancelled():
                future.set_result(result)
        self.addCallbacks(maybeSucceed, maybeFail)
        future.add_done_callback(checkCancel)
        return future


    @classmethod
    def fromFuture(cls, future):
        """
        Adapt an L{asyncio.Future} to a L{Deferred}.

        @note: This creates a L{Deferred} from a L{asyncio.Future}, I{not} from
            a C{coroutine}; in other words, you will need to call
            L{asyncio.ensure_future},
            L{asyncio.loop.create_task} or create an
            L{asyncio.Task} yourself to get from a C{coroutine} to a
            L{asyncio.Future} if what you have is an awaitable coroutine and
            not a L{asyncio.Future}.  (The length of this list of techniques is
            exactly why we have left it to the caller!)

        @since: Twisted 17.5.0

        @param future: The Future to adapt.
        @type future: L{asyncio.Future}

        @return: A Deferred which will fire when the Future fires.
        @rtype: L{Deferred}
        """
        def adapt(result):
            try:
                extracted = result.result()
            except:
                extracted = failure.Failure()
            adapt.actual.callback(extracted)
        futureCancel = object()
        def cancel(reself):
            future.cancel()
            reself.callback(futureCancel)
        self = cls(cancel)
        adapt.actual = self
        def uncancel(result):
            if result is futureCancel:
                adapt.actual = Deferred()
                return adapt.actual
            return result
        self.addCallback(uncancel)
        future.add_done_callback(adapt)
        return self



def _cancelledToTimedOutError(value, timeout):
    """
    A default translation function that translates L{Failure}s that are
    L{CancelledError}s to L{TimeoutError}s.

    @param value: Anything
    @type value: Anything

    @param timeout: The timeout
    @type timeout: L{int}

    @rtype: C{value}
    @raise: L{TimeoutError}

    @since: 16.5
    """
    if isinstance(value, failure.Failure):
        value.trap(CancelledError)
        raise TimeoutError(timeout, "Deferred")
    return value



def ensureDeferred(coro):
    """
    Schedule the execution of a coroutine that awaits/yields from L{Deferred}s,
    wrapping it in a L{Deferred} that will fire on success/failure of the
    coroutine. If a Deferred is passed to this function, it will be returned
    directly (mimicing C{asyncio}'s C{ensure_future} function).

    Coroutine functions return a coroutine object, similar to how generators
    work. This function turns that coroutine into a Deferred, meaning that it
    can be used in regular Twisted code. For example::

        import treq
        from twisted.internet.defer import ensureDeferred
        from twisted.internet.task import react

        async def crawl(pages):
            results = {}
            for page in pages:
                results[page] = await treq.content(await treq.get(page))
            return results

        def main(reactor):
            pages = [
                "http://localhost:8080"
            ]
            d = ensureDeferred(crawl(pages))
            d.addCallback(print)
            return d

        react(main)

    @param coro: The coroutine object to schedule, or a L{Deferred}.
    @type coro: A Python 3.5+ C{async def} C{coroutine}, a Python 3.4+
        C{yield from} using L{types.GeneratorType}, or a L{Deferred}.

    @rtype: L{Deferred}
    """
    from types import GeneratorType

    if version_info >= (3, 4, 0):
        from asyncio import iscoroutine

        if iscoroutine(coro) or isinstance(coro, GeneratorType):
            return _cancellableInlineCallbacks(coro)

    if not isinstance(coro, Deferred):
        raise ValueError("%r is not a coroutine or a Deferred" % (coro,))

    # Must be a Deferred
    return coro




@_oldStyle
class DebugInfo:
    """
    Deferred debug helper.
    """

    failResult = None

    def _getDebugTracebacks(self):
        info = ''
        if hasattr(self, "creator"):
            info += " C: Deferred was created:\n C:"
            info += "".join(self.creator).rstrip().replace("\n", "\n C:")
            info += "\n"
        if hasattr(self, "invoker"):
            info += " I: First Invoker was:\n I:"
            info += "".join(self.invoker).rstrip().replace("\n", "\n I:")
            info += "\n"
        return info


    def __del__(self):
        """
        Print tracebacks and die.

        If the *last* (and I do mean *last*) callback leaves me in an error
        state, print a traceback (if said errback is a L{Failure}).
        """
        if self.failResult is not None:
            # Note: this is two separate messages for compatibility with
            # earlier tests; arguably it should be a single error message.
            log.critical("Unhandled error in Deferred:",
                         isError=True)

            debugInfo = self._getDebugTracebacks()
            if debugInfo:
                format = "(debug: {debugInfo})"
            else:
                format = None

            log.failure(format,
                        self.failResult,
                        debugInfo=debugInfo)



@comparable
class FirstError(Exception):
    """
    First error to occur in a L{DeferredList} if C{fireOnOneErrback} is set.

    @ivar subFailure: The L{Failure} that occurred.
    @type subFailure: L{Failure}

    @ivar index: The index of the L{Deferred} in the L{DeferredList} where
        it happened.
    @type index: L{int}
    """
    def __init__(self, failure, index):
        Exception.__init__(self, failure, index)
        self.subFailure = failure
        self.index = index


    def __repr__(self):
        """
        The I{repr} of L{FirstError} instances includes the repr of the
        wrapped failure's exception and the index of the L{FirstError}.
        """
        return 'FirstError[#%d, %r]' % (self.index, self.subFailure.value)


    def __str__(self):
        """
        The I{str} of L{FirstError} instances includes the I{str} of the
        entire wrapped failure (including its traceback and exception) and
        the index of the L{FirstError}.
        """
        return 'FirstError[#%d, %s]' % (self.index, self.subFailure)


    def __cmp__(self, other):
        """
        Comparison between L{FirstError} and other L{FirstError} instances
        is defined as the comparison of the index and sub-failure of each
        instance.  L{FirstError} instances don't compare equal to anything
        that isn't a L{FirstError} instance.

        @since: 8.2
        """
        if isinstance(other, FirstError):
            return cmp(
                (self.index, self.subFailure),
                (other.index, other.subFailure))
        return -1



class DeferredList(Deferred):
    """
    L{DeferredList} is a tool for collecting the results of several Deferreds.

    This tracks a list of L{Deferred}s for their results, and makes a single
    callback when they have all completed.  By default, the ultimate result is a
    list of (success, result) tuples, 'success' being a boolean.
    L{DeferredList} exposes the same API that L{Deferred} does, so callbacks and
    errbacks can be added to it in the same way.

    L{DeferredList} is implemented by adding callbacks and errbacks to each
    L{Deferred} in the list passed to it.  This means callbacks and errbacks
    added to the Deferreds before they are passed to L{DeferredList} will change
    the result that L{DeferredList} sees (i.e., L{DeferredList} is not special).
    Callbacks and errbacks can also be added to the Deferreds after they are
    passed to L{DeferredList} and L{DeferredList} may change the result that
    they see.

    See the documentation for the C{__init__} arguments for more information.

    @ivar _deferredList: The L{list} of L{Deferred}s to track.
    """

    fireOnOneCallback = False
    fireOnOneErrback = False

    def __init__(self, deferredList, fireOnOneCallback=False,
                 fireOnOneErrback=False, consumeErrors=False):
        """
        Initialize a DeferredList.

        @param deferredList: The list of deferreds to track.
        @type deferredList:  L{list} of L{Deferred}s

        @param fireOnOneCallback: (keyword param) a flag indicating that this
            L{DeferredList} will fire when the first L{Deferred} in
            C{deferredList} fires with a non-failure result without waiting for
            any of the other Deferreds.  When this flag is set, the DeferredList
            will fire with a two-tuple: the first element is the result of the
            Deferred which fired; the second element is the index in
            C{deferredList} of that Deferred.
        @type fireOnOneCallback: L{bool}

        @param fireOnOneErrback: (keyword param) a flag indicating that this
            L{DeferredList} will fire when the first L{Deferred} in
            C{deferredList} fires with a failure result without waiting for any
            of the other Deferreds.  When this flag is set, if a Deferred in the
            list errbacks, the DeferredList will errback with a L{FirstError}
            failure wrapping the failure of that Deferred.
        @type fireOnOneErrback: L{bool}

        @param consumeErrors: (keyword param) a flag indicating that failures in
            any of the included L{Deferred}s should not be propagated to
            errbacks added to the individual L{Deferred}s after this
            L{DeferredList} is constructed.  After constructing the
            L{DeferredList}, any errors in the individual L{Deferred}s will be
            converted to a callback result of L{None}.  This is useful to
            prevent spurious 'Unhandled error in Deferred' messages from being
            logged.  This does not prevent C{fireOnOneErrback} from working.
        @type consumeErrors: L{bool}
        """
        self._deferredList = list(deferredList)
        self.resultList = [None] * len(self._deferredList)
        Deferred.__init__(self)
        if len(self._deferredList) == 0 and not fireOnOneCallback:
            self.callback(self.resultList)

        # These flags need to be set *before* attaching callbacks to the
        # deferreds, because the callbacks use these flags, and will run
        # synchronously if any of the deferreds are already fired.
        self.fireOnOneCallback = fireOnOneCallback
        self.fireOnOneErrback = fireOnOneErrback
        self.consumeErrors = consumeErrors
        self.finishedCount = 0

        index = 0
        for deferred in self._deferredList:
            deferred.addCallbacks(self._cbDeferred, self._cbDeferred,
                                  callbackArgs=(index,SUCCESS),
                                  errbackArgs=(index,FAILURE))
            index = index + 1


    def _cbDeferred(self, result, index, succeeded):
        """
        (internal) Callback for when one of my deferreds fires.
        """
        self.resultList[index] = (succeeded, result)

        self.finishedCount += 1
        if not self.called:
            if succeeded == SUCCESS and self.fireOnOneCallback:
                self.callback((result, index))
            elif succeeded == FAILURE and self.fireOnOneErrback:
                self.errback(failure.Failure(FirstError(result, index)))
            elif self.finishedCount == len(self.resultList):
                self.callback(self.resultList)

        if succeeded == FAILURE and self.consumeErrors:
            result = None

        return result


    def cancel(self):
        """
        Cancel this L{DeferredList}.

        If the L{DeferredList} hasn't fired yet, cancel every L{Deferred} in
        the list.

        If the L{DeferredList} has fired, including the case where the
        C{fireOnOneCallback}/C{fireOnOneErrback} flag is set and the
        L{DeferredList} fires because one L{Deferred} in the list fires with a
        non-failure/failure result, do nothing in the C{cancel} method.
        """
        if not self.called:
            for deferred in self._deferredList:
                try:
                    deferred.cancel()
                except:
                    log.failure(
                        "Exception raised from user supplied canceller"
                    )



def _parseDListResult(l, fireOnOneErrback=False):
    if __debug__:
        for success, value in l:
            assert success
    return [x[1] for x in l]



def gatherResults(deferredList, consumeErrors=False):
    """
    Returns, via a L{Deferred}, a list with the results of the given
    L{Deferred}s - in effect, a "join" of multiple deferred operations.

    The returned L{Deferred} will fire when I{all} of the provided L{Deferred}s
    have fired, or when any one of them has failed.

    This method can be cancelled by calling the C{cancel} method of the
    L{Deferred}, all the L{Deferred}s in the list will be cancelled.

    This differs from L{DeferredList} in that you don't need to parse
    the result for success/failure.

    @type deferredList:  L{list} of L{Deferred}s

    @param consumeErrors: (keyword param) a flag, defaulting to False,
        indicating that failures in any of the given L{Deferred}s should not be
        propagated to errbacks added to the individual L{Deferred}s after this
        L{gatherResults} invocation.  Any such errors in the individual
        L{Deferred}s will be converted to a callback result of L{None}.  This
        is useful to prevent spurious 'Unhandled error in Deferred' messages
        from being logged.  This parameter is available since 11.1.0.
    @type consumeErrors: L{bool}
    """
    d = DeferredList(deferredList, fireOnOneErrback=True,
                                   consumeErrors=consumeErrors)
    d.addCallback(_parseDListResult)
    return d



# Constants for use with DeferredList

SUCCESS = True
FAILURE = False



## deferredGenerator
@_oldStyle
class waitForDeferred:
    """
    See L{deferredGenerator}.
    """

    def __init__(self, d):
        warnings.warn(
            "twisted.internet.defer.waitForDeferred was deprecated in "
            "Twisted 15.0.0; please use twisted.internet.defer.inlineCallbacks "
            "instead", DeprecationWarning, stacklevel=2)

        if not isinstance(d, Deferred):
            raise TypeError("You must give waitForDeferred a Deferred. You gave it %r." % (d,))
        self.d = d


    def getResult(self):
        if isinstance(self.result, failure.Failure):
            self.result.raiseException()
        return self.result



def _deferGenerator(g, deferred):
    """
    See L{deferredGenerator}.
    """
    result = None

    # This function is complicated by the need to prevent unbounded recursion
    # arising from repeatedly yielding immediately ready deferreds.  This while
    # loop and the waiting variable solve that by manually unfolding the
    # recursion.

    waiting = [True, # defgen is waiting for result?
               None] # result

    while 1:
        try:
            result = next(g)
        except StopIteration:
            deferred.callback(result)
            return deferred
        except:
            deferred.errback()
            return deferred

        # Deferred.callback(Deferred) raises an error; we catch this case
        # early here and give a nicer error message to the user in case
        # they yield a Deferred.
        if isinstance(result, Deferred):
            return fail(TypeError("Yield waitForDeferred(d), not d!"))

        if isinstance(result, waitForDeferred):
            # a waitForDeferred was yielded, get the result.
            # Pass result in so it don't get changed going around the loop
            # This isn't a problem for waiting, as it's only reused if
            # gotResult has already been executed.
            def gotResult(r, result=result):
                result.result = r
                if waiting[0]:
                    waiting[0] = False
                    waiting[1] = r
                else:
                    _deferGenerator(g, deferred)
            result.d.addBoth(gotResult)
            if waiting[0]:
                # Haven't called back yet, set flag so that we get reinvoked
                # and return from the loop
                waiting[0] = False
                return deferred
            # Reset waiting to initial values for next loop
            waiting[0] = True
            waiting[1] = None

            result = None



@deprecated(Version('Twisted', 15, 0, 0),
            "twisted.internet.defer.inlineCallbacks")
def deferredGenerator(f):
    """
    L{deferredGenerator} and L{waitForDeferred} help you write
    L{Deferred}-using code that looks like a regular sequential function.
    Consider the use of L{inlineCallbacks} instead, which can accomplish
    the same thing in a more concise manner.

    There are two important functions involved: L{waitForDeferred}, and
    L{deferredGenerator}.  They are used together, like this::

        @deferredGenerator
        def thingummy():
            thing = waitForDeferred(makeSomeRequestResultingInDeferred())
            yield thing
            thing = thing.getResult()
            print(thing) #the result! hoorj!

    L{waitForDeferred} returns something that you should immediately yield; when
    your generator is resumed, calling C{thing.getResult()} will either give you
    the result of the L{Deferred} if it was a success, or raise an exception if it
    was a failure.  Calling C{getResult} is B{absolutely mandatory}.  If you do
    not call it, I{your program will not work}.

    L{deferredGenerator} takes one of these waitForDeferred-using generator
    functions and converts it into a function that returns a L{Deferred}. The
    result of the L{Deferred} will be the last value that your generator yielded
    unless the last value is a L{waitForDeferred} instance, in which case the
    result will be L{None}.  If the function raises an unhandled exception, the
    L{Deferred} will errback instead.  Remember that C{return result} won't work;
    use C{yield result; return} in place of that.

    Note that not yielding anything from your generator will make the L{Deferred}
    result in L{None}. Yielding a L{Deferred} from your generator is also an error
    condition; always yield C{waitForDeferred(d)} instead.

    The L{Deferred} returned from your deferred generator may also errback if your
    generator raised an exception.  For example::

        @deferredGenerator
        def thingummy():
            thing = waitForDeferred(makeSomeRequestResultingInDeferred())
            yield thing
            thing = thing.getResult()
            if thing == 'I love Twisted':
                # will become the result of the Deferred
                yield 'TWISTED IS GREAT!'
                return
            else:
                # will trigger an errback
                raise Exception('DESTROY ALL LIFE')

    Put succinctly, these functions connect deferred-using code with this 'fake
    blocking' style in both directions: L{waitForDeferred} converts from a
    L{Deferred} to the 'blocking' style, and L{deferredGenerator} converts from the
    'blocking' style to a L{Deferred}.
    """
    @wraps(f)
    def unwindGenerator(*args, **kwargs):
        return _deferGenerator(f(*args, **kwargs), Deferred())
    return unwindGenerator


## inlineCallbacks



class _DefGen_Return(BaseException):
    def __init__(self, value):
        self.value = value



def returnValue(val):
    """
    Return val from a L{inlineCallbacks} generator.

    Note: this is currently implemented by raising an exception
    derived from L{BaseException}.  You might want to change any
    'except:' clauses to an 'except Exception:' clause so as not to
    catch this exception.

    Also: while this function currently will work when called from
    within arbitrary functions called from within the generator, do
    not rely upon this behavior.
    """
    raise _DefGen_Return(val)



@attr.s
class _CancellationStatus(object):
    """
    Cancellation status of an L{inlineCallbacks} invocation.

    @ivar waitingOn: the L{Deferred} being waited upon (which
        L{_inlineCallbacks} must fill out before returning)

    @ivar deferred: the L{Deferred} to callback or errback when the generator
        invocation has finished.
    """

    deferred = attr.ib()
    waitingOn = attr.ib(default=None)



@failure._extraneous
def _inlineCallbacks(result, g, status):
    """
    Carry out the work of L{inlineCallbacks}.

    Iterate the generator produced by an C{@}L{inlineCallbacks}-decorated
    function, C{g}, C{send()}ing it the results of each value C{yield}ed by
    that generator, until a L{Deferred} is yielded, at which point a callback
    is added to that L{Deferred} to call this function again.

    @param result: The last result seen by this generator.  Note that this is
        never a L{Deferred} - by the time this function is invoked, the
        L{Deferred} has been called back and this will be a particular result
        at a point in its callback chain.

    @param g: a generator object returned by calling a function or method
        decorated with C{@}L{inlineCallbacks}

    @param status: a L{_CancellationStatus} tracking the current status of C{g}
    """
    # This function is complicated by the need to prevent unbounded recursion
    # arising from repeatedly yielding immediately ready deferreds.  This while
    # loop and the waiting variable solve that by manually unfolding the
    # recursion.

    waiting = [True, # waiting for result?
               None] # result

    while 1:
        try:
            # Send the last result back as the result of the yield expression.
            isFailure = isinstance(result, failure.Failure)
            if isFailure:
                result = result.throwExceptionIntoGenerator(g)
            else:
                result = g.send(result)
        except StopIteration as e:
            # fell off the end, or "return" statement
            status.deferred.callback(getattr(e, "value", None))
            return
        except _DefGen_Return as e:
            # returnValue() was called; time to give a result to the original
            # Deferred.  First though, let's try to identify the potentially
            # confusing situation which results when returnValue() is
            # accidentally invoked from a different function, one that wasn't
            # decorated with @inlineCallbacks.

            # The traceback starts in this frame (the one for
            # _inlineCallbacks); the next one down should be the application
            # code.
            appCodeTrace = exc_info()[2].tb_next
            if isFailure:
                # If we invoked this generator frame by throwing an exception
                # into it, then throwExceptionIntoGenerator will consume an
                # additional stack frame itself, so we need to skip that too.
                appCodeTrace = appCodeTrace.tb_next
            # Now that we've identified the frame being exited by the
            # exception, let's figure out if returnValue was called from it
            # directly.  returnValue itself consumes a stack frame, so the
            # application code will have a tb_next, but it will *not* have a
            # second tb_next.
            if appCodeTrace.tb_next.tb_next:
                # If returnValue was invoked non-local to the frame which it is
                # exiting, identify the frame that ultimately invoked
                # returnValue so that we can warn the user, as this behavior is
                # confusing.
                ultimateTrace = appCodeTrace
                while ultimateTrace.tb_next.tb_next:
                    ultimateTrace = ultimateTrace.tb_next
                filename = ultimateTrace.tb_frame.f_code.co_filename
                lineno = ultimateTrace.tb_lineno
                warnings.warn_explicit(
                    "returnValue() in %r causing %r to exit: "
                    "returnValue should only be invoked by functions decorated "
                    "with inlineCallbacks" % (
                        ultimateTrace.tb_frame.f_code.co_name,
                        appCodeTrace.tb_frame.f_code.co_name),
                    DeprecationWarning, filename, lineno)
            status.deferred.callback(e.value)
            return
        except:
            status.deferred.errback()
            return

        if isinstance(result, Deferred):
            # a deferred was yielded, get the result.
            def gotResult(r):
                if waiting[0]:
                    waiting[0] = False
                    waiting[1] = r
                else:
                    # We are not waiting for deferred result any more
                    _inlineCallbacks(r, g, status)

            result.addBoth(gotResult)
            if waiting[0]:
                # Haven't called back yet, set flag so that we get reinvoked
                # and return from the loop
                waiting[0] = False
                status.waitingOn = result
                return

            result = waiting[1]
            # Reset waiting to initial values for next loop.  gotResult uses
            # waiting, but this isn't a problem because gotResult is only
            # executed once, and if it hasn't been executed yet, the return
            # branch above would have been taken.

            waiting[0] = True
            waiting[1] = None



def _cancellableInlineCallbacks(g):
    """
    Make an C{@}L{inlineCallbacks} cancellable.

    @param g: a generator object returned by calling a function or method
        decorated with C{@}L{inlineCallbacks}

    @return: L{Deferred} for the C{@}L{inlineCallbacks} that is cancellable.
    """
    def cancel(it):
        it.callbacks, tmp = [], it.callbacks
        it.addErrback(handleCancel)
        it.callbacks.extend(tmp)
        it.errback(_InternalInlineCallbacksCancelledError())
    deferred = Deferred(cancel)
    status = _CancellationStatus(deferred)
    def handleCancel(result):
        """
        Propagate the cancellation of an C{@}L{inlineCallbacks} to the
        L{Deferred} it is waiting on.

        @param result: An L{_InternalInlineCallbacksCancelledError} from
            C{cancel()}.
        @return: A new L{Deferred} that the C{@}L{inlineCallback} generator
            can callback or errback through.
        """
        result.trap(_InternalInlineCallbacksCancelledError)
        status.deferred = Deferred(cancel)
        # We would only end up here if the inlineCallback is waiting on
        # another Deferred.  It needs to be cancelled.
        awaited = status.waitingOn
        awaited.cancel()
        return status.deferred
    _inlineCallbacks(None, g, status)
    return deferred



class _InternalInlineCallbacksCancelledError(Exception):
    """
    A unique exception used only in L{_cancellableInlineCallbacks} to verify
    that an L{inlineCallbacks} is being cancelled as expected.
    """



def inlineCallbacks(f):
    """
    L{inlineCallbacks} helps you write L{Deferred}-using code that looks like a
    regular sequential function. For example::

        @inlineCallbacks
        def thingummy():
            thing = yield makeSomeRequestResultingInDeferred()
            print(thing)  # the result! hoorj!

    When you call anything that results in a L{Deferred}, you can simply yield it;
    your generator will automatically be resumed when the Deferred's result is
    available. The generator will be sent the result of the L{Deferred} with the
    'send' method on generators, or if the result was a failure, 'throw'.

    Things that are not L{Deferred}s may also be yielded, and your generator
    will be resumed with the same object sent back. This means C{yield}
    performs an operation roughly equivalent to L{maybeDeferred}.

    Your inlineCallbacks-enabled generator will return a L{Deferred} object, which
    will result in the return value of the generator (or will fail with a
    failure object if your generator raises an unhandled exception). Note that
    you can't use C{return result} to return a value; use C{returnValue(result)}
    instead. Falling off the end of the generator, or simply using C{return}
    will cause the L{Deferred} to have a result of L{None}.

    Be aware that L{returnValue} will not accept a L{Deferred} as a parameter.
    If you believe the thing you'd like to return could be a L{Deferred}, do
    this::

        result = yield result
        returnValue(result)

    The L{Deferred} returned from your deferred generator may errback if your
    generator raised an exception::

        @inlineCallbacks
        def thingummy():
            thing = yield makeSomeRequestResultingInDeferred()
            if thing == 'I love Twisted':
                # will become the result of the Deferred
                returnValue('TWISTED IS GREAT!')
            else:
                # will trigger an errback
                raise Exception('DESTROY ALL LIFE')

    It is possible to use the C{return} statement instead of L{returnValue}::

        @inlineCallbacks
        def loadData(url):
            response = yield makeRequest(url)
            return json.loads(response)

    You can cancel the L{Deferred} returned from your L{inlineCallbacks}
    generator before it is fired by your generator completing (either by
    reaching its end, a C{return} statement, or by calling L{returnValue}).
    A C{CancelledError} will be raised from the C{yield}ed L{Deferred} that
    has been cancelled if that C{Deferred} does not otherwise suppress it.
    """
    @wraps(f)
    def unwindGenerator(*args, **kwargs):
        try:
            gen = f(*args, **kwargs)
        except _DefGen_Return:
            raise TypeError(
                "inlineCallbacks requires %r to produce a generator; instead"
                "caught returnValue being used in a non-generator" % (f,))
        if not isinstance(gen, types.GeneratorType):
            raise TypeError(
                "inlineCallbacks requires %r to produce a generator; "
                "instead got %r" % (f, gen))
        return _cancellableInlineCallbacks(gen)
    return unwindGenerator


## DeferredLock/DeferredQueue

class _ConcurrencyPrimitive(object):
    def __init__(self):
        self.waiting = []


    def _releaseAndReturn(self, r):
        self.release()
        return r


    def run(*args, **kwargs):
        """
        Acquire, run, release.

        This function takes a callable as its first argument and any
        number of other positional and keyword arguments.  When the
        lock or semaphore is acquired, the callable will be invoked
        with those arguments.

        The callable may return a L{Deferred}; if it does, the lock or
        semaphore won't be released until that L{Deferred} fires.

        @return: L{Deferred} of function result.
        """
        if len(args) < 2:
            if not args:
                raise TypeError("run() takes at least 2 arguments, none given.")
            raise TypeError("%s.run() takes at least 2 arguments, 1 given" % (
                args[0].__class__.__name__,))
        self, f = args[:2]
        args = args[2:]

        def execute(ignoredResult):
            d = maybeDeferred(f, *args, **kwargs)
            d.addBoth(self._releaseAndReturn)
            return d

        d = self.acquire()
        d.addCallback(execute)
        return d


    def __aenter__(self):
        """
        We can be used as an asynchronous context manager.
        """
        return self.acquire()


    def __aexit__(self, exc_type, exc_val, exc_tb):
        self.release()
        # We return False to indicate that we have not consumed the
        # exception, if any.
        return succeed(False)



class DeferredLock(_ConcurrencyPrimitive):
    """
    A lock for event driven systems.

    @ivar locked: C{True} when this Lock has been acquired, false at all other
        times.  Do not change this value, but it is useful to examine for the
        equivalent of a "non-blocking" acquisition.
    """

    locked = False


    def _cancelAcquire(self, d):
        """
        Remove a deferred d from our waiting list, as the deferred has been
        canceled.

        Note: We do not need to wrap this in a try/except to catch d not
        being in self.waiting because this canceller will not be called if
        d has fired. release() pops a deferred out of self.waiting and
        calls it, so the canceller will no longer be called.

        @param d: The deferred that has been canceled.
        """
        self.waiting.remove(d)


    def acquire(self):
        """
        Attempt to acquire the lock.  Returns a L{Deferred} that fires on
        lock acquisition with the L{DeferredLock} as the value.  If the lock
        is locked, then the Deferred is placed at the end of a waiting list.

        @return: a L{Deferred} which fires on lock acquisition.
        @rtype: a L{Deferred}
        """
        d = Deferred(canceller=self._cancelAcquire)
        if self.locked:
            self.waiting.append(d)
        else:
            self.locked = True
            d.callback(self)
        return d


    def release(self):
        """
        Release the lock.  If there is a waiting list, then the first
        L{Deferred} in that waiting list will be called back.

        Should be called by whomever did the L{acquire}() when the shared
        resource is free.
        """
        assert self.locked, "Tried to release an unlocked lock"
        self.locked = False
        if self.waiting:
            # someone is waiting to acquire lock
            self.locked = True
            d = self.waiting.pop(0)
            d.callback(self)



class DeferredSemaphore(_ConcurrencyPrimitive):
    """
    A semaphore for event driven systems.

    If you are looking into this as a means of limiting parallelism, you might
    find L{twisted.internet.task.Cooperator} more useful.

    @ivar limit: At most this many users may acquire this semaphore at
        once.
    @type limit: L{int}

    @ivar tokens: The difference between C{limit} and the number of users
        which have currently acquired this semaphore.
    @type tokens: L{int}
    """

    def __init__(self, tokens):
        """
        @param tokens: initial value of L{tokens} and L{limit}
        @type tokens: L{int}
        """
        _ConcurrencyPrimitive.__init__(self)
        if tokens < 1:
            raise ValueError("DeferredSemaphore requires tokens >= 1")
        self.tokens = tokens
        self.limit = tokens


    def _cancelAcquire(self, d):
        """
        Remove a deferred d from our waiting list, as the deferred has been
        canceled.

        Note: We do not need to wrap this in a try/except to catch d not
        being in self.waiting because this canceller will not be called if
        d has fired. release() pops a deferred out of self.waiting and
        calls it, so the canceller will no longer be called.

        @param d: The deferred that has been canceled.
        """
        self.waiting.remove(d)


    def acquire(self):
        """
        Attempt to acquire the token.

        @return: a L{Deferred} which fires on token acquisition.
        """
        assert self.tokens >= 0, "Internal inconsistency??  tokens should never be negative"
        d = Deferred(canceller=self._cancelAcquire)
        if not self.tokens:
            self.waiting.append(d)
        else:
            self.tokens = self.tokens - 1
            d.callback(self)
        return d


    def release(self):
        """
        Release the token.

        Should be called by whoever did the L{acquire}() when the shared
        resource is free.
        """
        assert self.tokens < self.limit, "Someone released me too many times: too many tokens!"
        self.tokens = self.tokens + 1
        if self.waiting:
            # someone is waiting to acquire token
            self.tokens = self.tokens - 1
            d = self.waiting.pop(0)
            d.callback(self)



class QueueOverflow(Exception):
    pass



class QueueUnderflow(Exception):
    pass



class DeferredQueue(object):
    """
    An event driven queue.

    Objects may be added as usual to this queue.  When an attempt is
    made to retrieve an object when the queue is empty, a L{Deferred} is
    returned which will fire when an object becomes available.

    @ivar size: The maximum number of objects to allow into the queue
    at a time.  When an attempt to add a new object would exceed this
    limit, L{QueueOverflow} is raised synchronously.  L{None} for no limit.

    @ivar backlog: The maximum number of L{Deferred} gets to allow at
    one time.  When an attempt is made to get an object which would
    exceed this limit, L{QueueUnderflow} is raised synchronously.  L{None}
    for no limit.
    """

    def __init__(self, size=None, backlog=None):
        self.waiting = []
        self.pending = []
        self.size = size
        self.backlog = backlog


    def _cancelGet(self, d):
        """
        Remove a deferred d from our waiting list, as the deferred has been
        canceled.

        Note: We do not need to wrap this in a try/except to catch d not
        being in self.waiting because this canceller will not be called if
        d has fired. put() pops a deferred out of self.waiting and calls
        it, so the canceller will no longer be called.

        @param d: The deferred that has been canceled.
        """
        self.waiting.remove(d)


    def put(self, obj):
        """
        Add an object to this queue.

        @raise QueueOverflow: Too many objects are in this queue.
        """
        if self.waiting:
            self.waiting.pop(0).callback(obj)
        elif self.size is None or len(self.pending) < self.size:
            self.pending.append(obj)
        else:
            raise QueueOverflow()


    def get(self):
        """
        Attempt to retrieve and remove an object from the queue.

        @return: a L{Deferred} which fires with the next object available in
        the queue.

        @raise QueueUnderflow: Too many (more than C{backlog})
        L{Deferred}s are already waiting for an object from this queue.
        """
        if self.pending:
            return succeed(self.pending.pop(0))
        elif self.backlog is None or len(self.waiting) < self.backlog:
            d = Deferred(canceller=self._cancelGet)
            self.waiting.append(d)
            return d
        else:
            raise QueueUnderflow()



class AlreadyTryingToLockError(Exception):
    """
    Raised when L{DeferredFilesystemLock.deferUntilLocked} is called twice on a
    single L{DeferredFilesystemLock}.
    """



class DeferredFilesystemLock(lockfile.FilesystemLock):
    """
    A L{FilesystemLock} that allows for a L{Deferred} to be fired when the lock is
    acquired.

    @ivar _scheduler: The object in charge of scheduling retries. In this
        implementation this is parameterized for testing.

    @ivar _interval: The retry interval for an L{IReactorTime} based scheduler.

    @ivar _tryLockCall: A L{DelayedCall} based on C{_interval} that will manage
        the next retry for acquiring the lock.

    @ivar _timeoutCall: A L{DelayedCall} based on C{deferUntilLocked}'s timeout
        argument.  This is in charge of timing out our attempt to acquire the
        lock.
    """
    _interval = 1
    _tryLockCall = None
    _timeoutCall = None


    def __init__(self, name, scheduler=None):
        """
        @param name: The name of the lock to acquire
        @param scheduler: An object which provides L{IReactorTime}
        """
        lockfile.FilesystemLock.__init__(self, name)

        if scheduler is None:
            from twisted.internet import reactor
            scheduler = reactor

        self._scheduler = scheduler


    def deferUntilLocked(self, timeout=None):
        """
        Wait until we acquire this lock.  This method is not safe for
        concurrent use.

        @type timeout: L{float} or L{int}
        @param timeout: the number of seconds after which to time out if the
            lock has not been acquired.

        @return: a L{Deferred} which will callback when the lock is acquired, or
            errback with a L{TimeoutError} after timing out or an
            L{AlreadyTryingToLockError} if the L{deferUntilLocked} has already
            been called and not successfully locked the file.
        """
        if self._tryLockCall is not None:
            return fail(
                AlreadyTryingToLockError(
                    "deferUntilLocked isn't safe for concurrent use."))

        def _cancelLock(reason):
            """
            Cancel a L{DeferredFilesystemLock.deferUntilLocked} call.

            @type reason: L{failure.Failure}
            @param reason: The reason why the call is cancelled.
            """
            self._tryLockCall.cancel()
            self._tryLockCall = None
            if self._timeoutCall is not None and self._timeoutCall.active():
                self._timeoutCall.cancel()
                self._timeoutCall = None

            if self.lock():
                d.callback(None)
            else:
                d.errback(reason)

        d = Deferred(lambda deferred: _cancelLock(CancelledError()))

        def _tryLock():
            if self.lock():
                if self._timeoutCall is not None:
                    self._timeoutCall.cancel()
                    self._timeoutCall = None

                self._tryLockCall = None

                d.callback(None)
            else:
                if timeout is not None and self._timeoutCall is None:
                    reason = failure.Failure(TimeoutError(
                        "Timed out acquiring lock: %s after %fs" % (
                            self.name,
                            timeout)))
                    self._timeoutCall = self._scheduler.callLater(
                        timeout, _cancelLock, reason)

                self._tryLockCall = self._scheduler.callLater(
                    self._interval, _tryLock)

        _tryLock()

        return d



__all__ = ["Deferred", "DeferredList", "succeed", "fail", "FAILURE", "SUCCESS",
           "AlreadyCalledError", "TimeoutError", "gatherResults",
           "maybeDeferred", "ensureDeferred",
           "waitForDeferred", "deferredGenerator", "inlineCallbacks",
           "returnValue",
           "DeferredLock", "DeferredSemaphore", "DeferredQueue",
           "DeferredFilesystemLock", "AlreadyTryingToLockError",
           "CancelledError",
          ]

