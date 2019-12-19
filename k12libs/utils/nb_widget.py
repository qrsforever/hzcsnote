#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @file nb_widget.py
# @brief
# @author QRS
# @blog qrsforever.github.io
# @version 1.0
# @date 2019-12-18 19:55:57


from IPython.display import clear_output
from IPython.core.display import display
from ipywidgets import (HTML, Text, BoundedIntText, Output,
                        BoundedFloatText, Box, HBox, VBox, Dropdown,
                        Layout, Tab, Accordion, ToggleButtons, Checkbox)
import json
import pprint

def _widget_add_child(widget, wdgs):
    if not isinstance(wdgs, list):
        wdgs = [wdgs]
    for child in wdgs:
        widget.children = list(widget.children) + [child]
    return widget

def k12widget(method):
    def _widget(self, *args, **kwargs):
        root, observes, cb = method(self, *args, **kwargs)

        def _on_value_change(change, cb):
            self._output(change)
            if cb:
                cb(change)

        for per in observes:
            per.observe(lambda change, cb = cb: _on_value_change(change, cb), 'value')
        return root
    return _widget

class K12WidgetGenerator():
    def __init__(self, lan = 'en', debug=False):
        self.out = Output(layout={'border': '1px solid black'})
        self.output = False
        self.wid_widget_map = {}
        self.wid_value_map = {}
        self.lan = lan
        self.basic_types = ['int', 'float', 'bool', 'string', 'string-enum']

        self.style = {
                # 'description_width': 'initial',
                'description_width': '120px',
                }

        self.vlo = Layout(
                width='auto',
                align_items='stretch',
                justify_content='flex-start',
                margin='3px 3px 3px 3px',
                )
        if debug:
            self.vlo.border = 'solid 3px red'

        self.hlo = Layout(
                width='100%',
                flex_flow='row wrap',
                align_items='stretch',
                justify_content='flex-start',
                margin='3px 0px 3px 0px',
                )
        if debug:
            self.hlo.border = 'solid 3px blue'

        self.page_layout = Layout(
                display='flex',
                width='100%',
                )
        if debug:
            self.page_layout.border = 'solid 3px black'

        self.tab_layout = Layout(
                display='flex',
                width='99%',
                )
        if debug:
            self.tab_layout.border = 'solid 3px yellow'

        self.accordion_layout = Layout(
                display='flex',
                width='99%',
                )
        if debug:
            self.accordion_layout.border = 'solid 3px green'

    def _print(self, *args, **kwargs):
        if self.debug:
            print(*args, **kwargs)

    def _output(self, *args, **kwargs):
        if self.output:
            with self.out:
                clear_output()
                pprint.pprint(*args, **kwargs)

    def Output(self, flag = False):
        self.output = flag

    def _wid_map(self, wid, widget, value):
        widget.id = wid
        self.wid_widget_map[wid] = widget
        self.wid_value_map[wid] = value

    @k12widget
    def Bool(self, wid, *args, **kwargs):
        wdg = Checkbox(*args, **kwargs)
        self._wid_map(wid, wdg, wdg.value)

        def _value_change(change):
            pass

        return wdg, [wdg], _value_change

    @k12widget
    def Int(self, wid, *args, **kwargs):
        wdg = BoundedIntText(*args, **kwargs)
        self._wid_map(wid, wdg, wdg.value)

        def _value_change(change):
            pass

        return wdg, [wdg], _value_change

    @k12widget
    def Float(self, wid, *args, **kwargs):
        wdg = BoundedFloatText(*args, **kwargs)
        self._wid_map(wid, wdg, wdg.value)

        def _value_change(change):
            pass
        return wdg, [wdg], _value_change

    @k12widget
    def String(self, wid, *args, **kwargs):
        wdg = Text(*args, **kwargs)
        self._wid_map(wid, wdg, wdg.value)

        def _value_change(change):
            pass
        return wdg, [wdg], _value_change

    @k12widget
    def Array(self, wid, *args, **kwargs):
        wdg = Text(*args, **kwargs)
        self._wid_map(wid, wdg, wdg.value)

        def _value_change(change):
            pass
        return wdg, [wdg], _value_change

    @k12widget
    def StringEnum(self, wid, *args, **kwargs):
        wdg = Dropdown(*args, **kwargs)
        self._wid_map(wid, wdg, wdg.value)

        def _value_change(change):
            pass
        return wdg, [wdg], _value_change

    @k12widget
    def BoolTrigger(self, wid, *args, **kwargs):
        parent_box = VBox(layout = self.vlo)
        parent_box.trigger_box = VBox(layout = self.vlo)

        wdg = Checkbox(*args, **kwargs)
        self._wid_map(wid, wdg, wdg.value)
        wdg.parent_box = parent_box

        def _value_change(change):
            wdg = change['owner']
            val = change['new']
            if val:
                trigger_box = wdg.parent_box.trigger_box
                wdg.parent_box.children = [wdg] + list(trigger_box.children)
            else:
                wdg.parent_box.children = [wdg]
        return parent_box, [wdg], _value_change

    @k12widget
    def StringEnumTrigger(self, wid, *args, **kwargs):
        parent_box = VBox(layout = self.vlo)
        wdg = Dropdown(*args, **kwargs)
        self._wid_map(wid, wdg, wdg.value)
        wdg.parent_box = parent_box
        parent_box.trigger_box = {
                value: VBox(layout = self.vlo) for _, value in wdg.options
                }

        def _value_change(change):
            wdg = change['owner']
            val = change['new']
            trigger_box = wdg.parent_box.trigger_box[val]
            wdg.parent_box.children = [wdg] + list(trigger_box.children)
        return parent_box, [wdg], _value_change

    @k12widget
    def StringEnumGroupTrigger(self, wid, options, groups):
        parent_box = VBox(layout = self.vlo)
        parent_box.trigger_box = {}
        options_hbox = HBox(layout = self.hlo)
        dynamic_hbox = HBox(layout = self.hlo)
        observes = []
        for name, real in options:
            dpd = Dropdown(options=groups,
                           description=name,
                           style = {'description_width': '150px'})
            dpd.name = real
            dpd.wid = wid + '.' + real
            dpd.parent_box = parent_box
            dpd.parent_box.trigger_box[real] = VBox(layout = self.vlo)
            observes.append(dpd)
        options_hbox.children = tuple(observes)
        parent_box.children = (options_hbox, dynamic_hbox)

        def _value_change(change):
            wdg = change['owner']
            val = change['new']
            parent_box = wdg.parent_box
            dynamic_box = parent_box.children[1]
            trigger_box = parent_box.trigger_box[wdg.name]
            if val == 'none':
                if trigger_box in dynamic_box.children:
                    dynamic_box.children = [w for w in dynamic_box.children if id(w) != id(trigger_box)]
            else:
                if trigger_box not in dynamic_box.children:
                    dynamic_box.children = list(dynamic_box.children) + [trigger_box]
        return parent_box, observes, _value_change

    @k12widget
    def Navigation(self, wid, *args, **kwargs):
        parent_box = VBox(layout = self.vlo)
        wdg = ToggleButtons(*args, **kwargs)
        print(wid, wdg.value)
        self._wid_map(wid, wdg, wdg.value)
        wdg.parent_box = parent_box
        trigger_box = {}
        for _, value in wdg.options:
            trigger_box[value] = VBox(layout = self.vlo)
        wdg.parent_box.trigger_box = trigger_box

        def _value_change(change):
            wdg = change['owner']
            val = change['new']
            parent_box = wdg.parent_box
            trigger_box = parent_box.trigger_box[val]
            parent_box.children = [wdg, trigger_box]
        return parent_box, [wdg], _value_change

    def _parse_config(self, widget, config):
        __id_ = config.get('_id_', None) or ''
        _name = config.get('name', None)
        _type = config.get('type', None)
        _objs = config.get('objs', None) or {}

        if _type == 'page':
            wdg = VBox(layout=Layout(
                width='100%'))
            for obj in _objs:
                self._parse_config(wdg, obj)
            return _widget_add_child(widget, wdg)

        elif _type == 'tab':
            for wdg in widget.children:
                if isinstance(wdg, Tab):
                    tab = wdg
                    break
            else:
                tab = Tab(layout = self.tab_layout)
                _widget_add_child(widget, tab)

            tab.set_title(len(tab.children), _name[self.lan])
            wdg = VBox(layout = self.vlo)
            for obj in _objs:
                self._parse_config(wdg, obj)
            return _widget_add_child(tab, wdg)

        elif _type == 'accordion':
            for wdg in widget.children:
                if isinstance(wdg, Accordion):
                    accord = wdg
                    break
            else:
                accord = Accordion(layout = self.accordion_layout)
                _widget_add_child(widget, accord)
            accord.set_title(len(accord.children), _name[self.lan])

            wdg = VBox(layout = self.vlo)
            for obj in _objs:
                self._parse_config(wdg, obj)
            return _widget_add_child(accord, wdg)

        elif _type == 'navigation':
            default = config.get('default', None)
            options = []
            for obj in _objs:
                if (not obj.get('value', None)) or (not obj.get('name', None)):
                    raise RuntimeError('Configure Error: no name and value')
                options.append((obj['name'][self.lan], obj['value']))
            wdg = self.Navigation(
                __id_,
                options = options,
                value = default,
                description = _name[self.lan])
            for obj in _objs:
                self._parse_config(wdg.trigger_box[obj['value']], obj)
            return _widget_add_child(widget, wdg)

        elif _type == 'output': # debug info
            if _name:
                wdg = HTML(value = f"<b><font color='black'>{_name[self.lan]} :</b>")
                _widget_add_child(widget, wdg)
            for obj in _objs:
                self._parse_config(widget, obj)
            self.Output(True)
            return _widget_add_child(widget, self.out)

        elif _type == 'object':
            if _name:
                wdg = HTML(value = f"<b><font color='black'>{_name[self.lan]} :</b>")
                _widget_add_child(widget, wdg)
            for obj in _objs:
                self._parse_config(widget, obj)
            return widget

        elif _type == 'H':
            wdg = HBox(layout = self.hlo)
            for obj in _objs:
                self._parse_config(wdg, obj)
            return _widget_add_child(widget, wdg)

        elif _type == 'V':
            wdg = VBox(layout = self.vlo)
            for obj in _objs:
                self._parse_config(wdg, obj)
            return _widget_add_child(widget, wdg)

        elif _type == 'HV':
            wdg = VBox(
                [HBox(layout = self.hlo), HBox(layout = self.hlo)],
                layout = self.vlo,
            )
            for obj in _objs:
                if obj.get('type') in self.basic_types:
                    self._parse_config(wdg.children[0], obj)
                else:
                    self._parse_config(wdg.children[1], obj)
            return _widget_add_child(widget, wdg)

        elif _type == 'bool':
            default = config.get('default', False)
            wdg = self.Bool(
                    __id_,
                    description = _name[self.lan],
                    value = default,
                    )
            return _widget_add_child(widget, wdg)

        elif _type == 'int':
            default = config.get('default', 0)
            min = config.get('min', 0)
            max = config.get('max', 100000)
            # width = config.get('width', 200)
            wdg = self.Int(
                __id_,
                description = _name[self.lan],
                value = default,
                min = min,
                max = max,
                step = 1,
                # layout = Layout(width = '%dpx' % width),
                continuous_update=False,
            )
            return _widget_add_child(widget, wdg)

        elif _type == 'float':
            default = config.get('default', 0.0)
            min = config.get('min', 0.0)
            max = config.get('max', 100.0)
            # width = config.get('width', 200)
            wdg = self.Float(
                __id_,
                description = _name[self.lan],
                value = default,
                min = min,
                max = max,
                step = 1.0,
                # layout = Layout(width = '%dpx' % width),
                continuous_update=False,
            )
            return _widget_add_child(widget, wdg)

        elif _type == 'string':
            default = config.get('default', 'none')
            # width = config.get('width', 200)
            wdg = self.String(
                __id_,
                description = _name[self.lan],
                value = default,
                # layout = Layout(width = '%dpx' % width),
                continuous_update=False,
            )
            return _widget_add_child(widget, wdg)

        elif _type == 'int-array' or _type == 'float-array' or _type == 'string-array':
            default = config.get('default', '[]')
            wdg = self.Array(
                __id_,
                description = _name[self.lan],
                value = json.dumps(default),
                continuous_update=False,
            )
            return _widget_add_child(widget, wdg)

        elif _type == 'string-enum':
            default = config.get('default', 'None')
            # width = config.get('width', 200)
            options = []
            for obj in _objs:
                options.append((obj['name'][self.lan], obj['value']))
            wdg = self.StringEnum(
                __id_,
                options = options,
                value = default,
                description = _name[self.lan],
                # layout = Layout(width = '%dpx' % width),
            )
            return _widget_add_child(widget, wdg)

        elif _type == 'bool-trigger':
            default = config.get('default', False)
            wdg = self.BoolTrigger(
                __id_,
                value = default,
                description = _name[self.lan])
            for obj in _objs:
                self._parse_config(wdg.trigger_box, obj['trigger'])
            return _widget_add_child(widget, wdg)

        elif _type == 'string-enum-trigger':
            default = config.get('default', 'none')
            # width = config.get('width', 200)
            options = []
            for obj in _objs:
                options.append((obj['name'][self.lan], obj['value']))
            wdg = self.StringEnumTrigger(
                __id_,
                options = options,
                value = default,
                description = _name[self.lan],
                # layout = Layout(width = '%dpx' % width),
            )
            for obj in _objs:
                self._parse_config(wdg.trigger_box[obj['value']], obj['trigger'])
            return _widget_add_child(widget, wdg)

        elif _type == 'string-enum-array-trigger':
            raise RuntimeError('not impl yet')

        elif _type == 'string-enum-group-trigger':
            options = []
            groups = []
            for obj in _objs:
                options.append((obj['name'][self.lan], obj['value']))
            for grp in config.get('groups'):
                groups.append((grp['name'][self.lan], grp['value']))
            wdg = self.StringEnumGroupTrigger(
                __id_,
                options,
                groups,
            )
            for obj in _objs:
                self._parse_config(wdg.trigger_box[obj['value']], obj['trigger'])

            description = HTML(value = f"<b><font color='black'>{_name[self.lan]} :</b>")
            return _widget_add_child(widget, [description, wdg])
        else:
            for obj in _objs:
                self._parse_config(widget, obj)

    def parse_schema(self, config):
        page = Box(layout=self.page_layout)
        self._parse_config(page, config)
        display(page)
        self.page = page
        for key, val in self.wid_value_map.items():
            print('---------', key, val)
            self.wid_widget_map[key].value = val

def k12ai_schema_parse(config, lan='en', debug=True):
    g = K12WidgetGenerator(lan, debug)
    g.parse_schema(config)
    return g
