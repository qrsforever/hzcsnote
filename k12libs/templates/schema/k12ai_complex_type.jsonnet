// @file k12ai_complex_type.jsonnet
// @brief
// @author QRS
// @version 1.0
// @date 2019-12-23 19:30

{
    description: |||
        K12 Data Template Model for complex type
    |||,

    type: 'page',
    objs: [
        {
            name: { en: 'BoolTriggerTest', cn: '布尔触发测试' },
            type: 'object',
            objs: [
                {
                    _id_: 'k12.test.k12booltrigger',
                    name: { en: 'Light', cn: '灯' },
                    type: 'bool-trigger',
                    objs: [
                        {
                            name: { en: 'TurnOn', cn: '开灯' },
                            value: true,
                            trigger: {
                                type: '_ignore_',
                                objs: [
                                    {
                                        _id_: 'k12.test.booltrigger.brightness',
                                        name: { en: 'Brightness', cn: '亮度' },
                                        type: 'int',
                                        default: 100,
                                    },
                                    {
                                        _id_: 'k12.test.booltrigger.colortemp',
                                        name: { en: 'ColorTemp', cn: '色温' },
                                        type: 'k12.test.booltrigger.float',
                                        default: 250.0,
                                    },
                                    {
                                        _id_: 'k12.test.booltrigger.hue',
                                        name: { en: 'HUE', cn: '饱和度' },
                                        type: 'float',
                                        default: 105.0,
                                    },
                                ],
                            },
                        },
                        {
                            name: { en: 'TurnOff', cn: '关灯' },
                            value: false,
                            trigger: {
                            },
                        },
                    ],
                    default: false,
                },
            ],
        },
        {
            name: { en: 'StringEnumTriggerTest', cn: '字符串枚举触发测试' },
            type: 'object',
            objs: [
                {
                    _id_: 'k12.test.k12stringenum',
                    name: { en: 'LightSelect', cn: '选择灯' },
                    type: 'string-enum-trigger',
                    objs: [
                        {
                            name: { en: 'Hue', cn: '飞利浦灯' },
                            value: 'hue',
                            trigger: {
                                type: '_ignore_',
                                objs: [
                                    {
                                        _id_: 'k12.test.stringenum.hue.brightness',
                                        name: { en: 'Brightness', cn: '亮度' },
                                        type: 'int',
                                        default: 100,
                                    },
                                    {
                                        _id_: 'k12.test.stringenum.hue.colortemp',
                                        name: { en: 'ColorTemp', cn: '色温' },
                                        type: 'float',
                                        default: 250.0,
                                    },
                                    {
                                        _id_: 'k12.test.stringenum.hue.hue',
                                        name: { en: 'HUE', cn: '饱和度' },
                                        type: 'float',
                                        default: 105.0,
                                    },
                                ],
                            },
                        },
                        {
                            name: { en: 'Konke', cn: '控客灯' },
                            value: 'konke',
                            trigger: {
                                type: '_ignore_',
                                objs: [
                                    {
                                        _id_: 'k12.test.stringenum.konke.brightness',
                                        name: { en: 'Brightness', cn: '亮度' },
                                        type: 'int',
                                        default: 100,
                                    },
                                ],
                            },
                        },
                    ],
                    default: 'hue',
                },
            ],
        },
        {
            name: { en: 'Debug Output', cn: '调试输出: ' },
            type: 'output',
            objs: [],
        },
    ],
}
