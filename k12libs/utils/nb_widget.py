#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @file nb_widget.py
# @brief
# @author QRS
# @blog qrsforever.github.io
# @version 1.0
# @date 2019-12-18 19:55:57


import ipywidgets as widgets
from IPython.display import clear_output
from IPython.core.display import display
from ipywidgets import (HTML, Text, BoundedIntText,
                        BoundedFloatText, Box, HBox, VBox, Dropdown,
                        Layout, Tab, Accordion, ToggleButtons, Checkbox)
import json

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
            if self.debug:
                with self.out:
                    clear_output()
                    print(change)
            if cb:
                cb(change)

        for per in observes:
            per.observe(lambda change, cb = cb: _on_value_change(change, cb), 'value')
        return root
    return _widget

class K12WidgetGenerator():
    def __init__(self, lan = 'en', debug=True):
        self.debug = debug
        self.out = widgets.Output(layout={'border': '1px solid black'})
        self.output = False
        self.lan = lan
        self.basic_types = ['int', 'float', 'bool', 'string', 'string-enum']
        self.wids_map = {}
        self.vlo = Layout(
            width='auto',
            align_items='stretch',
            justify_content='flex-start',
            margin='3px 3px 3px 3px',
            # border='solid 1px red',
        )
        self.hlo = Layout(
            width='100%',
            flex_flow='row wrap',
            align_items='stretch',
            justify_content='flex-start',
            margin='3px 0px 3px 0px',
            # border='solid 1px blue',
        )
        self.style = {
            # 'description_width': 'initial',
            'description_width': '120px',
        }

        self.tab_layout = Layout(
            display='flex',
            width='100%',
        )

        self.accordion_layout = Layout(
            display='inline-flex',
            # justify_content='flex-start',
            # align_items='stretch',
            width='99%'
        )

        self.box_layout = Layout(
            display='flex',
            flex_flow='row wrap',
            align_items='stretch',
            justify_content='flex-start',
            width='100%'
        )

    def _print(self, *args, **kwargs):
        if self.debug:
            print(*args, **kwargs)

    def _output(self, *args, **kwargs):
        if self.output:
            with self.out:
                clear_output()
                print(*args, **kwargs)

    def Output(self, flag = False):
        self.output = flag

    @k12widget
    def Bool(self, wid, *args, **kwargs):
        self.wids_map[wid] = Checkbox(*args, **kwargs)

        def _value_change(change):
            self._output('布尔控件可以用在除了page节点的任意其他非叶子节点中')
            self._print("Checkbox here")
        return self.wids_map[wid], [self.wids_map[wid]], _value_change

    @k12widget
    def Int(self, wid, *args, **kwargs):
        self.wids_map[wid] = BoundedIntText(*args, **kwargs)

        def _value_change(change):
            self._output('''整型控件可以用在除了page节点的任意其他非叶子节点中
            属性:
              default : [O]默认值
                  min : [O]最小值
                  max : [O]最大值
                width : [O]控件宽度 (当有特殊要求时,可以设置)
                    ''')
            self._print("BoundedIntText here")
        return self.wids_map[wid], [self.wids_map[wid]], _value_change

    @k12widget
    def Float(self, wid, *args, **kwargs):
        self.wids_map[wid] = BoundedFloatText(*args, **kwargs)

        def _value_change(change):
            self._output('''浮点型控件可以用在除了page节点的任意其他非叶子节点中
            属性:
              default : [O]默认值
                  min : [O]最小值
                  max : [O]最大值
                width : [O]控件宽度 (当有特殊要求时,可以设置)
                    ''')
            self._print("BoundedFloatText here")
        return self.wids_map[wid], [self.wids_map[wid]], _value_change

    @k12widget
    def String(self, wid, *args, **kwargs):
        self.wids_map[wid] = Text(*args, **kwargs)

        def _value_change(change):
            self._output('文本控件可以用在除了page节点的任意其他非叶子节点中')
        return self.wids_map[wid], [self.wids_map[wid]], _value_change

    @k12widget
    def Array(self, wid, *args, **kwargs):
        self.wids_map[wid] = Text(*args, **kwargs)

        def _value_change(change):
            self._print("IntArray here")
            self._print(json.loads(change['new']))
        return self.wids_map[wid], [self.wids_map[wid]], _value_change

    @k12widget
    def StringEnum(self, wid, *args, **kwargs):
        self.wids_map[wid] = Dropdown(*args, **kwargs)

        def _value_change(change):
            self._print("StringEnum here")
        return self.wids_map[wid], [self.wids_map[wid]], _value_change

    @k12widget
    def BoolTrigger(self, wid, *args, **kwargs):
        parent_box = VBox(layout = self.vlo)
        parent_box.trigger_box = VBox(layout = self.vlo)

        wdg = Checkbox(*args, **kwargs)
        wdg.parent_box = parent_box

        def _switch_widget(wdg, value):
            if value:
                trigger_box = wdg.parent_box.trigger_box
                wdg.parent_box.children = [wdg] + list(trigger_box.children)
            else:
                wdg.parent_box.children = [wdg]

        def _value_change(change):
            self._print("BoolTrigger here")
            wdg = change['owner']
            val = change['new']
            _switch_widget(wdg, val)
        _switch_widget(wdg, wdg.value)
        return parent_box, [wdg], _value_change

    @k12widget
    def StringEnumTrigger(self, wid, *args, **kwargs):
        parent_box = VBox(layout = self.vlo)
        wdg = Dropdown(*args, **kwargs)
        wdg.parent_box = parent_box
        parent_box.trigger_box = {
                value: VBox(layout = self.vlo) for _, value in wdg.options
        }

        def _switch_widget(wdg, value):
            trigger_box = wdg.parent_box.trigger_box[value]
            wdg.parent_box.children = [wdg] + list(trigger_box.children)
            # wdg.parent_box.children = [wdg, wdg.parent_box.trigger_box[value]]

        def _value_change(change):
            self._print("StringEnumTrigger here")
            wdg = change['owner']
            val = change['new']
            _switch_widget(wdg, val)
        _switch_widget(wdg, wdg.value)
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
            self._print("StringEnumGroupTrigger here")
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
        wdg.parent_box = parent_box
        trigger_box = {}
        for name in wdg.options:
            trigger_box[name] = VBox(layout = self.vlo)
        wdg.parent_box.trigger_box = trigger_box

        def _switch_widget(wdg, value):
            parent_box = wdg.parent_box
            trigger_box = parent_box.trigger_box[value]
            parent_box.children = [wdg, trigger_box]

        def _value_change(change):
            
            self._output('''导航按钮可以用在tab和accordion节点下面, 作用和accordion相似,只是展示形式不同
                    ''')
            self._print("ObjectEnumTrigger here")
            wdg = change['owner']
            val = change['new']
            _switch_widget(wdg, val)
        _switch_widget(wdg, wdg.value)
        return parent_box, [wdg], _value_change

    def _parse_config(self, widget, config):
        __id_ = config.get('_id_', None) or ''
        _name = config.get('name', None)
        _type = config.get('type', None)
        _objs = config.get('objs', None) or {}

        if _type == 'page':
            wdg = Tab(layout = self.tab_layout)
            for obj in _objs:
                self._parse_config(wdg, obj)
            return _widget_add_child(widget, wdg)

        elif _type == 'tab':
            if not isinstance(widget, Tab):
                raise RuntimeError('Configure Error')
            widget.set_title(len(widget.children), _name[self.lan])
            wdg = VBox(layout = self.vlo)
            for obj in _objs:
                self._parse_config(wdg, obj)
            return _widget_add_child(widget, wdg)

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
            default = config.get('default', 'none')
            options = []
            for obj in _objs:
                if obj.get('name', None):
                    options.append(obj['name'][self.lan])
            wdg = self.Navigation(
                __id_,
                options = options,
                description = _name[self.lan])
            for obj in _objs:
                if obj.get('name', None):
                    self._parse_config(wdg.trigger_box[obj['name'][self.lan]], obj)
            return _widget_add_child(widget, wdg)

        elif _type == 'object':
            if _name:
                wdg = HTML(value = f"<b><font color='black'>{_name[self.lan]} :</b>")
                _widget_add_child(widget, wdg)
            for obj in _objs:
                self._parse_config(widget, obj)
            return widget

        elif _type == 'output': # debug info
            self.Output(True)
            if _name:
                wdg = HTML(value = f"<b><font color='black'>{_name[self.lan]} :</b>")
                _widget_add_child(widget, wdg)
            for obj in _objs:
                self._parse_config(widget, obj)
            return _widget_add_child(widget, self.out)

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
            max = config.get('max', 100)
            # width = config.get('width', 200)
            wdg = self.Int(
                __id_,
                description = _name[self.lan],
                value = default,
                min = min,
                max = max,
                step = 1,
                # layout = Layout(width = '%dpx' % width),
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
            )
            return _widget_add_child(widget, wdg)

        elif _type == 'int-array' or _type == 'float-array':
            default = config.get('default', '[]')
            wdg = self.Array(
                __id_,
                description = _name[self.lan],
                value = json.dumps(default),
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

            description = widgets.HTML(value = f"<b><font color='black'>{_name[self.lan]} :</b>")
            return _widget_add_child(widget, [description, wdg])
        else:
            for obj in _objs:
                self._parse_config(widget, obj)

    def parse_schema(self, config):
        page = Box(layout=Layout(width='100%'))
        self._parse_config(page, config)
        # display(page, self.out)
        display(page)
        self.page = page

def k12ai_schema_parse(config, lan='en', debug=True):
    g = K12WidgetGenerator(lan, debug)
    g.parse_schema(config)
    return g
