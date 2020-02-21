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
    default: self.objs[0].value,
};

local _projects = {
    k12cv: [
        {
            task: { name: 'cls', value: self.name },
            networks: [
                { name: 'base_model', value: self.name },
                { name: 'custom_base', value: self.name },
            ],
            datasets: [
                { name: 'cifar10', value: self.name },
                { name: 'mnist', value: self.name },
                { name: 'Animals', value: self.name },
                { name: 'Boats', value: self.name },
                { name: 'cactus', value: self.name },
                { name: 'Chars74K', value: self.name },
                { name: 'dogsVsCats', value: self.name },
                { name: 'Dogs', value: self.name },
                { name: 'EMNIST_Balanced', value: self.name },
                { name: 'EMNIST_Digits', value: self.name },
                { name: 'EMNIST_Letters', value: self.name },
                { name: 'EMNIST_MNIST', value: self.name },
                { name: 'FashionMNIST', value: self.name },
                { name: 'Fruits360', value: self.name },
                { name: 'kannada', value: self.name },
                { name: 'kannada_dig', value: self.name },
                { name: 'KMNIST', value: self.name },
            ],
        },
        {
            task: { name: 'det', value: self.name },
            networks: [
                { name: 'vgg16_ssd300', value: self.name },
                { name: 'vgg16_ssd512', value: self.name },
                // { name: 'darknet_yolov3', value: self.name },
                // { name: 'faster_rcnn', value: self.name },
                { name: 'custom_ssd300', value: self.name },
                { name: 'custom_ssd512', value: self.name },
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
        {
            task: { name: 'mujoco', value: self.name },
            networks: [
                { name: 'pg', value: self.name },
            ],
            datasets: [
                { name: 'CartPole-v0', value: self.name },
                { name: 'Pendulum-v0', value: self.name },
            ],
        },
    ],
    k12ml: [
        {
            task: { name: 'classifier', value: self.name },
            networks: [
                { name: 'svc', value: self.name },
                { name: 'knn', value: self.name },
                { name: 'decision_tree', value: self.name },
                { name: 'random_forest', value: self.name },
                { name: 'gaussian_nb', value: self.name },
            ],
            datasets: [
                { name: 'iris', value: self.name },
                { name: 'digits', value: self.name },
                { name: 'wine', value: self.name },
                { name: 'breast_cancer', value: self.name },
            ],
        },
        {
            task: { name: 'regressor', value: self.name },
            networks: [
                { name: 'svr', value: self.name },
                { name: 'knn', value: self.name },
                { name: 'decision_tree', value: self.name },
                { name: 'random_forest', value: self.name },
            ],
            datasets: [
                { name: 'boston', value: self.name },
                { name: 'diabetes', value: self.name },
                { name: 'linnerud', value: self.name },
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
                {
                    name: { en: 'ml', cn: self.en },
                    value: 'k12ml',
                    trigger: {
                        type: '_ignore_',
                        objs: [_task_trigger('project.task', 'Task', _projects.k12ml)],
                    },
                },
            ],
            [if 'k12ai' != framework then 'readonly']: true,
            default: if 'k12ai' == framework then 'k12cv' else framework,
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
