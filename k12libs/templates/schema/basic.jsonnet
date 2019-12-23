// @file basic.jsonnet
// @brief
// @author QRS
// @version 1.0
// @date 2019-12-18 21:08

local default_schema = import 'default.libsonnet';

{
    description: |||
        K12 Data Template Model
    |||,

    type: 'page',
    objs: [
        {
            name: { en: 'tab1', cn: '页标签-1' },
            type: 'tab',
            objs: [
                {
                    name: { en: 'accordion1', cn: '折叠卡-1' },
                    type: 'accordion',
                    objs: [
                        {  // 1
                            name: { en: 'navigation1', cn: '导航栏-1' },
                            type: 'navigation',
                            objs: [
                                {
                                    name: { en: 'group1', cn: '选项卡-1' },
                                    type: '_ignore_',
                                    objs: [
                                        default_schema.bool('a.b', '1'),
                                        default_schema.int('a.b', '1'),
                                        default_schema.float('a.b', '1'),
                                        default_schema.string('a.b', '1'),
                                    ],
                                },
                                {
                                    name: { en: 'group2', cn: '选项卡-2' },
                                    type: '_ignore_',
                                    objs: [
                                        default_schema.bool('a.c', '2'),
                                        default_schema.int('a.c', '2'),
                                        default_schema.float('a.c', '2'),
                                        default_schema.string('a.c', '2'),
                                    ],  // objs
                                },
                            ],  // objs
                        },
                        {  // 2
                            name: { en: 'navigation2', cn: '导航栏-2' },
                            type: 'navigation',
                            objs: [
                                {  // 1
                                    name: { en: 'BoolTriggerTest', cn: '布尔触发测试' },
                                    type: 'object',
                                    objs: [
                                        {
                                            _id_: 'a.b.d.k12booltrigger',
                                            name: { en: 'Light', cn: '灯' },
                                            type: 'bool-trigger',
                                            objs: [
                                                {  // 1
                                                    name: { en: 'TurnOn', cn: '开灯' },
                                                    value: true,
                                                    trigger: {
                                                        type: '_ignore_',
                                                        objs: [
                                                            {
                                                                _id_: 'a.b.d.trigger.brightness',
                                                                name: { en: 'Brightness', cn: '亮度' },
                                                                type: 'int',
                                                                default: 100,
                                                            },
                                                            {
                                                                _id_: 'a.b.d.trigger.colortemp',
                                                                name: { en: 'ColorTemp', cn: '色温' },
                                                                type: 'float',
                                                                default: 250.0,
                                                            },
                                                            {
                                                                _id_: 'a.b.d.trigger.hue',
                                                                name: { en: 'HUE', cn: '饱和度' },
                                                                type: 'float',
                                                                default: 105.0,
                                                            },
                                                        ],
                                                    },
                                                },
                                                {  // 2
                                                    name: { en: 'TurnOff', cn: '关灯' },
                                                    value: false,
                                                    trigger: {
                                                    },
                                                },
                                            ],
                                            default: false,
                                        },  // end booltrigger001
                                    ],  // objs
                                },  // end 1
                                {  // 2
                                    name: { en: 'StringEnumTriggerTest', cn: '字符串枚举触发测试' },
                                    type: 'object',
                                    objs: [
                                        {  // 1
                                            _id_: 'a.c.d.k12stringenum',
                                            name: { en: 'LightSelect', cn: '选择灯' },
                                            type: 'string-enum-trigger',
                                            objs: [
                                                {  // 1
                                                    name: { en: 'Hue', cn: '飞利浦灯' },
                                                    value: 'hue',
                                                    trigger: {
                                                        type: '_ignore_',
                                                        objs: [
                                                            {
                                                                _id_: 'a.c.d.t1.brightness',
                                                                name: { en: 'Brightness', cn: '亮度' },
                                                                type: 'int',
                                                                default: 100,
                                                            },
                                                            {
                                                                _id_: 'a.c.d.t1.colortemp',
                                                                name: { en: 'ColorTemp', cn: '色温' },
                                                                type: 'float',
                                                                default: 250.0,
                                                            },
                                                            {
                                                                _id_: 'a.c.d.t1.hue',
                                                                name: { en: 'HUE', cn: '饱和度' },
                                                                type: 'float',
                                                                default: 105.0,
                                                            },
                                                        ],  // objs
                                                    },  // trigger
                                                },  // end 1
                                                {  // 2
                                                    name: { en: 'Konke', cn: '控客灯' },
                                                    value: 'konke',
                                                    trigger: {
                                                        type: '_ignore_',
                                                        objs: [
                                                            {
                                                                _id_: 'a.c.d.t2.brightness',
                                                                name: { en: 'Brightness', cn: '亮度' },
                                                                type: 'int',
                                                                default: 100,
                                                            },
                                                        ],  // objs
                                                    },  // trigger
                                                },  // end 2
                                            ],  // objs
                                            default: 'hue',
                                        },  // end stringenumtrigger001
                                    ],  // objs
                                },  // end 2
                            ],  // objs
                        },
                    ],  // objs
                },
                {
                    name: { en: 'accordion2', cn: '折叠卡-2' },
                    type: 'accordion',
                    objs: [
                        default_schema.bool('x.y', '3'),
                        default_schema.int('x.y', '3'),
                        default_schema.float('x.y', '3'),
                        default_schema.string('x.y', '3'),
                    ],
                },
                {
                    name: { en: 'accordion3', cn: '折叠卡-3' },
                    type: 'accordion',
                    objs: [],
                },
            ],
        },
        {
            name: { en: 'tab2', cn: '页标签-2' },
            type: 'tab',
            objs: [
                {
                    name: { en: 'navigation3', cn: '导航栏-2' },
                    type: 'navigation',
                    objs: [
                        {
                            name: { en: 'group1', cn: '选项卡-1' },
                            type: '_ignore_',
                            objs: [
                                default_schema.bool('x.y.z', '4'),
                                default_schema.int('x.y.z', '4'),
                                default_schema.float('x.y.z', '4'),
                                default_schema.string('x.y.z', '4'),
                            ],  // objs
                        },
                        {
                            name: { en: 'group2', cn: '选项卡-2' },
                            type: '_ignore_',
                            objs: [
                            ],  // objs
                        },
                    ],
                },
            ],
        },
        {
            name: { en: 'tab3', cn: '页标签-3' },
            type: 'tab',
            objs: [
                default_schema.bool('w', '5'),
                {
                    type: 'H',
                    objs: [
                        default_schema.int('w', '5'),
                        default_schema.float('w', '5'),
                        default_schema.string('v', '5'),
                        default_schema.string_enum('v', '5'),
                        default_schema.int_array('w.x', '5'),
                        default_schema.float_array('w.y', '5'),
                        default_schema.string_array('w.y', '5'),
                    ],
                },
            ],  // objs
        },
        {
            name: { en: 'Debug Output', cn: '调试输出: ' },
            type: 'output',
            objs: [],
        },
    ],  // objs
}
