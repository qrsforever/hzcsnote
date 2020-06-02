
 


// let datasets = [];
// let curdataset = null;

/**
 * 根据项目类型加载项目信息
 */
function loadProjectInfo(type,model){     
    if(model == 'custom'){
        $("#accordion").parent().show();
        $("#design_div").parent().css("padding-left","150px");
    }
    // nitDatasets(type);
}


function prtlog(data){
    if(debug)
        console.log(data);
}

function goTab(id){
    $('#main_tabs a[href="#' + id + '"]').tab('show');
    //$("#")   

}


/**
 * 判断字符串是否json格式
 */
function isJson(str){
    if(typeof str == 'string') {
        try {
            var obj=JSON.parse(str);
            if(typeof obj == 'object' && obj ){
                return true;
            }else{
                return false;
            }
        } catch(e) {
            //console.log('error：'+str+'!!!'+e);
            return false;
        }
    }else
        return false;    

}



function formatAug(aug_trans){
    
    function todata(str,type='int'){
        let ret = null;
        if(str == "")
            return ret;
        

        switch(type){
            case 'int':ret = parseInt(str);break;
            case 'float':ret = parseFloat(str);break;
            case 'bool':if(str == 'true')return true;else return false; 
            default:ret = str;break;
        }
        if(isNaN(ret))
            return null;
        else
            return ret;
    }

    let ret = {};
    if(!aug_trans) 
        aug_trans = {};
    if(!aug_trans.hasOwnProperty('trans_seq'))
        aug_trans.trans_seq = [];
     
    ret.trans_seq = aug_trans.trans_seq.slice(0);
    $.each(ret.trans_seq,function(index,val){         
        if(aug_trans.hasOwnProperty(val) && augmentation.hasOwnProperty(val)){
            ret[val] = {};
            Object.assign(ret[val], aug_trans[val]);   
                   
            for(var index in ret[val]){                
                
                let datatype = augmentation[val].param[index].type; 
                switch(datatype){
                    case 'float': 
                    case 'int': 
                    case 'bool':ret[val][index] = todata(ret[val][index],datatype);break;
                    case 'int-list':ret[val][index] = tolist(ret[val][index],'int');break;
                    case 'float-list':ret[val][index] = tolist(ret[val][index],'float');break;
                    default:break;                    
                }        
                if(ret[val][index] === null || ret[val][index] === '')
                    delete ret[val][index]; 
            } 
            if(val == "random_resize" || val == "random_crop"){
                ret[val].method="random";                
            } 
        }        
    });

    //console.log(ret);
     
     

    return ret;

}


function getprenodedata(model){
    let preconfig = {};
    $.each(diagram.model.nodeDataArray,function(index,val){
        if(prenodeParams[model]["property_map"].hasOwnProperty(val.category)){
            let propername = prenodeParams[model]["property_map"][val.category];
            preconfig[propername] = {};            
             
            for(let i in prenodeParams[model]){
                if(i != 'property_map'){
                    for(let j in prenodeParams[model][i]){
                        console.log(j);
                        if(val.info.hasOwnProperty(j)){
                            let data = null;
                            switch(prenodeParams[model][i][j].type){
                                case 'string':data = val.info[j];break;
                                case 'float':data = parseFloat(val.info[j]);break;
                                case 'listnumber':data = tolist(val.info[j]);break;
                                default:data = val.info[j];break;
                            }


                            preconfig[propername][j] = data;
                        }

                    }
                                   
                }               
            }
             
             
        }      

    }); 
    
    return preconfig;
}
 

/**
 * 生成配置文件
 */
function generateConfig(){
    let project_type = $("#hproject_type").val();
    let project_method = $("#hproject_method").val();
    config = {};        
        
    config.dataset = $("#dataset_name").val();
    config.project_dir = "[[project]]"; 
    config.task = project_type;
    
    config.method = project_method;
    curdataset.workers = parseInt($("#dataset_worker").val());
    config.data = curdataset;
    
    config.data.test_size = parseFloat($("#dataset_split").val());

    let train = {};
    let val = {};
    let test = {};

    train.batch_size = parseInt($("#dataset_train_batchsize").val());
     
    train.data_transformer = {};
     
    train.data_transformer.size_mode = $("#dataset_train_sizemode").val();
    train.data_transformer.input_size = [];
    if(train.data_transformer.size_mode == "fix_size"){
        train.data_transformer.input_size.push(parseInt($("#dataset_train_inputsize").val()));
        train.data_transformer.input_size.push(parseInt($("#dataset_train_inputsize").val()));
    }
    train.data_transformer.align_method = $("#dataset_train_align_method").val();

    
     
    train.aug_trans = formatAug(train_aug_trans);


    val.batch_size = parseInt($("#dataset_val_batchsize").val());
    
    val.data_transformer = {};
    val.data_transformer.size_mode = $("#dataset_val_sizemode").val();
    val.data_transformer.input_size = [];
    if(val.data_transformer.size_mode == "fix_size"){
        val.data_transformer.input_size.push(parseInt($("#dataset_val_inputsize").val()));
        val.data_transformer.input_size.push(parseInt($("#dataset_val_inputsize").val()));
    }
    val.data_transformer.align_method = $("#dataset_val_align_method").val();
     
    val.aug_trans = formatAug(val_aug_trans);

    test.batch_size = parseInt($("#dataset_test_batchsize").val());
    test.input_size = [];
    let test_aug_trans = {};
    
    test.data_transformer = {};
        test.data_transformer.size_mode = $("#dataset_test_sizemode").val();
        test.data_transformer.input_size = [];
    if(test.data_transformer.size_mode == "fix_size"){
        test.data_transformer.input_size.push(parseInt($("#dataset_test_inputsize").val()));
        test.data_transformer.input_size.push(parseInt($("#dataset_test_inputsize").val()));
        test.input_size.push(parseInt($("#dataset_test_inputsize").val()));
        test.input_size.push(parseInt($("#dataset_test_inputsize").val()));
        
    }
    test.data_transformer.align_method = $("#dataset_val_align_method").val();
    test_aug_trans.trans_seq = [];

    test.aug_trans = test_aug_trans;

    config.train = train;
    config.val = val;
    config.test = test;
    config.details = details[curdataset["name"]];

    config.network = {};     
    config.network.checkpoints_name = curdataset["name"] + "_" + project_type + "_" + $("#hproject_model_name").val();
    config.network.checkpoints_root = "/data/checkpoints/" + project_type + "/" + curdataset["name"];
    config.network.checkpoints_dir = "subdir";

    config.logging = {};
    config.logging.logfile_level = "info";
    config.logging.stdout_level = "info";
    config.logging.log_file = "./log/" + project_type + "/" + curdataset["name"] + ".log";
    config.logging.log_format = "%(asctime)s %(levelname)-7s %(message)s";
    config.logging.rewrite = true;

    config.solver = {};

    config.solver.lr = {};
    config.solver.lr.metric = $("#hparamter_metric").val();
    config.solver.lr.base_lr = parseFloat($("#hparamter_base_lr").val());
    config.solver.lr.lr_policy = $("#hparamter_lr_policy").val();
    config.solver.lr.step = {};
    config.solver.lr.multistep = {};
    if(config.solver.lr.lr_policy == "step" || config.solver.lr.lr_policy == "lambda_poly"){
        config.solver.lr.step.gamma = parseFloat($("#hparamter_gamma").val());
        config.solver.lr.step.step_size = parseInt($("#hparamter_step_value").val());
    }
    else if(config.solver.lr.lr_policy == "multistep"){
        config.solver.lr.multistep.gamma = parseFloat($("#hparamter_gamma").val());
        let vals = $("#hparamter_step_value").val().split(",");
        config.solver.lr.multistep.stepvalue = [];
        $.each(vals,function(index,val){                     
            config.solver.lr.multistep.stepvalue.push(parseInt(val));
        });                
    }
     
    config.solver.lr.iswarm = ($("#optim_iswarm").val() == "True")?true:false; 
    config.solver.lr.warm = {"warm_iters": parseInt($("#optim_warmiters").val()),"freeze_backbone": false};

     
    config.solver.display_iter = parseInt($("#solver_display_iter").val());
    config.solver.test_interval = parseInt($("#solver_test_interval").val());
    config.solver.max_epoch = parseInt($("#solver_max_epoch").val()); 
    config.solver.save_iters = parseInt($("#solver_save_interval").val());;


    config.solver.optim = {};
    config.solver.optim.optim_method = $("#optim_method").val();
    config.solver.optim.adam = {};
    config.solver.optim.sgd = {};
    if($("#optim_adam_betas").length > 0){
        let vals = $("#optim_adam_betas").val().split(",");
        config.solver.optim.adam.betas = [];
        $.each(vals,function(index,val){
            config.solver.optim.adam.betas.push(parseFloat(val));
        });

    }
    
    config.solver.optim.adam.eps = parseFloat($("#optim_adam_eps").val());
    config.solver.optim.adam.weight_decay = parseFloat($("#optim_adam_weight_decay").val());
    config.solver.optim.sgd.weight_decay = parseFloat($("#optim_sgd_weight_decay").val());
    config.solver.optim.sgd.momentum = parseFloat($("#optim_sgd_momentum").val());
    if($("#optim_sgd_nesterov").val() == "True")
        config.solver.optim.sgd.nesterov = true;
    else 
        config.solver.optim.sgd.nesterov = false;

    config.loss = {};
    config.loss.loss_type = $("#hparamter_loss_type").val();
    config.loss.params = {"ce_reduction":"mean"};


    config.res = {};

    config.res.nms = {};
    config.res.nms.mode = $("#hparamter_nms_mode").val();
    config.res.nms.max_threshold = parseFloat($("#hparamter_nms_max_threshold").val());
    config.res.nms.pre_nms = parseInt($("#hparamter_nms_pre").val());
     
    config.res.val_conf_thre = parseFloat($("#hparamter_res_val_conf_thre").val());
    config.res.vis_conf_thre = parseFloat($("#hparamter_res_vis_conf_thre").val());
    config.res.max_per_image = parseInt($("#hparamter_res_max_per_image").val());
    config.res.cls_keep_num = parseInt($("#hparamter_res_cls_keep_num").val());   
    
    

    
    config.anchor = {};
    
    
    if(project_model == "SSD"){ //
        config.network.backbone = "vgg16";//mobilenet_v2 resnet_50 resnet_101 
        config.network.model_name = "vgg300_ssd";
        config.network.num_feature_list = [512, 1024, 512, 256, 256, 256];
        config.network.stride_list = [8, 16, 30, 60, 100, 300];
        config.network.head_index_list = [0, 1, 2, 3, 4, 5];   
        config.network.ssd_lite = "true";  
        config.anchor.anchor_method = "ssd";
        config.anchor.iou_threshold = 0.45;
        //TODO QRS: why commont it ?
        config.anchor.num_anchor_list = [4, 6, 6, 6, 4, 4];
        config.anchor.feature_maps_wh = [[38, 38], [19, 19], [10, 10], [5, 5], [3, 3], [1, 1]];
        config.anchor.cur_anchor_sizes = [30, 60, 111, 162, 213, 264, 315];
        config.anchor.aspect_ratio_list = [[2], [2, 3], [2, 3], [2, 3], [2], [2]]; 
        //TODO QRS: why commont it ?
        config.val.use_07_metric = true;         

        let configret = getprenodedata(project_model);
         
        
        Object.assign(config.network,configret.network);
        Object.assign(config.anchor,configret.anchor);
         

    
    }else if(project_model == "Yolo"){
         
        config.network.backbone = "darknet53";
        config.network.model_name = "darknet_yolov3"; 
        config.network.stride_list = [32, 16, 8];
        config.loss.loss_weights = {};
        config.loss.loss_weights.coord_loss = 1.0;
        config.loss.loss_weights.obj_loss = 5.0;
        config.loss.loss_weights.cls_loss = 1.0;
        //config.val.use_07_metric = true; 
        config.anchor.iou_threshold = 0.5;
        config.anchor.anchors_list = [[[116, 90], [156, 198], [373, 326]],[[30, 61], [62, 45], [59, 119]],[[10, 13], [16, 30], [33, 23]]];
    }else if(project_model == "DeepLab"){
        config.network.backbone = "deepbase_resnet101_dilated8";
        config.network.bn_type = 'torchbn';
        config.network.stride = 8;
        config.network.model_name = 'deeplabv3';
        config.solver.max_iters = config.solver.max_epoch;
        
        config.val.data_transformer.fit_stride = 8;
        config.val.data_transformer.pad_mode = "pad_right_down";
        

        config.test = {};
        config.test.mode = 'ss_test';
        config.test.min_side_length = 520;
        config.test.fit_stride = 8;
        config.test.scale_search = [1.0];

        config.loss.loss_weights = {aux_loss:0.4,seg_loss:1.0};
        config.loss.params.ce_ignore_index = -1;
        config.data.reduce_zero_label = ($("#dataset_reduce_zero_label").val() == "true")?true:false;         
        delete config.res;      
        
    }else if(project_model == "PSPNet"){
        config.network.backbone = "deepbase_resnet101_dilated8";
        config.network.bn_type = 'torchbn';
        config.network.stride = 8;
        config.network.model_name = 'pspnet';
        config.solver.max_iters = config.solver.max_epoch;
        
        config.val.data_transformer.fit_stride = 8;
        config.val.data_transformer.pad_mode = "pad_right_down";
        

        config.test = {};
        config.test.mode = 'ss_test';
        config.test.min_side_length = 520;
        config.test.fit_stride = 8;
        config.test.scale_search = [1.0];

        config.loss.loss_weights = {aux_loss:0.4,seg_loss:1.0};
        config.loss.params.ce_ignore_index = -1;   
        config.data.reduce_zero_label = ($("#dataset_reduce_zero_label").val() == "true")?true:false;   
        delete config.res;      
        
    }else if(project_model == 'pretrained'){
        config.network.model_name = project_model_sub;     
        console.log($("#network_pretrained").val());            
        //config.network.model_name = "resnet_50"; 
        if($("#network_pretrained").val() == "true")
            config.network.pretrained = true;
        else 
            config.network.pretrained = false;      

        config.network.weights_host = 'http://0.0.0.0:28889/'; 
        config.network.unfreezed_layers = [];

    }else if(project_model == 'automl'){
        console.log($("#dataset_name").find("option:selected").text());         
        config.dataset = $("#dataset_name").find("option:selected").text(); 
         
        if($("#dataset_search_cutout").val() == "True")
            config.data.cutout = true;
        else 
            config.data.cutout = false;
        config.data.cutout_length = parseInt($("#dataset_search_cutout_length").val());
        config.train.batch_size = parseInt($("#dataset_search_train_batchsize").val());
        config.val.batch_size = parseInt($("#dataset_search_val_batchsize").val());
        config.test.batch_size = parseInt($("#dataset_search_test_batchsize").val());
        config.network.model_name = 'darts';
        config.network.seed = parseInt($("#hparamter_search_seed").val());
        config.network.init_ch = parseInt($("#hparamter_search_init_ch").val());
        config.network.layers_num = parseInt($("#hparamter_search_layers_num").val());
        config.network.unrolled = true;
        config.network.grad_clip = parseInt($("#hparamter_search_grad_clip").val());

        config.solver.lr.metric = $("#hparamter_search_metric").val();
        config.solver.lr.base_lr = parseFloat($("#hparamter_search_base_lr").val());
        config.solver.lr.lr_policy = $("#hparamter_search_lr_policy").val();
        config.solver.lr.lr_min = parseFloat($("#hparamter_search_lr_min").val());
        config.solver.lr.arch_lr = parseFloat($("#hparamter_search_arch_lr").val());


        
        config.solver.optim.optim_method = 'sgd';         
        config.solver.optim.sgd.weight_decay = parseFloat($("#optim_search_sgd_weight_decay").val());
        config.solver.optim.sgd.momentum = parseFloat($("#optim_search_sgd_momentum").val());
        if($("#optim_search_sgd_nesterov").val() == "True")
            config.solver.optim.sgd.nesterov = true;
        else 
            config.solver.optim.sgd.nesterov = false;
        config.solver.optim.sgd.arch_weight_decay = parseFloat($("#optim_search_sgd_arch_weight_decay").val());
        config.solver.optim.sgd.arch_momentum = parseFloat($("#optim_search_sgd_arch_momentum").val());

        config.solver.display_iter = parseInt($("#solver_search_display_iter").val());
        config.solver.test_interval = parseInt($("#solver_search_test_interval").val());
        config.solver.max_epoch = parseInt($("#solver_search_max_epoch").val()); 
        config.solver.save_iters = 200;
        delete config.loss;
        delete config.anchor;
        delete config.res;       

         

    }else{         
        config.network.model_name = "custom_" + $("#hproject_model_name").val();                 
            //config.network.model_name = "resnet_50"; 
        config.network.pretrained = false; 
        config.network.unfreezed_layers = [];
                
    }

    console.log(config);
     
}
 


function tolist(str,type='int'){
    let datas = str.split(',');
    let ret = [];
     
    if(datas.length == 0 || str == "")
        return null;
    $.each(datas,function(index,val){
        switch(type){
            case 'int':ret.push(parseInt(val));break;
            case 'float':ret.push(parseFloat(val));break;
            default:ret.push(val);break;
        }            
    });         
    return ret;
}


 
