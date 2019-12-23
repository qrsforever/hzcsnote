// @file k12ai_complex_type.jsonnet
// @brief
// @author QRS
// @version 1.0
// @date 2019-12-23 19:30

local city_group_item(city, descr, flg=0) = {
    _id_: '_js.k12.test.k12booltrigger.' + city,
    name: { en: 'Talk' + city, cn: '评价' + descr },
    type: 'bool-trigger',
    objs: [
        {
            value: true,
            trigger: {
                type: '_ignore_',
                objs: [
                    {
                        _id_: '_js_stringenumgroup.k12.test.' + city,
                        name: { en: city, cn: descr },
                        type: 'string-enum',
                        objs: [
                            {
                                name: { en: 'Good', cn: '良好' },
                                value: 'k12.test.stringenumgroup.good',
                            },
                            {
                                name: { en: 'Bad', cn: '很差' },
                                value: 'k12.test.stringenumgroup.bad',
                            },
                        ],
                        default: 'k12.test.stringenumgroup.good',
                    },
                    {
                        _id_: 'k12.test.stringenumgroup' + city + '.PM25',
                        name: { en: 'PM2.5', cn: self.en },
                        type: 'int',
                        max: 500,
                        min: 0,
                        default: 400,
                    },
                    {
                        _id_: 'k12.test.stringenumgroup' + city + '.AQI',
                        name: { en: 'AQI', cn: self.en },
                        type: 'float',
                        default: 10.0,
                    },
                    if flg == 1 then {
                        _id_: 'k12.test.stringenumgroup' + city + '.Humidity',
                        name: { en: 'Humidity', cn: self.en },
                        type: 'float',
                        default: 10.0,
                    } else {},
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
};


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
            name: { en: 'StringEnumGroupTriggerTest', cn: '字符串枚举分组触发测试' },
            type: 'H',
            objs: [
                {
                    type: 'object',
                    objs: [
                        city_group_item('BeiJing', '北京', 1),
                        city_group_item('ShangHai', '上海'),
                        city_group_item('ShenZhen', '深圳', 1),
                        city_group_item('TengZhou', '滕州'),
                    ],
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
