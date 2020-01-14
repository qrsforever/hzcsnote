// @file projects.jsonnet
// @brief
// @author QRS
// @version 1.0
// @date 2020-01-10 19:27

{
    type: 'page',
    objs: [
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
                                                    _id_: 'project.network',
                                                    name: { en: 'Method', cn: self.en },
                                                    type: 'string-enum',
                                                    objs: [
                                                        {
                                                            name: { en: 'base model', cn: self.en },
                                                            value: 'base_model',
                                                        },
                                                    ],
                                                    default: self.objs[0].value,
                                                },
                                                {
                                                    _id_: 'project.dataset',
                                                    name: { en: 'Dataset', cn: self.en },
                                                    type: 'string-enum',
                                                    objs: [
                                                        {
                                                            name: { en: 'cifar10', cn: self.en },
                                                            value: 'cifar10',
                                                        },
                                                        {
                                                            name: { en: 'mnist', cn: self.en },
                                                            value: 'mnist',
                                                        },
                                                    ],
                                                    default: self.objs[0].value,
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
                                                    _id_: 'project.network',
                                                    name: { en: 'Network', cn: self.en },
                                                    type: 'string-enum',
                                                    objs: [
                                                        {
                                                            name: { en: 'ssd300', cn: self.en },
                                                            value: 'vgg16_ssd300',
                                                        },
                                                        {
                                                            name: { en: 'ssd512', cn: self.en },
                                                            value: 'vgg16_ssd512',
                                                        },
                                                        {
                                                            name: { en: 'yolov3', cn: self.en },
                                                            value: 'darknet_yolov3',
                                                        },
                                                        {
                                                            name: { en: 'faster rcnn', cn: self.en },
                                                            value: 'faster_rcnn',
                                                        },
                                                    ],
                                                    default: self.objs[0].value,
                                                },
                                                {
                                                    _id_: 'project.dataset',
                                                    name: { en: 'Dataset', cn: self.en },
                                                    type: 'string-enum',
                                                    objs: [
                                                        {
                                                            name: { en: 'voc', cn: self.en },
                                                            value: 'VOC07+12_DET',
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
                    trigger: {
                        type: '_ignore_',
                        objs: [
                            {
                                _id_: 'project.task',
                                name: { en: 'Task', cn: self.en },
                                type: 'string-enum-trigger',
                                objs: [
                                    {
                                        name: { en: 'sa', cn: self.en },
                                        value: 'sentiment_analysis',
                                        trigger: {
                                            type: '_ignore_',
                                            objs: [
                                                {
                                                    _id_: 'project.network',
                                                    name: { en: 'Method', cn: self.en },
                                                    type: 'string-enum',
                                                    objs: [
                                                        {
                                                            name: { en: 'basic classifier', cn: self.en },
                                                            value: 'basic_classifier',
                                                        },
                                                    ],
                                                    default: self.objs[0].value,
                                                },
                                                {
                                                    _id_: 'project.dataset',
                                                    name: { en: 'Dataset', cn: self.en },
                                                    type: 'string-enum',
                                                    objs: [
                                                        {
                                                            name: { en: 'sst', cn: self.en },
                                                            value: 'sst',
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
