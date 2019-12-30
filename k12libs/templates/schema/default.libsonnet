// @file default.libsonnet
// @brief
// @author QRS
// @version 1.0
// @date 2019-12-23 19:10

local dataset_uri = 'http://116.85.5.40:8084/cv/mnist/imgs/test/';

{
    bool(id, num, tips=true): {
        _id_: id + '.k12bool',
        name: { en: 'Bool' + num, cn: '布尔-' + num },
        type: 'bool',
        default: true,
        [if tips then 'tips']: |||
            test int tips, here enter
            let's us continue another line,
        |||,
    },

    int(id, num, tips=true): {
        _id_: id + '.k12int',
        name: { en: 'Int-' + num, cn: '整型-' + num },
        type: 'int',
        min: 0,
        max: 120,
        default: 100,
        [if tips then 'tips']: |||
            test int tips, here enter
            let's us continue another line,
        |||,
    },

    float(id, num, readonly=false, tips=true): {
        _id_: id + '.k12float',
        name: { en: 'Float' + num, cn: '浮点-' + num },
        type: 'float',
        min: 0,
        max: 300,
        default: 200.0,
        readonly: readonly,
        [if tips then 'tips']: |||
            test float tips, here enter
            let's us continue another line,
        |||,
    },

    string(id, num, readonly=false, tips=false): {
        _id_: id + '.k12string',
        name: { en: 'String-' + num, cn: '字符串-' + num },
        type: 'string',
        default: 'string',
        readonly: readonly,
        [if tips then 'tips']: |||
            test string tips, here enter
            let's us continue another line,
        |||,
    },

    string_enum(id, num, tips=false): {
        _id_: id + '.k12stringenum',
        name: { en: 'StringEnum-' + num, cn: '字符串枚举-' + num },
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
        [if tips then 'tips']: |||
            test string-enum tips, here enter
            let's us continue another line,
        |||,
    },

    int_array(id, num, tips=false): {
        _id_: id + '.k12intarray',
        name: { en: 'IntArray-' + num, cn: '整型数组-' + num },
        type: 'int-array',
        default: [[1, 2], [3, 4]],
        [if tips then 'tips']: |||
            test int-array tips, here enter
            let's us continue another line,
        |||,
    },

    float_array(id, num, tips=true): {
        _id_: id + '.k12floatarray',
        name: { en: 'FloatArray' + num, cn: '浮点数组-' + num },
        type: 'float-array',
        default: [1.0, 200.0],
        [if tips then 'tips']: |||
            test float-array tips, here enter
            let's us continue another line,
        |||,
    },

    string_array(id, num, tips=false): {
        _id_: id + '.k12stringarray',
        name: { en: 'StringArray' + num, cn: '字符串数组-' + num },
        type: 'string-array',
        default: ['abc', 'xyz'],
        [if tips then 'tips']: |||
            test string-array tips, here enter
            let's us continue another line,
        |||,
    },

    image(id, num, link): {
        _id_: id + '.k12image',
        name: { en: 'MediaImage' + num, cn: '媒体图片-' + num },
        type: 'image',
        width: 60,
        height: 60,
        default: dataset_uri + link,
    },

    text(id, num, txt=''): {
        _id_: id + '.k12text',
        name: { en: 'Text' + num, cn: '文本-' + num },
        type: 'text',
        width: 300,
        height: 120,
        default: if std.length(txt) == 0 then
            |||
                line-1
                line-2
                line-3
            ||| else txt,
    },
}
