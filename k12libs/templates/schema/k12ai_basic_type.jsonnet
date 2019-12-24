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
        default_schema.bool('k12.test', '1'),
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
        default_schema.text('_js.text.k12.test.text', 1),
        {
            name: { en: 'Debug Output', cn: '调试输出: ' },
            type: 'output',
            objs: [
            ],
        },
    ],
}
