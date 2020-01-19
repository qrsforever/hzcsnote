// @file projects.jsonnet
// @brief
// @author QRS
// @version 1.0
// @date 2020-01-10 19:27

local _string_enum(id, label, options) = {
    _id_: id,
    name: { en: label, cn: self.en },
    type: 'string-enum',
    objs: [
        {
            name: { en: opt.name, cn: self.en },
            value: opt.value,
        }
        for opt in options
    ],
    default: self.objs[0].value,
};

local _cv = {
    cls: {
        networks: [
            { name: 'base model', value: 'base_model' },
        ],
        datasets: [
            { name: 'cifar10', value: 'cifar10' },
            { name: 'mnist', value: 'mnist' },
        ],
    },
    det: {
        networks: [
            { name: 'ssd300', value: 'vgg16_ssd300' },
            { name: 'ssd512', value: 'vgg16_ssd512' },
            { name: 'yolov3', value: 'darknet_yolov3' },
            { name: 'faster rcnn', value: 'faster_rcnn' },
        ],
        datasets: [
            { name: 'voc', value: 'VOC07+12_DET' },
        ],
    },
};

local _nlp = {
    sa: {
        networks: [
            { name: 'basic classifier', value: 'basic_classifier' },
        ],
        datasets: [
            { name: 'sst', value: 'sst' },
        ],
    },
};

local _rl = {
    atari: {
        networks: [
            { name: 'dqn', value: 'dqn' },
        ],
        datasets: [
            { name: 'pong', value: 'pong' },
        ],
    },
};

function(framework) {
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
                                                _string_enum('project.network', 'Network', _cv.cls.networks),
                                                _string_enum('project.dataset', 'Dataset', _cv.cls.datasets),
                                            ],
                                        },
                                    },
                                    {
                                        name: { en: 'det', cn: self.en },
                                        value: 'det',
                                        trigger: {
                                            type: '_ignore_',
                                            objs: [
                                                _string_enum('project.network', 'Network', _cv.det.networks),
                                                _string_enum('project.dataset', 'Dataset', _cv.det.datasets),
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
                                                _string_enum('project.network', 'Network', _nlp.sa.networks),
                                                _string_enum('project.dataset', 'Dataset', _nlp.sa.datasets),
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
                    name: { en: 'rl', cn: self.en },
                    value: 'k12rl',
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
                                                _string_enum('project.network', 'Network', _rl.atari.networks),
                                                _string_enum('project.dataset', 'Dataset', _rl.atari.datasets),
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
            default: framework,
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
