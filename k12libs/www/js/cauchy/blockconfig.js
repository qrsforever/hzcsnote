'use strict';
var blockEnum = [];




blockEnum["resBasicblock"] = {};
blockEnum["resBottleneckblock"] = {};



blockEnum["resBasicblock"].num_blocks = {type:'listnumber',default:"3,4,6,3"};
blockEnum["resBasicblock"].planes = {type:'listnumber',default:"64,128,256,512"};
blockEnum["resBasicblock"].strides = {type:'listnumber',default:"1,2,2,2"};
blockEnum["resBasicblock"].num_classes = {type:'string',default:"10"};

blockEnum["resBottleneckblock"].num_blocks = {type:'listnumber',default:"3,4,6,3"};
blockEnum["resBottleneckblock"].planes = {type:'listnumber',default:"64,128,256,512"};
blockEnum["resBottleneckblock"].strides = {type:'listnumber',default:"1,2,2,2"};
blockEnum["resBottleneckblock"].num_classes = {type:'string',default:"10"};
 