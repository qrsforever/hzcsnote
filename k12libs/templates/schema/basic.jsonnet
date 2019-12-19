// @file basic.jsonnet
// @brief
// @author QRS
// @version 1.0
// @date 2019-12-18 21:08

local default_schema = {
    bool(id): {
        _id_: 'bool-' + id,
        name: { en: 'Bool' + id, cn: '布尔-' + id },
        type: 'bool',
        default: true,
    },

    int(id): {
        _id_: 'int-' + id,
        name: { en: 'Int-' + id, cn: '整型-' + id },
        type: 'int',
        min: 0,
        max: 120,
        default: 100,
    },

    float(id): {
        _id_: 'float-' + id,
        name: { en: 'Float' + id, cn: '浮点-' + id },
        type: 'float',
        min: 0,
        max: 300,
        default: 200.0,
    },

    string(id): {
        _id_: 'string-' + id,
        name: { en: 'String-' + id, cn: '字符串-' + id },
        type: 'value',
        default: 'string',
    },

    string_enum(id): {
        _id_: 'stringenum-' + id,
        name: { en: 'StringEnum-' + id, cn: '字符串枚举-' + id },
        type: 'string-enum',
        objs: [
            {
                name: { en: 'Item-1', cn: self.en },
                value: 'item1',
            },
            {
                name: { en: 'Item-2', cn: self.en },
                value: 'item2',
            },
        ],
        default: 'item1',
    },

    int_array(id): {
        _id_: 'intarray-' + id,
        name: { en: 'IntArray-' + id, cn: '整型数组-' + id },
        type: 'int-array',
        default: [[1, 2], [3, 4]],
    },

    float_array(id): {
        _id_: 'floatarray-' + id,
        name: { en: 'FloatArray' + id, cn: '浮点数组-' + id },
        type: 'float-array',
        default: [1.0, 200.0],
    },

    string_array(id): {
        _id_: 'stringarray-' + id,
        name: { en: 'StringArray' + id, cn: '字符串数组-' + id },
        type: 'string-array',
        default: ['abc', 'xyz'],
    },
};

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
                            _id_: 'tab1.accordion1.navigation1',
                            name: { en: 'navigation1', cn: '导航栏-1' },
                            type: 'navigation',
                            objs: [
                                {
                                    name: { en: 'group1', cn: '选项卡-1' },
                                    value: 'nav1-1',
                                    type: '_ignore_',
                                    objs: [
                                        default_schema.bool('1'),
                                        default_schema.int('1'),
                                        default_schema.float('1'),
                                        default_schema.string('1'),
                                    ],
                                },
                                {
                                    name: { en: 'group2', cn: '选项卡-2' },
                                    value: 'nav1-2',
                                    type: '_ignore_',
                                    objs: [
                                        default_schema.bool('2'),
                                        default_schema.int('2'),
                                        default_schema.float('2'),
                                        default_schema.string('2'),
                                    ],  // objs
                                },
                            ],  // objs
                            default: 'nav1-1',
                        },
                        {  // 2
                            _id_: 'tab1.accordion1.navigation2',
                            name: { en: 'navigation2', cn: '导航栏-2' },
                            type: 'navigation',
                            objs: [
                                {  // 1
                                    name: { en: 'BoolTriggerTest', cn: '布尔触发测试' },
                                    value: 'nav2-1',
                                    type: 'object',
                                    objs: [
                                        {
                                            _id_: 'booltrigger001',
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
                                                                _id_: 'brightness001',
                                                                name: { en: 'Brightness', cn: '亮度' },
                                                                type: 'int',
                                                                default: 100,
                                                            },
                                                            {
                                                                _id_: 'colortemp',
                                                                name: { en: 'ColorTemp', cn: '色温' },
                                                                type: 'float',
                                                                default: 250.0,
                                                            },
                                                            {
                                                                _id_: 'hue',
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
                                    value: 'nav2-2',
                                    type: 'object',
                                    objs: [
                                        {  // 1
                                            _id_: 'stringenumtrigger001',
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
                                                                _id_: 'brightness002',
                                                                name: { en: 'Brightness', cn: '亮度' },
                                                                type: 'int',
                                                                default: 100,
                                                            },
                                                            {
                                                                _id_: 'colortemp',
                                                                name: { en: 'ColorTemp', cn: '色温' },
                                                                type: 'float',
                                                                default: 250.0,
                                                            },
                                                            {
                                                                _id_: 'hue',
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
                                                                _id_: 'brightness003',
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
                            default: 'nav2-1',
                        },
                    ],  // objs
                },
                {
                    name: { en: 'accordion2', cn: '折叠卡-2' },
                    type: 'accordion',
                    objs: [
                        default_schema.bool('3'),
                        default_schema.int('3'),
                        default_schema.float('3'),
                        default_schema.string('3'),
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
                    _id_: 'tab2.navigation3',
                    name: { en: 'navigation3', cn: '导航栏-2' },
                    type: 'navigation',
                    objs: [
                        {
                            name: { en: 'group1', cn: '选项卡-1' },
                            value: 'nav3-1',
                            type: '_ignore_',
                            objs: [
                                default_schema.bool('4'),
                                default_schema.int('4'),
                                default_schema.float('4'),
                                default_schema.string('4'),
                            ],  // objs
                        },
                        {
                            name: { en: 'group2', cn: '选项卡-2' },
                            value: 'nav3-2',
                            type: '_ignore_',
                            objs: [
                            ],  // objs
                        },
                    ],
                    default: 'nav3-1',
                },
            ],
        },
        {
            name: { en: 'tab3', cn: '页标签-3' },
            type: 'tab',
            objs: [
                default_schema.bool('5'),
                {
                    type: 'H',
                    objs: [
                        default_schema.int('5'),
                        default_schema.float('5'),
                        default_schema.string('5'),
                        default_schema.string_enum('5'),
                        default_schema.int_array('5'),
                        default_schema.float_array('5'),
                        default_schema.string_array('5'),
                    ],
                },
            ],  // objs
        },
        {
            name: { en: 'Debug Output', cn: '调试输出' },
            type: 'output',
            objs: [],
        },
    ],  // objs
}
