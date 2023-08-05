# -*- coding: utf-8 -*-
"""
Provides tools to help unit test projects using pop.
For now, provides mock Hub instances.
"""
# Import python libs
import inspect
import copy
from asyncio import iscoroutinefunction
from functools import partial

# Import third party libs
try:
    from asynctest.mock import create_autospec
except ImportError:
    from unittest.mock import create_autospec as mock_create_autospec

    def create_autospec(spec, *args, **kwargs):
        if iscoroutinefunction(spec):
            raise Exception(
                "MockHub requires asynctest in order to mock async functions"
            )
        return mock_create_autospec(spec, *args, **kwargs)


# Import pop libs
from pop.contract import Contracted
from pop.loader import LoadedMod
from pop.hub import Hub, Sub


class _LookUpTable:
    def __init__(self, *args, **kwargs):
        self._lut = {}
        super().__init__(*args, **kwargs)

    def contains(self, key):
        return self.is_hashable(key) and key in self._lut

    def update(self, key, value):
        if self.is_hashable(key):
            self._lut[key] = value

    def lookup(self, key):
        return self._lut[key]

    def is_hashable(self, key):
        try:
            _ = {key: None}
            return True
        except TypeError:
            return False

    def __len__(self):
        return len(self._lut)


class _LazyPop:
    __lazy_classes = [Hub, Sub, LoadedMod]

    class __Lazy:
        pass

    def __init__(self, obj, lut=None):
        if isinstance(obj, Hub):
            lut = _LookUpTable()
            lut.update("hub", obj)
            lut.update("lazy_hub", obj)
            lut.update(obj, self)
        elif isinstance(obj, Sub):
            obj._load_all()

        self.__lut = lut
        self.__obj = obj
        for attr_name in self.__attr_names():
            setattr(self, attr_name, _LazyPop.__Lazy)

    def __attr_names(self):
        # TODO: '_' - is this actually right? what should I really expose?
        attrs = [attr for attr in self.__obj.__dict__ if not attr.startswith("_")]

        if isinstance(self.__obj, Hub):
            attrs += list(self.__obj._subs)
        elif isinstance(self.__obj, Sub):
            attrs += list(self.__obj._loaded)
            attrs += list(self.__obj._subs)
        elif isinstance(self.__obj, LoadedMod):
            attrs += list(self.__obj._attrs)
        else:
            raise Exception(
                "Standard objects should not be lazy: {}".format(str(self.__obj))
            )

        return attrs

    def _find_subs(self):
        i = 0
        subs = [(s._subname, s) for s in self.__lut.lookup("hub")]
        while i < len(subs):
            for child in subs[i][1]._subs:
                subs.append((".".join([subs[i][0], child]), getattr(subs[i][1], child)))
            i += 1
        return subs

    def _find_module_from_file(self, file):
        for path, sub in self._find_subs():
            try:
                mod = sub._vmap[file]
                return ".".join([path, mod]), getattr(sub, mod)
            except AttributeError:
                pass
        else:
            raise Exception("Module not loaded on hub.")

    def __getattribute__(self, item):
        if item and not item.strip("_"):  # only contains underscores, resolve 'this'
            stack = inspect.stack(0)
            file = stack[1].filename
            path, mod = self._find_module_from_file(file)

            # go up N steps
            parts = path.split(".")
            resolved_path = parts[0 : len(parts) - len(item) + 1]
            if resolved_path:
                orig = getattr(self.__lut.lookup("hub"), ".".join(resolved_path))
            else:
                orig = self.__lut.lookup("hub")

            # find/create attr, return
            attr = self._orig_to_attr(orig)
            self.__lut.update(orig, attr)
            return attr

        if "." in item:
            result = self
            for part in item.split(".").copy():
                result = getattr(result, part)
            return result

        attr = super().__getattribute__(item)

        if attr is _LazyPop.__Lazy:
            orig = getattr(self.__obj, item)
            attr = self._orig_to_attr(orig)

            self.__lut.update(orig, attr)
            setattr(self, item, attr)

        return attr

    def _orig_to_attr(self, orig):
        if self.__lut.contains(orig):
            attr = self.__lut.lookup(orig)
        elif [True for cls in self.__lazy_classes if isinstance(orig, cls)]:
            attr = self.__class__(orig, self.__lut)
        elif isinstance(orig, Contracted):
            attr = self._mock_function(orig)
        else:
            attr = self._mock_attr(orig)
        return attr

    def _mock_attr(self, a):
        return create_autospec(a, spec_set=True)

    def _mock_function(self, f):
        raise NotImplementedError()


def strip_hub(f):
    """
    returns a no-op function with the same function signature... minus the first parameter (hub).
    """
    if inspect.iscoroutinefunction(f):
        newf = "async "
    else:
        newf = ""
    newf += "def {}(".format(f.__name__)
    params = inspect.signature(f).parameters
    new_params = []
    for param in params:
        if params[param].kind is inspect.Parameter.VAR_POSITIONAL:
            new_params.append("*{}".format(param))
        elif params[param].kind is inspect.Parameter.VAR_KEYWORD:
            new_params.append("**{}".format(param))
        else:
            new_params.append(param)
        if params[param].default is not inspect.Parameter.empty:
            new_params[-1] += '="has default"'
    newf += ", ".join(new_params[1:])  # skip hub
    newf += "): pass"

    scope = {}
    exec(newf, scope)

    return scope[f.__name__]


def mock_hub(hub):
    return MockHub(hub)


class MockHub(_LazyPop):
    """
    Provides mocks mirroring a real hub::

        hub.sub.mod.fn()  # mock
        hub.sub.mod.attr  # mock
    """

    def _mock_function(self, f):
        return create_autospec(strip_hub(f.func), spec_set=True)


def fn_hub(hub):
    return NoContractHub(hub)


class NoContractHub(_LazyPop):
    """
    Provides access to real functions, bypassing contracts and mocking attributes::

        hub.sub.mod.fn()  # executes real function, no contracts
        hub.sub.mod.attr  # mock
    """

    def _mock_function(self, f):
        mock_hub = self._LazyPop__lut.lookup("lazy_hub")
        return partial(f.func, mock_hub)


def mock_contracted(c):
    mock_func = create_autospec(c.func, spec_set=True)
    mock_func.__signature__ = c.signature  # required for python 3.6
    mock_func.__module__ = c.func.__module__
    mock_func.__dict__.update(copy.deepcopy(c.func.__dict__))
    return Contracted(c.hub, c.contracts, mock_func, c.ref, c.name)


class ContractHub(_LazyPop):
    """
    Runs a call through the contract system, but the function is a mock. Mostly useful for integration tests:

        hub.sub.mod.fn()  # executes mock function, real contracts
        hub.sub.mod.attr  # mock

    You can verify what parameters are passed to a function after going through loaded contracts::

        contract_hub.sub.mod.fn('foo')
        assert contract_hub.sub.mod.fn.called_with('bar')

    --------------------------------

    You can view or modify the contracts that will be executed on one function for a test - but first:
    MODIFYING CONTRACTS THIS WAY IS NOT SAFE ON REAL HUBS AND OTHER TESTING HUB VARIANTS!

    I have previously thought of modifying contracts with mocks, only to realize what I really want is to
    unit test a specific contract. Think twice before using this functionality.

    --------------------------------

    The contract modules are visible via hub.sub.mod.fn.contracts, and the contract functions that will
    be called, wrapping fn are visible via hub.sub.mod.fn.contract_functions. It is safe to modify the
    contracts list or contract_functions dict only on a ContractHub.

    Examine that the first contract function to be called is 'foo.pre_fn', then bypass it::

        assert contract_hub.sub.mod.fn.contract_functions['pre'][0].__module__ is 'foo'
        assert contract_hub.sub.mod.fn.contract_functions['pre'][0].__name__ is 'pre_fn'
        hub.sub.mod.fn.contract_functions['pre'][0] = create_autospec(hub.sub.mod.fn.contract_functions['pre'][0])

    Assert that one contract will be called before another::

        assert contract_hub.sub.mod.fn.contracts.index(contract1) < contract_hub.sub.mod.fn.contracts.index(contract2)
    """

    def _mock_function(self, f):
        return mock_contracted(f)
