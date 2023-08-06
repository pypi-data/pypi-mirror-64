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
# the rough gus of pypy: pypy: http://codespeak.net/svn/pypy/dist/pypy/config/
# the whole pypy projet is under MIT licence
# ____________________________________________________________
"enables us to carry out a calculation and return an option's value"
from typing import Any, Optional, Union, Callable, Dict, List
from itertools import chain

from .error import PropertiesOptionError, ConfigError, LeadershipError, ValueWarning
from .i18n import _
from .setting import undefined, ConfigBag, OptionBag, Undefined
# ____________________________________________________________


class Params:
    __slots__ = ('args', 'kwargs')
    def __init__(self, args=None, kwargs=None, **kwgs):
        if args is None:
            args = tuple()
        if kwargs is None:
            kwargs = {}
        if kwgs:
            kwargs.update(kwgs)
        if isinstance(args, Param):
            args = (args,)
        else:
            if not isinstance(args, tuple):
                raise ValueError(_('args in params must be a tuple'))
            for arg in args:
                if not isinstance(arg, Param):
                    raise ValueError(_('arg in params must be a Param'))
        if not isinstance(kwargs, dict):
            raise ValueError(_('kwargs in params must be a dict'))
        for arg in kwargs.values():
            if not isinstance(arg, Param):
                raise ValueError(_('arg in params must be a Param'))
        self.args = args
        self.kwargs = kwargs


class Param:
    pass


class ParamOption(Param):
    __slots__ = ('todict',
                 'option',
                 'notraisepropertyerror',
                 'raisepropertyerror')
    def __init__(self,
                 option: 'Option',
                 notraisepropertyerror: bool=False,
                 raisepropertyerror: bool=False,
                 todict: bool=False) -> None:
        if __debug__ and not hasattr(option, 'impl_is_symlinkoption'):
            raise ValueError(_('paramoption needs an option not {}').format(type(option)))
        if option.impl_is_symlinkoption():
            cur_opt = option.impl_getopt()
        else:
            cur_opt = option
        assert isinstance(notraisepropertyerror, bool), _('param must have a boolean not a {} for notraisepropertyerror').format(type(notraisepropertyerror))
        assert isinstance(raisepropertyerror, bool), _('param must have a boolean not a {} for raisepropertyerror').format(type(raisepropertyerror))
        self.todict = todict
        self.option = cur_opt
        self.notraisepropertyerror = notraisepropertyerror
        self.raisepropertyerror = raisepropertyerror


class ParamSelfOption(Param):
    __slots__ = ('todict', 'whole')
    def __init__(self,
                 todict: bool=False,
                 whole: bool=undefined) -> None:
        """whole: send all value for a multi, not only indexed value"""
        self.todict = todict
        if whole is not undefined:
            self.whole = whole


class ParamValue(Param):
    __slots__ = ('value',)
    def __init__(self, value):
        self.value = value


class ParamIndex(Param):
    __slots__ = tuple()


class ParamSuffix(Param):
    __slots__ = tuple()


class Calculation:
    __slots__ = ('function',
                 'params',
                 'help_function',
                 '_has_index',
                 'warnings_only')
    def __init__(self,
                 function: Callable,
                 params: Params=Params(),
                 help_function: Optional[Callable]=None,
                 warnings_only: bool=False):
        assert isinstance(function, Callable), _('first argument ({0}) must be a function').format(function)
        if help_function:
            assert isinstance(help_function, Callable), _('help_function ({0}) must be a function').format(help_function)
            self.help_function = help_function
        else:
            self.help_function = None
        self.function = function
        self.params = params
        for arg in chain(self.params.args, self.params.kwargs.values()):
            if isinstance(arg, ParamIndex):
                self._has_index = True
                break
        if warnings_only is True:
            self.warnings_only = warnings_only

    async def execute(self,
                option_bag: OptionBag,
                leadership_must_have_index: bool=False,
                orig_value: Any=undefined,
                allow_raises=False) -> Any:
        return await carry_out_calculation(option_bag.option,
                                           callback=self.function,
                                           callback_params=self.params,
                                           index=option_bag.index,
                                           config_bag=option_bag.config_bag,
                                           leadership_must_have_index=leadership_must_have_index,
                                           orig_value=orig_value,
                                           allow_raises=allow_raises)

    async def help(self,
                   option_bag: OptionBag,
                   leadership_must_have_index: bool=False) -> str:
        if not self.help_function:
            return await self.execute(option_bag,
                                      leadership_must_have_index=leadership_must_have_index)
        return await carry_out_calculation(option_bag.option,
                                           callback=self.help_function,
                                           callback_params=self.params,
                                           index=option_bag.index,
                                           config_bag=option_bag.config_bag,
                                           leadership_must_have_index=leadership_must_have_index)

    def has_index(self, current_option):
        if hasattr(self, '_has_index'):
            return self._has_index
        self._has_index = False
        for arg in chain(self.params.args, self.params.kwargs.values()):
            if isinstance(arg, ParamOption) and arg.option.impl_get_leadership() and \
                    arg.option.impl_get_leadership().in_same_group(current_option):
                self._has_index = True
                break
        return self._has_index


class Break(Exception):
    pass


async def manager_callback(callbk: Union[ParamOption, ParamValue],
                           option,
                           index: Optional[int],
                           orig_value,
                           config_bag: ConfigBag,
                           leadership_must_have_index: bool) -> Any:
    """replace Param by true value"""
    def calc_index(callbk, index, same_leadership):
        if index is not None:
            if hasattr(callbk, 'whole'):
                whole = callbk.whole
            else:
                # if value is same_leadership, follower are isolate by default
                # otherwise option is a whole option
                whole = not same_leadership
            if not whole:
                return index
        return None

    async def calc_self(callbk, option, index, value, config_bag):
        # index must be apply only if follower
        is_follower = option.impl_is_follower()
        apply_index = calc_index(callbk, index, is_follower)
        if value is undefined or (apply_index is None and is_follower):
            if config_bag is undefined:
                return undefined
            path = option.impl_getpath()
            option_bag = await get_option_bag(config_bag,
                                              option,
                                              apply_index,
                                              True)
            new_value = await get_value(callbk, option_bag, path)
            if apply_index is None and is_follower:
                new_value[index] = value
            value = new_value
        elif apply_index is not None and not is_follower:
            value = value[apply_index]
        return value

    async def get_value(callbk, option_bag, path):
        try:
            # get value
            value = await config_bag.context.getattr(path,
                                                     option_bag)
        except PropertiesOptionError as err:
            # raise PropertiesOptionError (which is catched) because must not add value None in carry_out_calculation
            if callbk.notraisepropertyerror or callbk.raisepropertyerror:
                raise err
            raise ConfigError(_('unable to carry out a calculation for "{}"'
                                ', {}').format(option.impl_get_display_name(), err), err)
        except ValueError as err:
            raise ValueError(_('the option "{0}" is used in a calculation but is invalid ({1})').format(option_bag.option.impl_get_display_name(), err))
        return value

    async def get_option_bag(config_bag,
                             opt,
                             index_,
                             self_calc):
        # don't validate if option is option that we tried to validate
        config_bag = config_bag.copy()
        config_bag.properties = config_bag.true_properties - {'warnings'}
        config_bag.set_permissive()
        #config_bag.properties -= {'warnings'}
        option_bag = OptionBag()
        option_bag.set_option(opt,
                              index_,
                              config_bag)
        if not self_calc:
            option_bag.properties = await config_bag.context.cfgimpl_get_settings().getproperties(option_bag)
        else:
            option_bag.config_bag.unrestraint()
            option_bag.config_bag.remove_validation()
            # if we are in properties calculation, cannot calculated properties
            option_bag.properties = await config_bag.context.cfgimpl_get_settings().getproperties(option_bag,
                                                                                                  apply_requires=False)
        return option_bag

    if isinstance(callbk, ParamValue):
        return callbk.value

    if isinstance(callbk, ParamIndex):
        return index

    if isinstance(callbk, ParamSuffix):
        if not option.issubdyn():
            raise ConfigError('option "{}" is not in a dynoptiondescription'.format(option.impl_get_display_name()))
        return option.impl_getsuffix()

    if isinstance(callbk, ParamSelfOption):
        if leadership_must_have_index and option.impl_get_leadership() and index is None:
            raise Break()
        value = await calc_self(callbk, option, index, orig_value, config_bag)
        if not callbk.todict:
            return value
        return {'name': option.impl_get_display_name(),
                'value': value}

    # it's ParamOption
    callbk_option = callbk.option
    if callbk_option.issubdyn():
        callbk_option = callbk_option.to_dynoption(option.rootpath,
                                                   option.impl_getsuffix(),
                                                   callbk_option.getsubdyn())
    if leadership_must_have_index and callbk_option.impl_get_leadership() and index is None:
        raise Break()
    if config_bag is undefined:
        return undefined
    if index is not None and callbk_option.impl_get_leadership() and \
            callbk_option.impl_get_leadership().in_same_group(option):
        if not callbk_option.impl_is_follower():
            # leader
            index_ = None
            with_index = True
        else:
            # follower
            index_ = index
            with_index = False
    else:
        index_ = None
        with_index = False
    path = callbk_option.impl_getpath()
    option_bag = await get_option_bag(config_bag,
                                      callbk_option,
                                      index_,
                                      False)
    value = await get_value(callbk, option_bag, path)
    if with_index:
        value = value[index]
    if not callbk.todict:
        return value
    return {'name': callbk_option.impl_get_display_name(),
            'value': value}


async def carry_out_calculation(option,
                                callback: Callable,
                                callback_params: Optional[Params],
                                index: Optional[int],
                                config_bag: Optional[ConfigBag],
                                orig_value=undefined,
                                leadership_must_have_index: bool=False,
                                allow_raises: int=False):
    """a function that carries out a calculation for an option's value

    :param option: the option
    :param callback: the name of the callback function
    :type callback: str
    :param callback_params: the callback's parameters
                            (only keyword parameters are allowed)
    :type callback_params: dict
    :param index: if an option is multi, only calculates the nth value
    :type index: int
    :param allow_raises: to know if carry_out_calculation is used to validate a value

    The callback_params is a dict. Key is used to build args (if key is '')
    and kwargs (otherwise). Values are tuple of:
    - values
    - tuple with option and boolean's force_permissive (True when don't raise
    if PropertiesOptionError)
    Values could have multiple values only when key is ''."""
    def fake_items(iterator):
        return ((None, i) for i in iterator)
    args = []
    kwargs = {}
    if callback_params:
        for key, callbk in chain(fake_items(callback_params.args), callback_params.kwargs.items()):
            try:
                value = await manager_callback(callbk,
                                               option,
                                               index,
                                               orig_value,
                                               config_bag,
                                               leadership_must_have_index)
                if value is undefined:
                    return undefined
                if key is None:
                    args.append(value)
                else:
                    kwargs[key] = value
            except PropertiesOptionError as err:
                if callbk.raisepropertyerror:
                    raise err
                if callbk.todict:
                    if key is None:
                        args.append({'propertyerror': str(err)})
                    else:
                        kwargs[key] = {'propertyerror': str(err)}
            except Break:
                continue
    ret = calculate(option,
                    callback,
                    allow_raises,
                    args,
                    kwargs)
    if isinstance(ret, list) and not option.impl_is_dynoptiondescription() and \
            option.impl_is_follower():
        if args or kwargs:
            raise LeadershipError(_('the "{}" function with positional arguments "{}" '
                                    'and keyword arguments "{}" must not return '
                                    'a list ("{}") for the follower option "{}"'
                                    '').format(callback.__name__,
                                               args,
                                               kwargs,
                                               ret,
                                               option.impl_get_display_name()))
        else:
            raise LeadershipError(_('the "{}" function must not return a list ("{}") '
                                    'for the follower option "{}"'
                                    '').format(callback.__name__,
                                               ret,
                                               option.impl_get_display_name()))
    return ret


def calculate(option,
              callback: Callable,
              allow_raises: bool,
              args,
              kwargs):
    """wrapper that launches the 'callback'

    :param callback: callback function
    :param args: in the callback's arity, the unnamed parameters
    :param kwargs: in the callback's arity, the named parameters

    """
    try:
        return callback(*args, **kwargs)
    except ValueError as err:
        if allow_raises:
            raise err
        error = err
    except ValueWarning as err:
        raise err
    except Exception as err:
        # import traceback
        # traceback.print_exc()
        error = err
    if args or kwargs:
        msg = _('unexpected error "{0}" in function "{1}" with arguments "{3}" and "{4}" '
                'for option "{2}"').format(str(error),
                                           callback.__name__,
                                           option.impl_get_display_name(),
                                           args,
                                           kwargs)
    else:
        msg = _('unexpected error "{0}" in function "{1}" for option "{2}"'
                '').format(str(error),
                           callback.__name__,
                           option.impl_get_display_name())
    del error
    raise ConfigError(msg)
