// @file basic.jsonnet
// @brief
// @author QRS
// @version 1.0
// @date 2019-12-18 21:08

local default_schema = import 'default.libsonnet';

{
    description: |||
        K12 Data Template Model For Layout
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
                                    ],
                                },
                                {
                                    name: { en: 'group2', cn: '选项卡-2' },
                                    type: 'object',
                                    objs: [
                                        default_schema.text('_js.text.a.v', '2'),
                                    ],
                                },
                            ],
                        },
                        {
                            name: { en: 'navigation2', cn: '导航栏-2' },
                            type: 'navigation',
                            objs: [
                                {
                                    name: { en: 'group3', cn: '选项卡-3' },
                                    type: '_ignore_',
                                    objs: [
                                        default_schema.text('_js.text.a.m', '3', |||
                                            我的右上角

                                            **没有**

                                            粗体黑字的分割标题
                                        |||),
                                    ],
                                },
                                {
                                    name: { en: 'group4', cn: '选项卡-4' },
                                    type: '_ignore_',
                                    objs: [
                                        default_schema.text('_js.text.a.k', '4'),
                                    ],
                                },
                            ],
                        },
                    ],
                },
                {
                    name: { en: 'accordion2', cn: '折叠卡-2' },
                    type: 'accordion',
                    objs: [
                        default_schema.text('_js.text.a.b', '5'),
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
                                default_schema.text('_js.text.a.y', '6'),
                            ],
                        },
                        {
                            name: { en: 'group2', cn: '选项卡-2' },
                            type: '_ignore_',
                            objs: [
                            ],
                        },
                    ],
                },
            ],
        },
        {
            name: { en: 'tab3', cn: '页标签-3' },
            type: 'tab',
            objs: [
                {
                    type: 'H',
                    objs: [
                        default_schema.text('_js.text.a.x', '7'),
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
