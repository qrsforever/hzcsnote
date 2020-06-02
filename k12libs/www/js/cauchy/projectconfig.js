'use strict';
let project_type = [{"type":"cls","name":"分类",method:["VGG:fc_classifier"]},{"type":"det","name":"检测",method:["SSD:single_shot_detector","Yolo:yolov3"]},{type:"seg","name":"分割",method:["FCN:fcn_segmentor"]},{type:"automl","name":"AutoML",method:["Darts:darts"]}];

let model_map = {};
model_map.cls = [{type:'custom',name:'自定义',category:'custom'},{type:'pretrained',name:'预置网络',category:'pretrained'}];
model_map.det = [{type:'custom',name:'自定义',category:'custom'},{type:'SSD',name:'SSD',category:'pretrained'},{type:'Yolo',name:'Yolo',category:'pretrained'}];
model_map.seg = [{type:'DeepLab',name:'DeepLab',category:'pretrained'},{type:'PSPNet',name:'PSPNet',category:'pretrained'}];
model_map.automl = [{type:'automl',name:'AutoML',category:'automl'}];

let sub_model_map = {};
sub_model_map.custom = [{type:'custom',name:'自定义',category:'custom'},{type:'resNet-Basic',name:'ResNet-Basic',category:'custom'},{type:'resNet-Bottleneck',name:'ResNet-Bottleneck',category:'custom'}];
sub_model_map.automl = [{type:'automl',name:'AutoML',category:'automl'}];
sub_model_map.pretrained = [
    {type:'resnet_18',name:'resnet_18',category:'pretrained'},
    {type:'resnet_34',name:'resnet_34',category:'pretrained'},
    {type:'resnet_50',name:'resnet_50',category:'pretrained'},
    {type:'resnet_101',name:'resnet_101',category:'pretrained'},
    {type:'resnet_152',name:'resnet_152',category:'pretrained'},
    {type:'densenet_121',name:'densenet_121',category:'pretrained'},
    {type:'densenet_161',name:'densenet_161',category:'pretrained'},
    {type:'densenet_169',name:'densenet_169',category:'pretrained'},
    {type:'densenet_201',name:'densenet_201',category:'pretrained'},
    {type:'alexnet',name:'alexnet',category:'pretrained'},
    {type:'inception',name:'inception',category:'pretrained'},
    {type:'vgg_11',name:'vgg_11',category:'pretrained'},
    {type:'vgg_13',name:'vgg_13',category:'pretrained'},
    {type:'vgg_16',name:'vgg_16',category:'pretrained'},
    {type:'vgg_19',name:'vgg_19',category:'pretrained'},
    {type:'vgg_11_bn',name:'vgg_11_bn',category:'pretrained'},
    {type:'vgg_13_bn',name:'vgg_13_bn',category:'pretrained'},
    {type:'vgg_16_bn',name:'vgg_16_bn',category:'pretrained'},
    {type:'vgg_19_bn',name:'vgg_19_bn',category:'pretrained'},
    {type:'squeezenet_1_0',name:'squeezenet_1_0',category:'pretrained'},
    {type:'squeezenet_1_1',name:'squeezenet_1_1',category:'pretrained'},];



