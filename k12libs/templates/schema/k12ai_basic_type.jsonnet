// @file k12ai_basic_type.jsonnet
// @brief
// @author QRS
// @version 1.0
// @date 2019-12-23 19:04

local default_schema = import 'default.libsonnet';

{
    description: |||
        K12 Data Template Model for Basic Type
    |||,

    type: 'page',
    objs: [
        default_schema.bool('k12.test', '5'),
        {
            type: 'H',
            objs: [
                default_schema.int('k12.test.basic', '1'),
                default_schema.float('k12.test.basic', '1'),
                default_schema.string('k12.test.basic', '1'),
                default_schema.string_enum('k12.test.basic', '1'),
                default_schema.int_array('k12.test.array', '1'),
                default_schema.float_array('k12.test.array', '1'),
                default_schema.string_array('k12.test.array', '1'),
            ],
        },
        {
            name: { en: 'Debug Output', cn: '调试输出: ' },
            type: 'output',
            objs: [],
        },
    ],
}
