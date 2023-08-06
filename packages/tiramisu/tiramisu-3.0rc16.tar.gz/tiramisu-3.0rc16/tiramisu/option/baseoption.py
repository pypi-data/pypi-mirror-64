# -*- coding: utf-8 -*-
# Copyright (C) 2014-2020 Team tiramisu (see AUTHORS for all contributors)
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by the
# Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# The original `Config` design model is unproudly borrowed from
# the rough pypy's guys: http://codespeak.net/svn/pypy/dist/pypy/config/
# the whole pypy projet is under MIT licence
# ____________________________________________________________
from types import FunctionType
from typing import FrozenSet, Callable, Tuple, Set, Optional, Union, Any, List
import weakref
from inspect import signature
from itertools import chain


from ..i18n import _
from ..setting import undefined, Settings
from ..value import Values
from ..error import ConfigError, display_list
from ..autolib import Calculation, Params, ParamOption, ParamIndex

STATIC_TUPLE = frozenset()


submulti = 2


def valid_name(name):
    if not isinstance(name, str):
        return False
    return True


#____________________________________________________________
#
class Base:
    """Base use by all *Option* classes (Option, OptionDescription, SymLinkOption, ...)
    """
    __slots__ = ('_name',
                 '_path',
                 '_informations',
                 '_subdyn',
                 '_properties',
                 '_has_dependency',
                 '_dependencies',
                 '__weakref__'
                )

    def __init__(self,
                 name: str,
                 doc: str,
                 properties=None,
                 is_multi: bool=False) -> None:
        if not valid_name(name):
            raise ValueError(_('"{0}" is an invalid name for an option').format(name))
        if properties is None:
            properties = frozenset()
        elif isinstance(properties, tuple):
            properties = frozenset(properties)
        if is_multi:
            # if option is a multi, it cannot be 'empty' (None not allowed in the list) and cannot have multiple time the same value
            # 'empty' and 'unique' are removed for follower's option
            if 'notunique' in properties:
                properties = properties - {'notunique'}
            else:
                properties = properties | {'unique'}
            if 'notempty' in properties:
                properties = properties - {'notempty'}
            else:
                properties = properties | {'empty'}
        assert isinstance(properties, frozenset), _('invalid properties type {0} for {1},'
                                                    ' must be a frozenset').format(type(properties),
                                                                                   name)
        for prop in properties:
            if not isinstance(prop, str):
                if not isinstance(prop, Calculation):
                    raise ValueError(_('invalid property type {0} for {1}, must be a string or a Calculation').format(type(prop), name))
                for param in chain(prop.params.args, prop.params.kwargs.values()):
                    if isinstance(param, ParamOption):
                        param.option._add_dependency(self)
        _setattr = object.__setattr__
        _setattr(self, '_name', name)
        _setattr(self, '_informations', {'doc': doc})
        if properties:
            _setattr(self, '_properties', properties)

    def impl_has_dependency(self,
                            self_is_dep: bool=True) -> bool:
        if self_is_dep is True:
            return getattr(self, '_has_dependency', False)
        return hasattr(self, '_dependencies')

    def _get_dependencies(self,
                          context_od) -> Set[str]:
        ret = set(getattr(self, '_dependencies', STATIC_TUPLE))
        if context_od and hasattr(context_od, '_dependencies'):
            # if context is set in options, add those options
            return set(context_od._dependencies) | ret
        return ret

    def _add_dependency(self,
                        option) -> None:
        options = self._get_dependencies(None)
        options.add(weakref.ref(option))
        self._dependencies = tuple(options)

    def _impl_set_callback(self,
                           callback: Callable,
                           callback_params: Optional[Params]=None) -> None:
        if __debug__:
            if callback is None and callback_params is not None:
                raise ValueError(_("params defined for a callback function but "
                                   "no callback defined"
                                   ' yet for option "{0}"').format(
                                       self.impl_getname()))
            self._validate_calculator(callback,
                                      callback_params)
        if callback is not None:
            callback_params = self._build_calculator_params(callback,
                                                            callback_params,
                                                            'callback')
            # first part is validator
            val = getattr(self, '_val_call', (None,))[0]
            if not callback_params:
                val_call = (callback,)
            else:
                val_call = (callback, callback_params)
            self._val_call = (val, val_call)

    def impl_is_optiondescription(self) -> bool:
        return False

    def impl_is_dynoptiondescription(self) -> bool:
        return False

    def impl_getname(self) -> str:
        return self._name

    def _set_readonly(self) -> None:
        if isinstance(self._informations, dict):
            _setattr = object.__setattr__
            dico = self._informations
            keys = tuple(dico.keys())
            if len(keys) == 1:
                dico = dico['doc']
            else:
                dico = tuple([keys, tuple(dico.values())])
            _setattr(self, '_informations', dico)
            extra = getattr(self, '_extra', None)
            if extra is not None:
                _setattr(self, '_extra', tuple([tuple(extra.keys()), tuple(extra.values())]))

    def impl_is_readonly(self) -> str:
        # _path is None when initialise SymLinkOption
        return hasattr(self, '_path') and self._path is not None

    def impl_getproperties(self) -> FrozenSet[str]:
        return getattr(self, '_properties', frozenset())

    def _setsubdyn(self,
                   subdyn) -> None:
        self._subdyn = weakref.ref(subdyn)

    def issubdyn(self) -> bool:
        return getattr(self, '_subdyn', None) is not None

    def getsubdyn(self):
        return self._subdyn()

    def impl_get_callback(self):
        call = getattr(self, '_val_call', (None, None))[1]
        if call is None:
            ret_call = (None, None)
        elif len(call) == 1:
            ret_call = (call[0], None)
        else:
            ret_call = call
        return ret_call

    # ____________________________________________________________
    # information
    def impl_get_information(self,
                             key: str,
                             default: Any=undefined) -> Any:
        """retrieves one information's item

        :param key: the item string (ex: "help")
        """
        dico = self._informations
        if isinstance(dico, tuple):
            if key in dico[0]:
                return dico[1][dico[0].index(key)]
        elif isinstance(dico, str):
            if key == 'doc':
                return dico
        elif isinstance(dico, dict):
            if key in dico:
                return dico[key]
        if default is not undefined:
            return default
        raise ValueError(_("information's item not found: {0}").format(
            key))

    def impl_set_information(self,
                             key: str,
                             value: Any) -> None:
        """updates the information's attribute
        (which is a dictionary)

        :param key: information's key (ex: "help", "doc"
        :param value: information's value (ex: "the help string")
        """
        if self.impl_is_readonly():
            raise AttributeError(_("'{0}' ({1}) object attribute '{2}' is"
                                   " read-only").format(self.__class__.__name__,
                                                        self,
                                                        key))
        self._informations[key] = value


class BaseOption(Base):
    """This abstract base class stands for attribute access
    in options that have to be set only once, it is of course done in the
    __setattr__ method
    """
    __slots__ = ('_display_name_function',)

    def __getstate__(self):
        raise NotImplementedError()

    def __setattr__(self,
                    name: str,
                    value: Any) -> Any:
        """set once and only once some attributes in the option,
        like `_name`. `_name` cannot be changed once the option is
        pushed in the :class:`tiramisu.option.OptionDescription`.

        if the attribute `_readonly` is set to `True`, the option is
        "frozen" (which has nothing to do with the high level "freeze"
        propertie or "read_only" property)
        """
        # never change _name in an option or attribute when object is readonly
        if self.impl_is_readonly():
            raise AttributeError(_('"{}" ({}) object attribute "{}" is'
                                   ' read-only').format(self.__class__.__name__,
                                                        self.impl_get_display_name(),
                                                        name))
        super(BaseOption, self).__setattr__(name, value)

    def impl_getpath(self) -> str:
        try:
            return self._path
        except AttributeError:
            raise AttributeError(_('"{}" not part of any Config').format(self.impl_get_display_name()))

    def impl_has_callback(self) -> bool:
        "to know if a callback has been defined or not"
        return self.impl_get_callback()[0] is not None

    def _impl_get_display_name(self,
                               dyn_name: Base=None) -> str:
        name = self.impl_get_information('doc', None)
        if name is None or name == '':
            if dyn_name is not None:
                name = dyn_name
            else:
                name = self.impl_getname()
        return name

    def impl_get_display_name(self,
                              dyn_name: Base=None) -> str:
        if hasattr(self, '_display_name_function'):
            return self._display_name_function(self, dyn_name)
        return self._impl_get_display_name(dyn_name)

    def reset_cache(self,
                    path: str,
                    config_bag: 'OptionBag',
                    resetted_opts: List[Base]) -> None:
        context = config_bag.context
        context._impl_properties_cache.delcache(path)
        context._impl_permissives_cache.delcache(path)
        if not self.impl_is_optiondescription():
            context._impl_values_cache.delcache(path)

    def impl_is_symlinkoption(self) -> bool:
        return False
