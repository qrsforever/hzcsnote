// @file lr.jsonnet
// @brief
// @author QRS
// @version 1.0
// @date 2019-12-12 19:58

{
    local this = self,
    _id_:: 'lr',
    name: { en: 'Learn Rate', cn: self.en },
    type: 'accordion',
    objs: [
        {
            type: 'HV',
            objs: [
                {
                    _id_: this._id_ + '.metric',
                    name: { en: 'Metric', cn: self.en },
                    type: 'string-enum',
                    objs: [
                        {
                            name: { en: 'epoch', cn: self.en },
                            value: 'epoch',
                        },
                        {
                            name: { en: 'iters', cn: self.en },
                            value: 'iters',
                        },
                    ],
                    default: 'epoch',
                },
                {
                    _id_: this._id_ + '.base_lr',
                    name: { en: 'Base LR', cn: self.en },
                    type: 'float',
                    default: 0.001,
                },
                {
                    _id_: this._id_ + '.is_warm',
                    name: { en: 'Warm up', cn: self.en },
                    type: 'bool-trigger',
                    objs: [
                        {
                            name: { en: 'True', cn: self.en },
                            value: true,
                            trigger: {
                                type: 'object',
                                objs: [
                                    {
                                        _id_: this._id_ + '.warm_iters',
                                        name: { en: 'Warm Iters', cn: self.en },
                                        type: 'int',
                                        default: 1000,
                                    },
                                    {
                                        _id_: this._id_ + '.warm.power',
                                        name: { en: 'Power', cn: self.en },
                                        type: 'float',
                                        default: 1.0,
                                    },
                                    {
                                        _id_: this._id_ + '.warm.freeze_backbone',
                                        name: { en: 'freeze backbone', cn: self.en },
                                        type: 'bool',
                                        default: false,
                                    },
                                ],
                            },
                        },
                        {
                            name: { en: 'False', cn: self.en },
                            value: false,
                            trigger: {
                            },
                        },
                    ],
                    default: false,
                },
                import 'lr_policy.jsonnet',
            ],
        },
    ],
}
