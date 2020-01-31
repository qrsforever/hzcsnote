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

local _task_trigger(id, label, options) = {
    _id_: id,
    name: { en: label, cn: self.en },
    type: 'string-enum-trigger',
    objs: [
        {
            name: { en: opt.task.name, cn: self.en },
            value: opt.task.value,
            trigger: {
                type: '_ignore_',
                objs: [
                    _string_enum('project.network', 'Network', opt.networks),
                    _string_enum('project.dataset', 'Dataset', opt.datasets),
                ],
            },
        }
        for opt in options
    ],
    tips: 'aaaa',
    default: self.objs[0].value,
};

local _projects = {
    k12cv: [
        {
            task: { name: 'cls', value: self.name },
            networks: [
                { name: 'base_model', value: self.name },
            ],
            datasets: [
                { name: 'cifar10', value: self.name },
                { name: 'mnist', value: self.name },
            ],
        },
        {
            task: { name: 'det', value: self.name },
            networks: [
                { name: 'vgg16_ssd300', value: self.name },
                { name: 'vgg16_ssd512', value: self.name },
                { name: 'darknet_yolov3', value: self.name },
                { name: 'faster_rcnn', value: self.name },
            ],
            datasets: [
                { name: 'VOC07+12_DET', value: self.name },
            ],
        },
    ],
    k12nlp: [
        {
            task: { name: 'sentiment_analysis', value: self.name },
            networks: [
                { name: 'basic_classifier', value: self.name },
            ],
            datasets: [
                { name: 'sst', value: self.name },
            ],
        },
    ],
    k12rl: [
        {
            task: { name: 'atari', value: self.name },
            networks: [
                { name: 'dqn', value: self.name },
            ],
            datasets: [
                { name: 'pong', value: self.name },
                { name: 'seaquest', value: self.name },
                { name: 'qbert', value: self.name },
                { name: 'chopper_command', value: self.name },
            ],
        },
    ],
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
                        objs: [_task_trigger('project.task', 'Task', _projects.k12cv)],
                    },
                },
                {
                    name: { en: 'nlp', cn: self.en },
                    value: 'k12nlp',
                    trigger: {
                        type: '_ignore_',
                        objs: [_task_trigger('project.task', 'Task', _projects.k12nlp)],
                    },
                },
                {
                    name: { en: 'rl', cn: self.en },
                    value: 'k12rl',
                    trigger: {
                        type: '_ignore_',
                        objs: [_task_trigger('project.task', 'Task', _projects.k12rl)],
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
            name: { en: 'Debug', cn: '调试输出: ' },
            type: 'output',
            objs: [
                { value: 'print', name: 'Print' },
                { value: 'kvs', name: 'Key-Value(all)' },
            ],
        },
    ],
}
