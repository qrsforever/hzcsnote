// @file basic.jsonnet
// @brief
// @author QRS
// @version 1.0
// @date 2019-12-18 21:08

local default_schema = import 'default.libsonnet';
local complex_schema = import 'k12ai_complex_type.jsonnet';

{
    description: |||
        K12 Data Template Model For Layout
    |||,

    type: 'page',
    objs: [
        {
            type: 'tab',
            objs: [
                {
                    name: { en: 'tab1', cn: '页标签-1' },
                    objs: [
                        {
                            type: 'accordion',
                            objs: [
                                {
                                    name: { en: 'accordion1', cn: '折叠卡-1' },
                                    objs: [
                                        {
                                            name: { en: 'navigation1', cn: '导航栏-1' },
                                            type: 'navigation',
                                            objs: [
                                                {
                                                    name: { en: 'group1', cn: '选项卡-1' },
                                                    type: 'object',
                                                    objs: [
                                                        default_schema.text('_js.text.a.b',
                                                                            '1',
                                                                            |||
                                                                                我的右上角

                                                                                **有**

                                                                                粗体黑字的分割标题
                                                                            |||),
                                                        default_schema.bool('k12.test', '1'),
                                                        {
                                                            type: 'H',
                                                            name: { en: 'Layout-H', cn: '水平-布局' },
                                                            objs: [
                                                                default_schema.int('k12.test.basic',
                                                                                   '1',
                                                                                   tips=true),
                                                                default_schema.float('k12.test.basic', '1'),
                                                                default_schema.string('k12.test.basic',
                                                                                      '1',
                                                                                      tips=true),
                                                                default_schema.string('k12.test.basic', '1', true),
                                                            ],
                                                        },
                                                    ],
                                                },
                                                {
                                                    name: { en: 'group2', cn: '选项卡-2' },
                                                    objs: [
                                                        default_schema.text('_js.text.a.m', '2', |||
                                                            我的右上角

                                                            **没有**

                                                            粗体黑字的分割标题
                                                        |||),
                                                        {
                                                            type: 'V',
                                                            name: { en: 'Layout-H', cn: '垂直-布局' },
                                                            objs: [
                                                                default_schema.int('k12.test.basic', '2'),
                                                                default_schema.float('k12.test.basic', '2'),
                                                                default_schema.string('k12.test.basic', '2'),
                                                                default_schema.string('k12.test.basic', '2', true),
                                                            ],
                                                        },
                                                    ],
                                                },
                                            ],
                                        },
                                        {
                                            name: { en: 'navigation2', cn: '导航栏-2' },
                                            type: 'navigation',
                                            objs: [
                                                {
                                                    name: { en: 'group3', cn: '选项卡-1' },
                                                    type: 'object',
                                                    objs: [
                                                        {
                                                            type: 'H',
                                                            name: { en: 'Layout-H', cn: '水平-布局' },
                                                            objs: [
                                                                default_schema.string_enum('k12.test.basic',
                                                                                           '1',
                                                                                           tips=true),
                                                                default_schema.int_array('k12.test.array', '1'),
                                                                default_schema.float_array('k12.test.array', '1'),
                                                                default_schema.string_array('k12.test.array', '1'),
                                                            ],
                                                        },
                                                    ],
                                                },
                                                {
                                                    name: { en: 'group4', cn: '选项卡-2' },
                                                    type: 'object',
                                                    objs: [
                                                        default_schema.text('_js.text.a.f', '4', |||
                                                            我的右上角

                                                            **没有**

                                                            粗体黑字的分割标题
                                                        |||),
                                                    ],
                                                },
                                            ],
                                        },

                                        {
                                            type: 'accordion',
                                            objs: [
                                                {
                                                    name: { en: 'accordion1-1', cn: '第二层折叠卡1-1(嵌套)' },
                                                    objs: [
                                                        {
                                                            type: 'H',
                                                            objs: [
                                                                default_schema.image('_js.image.k12.test.image', 0, '00000.jpg'),
                                                                default_schema.image('_js.image.k12.test.image', 1, '00001.jpg'),
                                                                default_schema.image('_js.image.k12.test.image', 2, '00002.jpg'),
                                                                default_schema.image('_js.image.k12.test.image', 3, '00003.jpg'),
                                                                default_schema.image('_js.image.k12.test.image', 4, '00004.jpg'),
                                                                default_schema.image('_js.image.k12.test.image', 5, '00005.jpg'),
                                                                default_schema.image('_js.image.k12.test.image', 6, '00006.jpg'),
                                                                default_schema.image('_js.image.k12.test.image', 7, '00007.jpg'),
                                                                default_schema.image('_js.image.k12.test.image', 8, '00008.jpg'),
                                                                default_schema.image('_js.image.k12.test.image', 9, '00009.jpg'),
                                                            ],
                                                        },
                                                    ] + complex_schema.objs[0:3],
                                                },
                                                {
                                                    name: { en: 'accordion1-2', cn: '第二层折叠卡1-2(嵌套)' },
                                                    objs: [
                                                        default_schema.bool('k12.test', '1-2'),
                                                    ],
                                                },
                                            ],
                                        },

                                    ],
                                },
                                {
                                    name: { en: 'accordion2', cn: '折叠卡-2' },
                                    objs: [
                                        default_schema.text('_js.text.a.w', '4'),
                                    ],
                                },
                                {
                                    name: { en: 'accordion3', cn: '折叠卡-3' },
                                    objs: [
                                        default_schema.bool('k12.test', '3-1'),
                                    ],
                                },
                            ],
                        },
                    ],
                },
                {
                    name: { en: 'tab2', cn: '页标签-2' },
                    objs: [
                        {
                            name: { en: 'navigation3', cn: '导航栏-2' },
                            type: 'navigation',
                            objs: [
                                {
                                    name: { en: 'group1', cn: '选项卡-1' },
                                    objs: [
                                        default_schema.text('_js.text.a.y', '5'),
                                    ],
                                },
                                {
                                    name: { en: 'group2', cn: '选项卡-2' },
                                    objs: [
                                    ],
                                },
                            ],
                        },
                    ],
                },
                {
                    name: { en: 'tab3', cn: '页标签-3' },
                    objs: [
                        {
                            type: 'H',
                            objs: [
                                default_schema.text('_js.text.a.x', '6'),
                            ],
                        },
                    ],  // objs
                },
            ],
        },
        {
            name: { en: 'Debug Output', cn: '调试输出: ' },
            type: 'output',
            objs: [],
        },
    ],  // objs
}
