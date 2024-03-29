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
                { name: 'resnet18', value: self.name },
                // { name: 'resnet50', value: self.name },
                // { name: 'resnet101', value: self.name },
                // { name: 'resnet152', value: self.name },
                // { name: 'vgg11', value: self.name },
                // { name: 'vgg16', value: self.name },
                // { name: 'vgg19', value: self.name },
                // { name: 'vgg16_bn', value: self.name },
                // { name: 'vgg19_bn', value: self.name },
                // { name: 'alexnet', value: self.name },
                { name: 'custom_base', value: self.name },
            ],
            datasets: [
                { name: 'rmnist', value: self.name },
                { name: 'rcifar10', value: self.name },
                { name: 'rflowers', value: self.name },
                { name: 'rchestxray', value: self.name },
                { name: 'rfruits', value: self.name },
                { name: 'rDogsVsCats', value: self.name },
                // { name: 'Animals', value: self.name },
                // { name: 'Boats', value: self.name },
                // { name: 'cactus', value: self.name },
                // { name: 'Chars74K', value: self.name },
                // { name: 'dogAndCat', value: self.name },
                // { name: 'Dogs', value: self.name },
                // { name: 'EMNIST_Balanced', value: self.name },
                // { name: 'EMNIST_Digits', value: self.name },
                // { name: 'EMNIST_Letters', value: self.name },
                // { name: 'EMNIST_MNIST', value: self.name },
                // { name: 'FashionMNIST', value: self.name },
                // { name: 'Fruits360', value: self.name },
                // { name: 'kannada', value: self.name },
                // { name: 'kannada_dig', value: self.name },
                // { name: 'KMNIST', value: self.name },
                // { name: 'cellular', value: self.name },
                // { name: 'aliproducts', value: self.name },
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
                { name: 'underwater', value: self.name },
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
        {
            task: { name: 'named_entity_recognization', value: self.name },
            networks: [
                { name: 'crf_tagger', value: self.name },
            ],
            datasets: [
                { name: 'conll2003', value: self.name },
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
                { name: 'Pong-v4', value: self.name },
            ],
        },
        {
            task: { name: 'classic', value: self.name },
            networks: [
                { name: 'dqn', value: self.name },
                { name: 'pg', value: self.name },
            ],
            datasets: [
                { name: 'CartPole-v0', value: self.name },
                { name: 'Pendulum-v0', value: self.name },
            ],
        },
        // {
        //     task: { name: 'algorithmic', value: self.name },
        //     networks: [],
        //     datasets: [],
        // },
        // {
        //     task: { name: 'box2d', value: self.name },
        //     networks: [],
        //     datasets: [],
        // },
        // {
        //     task: { name: 'toy_text', value: self.name },
        //     networks: [
        //     ],
        //     datasets: [
        //         { name: 'Blackjack-v0', value: self.name },
        //     ],
        // },
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
                { name: 'adaboost', value: self.name },
                { name: 'xgboost', value: self.name },
                { name: 'gradient_boosting', value: self.name },
            ],
            datasets: [
                { name: 'iris', value: self.name },
                { name: 'digits', value: self.name },
                { name: 'wine', value: self.name },
                { name: 'breast_cancer', value: self.name },
                { name: 'sf-crime', value: self.name },
                { name: 'titanic', value: self.name },
            ],
        },
        {
            task: { name: 'regressor', value: self.name },
            networks: [
                { name: 'svr', value: self.name },
                { name: 'knn', value: self.name },
                { name: 'decision_tree', value: self.name },
                { name: 'random_forest', value: self.name },
                { name: 'logistic', value: self.name },
                { name: 'gradient_boosting', value: self.name },
                { name: 'adaboost', value: self.name },
                { name: 'xgboost', value: self.name },
            ],
            datasets: [
                { name: 'boston', value: self.name },
                { name: 'diabetes', value: self.name },
                { name: 'linnerud', value: self.name },
                { name: 'sf-crime', value: self.name },
            ],
        },
        {
            task: { name: 'cluster', value: self.name },
            networks: [
                { name: 'kmeans', value: self.name },
            ],
            datasets: [
                { name: 'iris', value: self.name },
            ],
        },
    ],
    k123d: [
        {
            task: { name: 'make3d', value: self.name },
            networks: [
                { name: 'fcrn', value: self.name },
            ],
            datasets: [
                { name: 'nyu', value: self.name },
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
                {
                    name: { en: '3d', cn: self.en },
                    value: 'k123d',
                    trigger: {
                        type: '_ignore_',
                        objs: [_task_trigger('project.task', 'Task', _projects.k123d)],
                    },
                },
            ],
            [if 'k12ai' != framework then 'readonly']: true,
            default: if 'k12ai' == framework then 'k12cv' else framework,
        },
        {
            _id_: 'project.confirm',
            name: { en: 'Goto Project', cn: '进入项目' },
            type: 'button',
        },
    ],
}
