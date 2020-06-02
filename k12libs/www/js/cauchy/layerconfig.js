'use strict';
var nodeEnum = [];
nodeEnum["Input"] = {color: "#094AB2", img: "io-layers.png",subtype:["Input"],defaultsubtype:"Input"};
nodeEnum["Output"] = {color: "#094AB2", img: "io-layers.png",subtype:["Output"],defaultsubtype:"Output"};
nodeEnum["Conv"] = {color: "#3B9F5B", img: "convolutional-layers.png",subtype:["Conv1d","Conv2d","Conv3d","ConvTranspose1d","ConvTranspose2d","ConvTranspose3d"],defaultsubtype:"Conv2d"};
nodeEnum["Act"] = {color: "#008A00", img: "activations-layers.png",subtype:["Relu","Tanh","LeakyReLU","LogSigmoid","Sigmoid","Softsign","Tanhshrink","Hardshrink","Hardtanh","Relu6","SELU"],defaultsubtype:"Relu"};
nodeEnum["Padding"] = {color: "#C8533B", img: "convolutional-layers.png",subtype:["ReflectionPad1d","ReflectionPad2d","ReplicationPad1d","ReplicationPad2d","ReplicationPad3d","ZeroPad2d","ConstantPad1d","ConstantPad2d","ConstantPad3d"],defaultsubtype:"ZeroPad2d"};
nodeEnum["Pool"] = {color: "#FFB84D", img: "pooling-layers.png",subtype:["MaxPool1d","MaxPool2d","MaxPool3d","AvgPool1d","AvgPool2d","AvgPool3d","LPPool1d","LPPool2d","AdaptiveMaxPool1d","AdaptiveMaxPool2d","AdaptiveMaxPool3d","AdaptiveAvgPool1d","AdaptiveAvgPool2d","AdaptiveAvgPool3d"],defaultsubtype:"MaxPool2d"};
nodeEnum["Linear"] = {color: "#008299", img: "core-layers.png",subtype:["Linear"],defaultsubtype:"Linear"};
nodeEnum["Norm"] = {color: "#7F6998", img: "normalization-layers.png",subtype:["BatchNorm1d","BatchNorm2d","BatchNorm3d","InstanceNorm1d", "InstanceNorm2d","InstanceNorm3d"],defaultsubtype:"BatchNorm2d"};
nodeEnum["Loss"] = {color: "#2672EC", img: "core-layers.png",subtype:["L1Loss","MSELoss","CrossEntropyLoss"],defaultsubtype:"CrossEntropyLoss"};
nodeEnum["Dropout"] = {color: "#5133AB", img:"core-layers.png",subtype:["Dropout","Dropout2d","Dropout3d","AlphaDropout"],defaultsubtype:"Dropout"};
nodeEnum["BaseFunc"] = {color: "#5133AB", img:"core-layers.png",subtype:["Cat","Add"],defaultsubtype:"Cat"};
nodeEnum["Vulkan"] = {color: "#5133AB", img:"core-layers.png",subtype:["Reshape","Flatten"],defaultsubtype:"Flatten"};


var nodeParams = [];
//Convolution
nodeParams["Input"] = {};
nodeParams["Input"].in_features = {type:'listnumber'};
nodeParams["Output"] = {};
nodeParams["Output"].out_features = {type:'number'};


nodeParams["Conv1d"] = {};
nodeParams["Conv1d"].in_channels = {type:'string'};
nodeParams["Conv1d"].out_channels = {type:'string'};
nodeParams["Conv1d"].kernel_size = {type:'string'};
nodeParams["Conv1d"].stride = {type:'string',default:1};
nodeParams["Conv1d"].padding = {type:'string',default:0};
nodeParams["Conv1d"].dilation = {type:'string',default:1};
nodeParams["Conv1d"].groups = {type:'string',default:1};
nodeParams["Conv1d"].bias = {type:'list',options:['True','False'],default:'True'};
nodeParams["Conv2d"] = JSON.parse(JSON.stringify(nodeParams["Conv1d"]));
nodeParams["Conv3d"] = JSON.parse(JSON.stringify(nodeParams["Conv1d"]));
nodeParams["ConvTranspose1d"] = JSON.parse(JSON.stringify(nodeParams["Conv1d"]));
nodeParams["ConvTranspose1d"].output_padding = {type:'string',default:0};
nodeParams["ConvTranspose2d"] = JSON.parse(JSON.stringify(nodeParams["ConvTranspose1d"]));
nodeParams["ConvTranspose3d"] = JSON.parse(JSON.stringify(nodeParams["ConvTranspose1d"]));


//Pooling
nodeParams["MaxPool1d"] = {};
nodeParams["MaxPool1d"].kernel_size = {type:'string'};
nodeParams["MaxPool1d"].stride = {type:'string'};
nodeParams["MaxPool1d"].padding = {type:'string',default:0};
nodeParams["MaxPool1d"].dilation = {type:'string',default:1};
nodeParams["MaxPool1d"].dilation = {type:'string',default:1};
nodeParams["MaxPool1d"].return_indices = {type:'list',options:['True','False'],default:'False'};
nodeParams["MaxPool1d"].ceil_mode = {type:'list',options:['True','False'],default:'False'};
nodeParams["MaxPool2d"] = JSON.parse(JSON.stringify(nodeParams["MaxPool1d"]));
nodeParams["MaxPool3d"] = JSON.parse(JSON.stringify(nodeParams["MaxPool1d"]));
nodeParams["AvgPool1d"] = JSON.parse(JSON.stringify(nodeParams["MaxPool1d"]));
nodeParams["AvgPool2d"] = JSON.parse(JSON.stringify(nodeParams["MaxPool1d"]));
nodeParams["AvgPool3d"] = JSON.parse(JSON.stringify(nodeParams["MaxPool1d"]));
nodeParams["AdaptiveAvgPool1d"] = {};
nodeParams["AdaptiveAvgPool1d"].output_size = {type:'listnumber'};
nodeParams["AdaptiveAvgPool2d"] = JSON.parse(JSON.stringify(nodeParams["AdaptiveAvgPool1d"]));
nodeParams["AdaptiveAvgPool3d"] = JSON.parse(JSON.stringify(nodeParams["AdaptiveAvgPool1d"]));
nodeParams["AdaptiveMaxPool1d"] = JSON.parse(JSON.stringify(nodeParams["AdaptiveAvgPool1d"]));
nodeParams["AdaptiveMaxPool1d"].return_indices = {type:'list',options:['True','False'],default:'False'};
nodeParams["AdaptiveMaxPool2d"] = JSON.parse(JSON.stringify(nodeParams["AdaptiveMaxPool1d"]));
nodeParams["AdaptiveMaxPool3d"] = JSON.parse(JSON.stringify(nodeParams["AdaptiveMaxPool1d"]));
nodeParams["MaxUnpool1d"] = {};
nodeParams["MaxUnpool1d"].kernel_size = {type:'string'};
nodeParams["MaxUnpool1d"].stride = {type:'string'};
nodeParams["MaxUnpool1d"].padding = {type:'string',default:0};
nodeParams["MaxUnpool2d"] = JSON.parse(JSON.stringify(nodeParams["MaxUnpool1d"]));
nodeParams["MaxUnpool3d"] = JSON.parse(JSON.stringify(nodeParams["MaxUnpool1d"]));
nodeParams["LPPool1d"] = {};
nodeParams["LPPool1d"].norm_type = {type:'string'};
nodeParams["LPPool1d"].kernel_size = {type:'string'};
nodeParams["LPPool1d"].stride = {type:'string'};
nodeParams["LPPool1d"].ceil_mode = {type:'list',options:['True','False'],default:'False'};
nodeParams["LPPool2d"] = JSON.parse(JSON.stringify(nodeParams["LPPool1d"])); 





//Normalization
nodeParams["BatchNorm1d"] = {}; 
nodeParams["BatchNorm1d"].num_features = {type:'string'};
nodeParams["BatchNorm1d"].eps = {type:'string',default:1e-05};
nodeParams["BatchNorm1d"].momentum = {type:'string',default:0.1};
nodeParams["BatchNorm1d"].affine = {type:'list',options:['True','False'],default:'True'};
nodeParams["BatchNorm1d"].track_running_stats = {type:'list',options:['True','False'],default:'True'};
nodeParams["BatchNorm2d"] = JSON.parse(JSON.stringify(nodeParams["BatchNorm1d"]));
nodeParams["BatchNorm3d"] = JSON.parse(JSON.stringify(nodeParams["BatchNorm1d"]));
nodeParams["InstanceNorm1d"] = JSON.parse(JSON.stringify(nodeParams["BatchNorm1d"]));
nodeParams["InstanceNorm1d"].affine.default = 'False';
nodeParams["InstanceNorm1d"].track_running_stats.default = 'False';
nodeParams["InstanceNorm2d"] = JSON.parse(JSON.stringify(nodeParams["InstanceNorm1d"]));
nodeParams["InstanceNorm3d"] = JSON.parse(JSON.stringify(nodeParams["InstanceNorm1d"]));


//Padding
nodeParams["ReflectionPad1d"] = {}; 
nodeParams["ReflectionPad1d"].padding = {type:'string',default:0,force:true};
nodeParams["ReflectionPad2d"] = JSON.parse(JSON.stringify(nodeParams["ReflectionPad1d"]));
nodeParams["ReplicationPad1d"] = JSON.parse(JSON.stringify(nodeParams["ReflectionPad1d"]));
nodeParams["ReplicationPad2d"] = JSON.parse(JSON.stringify(nodeParams["ReflectionPad1d"]));
nodeParams["ReplicationPad3d"] = JSON.parse(JSON.stringify(nodeParams["ReflectionPad1d"]));
nodeParams["ZeroPad2d"] = JSON.parse(JSON.stringify(nodeParams["ReflectionPad1d"]));
nodeParams["ConstantPad1d"] = JSON.parse(JSON.stringify(nodeParams["ReflectionPad1d"]));
nodeParams["ConstantPad1d"].value = {type:'string'};
nodeParams["ConstantPad2d"] = JSON.parse(JSON.stringify(nodeParams["ConstantPad1d"]));
nodeParams["ConstantPad3d"] = JSON.parse(JSON.stringify(nodeParams["ConstantPad1d"]));


//Dropout
nodeParams["Dropout"] = {}; 
nodeParams["Dropout"].p = {type:'string',default:0.5};
nodeParams["Dropout"].inplace = {type:'list',options:['True','False'],default:'False'};
nodeParams["Dropout2d"] = JSON.parse(JSON.stringify(nodeParams["Dropout"]));
nodeParams["Dropout3d"] = JSON.parse(JSON.stringify(nodeParams["Dropout"]));
nodeParams["AlphaDropout"] = JSON.parse(JSON.stringify(nodeParams["Dropout"]));


//Linear
nodeParams["Linear"] = {}; 
nodeParams["Linear"].in_features = {type:'string'};
nodeParams["Linear"].out_features = {type:'string'};
nodeParams["Linear"].bias = {type:'list',options:['True','False'],default:'True'};


//Loss
nodeParams["L1Loss"] = {}; 
nodeParams["L1Loss"].size_average = {type:'string'};
nodeParams["L1Loss"].reduce = {type:'string'};
nodeParams["L1Loss"].reduction = {type:'list',default:'mean',options:['none','mean','sum']};
nodeParams["MSELoss"] = JSON.parse(JSON.stringify(nodeParams["L1Loss"]));
nodeParams["CrossEntropyLoss"] = JSON.parse(JSON.stringify(nodeParams["L1Loss"]));
nodeParams["CrossEntropyLoss"].weight = {type:'string'};
nodeParams["CrossEntropyLoss"].ignore_index = {type:'string',default:-100};
 

//Activation
nodeParams["Tanh"] = {}; 
nodeParams["Sigmoid"] = {};
nodeParams["LogSigmoid"] = {};
nodeParams["Softsign"] = {};
nodeParams["Tanhshrink"] = {};
nodeParams["Softmax2d"] = {}; 
nodeParams["Relu"] = {}; 
nodeParams["Relu"].inplace = {type:'list',options:['True','False'],default:'False'};
nodeParams["Relu6"] = JSON.parse(JSON.stringify(nodeParams["Relu"]));
nodeParams["SELU"] = JSON.parse(JSON.stringify(nodeParams["Relu"]));
nodeParams["LeakyReLU"] = JSON.parse(JSON.stringify(nodeParams["Relu"]));
nodeParams["LeakyReLU"].negative_slope = {type:'string',default:0.01};
nodeParams["Hardshrink"] = {}; 
nodeParams["Hardshrink"].lambd = {type:'string',default:0.5};
nodeParams["Hardtanh"] = {}; 
nodeParams["Hardtanh"].min_val = {type:'string',default:-1.0};
nodeParams["Hardtanh"].max_val = {type:'string',default:1.0};
nodeParams["Hardtanh"].inplace = {type:'list',options:['True','False'],default:'False'};
nodeParams["Softmin"] = {}; 
nodeParams["Softmin"].dim = {type:'string',default:1};
nodeParams["Softmax"] = JSON.parse(JSON.stringify(nodeParams["Softmin"])); 
nodeParams["LogSoftmax"] = JSON.parse(JSON.stringify(nodeParams["Softmin"])); 

 


//Data
nodeParams["Data"] = {}; 


//BaseFunc
nodeParams["Reshape"] = {}; 
nodeParams["Reshape"].target_shape = {type:'listnumber'};
nodeParams["Cat"] = {}; 
nodeParams["Cat"].dim = {type:'string',default:0,force:true};
nodeParams["Add"] = {};  
nodeParams["Flatten"] = {};
nodeParams["Flatten"].start_dim = {type:'string',default:1,force:true};
nodeParams["Flatten"].end_dim = {type:'string',default:-1};



var prenodeParams = [];
prenodeParams["SSD"] = [];
prenodeParams["SSD"]["property_map"] = {'Anchors':'anchor','Backbone Network':'network'};
prenodeParams["SSD"]["Anchors"] = {};
prenodeParams["SSD"]["Anchors"].num_anchor_list = {type:'listnumber',default:'4, 6, 6, 6, 4, 4'};
prenodeParams["SSD"]["Anchors"].iou_threshold = {type:'float',default:'0.45'};
prenodeParams["SSD"]["Anchors"].cur_anchor_sizes = {type:'listnumber',default:'30, 60, 111, 162, 213, 264, 315'};


//prenodeParams["SSD"]["Target Generator"] = {};
//prenodeParams["SSD"]["Target Generator"].ssd_target_generator = {type:'listnumber',default:'8, 16, 30, 60, 100, 300'};

prenodeParams["SSD"]["Backbone Network"] = {};
prenodeParams["SSD"]["Backbone Network"].num_feature_list = {type:'listnumber',default:'512, 1024, 512, 256, 256, 256'};

prenodeParams["PSPNet"] = [];
prenodeParams["PSPNet"]["Auxiliary Loss"] = {aux_loss:{type:'float',default:0.4}};
prenodeParams["PSPNet"]["Segmentation Loss"]= {seg_loss:{type:'float',default:1}};


prenodeParams["DeepLab"] = [];
prenodeParams["DeepLab"]["Auxiliary Loss"] = {aux_loss:{type:'float',default:0.4}};
prenodeParams["DeepLab"]["Segmentation Loss"]= {seg_loss:{type:'float',default:1}};
 