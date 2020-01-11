// @file projects.jsonnet
// @brief
// @author QRS
// @version 1.0
// @date 2020-01-10 19:27

{
    type: 'page',
    objs: [
        {
            _id_: 'project.user',
            name: { en: 'User', cn: self.en },
            type: 'string',
            default: '16601548608',
        },
        {
            _id_: 'project.uuid',
            name: { en: 'UUID', cn: self.en },
            type: 'string',
            default: '10000',
        },
        {
            _id_: 'project.framework',
            name: { en: 'Framework', cn: self.en },
            type: 'string-enum-trigger',
            objs: [
                {
                    name: { en: 'cv', cn: self.en },
                    value: 'k12cv',
                    trigger: {
                        type: '_ignore_',
                        objs: [
                            {
                                _id_: 'project.task',
                                name: { en: 'Task', cn: self.en },
                                type: 'string-enum-trigger',
                                objs: [
                                    {
                                        name: { en: 'cls', cn: self.en },
                                        value: 'cls',
                                        trigger: {
                                            type: '_ignore_',
                                            objs: [
                                                {
                                                    _id_: 'project.dataset',
                                                    name: { en: 'Dataset', cn: self.en },
                                                    type: 'string-enum',
                                                    objs: [
                                                        {
                                                            name: { en: 'mnist', cn: self.en },
                                                            value: 'mnist',
                                                        },
                                                        {
                                                            name: { en: 'cifar10', cn: self.en },
                                                            value: 'cifar10',
                                                        },
                                                    ],
                                                    default: self.objs[1].value,
                                                },
                                            ],
                                        },
                                    },
                                    {
                                        name: { en: 'det', cn: self.en },
                                        value: 'det',
                                        trigger: {
                                            type: '_ignore_',
                                            objs: [
                                                {
                                                    _id_: 'project.dataset',
                                                    name: { en: 'Dataset', cn: self.en },
                                                    type: 'string-enum',
                                                    objs: [
                                                        {
                                                            name: { en: 'voc', cn: self.en },
                                                            value: 'voc',
                                                        },
                                                    ],
                                                    default: self.objs[0].value,
                                                },
                                            ],
                                        },
                                    },
                                ],
                                default: self.objs[0].value,
                            },
                        ],
                    },
                },
                {
                    name: { en: 'nlp', cn: self.en },
                    value: 'k12nlp',
                    trigger: {},
                },
            ],
            default: self.objs[0].value,
        },
        {
            _id_: 'project.confirm',
            name: { en: 'Gen Project Schema', cn: self.en },
            type: 'button',
        },
        {
            name: { en: 'Debug Output', cn: '调试输出: ' },
            type: 'output',
            objs: [
                { value: 'print', name: 'Print' },
                { value: 'kvs', name: 'Key-Value(all)' },
            ],
        },
    ],
}
