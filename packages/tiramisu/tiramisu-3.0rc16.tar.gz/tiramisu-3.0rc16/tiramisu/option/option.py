# -*- coding: utf-8 -*-
"option types and option description"
# Copyright (C) 2012-2020 Team tiramisu (see AUTHORS for all contributors)
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
import warnings
import weakref
from typing import Any, List, Callable, Optional, Dict, Union, Tuple
from itertools import chain

from .baseoption import BaseOption, submulti, STATIC_TUPLE
from ..i18n import _
from ..setting import undefined, OptionBag, Undefined
from ..autolib import Calculation, Params, ParamValue, ParamOption
from ..error import (ConfigError, ValueWarning, ValueErrorWarning, PropertiesOptionError,
                     ValueOptionError, display_list)
from .syndynoption import SynDynOption
#ALLOWED_CONST_LIST = ['_cons_not_equal']


class Option(BaseOption):
    """
    Abstract base class for configuration option's.

    Reminder: an Option object is **not** a container for the value.
    """
    __slots__ = ('_extra',
                 '_warnings_only',
                 # multi
                 '_multi',
                 # value
                 '_default',
                 '_default_multi',
                 #
                 '_validators',
                 #
                 '_leadership',
                 '_choice_values',
                 '_choice_values_params',
                )
    _empty = ''
    def __init__(self,
                 name: str,
                 doc: str,
                 default: Any=undefined,
                 default_multi: Any=None,
                 multi: bool=False,
                 validators: Optional[List[Calculation]]=None,
                 properties: Optional[List[str]]=None,
                 warnings_only: bool=False,
                 extra: Optional[Dict]=None):
        _setattr = object.__setattr__
        if not multi and default_multi is not None:
            raise ValueError(_("default_multi is set whereas multi is False"
                               " in option: {0}").format(name))
        if default is undefined:
            if multi is False:
                default = None
            else:
                default = []
        if multi is True:
            is_multi = True
            _multi = 0
        elif multi is False:
            is_multi = False
            _multi = 1
        elif multi is submulti:
            is_multi = True
            _multi = submulti
        else:
            raise ValueError(_('invalid multi type "{}"').format(multi))
        if _multi != 1:
            _setattr(self, '_multi', _multi)
        if multi is not False and default is None:
            default = []
        super().__init__(name,
                         doc,
                         properties=properties,
                         is_multi=is_multi)
        if __debug__:
            if validators is not None:
                if not isinstance(validators, list):
                    raise ValueError(_('validators must be a list of Calculation for "{}"').format(name))
                for validator in validators:
                    if not isinstance(validator, Calculation):
                        raise ValueError(_('validators must be a Calculation for "{}"').format(name))
                    for param in chain(validator.params.args, validator.params.kwargs.values()):
                        if isinstance(param, ParamOption):
                            param.option._add_dependency(self)
                            self._has_dependency = True

                self._validators = tuple(validators)
        if extra is not None and extra != {}:
            _setattr(self, '_extra', extra)
        if warnings_only is True:
            _setattr(self, '_warnings_only', warnings_only)
        if is_multi and default_multi is not None:
            def test_multi_value(value):
                if isinstance(value, Calculation):
                    return
                option_bag = OptionBag()
                option_bag.set_option(self,
                                      None,
                                      undefined)
                try:
                    self.validate(value)
                    self.sync_validate_with_option(value,
                                                   option_bag)
                except ValueError as err:
                    str_err = str(err)
                    if not str_err:
                        raise ValueError(_('invalid default_multi value "{0}" '
                                           'for option "{1}"').format(str(value),
                                                                      self.impl_get_display_name()))
                    else:
                        raise ValueError(_('invalid default_multi value "{0}" '
                                           'for option "{1}", {2}').format(str(value),
                                                                           self.impl_get_display_name(),
                                                                           str_err))
            if _multi is submulti:
                if not isinstance(default_multi, Calculation):
                    if not isinstance(default_multi, list):
                        raise ValueError(_('invalid default_multi value "{0}" '
                                           'for option "{1}", must be a list for a submulti'
                                           '').format(str(default_multi),
                                                     self.impl_get_display_name()))
                    for value in default_multi:
                        test_multi_value(value)
            else:
                test_multi_value(default_multi)
            _setattr(self, '_default_multi', default_multi)
        option_bag = OptionBag()
        option_bag.set_option(self,
                              None,
                              undefined)
        self.sync_impl_validate(default,
                                option_bag)
        self.sync_impl_validate(default,
                                option_bag,
                                check_error=False)
        self.value_dependencies(default)
        if (is_multi and default != []) or \
                (not is_multi and default is not None):
            if is_multi and isinstance(default, list):
                default = tuple(default)
            _setattr(self, '_default', default)

    def value_dependencies(self,
                           value: Any) -> Any:
        if isinstance(value, list):
            for val in value:
                if isinstance(value, list):
                    self.value_dependencies(val)
                elif isinstance(value, Calculation):
                    self.value_dependency(val)
        elif isinstance(value, Calculation):
            self.value_dependency(value)

    def value_dependency(self,
                         value: Any) -> Any:
        for param in chain(value.params.args, value.params.kwargs.values()):
            if isinstance(param, ParamOption):
                param.option._add_dependency(self)

    #__________________________________________________________________________
    # option's information

    def impl_is_multi(self) -> bool:
        return getattr(self, '_multi', 1) != 1

    def impl_is_submulti(self) -> bool:
        return getattr(self, '_multi', 1) == 2

    def impl_is_dynsymlinkoption(self) -> bool:
        return False

    def get_type(self) -> str:
        # _display_name for compatibility with older version than 3.0rc3
        return getattr(self, '_type', self._display_name)

    def get_display_type(self) -> str:
        return self._display_name

    def impl_getdefault(self) -> Any:
        "accessing the default value"
        is_multi = self.impl_is_multi()
        default = getattr(self, '_default', undefined)
        if default is undefined:
            if is_multi:
                default = []
            else:
                default = None
        else:
            if is_multi and isinstance(default, list):
                default = list(default)
        return default

    def impl_getdefault_multi(self) -> Any:
        "accessing the default value for a multi"
        if self.impl_is_submulti():
            default_value = []
        else:
            default_value = None
        return getattr(self, '_default_multi', default_value)

    def impl_get_extra(self,
                       key: str) -> Any:
        extra = getattr(self, '_extra', {})
        if isinstance(extra, tuple):
            if key in extra[0]:
                return extra[1][extra[0].index(key)]
            return None
        else:
            return extra.get(key)

    #__________________________________________________________________________
    # validator
    def sync_impl_validate(self,
                           value: Any,
                           option_bag: OptionBag,
                           check_error: bool=True) -> None:
        """
        """
        is_warnings_only = getattr(self, '_warnings_only', False)

        def do_validation(_value,
                          _index):
            if isinstance(_value, list):
                raise ValueError(_('which must not be a list').format(_value,
                                                                      self.impl_get_display_name()))
            if _value is not None:
                if check_error:
                    # option validation
                    self.validate(_value)
                    self.sync_validate_with_option(_value,
                                                   option_bag)
                if ((check_error and not is_warnings_only) or
                        (not check_error and is_warnings_only)):
                    try:
                        self.second_level_validation(_value,
                                                     is_warnings_only)
                    except ValueError as err:
                        if is_warnings_only:
                            warnings.warn_explicit(ValueWarning(_value,
                                                                self._display_name,
                                                                self,
                                                                '{0}'.format(err),
                                                                _index),
                                                   ValueWarning,
                                                   self.__class__.__name__, 0)
                        else:
                            raise err
        try:
            err_index = None
            if isinstance(value, Calculation):
                pass
            elif not self.impl_is_multi():
                val = value
                do_validation(val, None)
            elif self.impl_is_submulti():
                if not isinstance(value, list):
                    raise ValueError(_('which must be a list'))
                for err_index, lval in enumerate(value):
                    if isinstance(lval, Calculation):
                        continue
                    if not isinstance(lval, list):
                        raise ValueError(_('which "{}" must be a list of list'
                                           '').format(lval))
                    for val in lval:
                        if isinstance(val, Calculation):
                            continue
                        do_validation(val,
                                      err_index)
            else:
                # it's a multi
                if not isinstance(value, list):
                    raise ValueError(_('which must be a list'))
                for err_index, val in enumerate(value):
                    if isinstance(val, Calculation):
                        continue
                    do_validation(val,
                                  err_index)
        except ValueError as err:
            raise ValueOptionError(value,
                                   self._display_name,
                                   option_bag.ori_option,
                                   '{0}'.format(err),
                                   err_index)

    async def impl_validate(self,
                            value: Any,
                            option_bag: OptionBag,
                            check_error: bool=True) -> None:
        """
        """
        config_bag = option_bag.config_bag
        force_index = option_bag.index
        is_warnings_only = getattr(self, '_warnings_only', False)

        if check_error and config_bag is not undefined and \
                not 'validator' in config_bag.properties:
            return


        def _is_not_unique(value, option_bag):
            # if set(value) has not same length than value
            if config_bag is not undefined and check_error and \
                    'unique' in option_bag.properties:
                lvalue = [val for val in value if val is not None]
                if len(set(lvalue)) != len(lvalue):
                    for idx, val in enumerate(value):
                        if val in value[idx+1:]:
                            raise ValueError(_('the value "{}" is not unique'
                                               '').format(val))

        async def calculation_validator(val,
                                        _index):
            for validator in getattr(self, '_validators', []):
                calc_is_warnings_only = hasattr(validator, 'warnings_only') and validator.warnings_only
                if ((check_error and not calc_is_warnings_only) or
                        (not check_error and calc_is_warnings_only)):
                    try:
                        kwargs = {'allow_raises': True}
                        if _index is not None and option_bag.index == _index:
                            soption_bag = option_bag
                        else:
                            soption_bag = option_bag.copy()
                            soption_bag.index = _index
                        kwargs['orig_value'] = value

                        await validator.execute(soption_bag,
                                                leadership_must_have_index=True,
                                                **kwargs)
                    except ValueError as err:
                        if calc_is_warnings_only:
                            warnings.warn_explicit(ValueWarning(val,
                                                                self._display_name,
                                                                self,
                                                                '{0}'.format(err),
                                                                _index),
                                                   ValueWarning,
                                                   self.__class__.__name__, 306)
                        else:
                            raise err
                    except ValueWarning as warn:
                        warnings.warn_explicit(ValueWarning(val,
                                                            self._display_name,
                                                            self,
                                                            '{0}'.format(warn),
                                                            _index),
                                               ValueWarning,
                                               self.__class__.__name__, 316)

        async def do_validation(_value,
                                _index):
            if isinstance(_value, list):
                raise ValueError(_('which must not be a list').format(_value,
                                                                      self.impl_get_display_name()))
            if isinstance(_value, Calculation) and config_bag is undefined:
                return
            if _value is not None:
                if check_error:
                    # option validation
                    self.validate(_value)
                    await self.validate_with_option(_value,
                                                    option_bag)
                if ((check_error and not is_warnings_only) or
                        (not check_error and is_warnings_only)):
                    try:
                        self.second_level_validation(_value,
                                                     is_warnings_only)
                    except ValueError as err:
                        if is_warnings_only:
                            warnings.warn_explicit(ValueWarning(_value,
                                                                self._display_name,
                                                                self,
                                                                '{0}'.format(err),
                                                                _index),
                                                   ValueWarning,
                                                   self.__class__.__name__, 0)
                        else:
                            raise err
                await calculation_validator(_value,
                                            _index)
        try:
            val = value
            err_index = force_index
            if not self.impl_is_multi():
                await do_validation(val, None)
            elif force_index is not None:
                if self.impl_is_submulti():
                    if not isinstance(value, list):
                        raise ValueError(_('which must be a list'))
                    for val in value:
                        await do_validation(val,
                                            force_index)
                    _is_not_unique(value, option_bag)
                else:
                    await do_validation(val,
                                        force_index)
            elif isinstance(value, Calculation) and config_bag is undefined:
                pass
            elif not isinstance(value, list):
                raise ValueError(_('which must be a list'))
            elif self.impl_is_submulti():
                for err_index, lval in enumerate(value):
                    if isinstance(lval, Calculation):
                        continue
                    if not isinstance(lval, list):
                        raise ValueError(_('which "{}" must be a list of list'
                                           '').format(lval))
                    for val in lval:
                        await do_validation(val,
                                            err_index)
                    _is_not_unique(lval, option_bag)
            else:
                # FIXME subtimal, not several time is whole=True!
                for err_index, val in enumerate(value):
                    await do_validation(val,
                                        err_index)
                _is_not_unique(value, option_bag)
        except ValueError as err:
            if config_bag is undefined or \
                    'demoting_error_warning' not in config_bag.properties:
                raise ValueOptionError(val,
                                       self._display_name,
                                       option_bag.ori_option,
                                       '{0}'.format(err),
                                       err_index)
            warnings.warn_explicit(ValueErrorWarning(val,
                                                     self._display_name,
                                                     option_bag.ori_option,
                                                     '{0}'.format(err),
                                                     err_index),
                                   ValueErrorWarning,
                                   self.__class__.__name__, 0)

    def _validate_calculator(self,
                            callback: Callable,
                            callback_params: Optional[Params]=None) -> None:
        if callback is None:
            return
        default_multi = getattr(self, '_default_multi', None)
        is_multi = self.impl_is_multi()
        default = self.impl_getdefault()
        if (not is_multi and (default is not None or default_multi is not None)) or \
                (is_multi and (default != [] or default_multi is not None)):
            raise ValueError(_('default value not allowed if option "{0}" '
                             'is calculated').format(self.impl_getname()))

    def sync_validate_with_option(self,
                                  value: Any,
                                  option_bag: OptionBag) -> None:
        pass

    async def validate_with_option(self,
                                   value: Any,
                                   option_bag: OptionBag) -> None:
        pass

    def second_level_validation(self,
                                value: Any,
                                warnings_only: bool) -> None:
        pass

    def impl_is_leader(self):
        leadership = self.impl_get_leadership()
        if leadership is None:
            return False
        return leadership.is_leader(self)

    def impl_is_follower(self):
        leadership = self.impl_get_leadership()
        if leadership is None:
            return False
        return not leadership.is_leader(self)

    def impl_get_leadership(self):
        leadership = getattr(self, '_leadership', None)
        if leadership is None:
            return leadership
        return leadership()

    def to_dynoption(self,
                     rootpath: str,
                     suffix: str,
                     ori_dyn) -> SynDynOption:
        return SynDynOption(self,
                            rootpath,
                            suffix,
                            ori_dyn)
