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
                                            ],
                                        },
                                    ],
                                },
                                {
                                    name: { en: 'accordion2', cn: '折叠卡-2' },
                                    objs: [
                                        default_schema.text('_js.text.a.b', '4'),
                                    ],
                                },
                                {
                                    name: { en: 'accordion3', cn: '折叠卡-3' },
                                    objs: [],
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
                                    type: '_ignore_',
                                    objs: [
                                        default_schema.text('_js.text.a.y', '5'),
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
                    objs: [
                        {
                            type: 'V',
                            objs: [
                                {
                                    type: 'H',
                                    objs: [
                                        default_schema.int('_js.text.x.v', 'V1-H1'),
                                        default_schema.int('_js.text.x.v', 'V1-H2'),
                                    ],
                                },
                                {
                                    type: 'H',
                                    objs: [
                                        default_schema.int('_js.text.x.v', 'V2-H1'),
                                        default_schema.int('_js.text.x.v', 'V2-H2'),
                                    ],
                                },
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
