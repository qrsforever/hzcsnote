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
from pyhocon import ConfigFactory
from pyhocon import HOCONConverter

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
            wdg = change['owner']
            val = change['new']
            if hasattr(wdg, 'id'):
                self.wid_value_map[wdg.id] = val
            if cb:
                cb(change)
            self._output(1, change)

        for per in observes:
            per.observe(lambda change, cb = cb: _on_value_change(change, cb), 'value')
        return root
    return _widget

class K12WidgetGenerator():
    def __init__(self, lan = 'en', debug=False):
        self.out = Output(layout={'border': '1px solid black'})
        self.output_type = 'none'
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

    def _output(self, flag, *args, **kwargs):
        if self.output_type == 'none':
            return
        if flag == 1:
            with self.out:
                clear_output()
                if self.output_type == 'change':
                    pprint.pprint(*args, **kwargs)
                elif self.output_type == 'idvalue':
                    pprint.pprint(self.wid_value_map)
                elif self.output_type == 'json':
                    config = ConfigFactory.from_dict(self.wid_value_map)
                    print(HOCONConverter.convert(config, 'json'))

    @k12widget
    def Output(self, description):
        wdg = ToggleButtons(
                options=[('Widget Change ', 'change'), 
                    ('ID Value ', 'idvalue'), ('Gen Json ', 'json')],
                description=description,
                disabled=False,
                button_style='warning')

        def _value_change(change):
            self.output_type = change['new']

        self.output_type = 'change'
        return wdg, [wdg], _value_change

    def _wid_map(self, wid, widget):
        widget.id = wid
        self.wid_widget_map[wid] = widget

    def _rm_sub_wid(self, widget):
        if isinstance(widget, Box):
            for child in widget.children:
                self._rm_sub_wid(child)
        else:
            if hasattr(widget, 'id'):
                if widget.id in self.wid_value_map.keys():
                    del self.wid_value_map[widget.id]

    @k12widget
    def Bool(self, wid, *args, **kwargs):
        wdg = Checkbox(*args, **kwargs)
        self._wid_map(wid, wdg)

        def _value_change(change):
            pass

        return wdg, [wdg], _value_change

    @k12widget
    def Int(self, wid, *args, **kwargs):
        wdg = BoundedIntText(*args, **kwargs)
        self._wid_map(wid, wdg)

        def _value_change(change):
            pass

        return wdg, [wdg], _value_change

    @k12widget
    def Float(self, wid, *args, **kwargs):
        wdg = BoundedFloatText(*args, **kwargs)
        self._wid_map(wid, wdg)

        def _value_change(change):
            pass
        return wdg, [wdg], _value_change

    @k12widget
    def String(self, wid, *args, **kwargs):
        wdg = Text(*args, **kwargs)
        self._wid_map(wid, wdg)

        def _value_change(change):
            pass
        return wdg, [wdg], _value_change

    @k12widget
    def Array(self, wid, *args, **kwargs):
        wdg = Text(*args, **kwargs)
        self._wid_map(wid, wdg)

        def _value_change(change):
            wdg = change['owner']
            val = change['new']
            self.wid_value_map[wdg.id] = json.loads(val)
        return wdg, [wdg], _value_change

    @k12widget
    def StringEnum(self, wid, *args, **kwargs):
        wdg = Dropdown(*args, **kwargs)
        self._wid_map(wid, wdg)

        def _value_change(change):
            pass
        return wdg, [wdg], _value_change

    @k12widget
    def BoolTrigger(self, wid, *args, **kwargs):
        wdg = Checkbox(*args, **kwargs)
        self._wid_map(wid, wdg)
        parent_box = VBox(layout = self.vlo)
        parent_box.trigger_box = VBox(layout = self.vlo)
        wdg.parent_box = parent_box

        def _update_layout(wdg, val):
            if val:
                trigger_box = wdg.parent_box.trigger_box
                wdg.parent_box.children = [wdg, trigger_box]
            else:
                self._rm_sub_wid(wdg.parent_box.trigger_box)
                wdg.parent_box.children = [wdg]

        def _value_change(change):
            wdg = change['owner']
            val = change['new']
            _update_layout(wdg, val)
        _update_layout(wdg, wdg.value)
        return parent_box, [wdg], _value_change

    @k12widget
    def StringEnumTrigger(self, wid, *args, **kwargs):
        wdg = Dropdown(*args, **kwargs)
        self._wid_map(wid, wdg)
        parent_box = VBox(layout = self.vlo)
        parent_box.trigger_box = {value: VBox(layout = self.vlo) for _, value in wdg.options}
        wdg.parent_box = parent_box

        def _update_layout(wdg, val, old):
            trigger_box = wdg.parent_box.trigger_box[val]
            wdg.parent_box.children = [wdg, trigger_box]
            if old:
                self._rm_sub_wid(wdg.parent_box.trigger_box[old])

        def _value_change(change):
            wdg = change['owner']
            val = change['new']
            old = change['old']
            _update_layout(wdg, val, old)
        _update_layout(wdg, wdg.value, None)
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
            options = [(obj['name'][self.lan], idx) for idx, obj in enumerate(_objs)]
            if len(options) == 0:
                raise RuntimeError('Configure Error: no options')
            trigger_boxes = [VBox(layout = self.vlo) for _ in options]
            tbtn = ToggleButtons(
                    options=options,
                    description = _name[self.lan])
            wdg = VBox([tbtn, trigger_boxes[0]], layout = self.vlo)
            wdg.trigger_boxes = trigger_boxes
            tbtn.parent_box = wdg

            def _value_change(change):
                wdg = change['owner']
                val = change['new']
                parent_box = wdg.parent_box
                trigger_box = parent_box.trigger_boxes[val]
                parent_box.children = [wdg, trigger_box]

            tbtn.observe(_value_change, 'value')
            for idx, obj in enumerate(_objs):
                self._parse_config(trigger_boxes[idx], obj)
            return _widget_add_child(widget, wdg)

        elif _type == 'output': # debug info
            wdg = self.Output(_name[self.lan])
            for obj in _objs:
                self._parse_config(widget, obj)
            return _widget_add_child(widget, [wdg, self.out])

        elif _type == 'object':
            if _name:
                wdg = HTML(value = f"<b><font color='black'>{_name[self.lan]} :</b>")
                _widget_add_child(widget, wdg)
            for obj in _objs:
                self._parse_config(widget, obj)
            return widget

        elif _type == 'H':
            if _name:
                wdg = HTML(value = f"<b><font color='black'>{_name[self.lan]} :</b>")
                _widget_add_child(widget, wdg)
            wdg = HBox(layout = self.hlo)
            for obj in _objs:
                self._parse_config(wdg, obj)
            return _widget_add_child(widget, wdg)

        elif _type == 'V':
            if _name:
                wdg = HTML(value = f"<b><font color='black'>{_name[self.lan]} :</b>")
                _widget_add_child(widget, wdg)
            wdg = VBox(layout = self.vlo)
            for obj in _objs:
                self._parse_config(wdg, obj)
            return _widget_add_child(widget, wdg)

        elif _type == 'HV':
            if _name:
                wdg = HTML(value = f"<b><font color='black'>{_name[self.lan]} :</b>")
                _widget_add_child(widget, wdg)
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

        else:
            for obj in _objs:
                self._parse_config(widget, obj)

    def parse_schema(self, config):
        page = Box(layout=self.page_layout)
        self._parse_config(page, config)
        display(page)
        self.page = page

    def set_widget_value(self, wid_value_map):
        if wid_value_map:
            pass

def k12ai_schema_parse(config, lan='en', debug=True):
    g = K12WidgetGenerator(lan, debug)
    g.parse_schema(config)
    return g
