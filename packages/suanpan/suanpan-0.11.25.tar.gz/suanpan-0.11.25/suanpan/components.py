# coding=utf-8
from __future__ import absolute_import, print_function

import gc
import contextlib
import itertools
from collections import defaultdict

from suanpan import error, runtime
from suanpan.arguments.auto import AutoArg
from suanpan.interfaces import (
    HasArguments,
    HasCallHooks,
    HasExitHooks,
    HasInitHooks,
    HasResetHooks,
    HasSaveHooks,
)
from suanpan.log import logger
from suanpan.objects import Context


class Arguments(Context):
    pass


class Result(Context):
    pass


class Component(
    HasArguments, HasInitHooks, HasSaveHooks, HasResetHooks, HasCallHooks, HasExitHooks
):
    def __init__(self, funcOrComponent):
        if isinstance(funcOrComponent, Component):
            self.runFunc = funcOrComponent.runFunc
            self.arguments = funcOrComponent.arguments
            self.beforeInitHooks = funcOrComponent.beforeInitHooks
            self.afterInitHooks = funcOrComponent.afterInitHooks
            self.beforeCallHooks = funcOrComponent.beforeCallHooks
            self.afterCallHooks = funcOrComponent.afterCallHooks
            self.beforeSaveHooks = funcOrComponent.beforeSaveHooks
            self.afterSaveHooks = funcOrComponent.afterSaveHooks
            self.beforeResetHooks = funcOrComponent.beforeResetHooks
            self.afterResetHooks = funcOrComponent.afterResetHooks
        else:
            super(Component, self).__init__()
            self.runFunc = funcOrComponent
            self.arguments = defaultdict(list)

    def __call__(self, *arg, **kwargs):
        self.run(*arg, **kwargs)
        return self

    def start(self):
        pass

    @property
    def name(self):
        return self.runFunc.__name__

    @runtime.globalrun
    def run(self, *arg, **kwargs):
        self.callBeforeInitHooks()
        context = self.init(*arg, **kwargs)
        self.callAfterInitHooks(context)
        self.registerBeforeExitHooks(context)

        self.callBeforeCallHooks(context)
        results = self.runFunc(context)
        self.callAfterCallHooks(context)

        self.callBeforeSaveHooks(context)
        outputs = self.save(context, results)
        self.callAfterSaveHooks(context)

        self.callBeforeResetHooks(context)
        self.reset(context)
        self.callAfterResetHooks(context)

        return outputs

    def init(self, *arg, **kwargs):
        restArgs = self.getArgList(*arg, **kwargs)
        globalArgs, restArgs = self.loadGlobalArguments(restArgs=restArgs)
        self.initBase(globalArgs)
        context = self._getContext(globalArgs)
        args, restArgs = self.loadComponentArguments(context, restArgs=restArgs)
        context.update(args=args)
        return context

    def initBase(self, args):
        pass

    def save(self, context, results):
        outputs = self.saveOutputs(context, results)
        self._closeContext()
        return outputs

    def reset(self, context):
        self._resetArguments(self.getArguments(include=["inputs", "outputs"]))
        gc.collect()

    @contextlib.contextmanager
    def context(self, args=None):  # pylint: disable=unused-argument
        yield Context()

    def _getContext(self, *args, **kwargs):
        self.contextManager = self.context(  # pylint: disable=attribute-defined-outside-init
            *args, **kwargs
        )
        return next(self.contextManager.gen)  # pylint: disable-msg=e1101

    def _closeContext(self):
        try:
            next(self.contextManager.gen)  # pylint: disable-msg=e1101
        except StopIteration:
            pass

    def loadGlobalArguments(self, restArgs=None, **kwargs):
        logger.info("Loading Global Arguments:")
        arguments, restArgs = super(Component, self).loadGlobalArguments(
            restArgs=restArgs, **kwargs
        )
        args = self.argumentsDict(arguments)
        return Arguments.froms(args), restArgs

    def loadComponentArguments(self, context, restArgs=None):
        logger.info("Loading Component Arguments:")
        _, restArgs = self.loadFormatArguments(
            context, restArgs=restArgs, exclude="outputs"
        )
        _, restArgs = self.loadCleanArguments(
            context, restArgs=restArgs, include="outputs"
        )
        arguments = {
            k: self.argumentsDict(arg for arg in v if arg.isSet)
            for k, v in self.arguments.items()
        }
        arguments.update(self.argumentsDict(itertools.chain(*self.arguments.values())))
        return Arguments.froms(arguments), restArgs

    def getArguments(self, include=None, exclude=None):
        includes = set(self.arguments.keys() if not include else self._list(include))
        excludes = set([] if not exclude else self._list(exclude))
        includes = includes - excludes
        argumentsLists = [self.arguments[c] for c in includes]
        return list(itertools.chain(*argumentsLists))

    def saveMutipleOutputs(self, context, outputs, results):
        if isinstance(results, (tuple, list)):
            results = (Result.froms(value=result) for result in results)
            return self.saveArguments(context, outputs, results)
        if isinstance(results, dict):
            outputs, results = zip(
                *[
                    (
                        argument,
                        Result.froms(
                            value=self.getArgumentValueFromDict(results, argument)
                        ),
                    )
                    for argument in outputs
                    if self.getArgumentValueFromDict(results, argument) is not None
                ]
            )
            return self.saveArguments(context, outputs, results)
        raise error.ComponentError(f"Incorrect results {results}")

    def saveOneOutput(self, context, output, results):
        result = (
            Result.froms(value=self.getArgumentValueFromDict(results, output))
            if isinstance(results, dict)
            and self.hasArgumentValueFromDict(results, output)
            else Result.froms(value=results)
        )
        return {output.key: output.save(context, result)}

    def saveOutputs(self, context, results):
        logger.info("Saving...")
        outputs = self.getArguments(include="outputs")
        if len(outputs) > 1:
            return self.saveMutipleOutputs(context, outputs, results)
        if len(outputs) == 1:
            return self.saveOneOutput(context, outputs[0], results)
        return None

    def addArgument(self, arg, argtype="args", reverse=True):
        if reverse:
            self.arguments[argtype].insert(0, arg)
        else:
            self.arguments[argtype].append(arg)

    @classmethod
    def use(cls, funcOrComponent):
        return (
            funcOrComponent
            if isinstance(funcOrComponent, cls)
            else cls(funcOrComponent)
        )

    @classmethod
    def arg(cls, argument, argtype="args", reverse=True):
        def _dec(funcOrComponent):
            funcOrComponent = (
                funcOrComponent
                if isinstance(funcOrComponent, cls)
                else cls(funcOrComponent)
            )
            if isinstance(argument, AutoArg):
                argument.setBackend(argtype=argtype)
            funcOrComponent.addArgument(argument, argtype=argtype, reverse=reverse)
            return funcOrComponent

        return _dec

    @classmethod
    def input(cls, *args, **kwargs):
        kwargs.update(argtype="inputs")
        return cls.arg(*args, **kwargs)

    @classmethod
    def output(cls, *args, **kwargs):
        kwargs.update(argtype="outputs")
        return cls.arg(*args, **kwargs)

    @classmethod
    def param(cls, *args, **kwargs):
        kwargs.update(argtype="params")
        return cls.arg(*args, **kwargs)

    @classmethod
    def column(cls, *args, **kwargs):
        kwargs.update(argtype="columns")
        return cls.arg(*args, **kwargs)

    def _list(self, params=None):
        return [params] if isinstance(params, str) else list(params)
