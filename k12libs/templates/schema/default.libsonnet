// @file default.libsonnet
// @brief
// @author QRS
// @version 1.0
// @date 2019-12-23 19:10

{
    bool(id, num): {
        _id_: id + '.k12bool',
        name: { en: 'Bool' + num, cn: '布尔-' + num },
        type: 'bool',
        default: true,
    },

    int(id, num): {
        _id_: id + '.k12int',
        name: { en: 'Int-' + num, cn: '整型-' + num },
        type: 'int',
        min: 0,
        max: 120,
        default: 100,
    },

    float(id, num): {
        _id_: id + '.k12float',
        name: { en: 'Float' + num, cn: '浮点-' + num },
        type: 'float',
        min: 0,
        max: 300,
        default: 200.0,
    },

    string(id, num): {
        _id_: id + '.k12string',
        name: { en: 'String-' + num, cn: '字符串-' + num },
        type: 'value',
        default: 'string',
    },

    string_enum(id, num): {
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
    },

    int_array(id, num): {
        _id_: id + '.k12intarray',
        name: { en: 'IntArray-' + num, cn: '整型数组-' + num },
        type: 'int-array',
        default: [[1, 2], [3, 4]],
    },

    float_array(id, num): {
        _id_: id + '.k12floatarray',
        name: { en: 'FloatArray' + num, cn: '浮点数组-' + num },
        type: 'float-array',
        default: [1.0, 200.0],
    },

    string_array(id, num): {
        _id_: id + '.k12stringarray',
        name: { en: 'StringArray' + num, cn: '字符串数组-' + num },
        type: 'string-array',
        default: ['abc', 'xyz'],
    },
}
