'use strict'
let augmentation = {};
augmentation['random_saturation'] = {name:'Random Saturation'};
augmentation['random_hue'] = {name:'Random Hue'};
augmentation['random_perm'] = {name:'Random Perm'};
augmentation['random_contrast'] = {name:'Random Contrast'};
augmentation['random_brightness'] = {name:'Random Brightness'};
augmentation['random_pad'] = {name:'Random Pad'};
augmentation['padding'] = {name:'Padding'};
augmentation['random_hflip'] = {name:'Random Hflip'};
augmentation['random_resize'] = {name:'Random Resize'};
augmentation['random_crop'] = {name:'Random Crop'};
augmentation['random_focus_crop'] = {name:'Random Focus Crop'};
augmentation['random_det_crop'] = {name:'Random Det Crop'};
augmentation['random_resized_crop'] = {name:'Random Resized Crop'};
augmentation['random_rotate'] = {name:'Random Rotate'};
augmentation['resize'] = {name:'Resize'};
 
augmentation['random_saturation'].param = {"lower":{name:'Lower','type':'float','default':0.5},"upper":{name:'Upper','type':'float','default':1.5},"ratio":{name:'ratio','type':'float','default':0.5}};
augmentation['random_hue'].param = {"delta":{name:'Delta','type':'int','default':18,max:360,min:0},"ratio":{name:'ratio','type':'float','default':0.5}};
augmentation['random_perm'].param = {"ratio":{name:'ratio','type':'float','default':0.5}};
augmentation['random_contrast'].param = {"lower":{name:'Lower','type':'float','default':0.5},"upper":{name:'Upper','type':'float','default':1.5},"ratio":{name:'ratio','type':'float','default':0.5}};
augmentation['random_brightness'].param = {"shift_value":{name:'Shift Value','type':'int','default':30},"ratio":{name:'ratio','type':'float','default':0.5}};
augmentation['random_resized_crop'].param = {"size":{name:'Size','type':'int','default':3},"scale_range":{name:'Scale Range','type':'tuple','default':(0.08, 1.0)},"aspect_range":{name:'Aspect Range','type':'float-list','default':(3. / 4., 4. / 3.)}};
augmentation['random_resize'].param = {"ratio":{name:'ratio','type':'float','default':0.5},"scale_range":{name:'Scale Range','type':'float-list','default':(0.75, 1.25)},"aspect_range":{name:'Aspect Range','type':'float-list','default':(0.9, 1.1)}};
augmentation['random_rotate'].param = {"max_degree":{name:'Max Degree','type':'int','default':0},"ratio":{name:'ratio','type':'float','default':0.5},"mean":{name:'Mean','type':'float-list','default':[104, 117, 123]}};
augmentation['random_crop'].param = {"crop_size":{name:'Crop Size','type':'int-list','default':''},"ratio":{name:'ratio','type':'float','default':0.5},"allow_outside_center":{name:'Allow Outside Center',type:'bool',default:false},};
augmentation['random_focus_crop'].param = {"crop_size":{name:'Crop Size','type':'int-list','default':''},"ratio":{name:'ratio','type':'float','default':0.5},"mean":{name:'Mean','type':'float-list','default':[104, 117, 123]},"allow_outside_center":{name:'Allow Outside Center',type:'bool',default:false}}; 
augmentation['random_det_crop'].param = {"ratio":{name:'ratio','type':'float','default':0.5},"allow_outside_center":{name:'Allow Outside Center',type:'bool',default:false}}; 
augmentation['resize'].param = {"target_size":{name:'Target Size','type':'int','default':null},"min_side_length":{name:'Min Side Length','type':'int','default':null},"max_side_length":{name:'Max Side Length','type':'int','default':null}}; 
augmentation['random_hflip'].param = {"swap_pair":{name:'Swap Pair',type:'int-list',default:''},"ratio":{name:'ratio',type:'float',default:0.5}};
augmentation['padding'].param = {"allow_outside_center":{name:'Allow Outside Center',type:'bool',default:false},"ratio":{name:'ratio','type':'float','default':1.0},"pad":{name:'Pad',type:'int-list',default:[4,4,4,4]}};
augmentation['random_pad'].param = {"up_scale_range":{name:'Up Scale Range',type:'int-list',default:''},ratio:{name:'ratio','type':'float','default':1.0},mean:{name:'Mean','type':'int-list','default':[104, 117, 123]}};


 




 
 