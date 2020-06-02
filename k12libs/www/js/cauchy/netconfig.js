'use strict';
var netEnum = [];
//netEnum["denseNet"] = {};
netEnum["resNet-Basic"] = {};
netEnum["resNet-Bottle"] = {};
netEnum["SSD"] = {};
netEnum["DeepLab"] = {};
netEnum["PSPNet"] = {};
netEnum["Yolo"] = {};
//netEnum["resNet"] = {};
//netEnum["squeezeNet"] = {};
//netEnum["inceptionNet"] = {};
// netEnum["denseNet"].layout = "seqblock";
// netEnum["denseNet"].nodes = [{key:"dense_Conv1",category:"Conv"},{key:"dense_Relu1",category:"Act"},{key:"dense_Norm1",category:"Norm"},{key:"dense_block",category:"seqblock",name:"subnet"}];
// netEnum["denseNet"].links = [{from:"dense_Conv1",to:"dense_Relu1"},{from:"dense_Relu1",to:"dense_dense_Norm1"},{from:"Norm1",to:"dense_Conv"}];
// netEnum["denseNet"].subnet = {};
// netEnum["denseNet"].subnet.type = "";
// netEnum["denseNet"].subnet.nodes = [{key:"dense_Conv",category:"Conv"},{key:"dense_Relu",category:"Act"},{key:"dense_Norm",category:"Norm"}];
// netEnum["denseNet"].subnet.links = [{from:"dense_Conv",to:"dense_Relu"},{from:"dense_",to:"dense_Norm"}];

netEnum["resNet-Basic"].layout = "seqblock";

netEnum["resNet-Basic"].nodes = [{key:"Input",category:"Input",subtype:"Input",params:{}},
    {key:"resNet1_Conv1",category:"Conv",subtype:"Conv2d",params:{in_channels:"3",out_channels:"64",kernel_size:"7",stride:"2",padding:"3",bias:'False'}},
    {key:"resNet1_Norm1",category:"Norm",subtype:"BatchNorm2d",params:{num_features:"64"}},
    {key:"resNet1_Relu1",category:"Act",subtype:"Relu",params:{inplace:'True'}},
    {key:"resNet1_Pooling1",category:"Pool",subtype:"MaxPool2d",params:{kernel_size:"3",stride:"2",padding:"1"}},
    {key:"resBasicblock",category:"seqblock",name:"subnet"},
    {key:"resNet1_Pooling2",category:"Pool", subtype:"AdaptiveAvgPool2d",params:{output_size : "1"}},
    {key:"resNet1_Func1",category:"Vulkan", subtype:"Flatten",params:{start_dim : "1"}},
    {key:"resNet1_Linear1",category:"Linear",subtype:"Linear",params:{in_features : "512 * block.expansion",out_features:"num_classes"}},
    {key:"resNet1_Output",category:"Output",subtype:"Output",params:{}}];
    
netEnum["resNet-Basic"].links = [{from:"Input",to:"resNet1_Conv1"},
    {from:"resNet1_Conv1",to:"resNet1_Norm1"},
    {from:"resNet1_Norm1",to:"resNet1_Relu1"},
    {from:"resNet1_Relu1",to:"resNet1_Pooling1"},
    {from:"resNet1_Pooling1",to:"resNet1_Conv"},
    {from:"resNet1_Norm2",to:"resNet1_Pooling2"},
    {from:"resNet1_Pooling2",to:"resNet1_Func1"},
    {from:"resNet1_Func1",to:"resNet1_Linear1"},
    {from:"resNet1_Linear1",to:"resNet1_Output"}];

netEnum["resNet-Basic"].subnet = {};
netEnum["resNet-Basic"].subnet.type = "resBasicblock";
netEnum["resNet-Basic"].subnet.nodes = [    
    {key:"resNet1_Conv",category:"Conv",params:{in_channels:"in_planes",out_channels:"planes",kernel_size:"3",stride:"1",padding:"1"}},
    {key:"resNet1_Norm",category:"Norm",params:{num_features : "planes"}},
    {key:"resNet1_Relu",category:"Act",params:{inplace : "True"}}
    ,{key:"resNet1_Conv2",category:"Conv",params:{in_channels:"planes",out_channels:"planes",kernel_size:"3",stride:"stride",padding:"1",bias:"True"}},
    {key:"resNet1_Norm2",category:"Norm",params:{num_features : "planes"}}];
netEnum["resNet-Basic"].subnet.links = [
    {from:"resNet1_Conv",to:"resNet1_Norm"},
    {from:"resNet1_Norm",to:"resNet1_Relu"},
    {from:"resNet1_Relu",to:"resNet1_Conv2"},
    {from:"resNet1_Conv2",to:"resNet1_Norm2"}];


netEnum["resNet-Bottle"].layout = "seqblock";
netEnum["resNet-Bottle"].nodes = [
    {key:"resNet2_Input",category:"Input",subtype:"Input",params:{}},
    {key:"resNet2_Conv1",category:"Conv",subtype:"Conv2d",params:{in_channels:"3",out_channels:"64",kernel_size:"7",stride:"2",padding:"3",bias:'True'}},
    {key:"resNet2_Norm1",category:"Norm",subtype:"BatchNorm2d",params:{num_features:"64"}},
    {key:"resNet2_Relu1",category:"Act",subtype:"Relu",params:{inplace:'True'}},
    {key:"resNet2_Pooling1",category:"Pool",subtype:"MaxPool2d",params:{kernel_size:"3",stride:"2",padding:"1"}},
    {key:"resBottleneckblock",category:"seqblock",name:"subnet"},
    {key:"resNet2_Pooling2",category:"Pool", subtype:"AdaptiveAvgPool2d",params:{output_size : "1,1"}},
    {key:"resNet2_Func1",category:"Vulkan", subtype:"Flatten",params:{start_dim : "1"}},
    {key:"resNet2_Linear1",category:"Linear",subtype:"Linear",params:{in_features : "512 * block.expansion",out_features:"num_classes"}},
    {key:"resNet2_Output",category:"Output",subtype:"Output",params:{}}];
netEnum["resNet-Bottle"].links = [
    {from:"resNet2_Input",to:"resNet2_Conv1"},
    {from:"resNet2_Conv1",to:"resNet2_Norm1"},
    {from:"resNet2_Norm1",to:"resNet2_Relu1"},
    {from:"resNet2_Relu1",to:"resNet2_Pooling1"},
    {from:"resNet2_Pooling1",to:"resNet2_Conv"},
    {from:"resNet2_Norm3",to:"resNet2_Pooling2"},
    {from:"resNet2_Pooling2",to:"resNet2_Func1"},
    {from:"resNet2_Func1",to:"resNet2_Linear1"},
    {from:"resNet2_Linear1",to:"resNet2_Output"}];
netEnum["resNet-Bottle"].subnet = {};
netEnum["resNet-Bottle"].subnet.type = "resBottleneckblock";
netEnum["resNet-Bottle"].subnet.nodes = [
    {key:"resNet2_Conv",category:"Conv",params:{in_channels:"in_planes",out_channels:"planes",kernel_size:"1",stride:"1",padding:"0"}},
    {key:"resNet2_Norm",category:"Norm",params:{num_features : "planes"}},
    {key:"resNet2_Relu",category:"Act",params:{inplace : "True"}},
    {key:"resNet2_Conv2",category:"Conv",params:{in_channels:"planes",out_channels:"planes",kernel_size:"3",stride:"stride",padding:"1",bias:"True"}},
    {key:"resNet2_Norm2",category:"Norm",params:{num_features : "planes"}},
    {key:"resNet2_Relu2",category:"Act",params:{inplace : "True"}},
    {key:"resNet2_Conv3",category:"Conv",params:{in_channels:"planes",out_channels:"planes * self.expansion",kernel_size:"1",stride:"1",padding:"0",bias:"True"}},
    {key:"resNet2_Norm3",category:"Norm",params:{num_features : "planes * self.expansion"}}];
netEnum["resNet-Bottle"].subnet.links = [
    {from:"resNet2_Conv",to:"resNet2_Norm"},
    {from:"resNet2_Norm",to:"resNet2_Relu"},
    {from:"resNet2_Relu",to:"resNet2_Conv2"},
    {from:"resNet2_Conv2",to:"resNet2_Norm2"},
    {from:"resNet2_Norm2",to:"resNet2_Relu2"},
    {from:"resNet2_Relu2",to:"resNet2_Conv3"},
    {from:"resNet2_Conv3",to:"resNet2_Norm3"}];

netEnum["SSD"].layout = "custom";
netEnum["SSD"].nodes = [
    {key:"SSD_raw_image",category:"Raw Image",loc:"0 0",color:"orange"},
    {key:"SSD_transform",category:"Transform",loc:"0 80"},
    {key:"SSD_backbone_network",category:"Backbone Network",loc:"0 160"},
    {key:"SSD_image_feature",category:"Image Feature",loc:"0 240"},
    {key:"SSD_anchor_generator",category:"Anchor Generator",loc:"160 320"},
    {key:"SSD_anchors",category:"Anchors",loc:"160 400"},
    {key:"SSD_gt_bbox_coord",category:"GT BBox Coord",loc:"400 400"},
    {key:"SSD_gt_bbox_label",category:"GT BBox Label",loc:"620 400"},
    {key:"SSD_target_generator",category:"Target Generator",loc:"400 480"},
    {key:"SSD_target_bboxes",category:"Target BBoxes",loc:"160 560"},
    {key:"SSD_target_conf",category:"Target Conf",loc:"620 560"},
    {key:"SSD_loss_calculator",category:"Loss Calculator",loc:"400 640"},
    {key:"SSD_optimizer",category:"Optimizer",loc:"400 720"}]; 
netEnum["SSD"].links = [{from:'SSD_raw_image',to:'SSD_transform',fromPort:"B",toPort:"T"},
    {from:'SSD_transform',to:'SSD_backbone_network',fromPort:"B",toPort:"T"},
    {from:'SSD_backbone_network',to:'SSD_image_feature',fromPort:"B",toPort:"T"},
    {from:'SSD_image_feature',to:'SSD_anchor_generator',fromPort:"R",toPort:"T"},
    {from:'SSD_image_feature',to:'SSD_loss_calculator',fromPort:"B",toPort:"L"},
    {from:'SSD_anchor_generator',to:'SSD_anchors',fromPort:"B",toPort:"T"},
    {from:'SSD_anchors',to:'SSD_target_generator',fromPort:"B",toPort:"T"},
    {from:'SSD_gt_bbox_label',to:'SSD_target_generator',fromPort:"B",toPort:"T"},
    {from:'SSD_gt_bbox_coord',to:'SSD_target_generator',fromPort:"B",toPort:"T"},
    {from:'SSD_target_generator',to:'SSD_target_bboxes',fromPort:"B",toPort:"T"},
    {from:'SSD_target_generator',to:'SSD_target_conf',fromPort:"B",toPort:"T"},
    {from:'SSD_target_conf',to:'SSD_loss_calculator',fromPort:"B",toPort:"T"},
    {from:'SSD_target_bboxes',to:'SSD_loss_calculator',fromPort:"B",toPort:"T"},
    {from:'SSD_loss_calculator',to:'SSD_optimizer',fromPort:"B",toPort:"T"}];

netEnum["Yolo"].layout = "custom";
netEnum["Yolo"].nodes = [
    {key:"Yolo_raw_image",category:"Raw Image",loc:"0 0",color:"orange"},
    {key:"Yolo_transform",category:"Transform",loc:"0 80"},
    {key:"Yolo_backbone_network",category:"Backbone Network",loc:"0 160"},
    {key:"Yolo_detection_layer",category:"Detection Layer",loc:"0 240"},
    {key:"Yolo_feature_lists",category:"Feature Lists",loc:"160 320"},    
    {key:"Yolo_gt_bbox_coord",category:"GT BBox Coord",loc:"400 400"},
    {key:"Yolo_gt_bbox_label",category:"GT BBox Label",loc:"620 400"},
    {key:"Yolo_target_generator",category:"Target Generator",loc:"400 480"},
    {key:"Yolo_target_bboxes",category:"Target BBoxes",loc:"160 560"},
    {key:"Yolo_objmask",category:"Obj Mask",loc:"160 560"},
    {key:"Yolo_noobjmask",category:"Non Obj Mask",loc:"160 560"},
    {key:"Yolo_predictions",category:"Predictions",loc:"620 560"},
    {key:"Yolo_loss_calculator",category:"Loss Calculator",loc:"400 640"}]; 
netEnum["Yolo"].links = [
    {from:'Yolo_raw_image',to:'Yolo_transform',fromPort:"B",toPort:"T"},
    {from:'Yolo_transform',to:'Yolo_backbone_network',fromPort:"B",toPort:"T"},
    {from:'Yolo_backbone_network',to:'Yolo_detection_layer',fromPort:"B",toPort:"T"},
    {from:'Yolo_detection_layer',to:'Yolo_feature_lists',fromPort:"L",toPort:"T"},    
    {from:'Yolo_detection_layer',to:'Yolo_predictions',fromPort:"R",toPort:"T"},    
    {from:'Yolo_gt_bbox_label',to:'Yolo_target_generator',fromPort:"B",toPort:"T"},
    {from:'Yolo_gt_bbox_coord',to:'Yolo_target_generator',fromPort:"B",toPort:"T"},
    {from:'Yolo_target_generator',to:'Yolo_target_bboxes',fromPort:"B",toPort:"T"},
    {from:'Yolo_target_generator',to:'Yolo_objmask',fromPort:"B",toPort:"T"},
    {from:'Yolo_target_generator',to:'Yolo_noobjmask',fromPort:"B",toPort:"T"},
    {from:'Yolo_target_bboxes',to:'Yolo_loss_calculator',fromPort:"B",toPort:"T"},
    {from:'Yolo_objmask',to:'Yolo_loss_calculator',fromPort:"B",toPort:"T"},     
    {from:'Yolo_predictions',to:'Yolo_loss_calculator',fromPort:"B",toPort:"T"}];

netEnum["DeepLab"].layout = "custom";
netEnum["DeepLab"].nodes = [
    {key:"DeepLab_raw_image",category:"Raw Image",loc:"200 0",color:"orange"},
    {key:"DeepLab_transform",category:"Transform",loc:"200 80"},
    {key:"DeepLab_backbone_network",category:"Backbone Network",loc:"200 160"},
    {key:"DeepLab_conv2d",category:"Conv2d",loc:"400 240"},
    {key:"DeepLab_batchnorm",category:"BatchNorm",loc:"400 320"},
    {key:"DeepLab_relu",category:"ReLU",loc:"400 400"},
    {key:"DeepLab_dropout2d",category:"Dropout2d",loc:"400 480"},
    {key:"DeepLab_conv2d1",category:"Conv2d",loc:"400 560"},
    {key:"DeepLab_interpolate",category:"Interpolate",loc:"400 640"},
    {key:"DeepLab_scale",category:"scale",loc:"400 720"},
    {key:"DeepLab_aspp_module",category:"ASSP Module",loc:"0 240"},
    {key:"DeepLab_conv2d2",category:"Conv2d",loc:"0 480"},
    {key:"DeepLab_interpolate1",category:"Interpolate",loc:"0 720"},     
    {key:"DeepLab_segmentation_loss",category:"Segmentation Loss",loc:"0 840"},
    {key:"DeepLab_auxiliary_loss",category:"Auxiliary Loss",loc:"400 840"},
    {key:"DeepLab_total_loss",category:"Totol Loss",loc:"200 920"},
    {key:"DeepLab_target",category:"Target",loc:"200 640"}     
]; 
netEnum["DeepLab"].links = [
    {from:'DeepLab_raw_image',to:'DeepLab_transform',fromPort:"B",toPort:"T"},
    {from:'DeepLab_transform',to:'DeepLab_backbone_network',fromPort:"B",toPort:"T"},
    {from:'DeepLab_backbone_network',to:'DeepLab_conv2d',fromPort:"B",toPort:"T"},
    {from:'DeepLab_backbone_network',to:'DeepLab_aspp_module',fromPort:"B",toPort:"T"},
    {from:'DeepLab_conv2d',to:'DeepLab_batchnorm',fromPort:"B",toPort:"T"},
    {from:'DeepLab_batchnorm',to:'DeepLab_relu',fromPort:"B",toPort:"T"},
    {from:'DeepLab_relu',to:'DeepLab_dropout2d',fromPort:"B",toPort:"T"},
    {from:'DeepLab_dropout2d',to:'DeepLab_conv2d1',fromPort:"B",toPort:"T"},
    {from:'DeepLab_conv2d1',to:'DeepLab_interpolate',fromPort:"B",toPort:"T"},
    {from:'DeepLab_interpolate',to:'DeepLab_scale',fromPort:"B",toPort:"T"},
    {from:'DeepLab_aspp_module',to:'DeepLab_conv2d2',fromPort:"B",toPort:"T"},
    {from:'DeepLab_conv2d2',to:'DeepLab_interpolate1',fromPort:"B",toPort:"T"},
    {from:'DeepLab_interpolate1',to:'DeepLab_segmentation_loss',fromPort:"B",toPort:"T"},
    {from:'DeepLab_scale',to:'DeepLab_auxiliary_loss',fromPort:"B",toPort:"T"},   
    {from:'DeepLab_target',to:'DeepLab_auxiliary_loss',fromPort:"B",toPort:"T"},
    {from:'DeepLab_target',to:'DeepLab_segmentation_loss',fromPort:"B",toPort:"T"},    
    {from:'DeepLab_segmentation_loss',to:'DeepLab_total_loss',fromPort:"B",toPort:"T"},
    {from:'DeepLab_auxiliary_loss',to:'DeepLab_total_loss',fromPort:"B",toPort:"T"}];

netEnum["PSPNet"].layout = "custom";
netEnum["PSPNet"].nodes = [
    {key:"PSPNet_raw_image",category:"Raw Image",loc:"200 0",color:"orange"},
    {key:"PSPNet_transform",category:"Transform",loc:"200 80"},
    {key:"PSPNet_backbone_network",category:"Backbone Network",loc:"200 160"},
    {key:"PSPNet_pyramid_pooling",category:"Pyramid Pooling",loc:"400 240"},
    {key:"PSPNet_conv2d",category:"Conv2d",loc:"400 320"},
    {key:"PSPNet_batchnorm",category:"BatchNorm",loc:"400 400"},
    {key:"PSPNet_relu",category:"ReLU",loc:"400 480"},
    {key:"PSPNet_dropout2d",category:"Dropout2d",loc:"400 560"},
    {key:"PSPNet_conv2d1",category:"Conv2d",loc:"400 640"},
    {key:"PSPNet_interpolate",category:"Interpolate",loc:"400 720"},    
    {key:"PSPNet_conv2d2",category:"Conv2d",loc:"0 240"},
    {key:"PSPNet_batchnorm1",category:"BatchNorm",loc:"0 320"},
    {key:"PSPNet_relu1",category:"ReLU",loc:"0 400"},
    {key:"PSPNet_conv2d3",category:"Conv2d",loc:"0 500"},
    {key:"PSPNet_interpolate1",category:"Interpolate",loc:"0 720"},     
    {key:"PSPNet_segmentation_loss",category:"Segmentation Loss",loc:"400 840"},
    {key:"PSPNet_auxiliary_loss",category:"Auxiliary Loss",loc:"0 840"},
    {key:"PSPNet_total_loss",category:"Totol Loss",loc:"200 920"},
    {key:"PSPNet_target",category:"Target",loc:"200 640"},
     
]; 
netEnum["PSPNet"].links = [
    {from:'PSPNet_raw_image',to:'PSPNet_transform',fromPort:"B",toPort:"T"},
    {from:'PSPNet_transform',to:'PSPNet_backbone_network',fromPort:"B",toPort:"T"},
    {from:'PSPNet_backbone_network',to:'PSPNet_conv2d2',fromPort:"B",toPort:"T"},
    {from:'PSPNet_backbone_network',to:'PSPNet_pyramid_pooling',fromPort:"B",toPort:"T"},
    {from:'PSPNet_pyramid_pooling',to:'PSPNet_conv2d',fromPort:"B",toPort:"T"},
    {from:'PSPNet_conv2d',to:'PSPNet_batchnorm',fromPort:"B",toPort:"T"},
    {from:'PSPNet_batchnorm',to:'PSPNet_relu',fromPort:"B",toPort:"T"},
    {from:'PSPNet_relu',to:'PSPNet_dropout2d',fromPort:"B",toPort:"T"},
    {from:'PSPNet_dropout2d',to:'PSPNet_conv2d1',fromPort:"B",toPort:"T"},
    {from:'PSPNet_conv2d1',to:'PSPNet_interpolate',fromPort:"B",toPort:"T"},
    {from:'PSPNet_interpolate',to:'PSPNet_segmentation_loss',fromPort:"B",toPort:"T"},    
    {from:'PSPNet_conv2d2',to:'PSPNet_batchnorm1',fromPort:"B",toPort:"T"},
    {from:'PSPNet_batchnorm1',to:'PSPNet_relu1',fromPort:"B",toPort:"T"},
    {from:'PSPNet_relu1',to:'PSPNet_conv2d3',fromPort:"B",toPort:"T"},
    {from:'PSPNet_conv2d3',to:'PSPNet_interpolate1',fromPort:"B",toPort:"T"},
    {from:'PSPNet_interpolate1',to:'PSPNet_auxiliary_loss',fromPort:"B",toPort:"T"},     
    {from:'PSPNet_target',to:'PSPNet_auxiliary_loss',fromPort:"B",toPort:"T"},
    {from:'PSPNet_target',to:'PSPNet_segmentation_loss',fromPort:"B",toPort:"T"},    
    {from:'PSPNet_segmentation_loss',to:'PSPNet_total_loss',fromPort:"B",toPort:"T"},
    {from:'PSPNet_auxiliary_loss',to:'PSPNet_total_loss',fromPort:"B",toPort:"T"}];

//console.log(netEnum["Yolo"]);
//netEnum["Yolo"].layout = "custom";
//netEnum["Yolo"].nodes = [];
//netEnum["Yolo"].links = [];



var netJSON = [];

netJSON["resNet-Basic"] = {};
netJSON["resNet-Bottle"] = {};
netJSON["SSD"] = {};
netJSON["DeepLab"] = {};
netJSON["PSPNet"] = {};

 



