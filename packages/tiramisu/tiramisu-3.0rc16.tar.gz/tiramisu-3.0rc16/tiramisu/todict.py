# -*- coding: utf-8 -*-

import warnings
import sys
from copy import copy
from itertools import chain
from .error import ValueWarning, ValueErrorWarning, PropertiesOptionError, ConfigError
from .setting import undefined
from . import SynDynOption, RegexpOption, ChoiceOption, ParamOption
from .i18n import _


TYPES = {'SymLinkOption': 'symlink',
         'IntOption': 'integer',
         'FloatOption': 'integer',
         'ChoiceOption': 'choice',
         'BoolOption': 'boolean',
         'PasswordOption': 'password',
         'PortOption': 'integer',
         'DateOption': 'date',
         'DomainnameOption': 'domainname',
         'StrOption': 'string'
         }
INPUTS = ['string',
          'integer',
          'filename',
          'password',
          'email',
          'username',
          'ip',
          'domainname']


# return always warning (even if same warning is already returned)
warnings.simplefilter("always", ValueWarning)
warnings.simplefilter("always", ValueErrorWarning)


class Callbacks(object):
    def __init__(self, tiramisu_web):
        self.tiramisu_web = tiramisu_web
        self.clearable = tiramisu_web.clearable
        self.remotable = tiramisu_web.remotable
        self.callbacks = []

    async def add(self,
                  path,
                  childapi,
                  schema,
                  force_store_value):
        if self.remotable == 'all' or await childapi.option.isoptiondescription():
            return
        callback, callback_params = await childapi.option.callbacks()
        if callback is None:  # FIXME ? and force_store_value and self.clearable != 'all':
            return
        self.callbacks.append((callback, callback_params, path, childapi, schema, force_store_value))

    async def process_properties(self, form):
        for callback, callback_params, path, childapi, schema, force_store_value in self.callbacks:
            if await childapi.option.isfollower():
                await self.tiramisu_web.set_remotable(path, form, childapi)
                continue
            has_option = False
            if callback_params is not None:
                for callback_param in chain(callback_params.args, callback_params.kwargs.values()):
                    if isinstance(callback_param, ParamOption):
                        has_option = True
                        if 'expire' in await childapi.option.properties():
                            await self.tiramisu_web.set_remotable(callback_param.option.impl_getpath(), form)
            if not has_option and form.get(path, {}).get('remote', False) == False:
                if 'expire' in await childapi.option.properties():
                    await self.tiramisu_web.set_remotable(path, form, childapi)
                elif await childapi.owner.isdefault():
                    # get calculated value and set clearable
                    schema[path]['value'] = await childapi.value.get()
                    if self.clearable == 'minimum':
                        form.setdefault(path, {})['clearable'] = True

    def manage_callbacks(self, form):
        pass
        #for callback, callback_params, path, childapi, schema, force_store_value in self.callbacks:
        #    if callback_params is not None:
        #        for callback_param in chain(callback_params.args, callback_params.kwargs.values()):
        #            if isinstance(callback_param, ParamOption) and callback.__name__ == 'tiramisu_copy':
        #                opt_path = callback_param.option.impl_getpath()
        #                if form.get(opt_path, {}).get('remote') is not True:
        #                    form.setdefault(opt_path, {})
        #                    form[opt_path].setdefault('copy', []).append(path)

    async def process(self,
                      form):
        await self.process_properties(form)
        self.manage_callbacks(form)


class Consistencies(object):
    def __init__(self, tiramisu_web):
        self.not_equal = {}
        self.tiramisu_web = tiramisu_web

    async def add(self, path, childapi, form):
        return
        if not await childapi.option.isoptiondescription():
            for consistency in await childapi.option.consistencies():
                cons_id, func, all_cons_opts, params = consistency
                if func == '_cons_not_equal' and params.get('transitive', True) is True:
                    options_path = []
                    for option in all_cons_opts:
                        options_path.append(option()._path)
                    for idx, option in enumerate(all_cons_opts):
                        option = option()
                        paths = options_path.copy()
                        paths.pop(idx)
                        warnings_only = params.get('warnings_only') or getattr(option, '_warnings_only', False)
                        self.not_equal.setdefault(option._path, {}).setdefault(warnings_only, []).extend(paths)
                else:
                    for option in all_cons_opts:
                        await self.tiramisu_web.set_remotable(option()._path, form)

    async def process(self, form):
        for path in self.not_equal:
            if self.tiramisu_web.is_remote(path, form):
                continue
            if path not in form:
                form[path] = {}
            for warnings_only in self.not_equal[path]:
                options = self.not_equal[path][warnings_only]
                if 'not_equal' not in form[path]:
                    form[path]['not_equal'] = []
                obj = {'options': options}
                if warnings_only:
                    obj['warnings'] = True
                form[path]['not_equal'].append(obj)


class Requires(object):
    def __init__(self, tiramisu_web):
        self.requires = {}
        self.options = {}
        self.tiramisu_web = tiramisu_web
        self.action_hide = self.tiramisu_web.config._config_bag.properties

    async def set_master_remote(self, childapi, path, form):
        if await childapi.option.isoptiondescription():
            isfollower = False
        else:
            isfollower = await childapi.option.isfollower()
        if isfollower:
            parent_path = path.rsplit('.', 1)[0]
            parent = await self.tiramisu_web.config.unrestraint.option(parent_path)
            leader = await parent.list()[0]
            await self.tiramisu_web.set_remotable(await leader.option.path(), form, leader)

    async def manage_requires(self,
                              childapi,
                              path,
                              form,
                              current_action):
        for requires in await childapi.option.properties(uncalculated=True):
            if not isinstance(requires, str):
                option = requires.params.kwargs['condition'].option
                expected = [requires.params.kwargs['expected'].value]
                action = requires.params.args[0].value
                if 'reverse_condition' in requires.params.kwargs:
                    inverse = requires.params.kwargs['reverse_condition'].value
                else:
                    inverse = False
                transitive = True
                same_action = True
                operator = 'or'
                if 1 == 1:
#            len_to_long = len(requires) > 1
#            for require in requires:
#                options, action, inverse, transitive, same_action, operator = require
#                if not len_to_long:
#                    len_to_long = len(options) > 1
#                for option, expected in options:
                    if isinstance(option, tuple):
                        for option_param in chain(option[1].args, option[1].kwargs.values()):
                            if isinstance(option_param, ParamOption):
                                await self.tiramisu_web.set_remotable(option_param.option.impl_getpath(), form)
                        await self.set_master_remote(childapi, path, form)
#                    elif len_to_long:
#                        self.tiramisu_web.set_remotable(option.impl_getpath(), form)
#                        self.set_master_remote(childapi, path, form)
                    else:
                        option_path = option.impl_getpath()
                        if action in self.action_hide:
                            require_option = self.tiramisu_web.config.unrestraint.option(option_path)
                            if transitive is False or same_action is False or operator == 'and':
                                # transitive to "False" not supported yet for a requirement
                                # same_action to "False" not supported yet for a requirement
                                # operator "and" not supported yet for a requirement
                                await self.tiramisu_web.set_remotable(option_path, form, require_option)
                                await self.set_master_remote(childapi, path, form)
#                            if require_option.option.requires():
#                                for reqs in require_option.option.requires():
#                                    for req in reqs:
#                                        for subopt, subexp in req[0]:
#                                            if not isinstance(subopt, tuple):
#                                                self.tiramisu_web.set_remotable(subopt.impl_getpath(), form)
#                                                self.set_master_remote(childapi, path, form)
                            if inverse:
                                act = 'show'
                                inv_act = 'hide'
                            else:
                                act = 'hide'
                                inv_act = 'show'
                            if option.get_type() == 'choice':
                                require_option = self.tiramisu_web.config.unrestraint.option(option_path)
                                values = await self.tiramisu_web.get_enum(require_option,
                                                                          await require_option.option.ismulti(),
                                                                          option_path,
                                                                          await require_option.option.properties())
                                for value in values:
                                    if value not in expected:
                                        self.requires.setdefault(path,
                                                                  {'expected': {}}
                                                                 )['expected'].setdefault(value,
                                                                                          {}).setdefault(inv_act,
                                                                                                         []).append(option_path)
                            if current_action is None:
                                current_action = action
                            elif current_action != action:
                                await self.tiramisu_web.set_remotable(option_path, form)
                                await self.set_master_remote(childapi, path, form)
                            for exp in expected:
                                self.requires.setdefault(path,
                                                         {'expected': {}}
                                                         )['expected'].setdefault(exp,
                                                                                  {}).setdefault(act,
                                                                                                 []).append(option_path)
                            self.requires[path].setdefault('default', {}).setdefault(inv_act, []).append(option_path)
                        else:
                            await self.tiramisu_web.set_remotable(option_path, form)
                            await self.set_master_remote(childapi, path, form)

    async def add(self, path, childapi, form):
        #collect id of all options
        child = await childapi.option.get()
        if isinstance(child, SynDynOption):
            child = child.opt
        self.options[child] = path
        current_action = None

        await self.manage_requires(childapi,
                                   path,
                                   form,
                                   current_action)

    async def process(self, form):
        dependencies = {}
        for path, values in self.requires.items():
            if 'default' in values:
                for option in values['default'].get('show', []):
                    if path == option:
                        await self.tiramisu_web.set_remotable(path, form)
                    if not self.tiramisu_web.is_remote(option, form):
                        dependencies.setdefault(option,
                                                {'default': {}, 'expected': {}}
                                                )['default'].setdefault('show', [])
                        if path not in dependencies[option]['default']['show']:
                            dependencies[option]['default']['show'].append(path)
                for option in values['default'].get('hide', []):
                    if path == option:
                        await self.tiramisu_web.set_remotable(path, form)
                    if not self.tiramisu_web.is_remote(option, form):
                        dependencies.setdefault(option,
                                                {'default': {}, 'expected': {}}
                                                )['default'].setdefault('hide', [])
                        if path not in dependencies[option]['default']['hide']:
                            dependencies[option]['default']['hide'].append(path)
            for expected, actions in values['expected'].items():
                if expected is None:
                    expected = ''
                for option in actions.get('show', []):
                    if path == option:
                        await self.tiramisu_web.set_remotable(path, form)
                    if not self.tiramisu_web.is_remote(option, form):
                        dependencies.setdefault(option,
                                                {'expected': {}}
                                                )['expected'].setdefault(expected,
                                                                         {}).setdefault('show', [])
                        if path not in dependencies[option]['expected'][expected]['show']:
                            dependencies[option]['expected'][expected]['show'].append(path)
                for option in actions.get('hide', []):
                    if path == option:
                        await self.tiramisu_web.set_remotable(path, form)
                    if not self.tiramisu_web.is_remote(option, form):
                        dependencies.setdefault(option,
                                                {'expected': {}}
                                                )['expected'].setdefault(expected,
                                                                         {}).setdefault('hide', [])
                        if path not in dependencies[option]['expected'][expected]['hide']:
                            dependencies[option]['expected'][expected]['hide'].append(path)
        for path, dependency in dependencies.items():
            form.setdefault(path, {})['dependencies'] = dependency


class TiramisuDict:

    # propriete:
    #   hidden
    #   mandatory
    #   editable

    # FIXME model:
    # #optionnel mais qui bouge
    # choices/suggests
    # warning
    #
    # #bouge
    # owner
    # properties

    def __init__(self,
                 config,
                 root=None,
                 clearable="all",
                 remotable="minimum"):
        self.config = config
        self.root = root
        self.requires = None
        self.callbacks = None
        self.consistencies = None
        #all, minimum, none
        self.clearable = clearable
        #all, minimum, none
        self.remotable = remotable

    async def add_help(self,
                       obj,
                       childapi):
        hlp = await childapi.information.get('help', None)
        if hlp is not None:
            obj['help'] = hlp

    async def get_list(self, root, subchildapi):
        ret = []
        for childapi in await subchildapi.list('all'):
            childname = await childapi.option.name()
            if root is None:
                path = childname
            else:
                path = root + '.' + childname
            ret.append((path, childapi))
        return ret

    def is_remote(self, path, form):
        if self.remotable == 'all':
            return True
        else:
            return path in form and form[path].get('remote', False) == True

    async def set_remotable(self, path, form, childapi=None):
        if self.remotable == 'none':
            raise ValueError(_('option {} only works when remotable is not "none"').format(path))
        form.setdefault(path, {})['remote'] = True
        if childapi is None:
            childapi = self.config.unrestraint.option(path)
        if await childapi.option.isfollower():
            parent_path = path.rsplit('.', 1)[0]
            parent = await self.config.unrestraint.option(parent_path)
            leader = await parent.list()[0]
            form.setdefault(await leader.option.path(), {})['remote'] = True

    async def walk(self,
                   root,
                   subchildapi,
                   schema,
                   model,
                   form,
                   order,
                   updates_status,
                   init=False):
        error = None
        if init:
            if form is not None:
                self.requires = Requires(self)
                self.consistencies = Consistencies(self)
                self.callbacks = Callbacks(self)
        else:
            init = False
        try:
            if subchildapi is None:
                if root is None:
                    subchildapi = self.config.unrestraint.option
                else:
                    subchildapi = self.config.unrestraint.option(root)
                isleadership = False
            else:
                isleadership = await subchildapi.option.isleadership()
            leader_len = None
            for path, childapi in await self.get_list(root, subchildapi):
                if isleadership and leader_len is None:
                    leader_len = await childapi.value.len()
                    one_is_remote = False
                props_no_requires = set(await childapi.option.properties())
                if form is not None:
                    await self.requires.add(path,
                                            childapi,
                                            form)
                    await self.consistencies.add(path,
                                                 childapi,
                                                 form)
                    await self.callbacks.add(path,
                                             childapi,
                                             schema,
                                             'force_store_value' in props_no_requires)
                childapi_option = childapi.option
                if model is not None and await childapi.option.isoptiondescription() or not await childapi_option.issymlinkoption():
                    await self.gen_model(model,
                                         childapi,
                                         path,
                                         leader_len,
                                         updates_status)
                if order is not None:
                    order.append(path)
                if await childapi.option.isoptiondescription():
                    web_type = 'optiondescription'
                    if await childapi_option.isleadership():
                        type_ = 'array'
                    else:
                        type_ = 'object'
                    if schema is not None:
                        schema[path] = {'properties': {},
                                        'type': type_}
                        subschema = schema[path]['properties']
                    else:
                        subschema = schema
                    await self.walk(path,
                                    childapi,
                                    subschema,
                                    model,
                                    form,
                                    order,
                                    updates_status)
                else:
                    child = await childapi_option.get()
                    childtype = child.__class__.__name__
                    if childtype == 'SynDynOption':
                        childtype = child.opt.__class__.__name__
                    if await childapi_option.issymlinkoption():
                        web_type = 'symlink'
                        value = None
                        defaultmulti = None
                        is_multi = False
                    else:
                        web_type = await childapi_option.type()
                        value = await childapi.option.default()
                        if value == []:
                            value = None

                        is_multi = await childapi_option.ismulti()
                        if is_multi:
                            defaultmulti = await childapi_option.defaultmulti()
                            if defaultmulti == []:
                                defaultmulti = None
                        else:
                            defaultmulti = None

                    if schema is not None:
                        await self.gen_schema(schema,
                                              childapi,
                                              childapi_option,
                                              path,
                                              props_no_requires,
                                              value,
                                              defaultmulti,
                                              is_multi,
                                              web_type,
                                              form)
                    if form is not None:
                        await self.gen_form(form,
                                            web_type,
                                            path,
                                            child,
                                            childapi_option,
                                            childtype)
                if schema is not None:
                    if web_type != 'symlink':
                        schema[path]['title'] = await childapi_option.description()
                    await self.add_help(schema[path],
                                        childapi)
        except Exception as err:
            import traceback
            traceback.print_exc()
            if not init:
                raise err
            error = err
        if init and form is not None:
            await self.callbacks.process(form)
            await self.requires.process(form)
            await self.consistencies.process(form)
            del self.requires
            del self.consistencies
            del self.callbacks
        if error:
            msg = str(error)
            del error
            raise ConfigError(_('unable to transform tiramisu object to dict: {}').format(msg))


    async def gen_schema(self,
                         schema,
                         childapi,
                         childapi_option,
                         path,
                         props_no_requires,
                         value,
                         defaultmulti,
                         is_multi,
                         web_type,
                         form):
        schema[path] = {'type': web_type}
        if await childapi_option.issymlinkoption():
            sym_option = await childapi_option.get()
            schema[path]['opt_path'] = sym_option.impl_getopt().impl_getpath()
        else:
            if defaultmulti is not None:
                schema[path]['defaultmulti'] = defaultmulti

            if is_multi:
                schema[path]['isMulti'] = is_multi

            if await childapi_option.issubmulti():
                schema[path]['isSubMulti'] = True

            if 'auto_freeze' in props_no_requires:
                schema[path]['autoFreeze'] = True

            if web_type == 'choice':
                #values, values_params = childapi.value.callbacks()
                #if values_params:
                #    for values_param in chain(values_params.args, values_params.kwargs.values()):
                #        if isinstance(values_param, ParamOption):
                #            self.set_remotable(path, form, childapi)
                #            return
                schema[path]['enum'] = await self.get_enum(childapi,
                                                           is_multi,
                                                           path,
                                                           props_no_requires)
            if value is not None and not self.is_remote(path, form):
                schema[path]['value'] = value


    async def get_enum(self,
                       childapi,
                       is_multi,
                       path,
                       props_no_requires):
        values = await childapi.value.list()
        empty_is_required = not await childapi.option.isfollower() and is_multi
        if '' not in values and ((empty_is_required and not 'empty' in props_no_requires) or \
                (not empty_is_required and not 'mandatory' in props_no_requires)):
            values = [''] + list(values)
        return values

    async def gen_form(self,
                       form,
                       web_type,
                       path,
                       child,
                       childapi_option,
                       childtype):
        obj_form = {}
        if path in form:
            obj_form.update(form[path])
        if not await childapi_option.issymlinkoption():
            #if childapi_option.validator() != (None, None):
            #    obj_form['remote'] = True
            #    params = childapi_option.validator()[1]
            #    if params is not None:
            #        for param in chain(params.args, params.kwargs.values()):
            #            if isinstance(param, ParamOption):
            #                self.set_remotable(param.option.impl_getpath(), form)
            if self.clearable == 'all':
                obj_form['clearable'] = True
            if self.clearable != 'none':
                obj_form['clearable'] = True
            if self.remotable == 'all' or await childapi_option.has_dependency():
                obj_form['remote'] = True
            if childtype == 'IPOption' and (child.impl_get_extra('_private_only') or not child.impl_get_extra('_allow_reserved') or child.impl_get_extra('_cidr')):
                obj_form['remote'] = True
            if childtype == 'DateOption':
                obj_form['remote'] = True
            if not obj_form.get('remote', False):
                pattern = await childapi_option.pattern()
                if pattern is not None:
                    obj_form['pattern'] = pattern
                if childtype == 'PortOption':
                    obj_form['min'] = child.impl_get_extra('_min_value')
                    obj_form['max'] = child.impl_get_extra('_max_value')
            if childtype == 'FloatOption':
                obj_form['step'] = 'any'
            if web_type == 'choice':
                obj_form['type'] = 'choice'
            elif web_type in INPUTS:
                obj_form['type'] = 'input'
            if obj_form:
                form[path] = obj_form

    async def calc_raises_properties(self,
                                     obj,
                                     childapi):
        old_properties = childapi._option_bag.config_bag.properties
        config = childapi._option_bag.config_bag.context
        settings = config.cfgimpl_get_settings()
        childapi._option_bag.config_bag.properties = await self.config.property.get(default=True)  # settings.get_context_properties(config._impl_properties_cache)
        childapi._option_bag.config_bag.properties -= {'permissive'}
        properties = await childapi.property.get(only_raises=True,
                                                 uncalculated=True)
        properties -= await childapi.permissive.get()
        # 'hidden=True' means cannot access with or without permissive option
        # 'display=False' means cannot access only without permissive option
        if properties:
            obj['display'] = False
        properties -= await self.config.permissive.get()
        if properties:
            obj['hidden'] = True
        childapi._option_bag.config_bag.properties = old_properties

    async def _gen_model_properties(self,
                                    childapi,
                                    path,
                                    index):
        isfollower = await childapi.option.isfollower()
        props = set(await childapi.property.get())
        obj = self.gen_properties(props,
                                  isfollower,
                                  await childapi.option.ismulti(),
                                  index)
        await self.calc_raises_properties(obj, childapi)
        return obj

    def gen_properties(self,
                       properties,
                       isfollower,
                       ismulti,
                       index):
        obj = {}
        if not isfollower and ismulti:
            if 'empty' in properties:
                if index is None:
                    obj['required'] = True
                properties.remove('empty')
            if 'mandatory' in properties:
                if index is None:
                    obj['needs_len'] = True
                properties.remove('mandatory')
        elif 'mandatory' in properties:
            if index is None:
                obj['required'] = True
            properties.remove('mandatory')
        if 'frozen' in properties:
            if index is None:
                obj['readOnly'] = True
            properties.remove('frozen')
        if 'hidden' in properties:
            properties.remove('hidden')
        if 'disabled' in properties:
            properties.remove('disabled')
        if properties:
            lprops = list(properties)
            lprops.sort()
            obj['properties'] = lprops
        return obj

    async def gen_model(self,
                        model,
                        childapi,
                        path,
                        leader_len,
                        updates_status):
        if await childapi.option.isoptiondescription():
            props = set(await childapi.property.get())
            obj = {}
            await self.calc_raises_properties(obj, childapi)
            if props:
                lprops = list(props)
                lprops.sort()
                obj['properties'] = lprops
            try:
                await self.config.option(path).option.get()
            except PropertiesOptionError:
                pass
        else:
            obj = await self._gen_model_properties(childapi,
                                                   path,
                                                   None)
            if await childapi.option.isfollower():
                for index in range(leader_len):
                    follower_childapi = self.config.unrestraint.option(path, index)
                    sobj = await self._gen_model_properties(follower_childapi,
                                                            path,
                                                            index)
                    await self._get_model_value(follower_childapi,
                                                path,
                                                sobj,
                                                index,
                                                updates_status)
                    if sobj:
                        model.setdefault(path, {})[str(index)] = sobj
            else:
                await self._get_model_value(childapi,
                                            path,
                                            obj,
                                            None,
                                            updates_status)
        if obj:
            if not await childapi.option.isoptiondescription() and await childapi.option.isfollower():
                model.setdefault(path, {})['null'] = obj
            else:
                model[path] = obj

    async def _get_model_value(self,
                               childapi,
                               path,
                               obj,
                               index,
                               updates_status):
        if path in updates_status and index in updates_status[path]:
            value = await childapi.value.get()
            self._get_value_with_exception(obj,
                                           childapi,
                                           updates_status[path][index])
            del updates_status[path][index]
        else:
            try:
                with warnings.catch_warnings(record=True) as warns:
                    value = await self.config.option(path, index=index).value.get()
                self._get_value_with_exception(obj,
                                               childapi,
                                               warns)
            except ValueError as err:
                self._get_value_with_exception(obj,
                                               childapi,
                                               [err])
                value = await self.config.unrestraint.option(path, index=index).value.get()
            except PropertiesOptionError as err:
                config_bag = self.config._config_bag
                settings = config_bag.context.cfgimpl_get_settings()
                if settings._calc_raises_properties(config_bag.properties,
                                                    config_bag.permissives,
                                                    set(err.proptype)):
                    obj['hidden'] = True
                obj['display'] = False
                value = await childapi.value.get()
        if value is not None and value != []:
            obj['value'] = value
        if not await childapi.owner.isdefault():
            obj['owner'] = await childapi.owner.get()

    def _get_value_with_exception(self,
                                  obj,
                                  childapi,
                                  values):
        for value in values:
            if isinstance(value, ValueError):
                obj.setdefault('error', [])
                msg = str(value)
                if msg not in obj.get('error', []):
                    obj['error'].append(msg)
                    obj['invalid'] = True
            elif isinstance(value.message, ValueErrorWarning):
                value.message.prefix = ''
                obj.setdefault('error', [])
                msg = str(value.message)
                if msg not in obj.get('error', []):
                    obj['error'].append(msg)
                    obj['invalid'] = True
            else:
                value.message.prefix = ''
                obj.setdefault('warnings', [])
                msg = str(value.message)
                if msg not in obj.get('error', []):
                    obj['warnings'].append(msg)
                    obj['hasWarnings'] = True

    async def gen_global(self):
        ret = {}
        ret['owner'] = await self.config.owner.get()
        ret['properties'] = list(await self.config.property.get())
        ret['properties'].sort()
        ret['permissives'] = list(await self.config.permissive.get())
        ret['permissives'].sort()
        return ret

    def get_form(self, form):
        ret = []
        buttons = []
        dict_form = {}
        for form_ in form:
            if 'key' in form_:
                dict_form[form_['key']] = form_
            elif form_.get('type') == 'submit':
                if 'cmd' not in form_:
                    form_['cmd'] = 'submit'
                buttons.append(form_)
            else:
                raise ValueError(_('unknown form {}').format(form_))

        for key, form_ in self.form.items():
            form_['key'] = key
            if key in dict_form:
                form_.update(dict_form[key])
            ret.append(form_)
        ret.extend(buttons)
        return ret

    async def del_value(self, childapi, path, index):
        if index is not None and await childapi.option.isleader():
            await childapi.value.pop(index)
        elif index is None or await childapi.option.isfollower():
            await childapi.value.reset()
        else:
            multi = await childapi.value.get()
            multi.pop(index)
            await childapi.value.set(multi)

    async def add_value(self, childapi, path, value):
        multi = await childapi.value.get()
        multi.append(value)
        await childapi.value.set(multi)

    async def mod_value(self, childapi, path, index, value):
        if index is None or await childapi.option.isfollower():
            await childapi.value.set(value)
        else:
            multi = await childapi.value.get()
            if len(multi) < index + 1:
                multi.append(value)
            else:
                multi[index] = value
            await childapi.value.set(multi)

    async def apply_updates(self,
                            oripath,
                            updates,
                            model_ori):
        updates_status = {}
        for update in updates:
            path = update['name']
            index = update.get('index')
            if oripath is not None and not path.startswith(oripath):
                raise ValueError(_('not in current area'))
            childapi = self.config.option(path)
            childapi_option = childapi.option
            if await childapi_option.isfollower():
                childapi = self.config.option(path, index)
            with warnings.catch_warnings(record=True) as warns:
                try:
                    if update['action'] == 'modify':
                        await self.mod_value(childapi,
                                             path,
                                             index,
                                             update.get('value', undefined))
                    elif update['action'] == 'delete':
                        await self.del_value(childapi,
                                             path,
                                             index)
                    elif update['action'] == 'add':
                        if await childapi_option.ismulti():
                            await self.add_value(childapi, path, update['value'])
                        else:
                            raise ValueError(_('only multi option can have action "add", but "{}" is not a multi').format(path))
                    else:
                        raise ValueError(_('unknown action {}').format(update['action']))
                except ValueError as err:
                    updates_status.setdefault(path, {})[index] = [err]
            if warns != []:
                updates_status.setdefault(path, {}).setdefault(index, []).extend(warns)
        return updates_status

    async def set_updates(self,
                          body):
        root_path = self.root
        updates = body.get('updates', [])
        updates_status = await self.apply_updates(root_path,
                                                  updates,
                                                  body.get('model'))
        if 'model' in body:
            order = []
            old_model = body['model']
            new_model = await self.todict(order=order,
                                          build_schema=False,
                                          build_form=False,
                                          updates_status=updates_status)
            values = {'updates': list_keys(old_model, new_model['model'], order, updates_status),
                      'model': new_model['model']}
        else:
            values = updates_status
        return values

    async def todict(self,
                     custom_form=[],
                     build_schema=True,
                     build_model=True,
                     build_form=True,
                     order=None,
                     updates_status={}):
        rootpath = self.root
        if build_schema:
            schema = {}
        else:
            schema = None
        if build_model:
            model = {}
        else:
            model = None
        if build_form:
            form = {}
            buttons = []
        else:
            form = None
        await self.walk(rootpath,
                        None,
                        schema,
                        model,
                        form,
                        order,
                        updates_status,
                        init=True)
        if build_form:
            for form_ in custom_form:
                if 'key' in form_:
                    key = form_.pop('key')
                    form.setdefault(key, {}).update(form_)
                elif form_.get('type') == 'submit':
                    # FIXME if an Option has a key "null"?
                    form.setdefault(None, []).append(form_)
                else:
                    raise ValueError(_('unknown form {}').format(form_))
        ret = {}
        if build_schema:
            ret['schema'] = schema
        if build_model:
            ret['model'] = model
            ret['global'] = await self.gen_global()
        if build_form:
            ret['form'] = form
        ret['version'] = '1.0'
        return ret


def list_keys(model_a, model_b, ordered_key, updates_status):
    model_a_dict = {}
    model_b_dict = {}

    keys_a = set(model_a.keys())
    keys_b = set(model_b.keys())

    keys = (keys_a ^ keys_b) | set(updates_status.keys())

    for key in keys_a & keys_b:
        keys_mod_a = set(model_a[key].keys())
        keys_mod_b = set(model_b[key].keys())
        if keys_mod_a != keys_mod_b:
            keys.add(key)
        else:
            for skey in keys_mod_a:
                if model_a[key][skey] != model_b[key][skey]:
                    keys.add(key)
                    break
    def sort_key(key):
        try:
            return ordered_key.index(key)
        except ValueError:
            return -1
    return sorted(list(keys), key=sort_key)
