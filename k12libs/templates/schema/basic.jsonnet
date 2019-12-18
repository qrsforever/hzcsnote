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
        name: { en: 'String' + id, cn: '字符串-' + id },
        type: 'string',
        default: 'string',
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
                        {
                            name: { en: 'navigation1', cn: '导航栏-1' },
                            type: 'navigation',
                            objs: [
                                {
                                    name: { en: 'group1', cn: '组-1' },
                                    type: '_ignore_',
                                    objs: [
                                        default_schema.bool('1'),
                                        default_schema.int('1'),
                                        default_schema.float('1'),
                                        default_schema.string('1'),
                                    ],  // objs
                                },
                                {
                                    name: { en: 'group2', cn: '组-2' },
                                    type: '_ignore_',
                                    objs: [
                                        default_schema.bool('2'),
                                        default_schema.int('2'),
                                        default_schema.float('2'),
                                        default_schema.string('2'),
                                    ],  // objs
                                },
                            ],  // objs
                        },
                        {
                            name: { en: 'output', cn: '输出信息' },
                            type: 'output',
                            objs: [],
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
                    name: { en: 'navigation2', cn: '导航栏-2' },
                    type: 'navigation',
                    objs: [
                        {
                            name: { en: 'group1', cn: '组-1' },
                            type: '_ignore_',
                            objs: [
                                default_schema.bool('4'),
                                default_schema.int('4'),
                                default_schema.float('4'),
                                default_schema.string('4'),
                            ],  // objs
                        },
                        {
                            name: { en: 'group2', cn: '组-2' },
                            type: '_ignore_',
                            objs: [
                            ],  // objs
                        },
                    ],  // objs
                },
            ],
        },
        {
            name: { en: 'tab3', cn: '页标签-3' },
            type: 'tab',
            objs: [
                default_schema.bool('5'),
                default_schema.int('5'),
                default_schema.float('5'),
                default_schema.string('5'),
            ],  // objs
        },
    ],  // objs
}
