# Copyright (C) 2018-2020 Team tiramisu (see AUTHORS for all contributors)
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
from typing import Any, List, Optional
from operator import add, mul, sub, truediv
from ipaddress import ip_address, ip_interface, ip_network
from .i18n import _
from .setting import undefined
from .error import display_list


def valid_network_netmask(network: str,
                          netmask: str):
    """FIXME
    """
    if isinstance(network, dict):
        network_value = network['value']
        network_display_name = '({})'.format(network['name'])
    else:
        network_value = network
        network_display_name = ''
    if None in [network_value, netmask]:
        return
    try:
        ip_network('{0}/{1}'.format(network_value, netmask))
    except ValueError:
        raise ValueError(_('network "{0}" {1}does not match with this netmask').format(network_value,
                                                                                       network_display_name))

def valid_ip_netmask(ip: str,
                     netmask: str):
    if isinstance(ip, dict):
        ip_value = ip['value']
        ip_display_name = '({})'.format(ip['name'])
    else:
        ip_value = ip
        ip_display_name = ''
    if None in [ip_value, netmask]:
        return
    ip_netmask = ip_interface('{0}/{1}'.format(ip_value, netmask))
    if ip_netmask.ip == ip_netmask.network.network_address:
        raise ValueError(_('IP \"{0}\" {1}with this netmask is in fact a network address').format(ip_value, ip_display_name))
    elif ip_netmask.ip == ip_netmask.network.broadcast_address:
        raise ValueError(_('IP \"{0}\" {1}with this netmask is in fact a broacast address').format(ip_value, ip_display_name))


# FIXME CIDR ?
def valid_broadcast(network: 'NetworkOption',
                    netmask: 'NetmaskOption',
                    broadcast: 'BroadcastOption'):
    if isinstance(network, dict):
        network_value = network['value']
        network_display_name = ' ({})'.format(network['name'])
    else:
        network_value = network
        network_display_name = ''
    if isinstance(netmask, dict):
        netmask_value = netmask['value']
        netmask_display_name = ' ({})'.format(netmask['name'])
    else:
        netmask_value = netmask
        netmask_display_name = ''
    if ip_network('{0}/{1}'.format(network, netmask)).broadcast_address != ip_address(broadcast):
        raise ValueError(_('broadcast invalid with network {0}{1} and netmask {2}{3}'
                           '').format(network_value,
                                      network_display_name,
                                      netmask_value,
                                      netmask_display_name))


def valid_in_network(ip,
                     network,
                     netmask=None):
    if isinstance(network, dict):
        network_value = network['value']
        network_display_name = ' ({})'.format(network['name'])
    else:
        network_value = network
        network_display_name = ''
    if isinstance(netmask, dict):
        netmask_value = netmask['value']
        netmask_display_name = ' ({})'.format(netmask['name'])
    else:
        netmask_value = netmask
        netmask_display_name = ''
    if network_value is None:
        return
    if '/' in network_value:
        network_obj = ip_network('{0}'.format(network_value))
    else:
        if netmask_value is None:
            return
        network_obj = ip_network('{0}/{1}'.format(network_value,
                                                  netmask_value))
    if ip_interface(ip) not in network_obj:
        if netmask is None:
            msg = _('this IP is not in network {0}{1}').format(network_value,
                                                               network_display_name)
        else:
            msg = _('this IP is not in network {0}{1} with netmask {2}{3}').format(network_value,
                                                                                   network_display_name,
                                                                                   netmask_value,
                                                                                   netmask_display_name)
        raise ValueError(msg)

    # test if ip is not network/broadcast IP
    ip_netmask = ip_interface('{0}/{1}'.format(ip, network_obj.netmask))
    if ip_netmask.ip == ip_netmask.network.network_address:
        if netmask is None:
            msg = _('this IP with the network {0}{1} is in fact a network address').format(network_value,
                                                                                           network_display_name)
        else:
            msg = _('this IP with the netmask {0}{1} is in fact a network address').format(netmask_value,
                                                                                           netmask_display_name)
        raise ValueError(msg)
    elif ip_netmask.ip == ip_netmask.network.broadcast_address:
        if netmask is None:
            msg = _('this IP with the network {0}{1} is in fact a broadcast address').format(network_value,
                                                                                             network_display_name)
        else:
            msg = _('this IP with the netmask {0}{1} is in fact a broadcast address').format(netmask_value,
                                                                                             netmask_display_name)
        raise ValueError(msg)


def valid_not_equal(*values):
    equal = set()
    for idx, val in enumerate(values[1:]):
        if isinstance(val, dict):
            if 'propertyerror' in val:
                continue
            tval = val['value']
        else:
            tval = val
        if values[0] == tval is not None:
            if isinstance(val, dict):
                if equal is True:
                    equal = set()
                equal.add(val['name'])
            elif not equal:
                equal = True
    if equal:
        if equal is not True:
            msg = _('value is identical to {}').format(display_list(list(equal), add_quote=True))
        else:
            msg = _('value is identical')
        raise ValueError(msg)


class CalcValue:
    def __call__(self,
                 *args: List[Any],
                 multi: bool=False,
                 default: Any=undefined,
                 condition: Any=undefined,
                 no_condition_is_invalid: bool=False,
                 expected: Any=undefined,
                 condition_operator: str='AND',
                 reverse_condition: bool=False,
                 allow_none: bool=False,
                 remove_duplicate_value: bool=False,
                 join: Optional[str]=None,
                 min_args_len: Optional[int]=None,
                 operator: Optional[str]=None,
                 index: Optional[int]=None,
                 **kwargs) -> Any:
        """calculate value
        :param args: list of value
        :param multi: value returns must be a list of value
        :param default: default value if condition is not matched or if args is empty
                        if there is more than one default value, set default_0, default_1, ...
        :param condition: test if condition is equal to expected value
                          if there is more than one condition, set condition_0, condition_1, ...
        :param expected: value expected for all conditions
                         if expected value is different between condition, set expected_0, expected_1, ...
        :param no_condition_is_invalid: if no condition and not condition_0, condition_1, ... (for
                                        example if option is disabled) consider that condition not matching
        :param condition_operator: OR or AND operator for condition
        :param allow_none: if False, do not return list in None is present in list
        :param remove_duplicate_value: if True, remote duplicated value
        :param join: join all args with specified characters
        :param min_args_len: if number of arguments is smaller than this value, return default value
        :param operator: 'add', 'mul', 'div' or 'sub' all args (args must be integer value)
        :param index: index for follower

        examples:
        * you want to copy value from an option to an other option:
        >>> from tiramisu import calc_value, StrOption, OptionDescription, Config, Params, ParamOption
        >>> val1 = StrOption('val1', '', 'val1')
        >>> val2 = StrOption('val2', '', callback=calc_value, callback_params=Params(ParamOption(val1)))
        >>> od = OptionDescription('root', '', [val1, val2])
        >>> cfg = Config(od)
        >>> cfg.value.dict()
        {'val1': 'val1', 'val2': 'val1'}

        * you want to copy values from two options in one multi option
        >>> from tiramisu import calc_value, StrOption, OptionDescription, Config, Params, ParamOption, ParamValue
        >>> val1 = StrOption('val1', "", 'val1')
        >>> val2 = StrOption('val2', "", 'val2')
        >>> val3 = StrOption('val3', "", multi=True, callback=calc_value, callback_params=Params((ParamOption(val1), ParamOption(val2)), multi=ParamValue(True)))
        >>> od = OptionDescription('root', '', [val1, val2, val3])
        >>> cfg = Config(od)
        >>> cfg.value.dict()
        {'val1': 'val1', 'val2': 'val2', 'val3': ['val1', 'val2']}

        * you want to copy a value from an option if it not disabled, otherwise set 'default_value'
        >>> from tiramisu import calc_value, StrOption, OptionDescription, Config, Params, ParamOption, ParamValue
        >>> val1 = StrOption('val1', '', 'val1')
        >>> val2 = StrOption('val2', '', callback=calc_value, callback_params=Params(ParamOption(val1, True), default=ParamValue('default_value')))
        >>> od = OptionDescription('root', '', [val1, val2])
        >>> cfg = Config(od)
        >>> cfg.property.read_write()
        >>> cfg.value.dict()
        {'val1': 'val1', 'val2': 'val1'}
        >>> cfg.option('val1').property.add('disabled')
        >>> cfg.value.dict()
        {'val2': 'default_value'}

        * you want to copy value from an option if an other is True, otherwise set 'default_value'
        >>> from tiramisu import calc_value, BoolOption, StrOption, OptionDescription, Config, Params, ParamOption, ParamValue
        >>> boolean = BoolOption('boolean', '', True)
        >>> val1 = StrOption('val1', '', 'val1')
        >>> val2 = StrOption('val2', '', callback=calc_value, callback_params=Params(ParamOption(val1, True),
        ...                                                                          default=ParamValue('default_value'),
        ...                                                                          condition=ParamOption(boolean),
        ...                                                                          expected=ParamValue(True)))
        >>> od = OptionDescription('root', '', [boolean, val1, val2])
        >>> cfg = Config(od)
        >>> cfg.property.read_write()
        >>> cfg.value.dict()
        {'boolean': True, 'val1': 'val1', 'val2': 'val1'}
        >>> cfg.option('boolean').value.set(False)
        >>> cfg.value.dict()
        {'boolean': False, 'val1': 'val1', 'val2': 'default_value'}

        * you want to copy option even if None is present
        >>> from tiramisu import calc_value, StrOption, OptionDescription, Config, Params, ParamOption, ParamValue
        >>> val1 = StrOption('val1', "", 'val1')
        >>> val2 = StrOption('val2', "")
        >>> val3 = StrOption('val3', "", multi=True, callback=calc_value, callback_params=Params((ParamOption(val1), ParamOption(val2)), multi=ParamValue(True), allow_none=ParamValue(True)))
        >>> od = OptionDescription('root', '', [val1, val2, val3])
        >>> cfg = Config(od)
        >>> cfg.value.dict()
        {'val1': 'val1', 'val2': None, 'val3': ['val1', None]}

        * you want uniq value
        >>> from tiramisu import calc_value, StrOption, OptionDescription, Config, Params, ParamOption, ParamValue
        >>> val1 = StrOption('val1', "", 'val1')
        >>> val2 = StrOption('val2', "", 'val1')
        >>> val3 = StrOption('val3', "", multi=True, callback=calc_value, callback_params=Params((ParamOption(val1), ParamOption(val2)), multi=ParamValue(True), remove_duplicate_value=ParamValue(True)))
        >>> od = OptionDescription('root', '', [val1, val2, val3])
        >>> cfg = Config(od)
        >>> cfg.value.dict()
        {'val1': 'val1', 'val2': 'val1', 'val3': ['val1']}

        * you want to join two values with '.'
        >>> from tiramisu import calc_value, StrOption, OptionDescription, Config, Params, ParamOption, ParamValue
        >>> val1 = StrOption('val1', "", 'val1')
        >>> val2 = StrOption('val2', "", 'val2')
        >>> val3 = StrOption('val3', "", callback=calc_value, callback_params=Params((ParamOption(val1), ParamOption(val2)), join=ParamValue('.')))
        >>> od = OptionDescription('root', '', [val1, val2, val3])
        >>> cfg = Config(od)
        >>> cfg.value.dict()
        {'val1': 'val1', 'val2': 'val2', 'val3': 'val1.val2'}

        * you want join three values, only if almost three values are set
        >>> from tiramisu import calc_value, StrOption, OptionDescription, Config, Params, ParamOption, ParamValue
        >>> val1 = StrOption('val1', "", 'val1')
        >>> val2 = StrOption('val2', "", 'val2')
        >>> val3 = StrOption('val3', "", 'val3')
        >>> val4 = StrOption('val4', "", callback=calc_value, callback_params=Params((ParamOption(val1), ParamOption(val2), ParamOption(val3, True)), join=ParamValue('.'), min_args_len=ParamValue(3)))
        >>> od = OptionDescription('root', '', [val1, val2, val3, val4])
        >>> cfg = Config(od)
        >>> cfg.property.read_write()
        >>> cfg.value.dict()
        {'val1': 'val1', 'val2': 'val2', 'val3': 'val3', 'val4': 'val1.val2.val3'}
        >>> cfg.option('val3').property.add('disabled')
        >>> cfg.value.dict()
        {'val1': 'val1', 'val2': 'val2', 'val4': ''}

        * you want to add all values
        >>> from tiramisu import calc_value, IntOption, OptionDescription, Config, Params, ParamOption, ParamValue
        >>> val1 = IntOption('val1', "", 1)
        >>> val2 = IntOption('val2', "", 2)
        >>> val3 = IntOption('val3', "", callback=calc_value, callback_params=Params((ParamOption(val1), ParamOption(val2)), operator=ParamValue('add')))
        >>> od = OptionDescription('root', '', [val1, val2, val3])
        >>> cfg = Config(od)
        >>> cfg.value.dict()
        {'val1': 1, 'val2': 2, 'val3': 3}

        """
        self.args = args
        self.condition = condition
        self.expected = expected
        self.condition_operator = condition_operator
        self.reverse_condition = reverse_condition
        self.kwargs = kwargs
        self.no_condition_is_invalid = no_condition_is_invalid
        value = self.get_value(default,
                               min_args_len)
        if not multi:
            if join is not None:
                value = join.join(value)
            elif value and operator:
                new_value = value[0]
                op = {'mul': mul,
                      'add': add,
                      'div': truediv,
                      'sub': sub}[operator]
                for val in value[1:]:
                    new_value = op(new_value, val)
                value = new_value
            elif value == []:
                value = None
            else:
                value = value[0]
                if isinstance(value, list) and index is not None:
                    if len(value) > index:
                        value = value[index]
                    else:
                        value = None
        elif None in value and not allow_none:
            value = []
        elif remove_duplicate_value:
            new_value = []
            for val in value:
                if val not in new_value:
                    new_value.append(val)
            value = new_value
        return value

    def value_from_kwargs(self,
                          value: Any,
                          pattern: str,
                          to_dict: bool=False,
                          empty_test=undefined) -> Any:
        # if value attribute exist return it's value
        # otherwise pattern_0, pattern_1, ...
        # otherwise undefined
        if value is not empty_test:
            if to_dict == 'all':
                returns = {None: value}
            else:
                returns = value
        else:
            kwargs_matches = {}
            len_pattern = len(pattern)
            for key in self.kwargs.keys():
                if key.startswith(pattern):
                    index = int(key[len_pattern:])
                    pattern_value = self.kwargs[key]
                    if isinstance(pattern_value, dict):
                        pattern_value = pattern_value['value']
                    kwargs_matches[index] = pattern_value
            if not kwargs_matches:
                returns = undefined
            else:
                keys = sorted(kwargs_matches)
                if to_dict:
                    returns = {}
                else:
                    returns = []
                for key in keys:
                    if to_dict:
                        returns[key] = kwargs_matches[key]
                    else:
                        returns.append(kwargs_matches[key])
        return returns

    def is_condition_matches(self,
                             condition_value):
        calculated_conditions = self.value_from_kwargs(condition_value,
                                                       'condition_',
                                                       to_dict='all')
        if calculated_conditions is undefined:
            is_matches = not self.no_condition_is_invalid
        else:
            is_matches = None
            calculated_expected = self.value_from_kwargs(self.expected,
                                                         'expected_',
                                                         to_dict=True)
            calculated_reverse = self.value_from_kwargs(self.reverse_condition,
                                                        'reverse_condition_',
                                                        to_dict=True,
                                                        empty_test=False)
            for idx, calculated_condition in calculated_conditions.items():
                if isinstance(calculated_expected, dict):
                    if idx is not None:
                        current_matches = calculated_condition == calculated_expected[idx]
                    else:
                        current_matches = calculated_condition in calculated_expected.values()
                else:
                    current_matches = calculated_condition == calculated_expected
                if isinstance(calculated_reverse, dict) and idx in calculated_reverse:
                    reverse_condition = calculated_reverse[idx]
                else:
                    reverse_condition = False
                if is_matches is None:
                    is_matches = current_matches
                if self.condition_operator == 'AND':
                    is_matches = is_matches and current_matches
                    if reverse_condition:
                        is_matches = not is_matches
                    if not is_matches:
                        break
                elif self.condition_operator == 'OR':
                    is_matches = is_matches or current_matches
                    if reverse_condition:
                        is_matches = not is_matches
                    if is_matches:
                        break
                else:
                    raise ValueError(_('unexpected {} condition_operator in calc_value').format(self.condition_operator))
            is_matches = is_matches and not self.reverse_condition \
                         or not is_matches and self.reverse_condition
        return is_matches

    def get_value(self,
                  default,
                  min_args_len):
        if isinstance(self.condition, dict):
            if 'value' in self.condition:
                condition_value = self.condition['value']
            else:
                condition_value = undefined
        else:
            condition_value = self.condition
        condition_matches = self.is_condition_matches(condition_value)
        if not condition_matches:
            # force to default
            value = []
        else:
            value = self.get_args()
        if min_args_len and not len(value) >= min_args_len:
            value = []
        if value == []:
            # default value
            new_default = self.value_from_kwargs(default,
                                                 'default_')
            if new_default is not undefined:
                if not isinstance(new_default, list):
                    value = [new_default]
                else:
                    value = new_default
        return value

    def get_args(self):
        return list(self.args)


class CalcValuePropertyHelp(CalcValue):
    def get_name(self):
        return self.condition['name']

    def get_indexed_name(self, index):
        return self.kwargs.get(f'condition_{index}')['name']

    def has_condition_kwargs(self):
        for condition in self.kwargs:
            if condition.startswith('condition_'):
                return True
        return False

    def build_arg(self, name, value):
        #if isinstance(option, tuple):
        #    if not reverse:
        #        msg = _('the calculated value is {0}').format(display_value)
        #    else:
        #        msg = _('the calculated value is not {0}').format(display_value)
        #else:
        if not self.reverse_condition:
            msg = _('the value of "{0}" is {1}').format(name, value)
        else:
            msg = _('the value of "{0}" is not {1}').format(name, value)
        return msg

    def get_args(self):
        args = super().get_args()
        if args:
            if len(self.args) != 1:
                raise ValueError(_('only one property is allowed for a calculation'))
            action = args[0]
            calculated_expected = self.value_from_kwargs(self.expected,
                                                         'expected_',
                                                         to_dict=True)
            if self.condition is not undefined:
                if 'propertyerror' in self.condition:
                    msg = self.condition['propertyerror']
                else:
                    name = self.get_name()
                    if isinstance(calculated_expected, dict):
                        calc_values = calculated_expected.values()
                    else:
                        calc_values = [calculated_expected]
                    display_value = display_list([str(val) for val in calc_values],
                                                 'or',
                                                 add_quote=True)
                    msg = self.build_arg(name, display_value)
            elif self.has_condition_kwargs():
                msgs = []
                for key, value in calculated_expected.items():
                    name = self.get_indexed_name(key)
                    msgs.append(self.build_arg(name, f'"{value}"'))
                msg = display_list(msgs, self.condition_operator.lower())
            else:
                return [(action, f'"{action}"')]
            return [(action, f'"{action}" ({msg})')]
        return
        ##    calc_properties.setdefault(action, []).append(msg)


calc_value = CalcValue()
calc_value.__name__ = 'calc_value'
calc_value_property_help = CalcValuePropertyHelp()
calc_value_property_help.__name__ = 'calc_value_property_help'
