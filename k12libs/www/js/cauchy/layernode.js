'use strict';

class LayerNode{
    constructor(name,id="") {
        this._key = '';
        this._type = '';
        this.subtype = '';
        if(id == "")
          this._id = Math.round(Math.random()*8999 + 1000).toString();
        else
          this._id = id;
        this._group = '';
        this._output_shape = '';
        this.name = name;
        this.layer_builder = 'NNTorchLayer';
        this.inputs = [];
        this.outputs = [];

    }

    get id(){
        return this._id;
    }

    set id(value){
        //this._id = value;
    }

    get group(){
        return this._group;
    }

    set group(value){
        this._group = value;
    }


    gettext(){

        if(this.subtype != "")
          return this.subtype + "_" + this._id;
        else
          return this.name;
    }

    /**
     * 生成子类型
     * @param {*} value
     */
    gensubtype(value=""){
        let subtypeset = nodeEnum[this._type].subtype;
        if(typeof(value) != undefined && subtypeset.indexOf(value) >= 0)
            return value;
        else
            return nodeEnum[this._type].defaultsubtype;
    }

    /**
     * 更新子类型
     * @param {*} value
     */
    updatesubtype(value){
        let subtypeset = nodeEnum[this._type].subtype;
        if(subtypeset.includes(value) && value != this.subtype){
            this.subtype = value;

            //this.name = this.subtype + "_" + Math.round(Math.random()*1000);
            return true;
        }
        else
            return false;
    }

    /**
     * 计算Shape
     */
    computeShape(obj){
        if(this.inputs.length != 1)
            return {code:-1,msg:`${this.gettext()}连线错误`};
        let inputs = this.getInputinfo(obj);


        let w = inputs[0].out_shapes.w;
        let h = inputs[0].out_shapes.h;
        let channel = inputs[0].out_shapes.channel;
        let ret = this.validateRequired();
        if(ret.code != 200)
            return ret;

        this.out_shapes = {w:w,h:h,channel:channel};
        return {code:200,w:w,h:h,channel:channel};
    }

    /**
     * 生成proto对象
     * @param {bool} showall 是否显示全部参数
     */
    toProtoObj(showall){
        function getLayermode(subtype){

            switch(subtype){
                case "ConvTranspose1d":return Symbol.for("TRANSCONV1D");
                case "ConvTranspose2d":return Symbol.for("TRANSCONV2D");
                case "ConvTranspose3d":return Symbol.for("TRANSCONV3D");
                default:return Symbol.for(subtype.toUpperCase());
            }

        }

        let obj = {};
        obj.name = this.gettext();
        obj._type = this._type;
        obj.subtype = this.subtype;
        if(this.layer_builder != ""){
            obj.layer_builder = this.layer_builder;
            obj.layer_mode = getLayermode(this.subtype);

        }

        if(this.hasOwnProperty("inputs")){
            obj.inputs = [];
            for(let i = 0; i < this.inputs.length; ++i){
                if(this.inputs[i].startsWith("Input"))
                    obj.inputs.push("x");
                else
                    obj.inputs.push(this.inputs[i]);
            }
        }
        if(this.hasOwnProperty("outputs"))
            obj.outputs = this.outputs;

        obj.layer_params = {};



        for(let key in nodeParams[this.subtype]){

            if(this.hasOwnProperty(key) && typeof(this[key]) !="undefined"){
                if(!nodeParams[this.subtype][key].hasOwnProperty("default") || this[key] != nodeParams[this.subtype][key]["default"] || showall || nodeParams[this.subtype][key].hasOwnProperty("force")){

                    if(nodeParams[this.subtype][key].type == "number" && !Number.isNaN(Number(this[key]))){
                        obj.layer_params[key] = parseInt(this[key]);
                    }
                    else
                        obj.layer_params[key] = this[key];

                }
            }

        }




        return obj;
    }

    /**
     * 生成protostr
     * @param {bool} showall
     */
    toProtoStr(showall = false){
        function obj2str(obj, prefix){
            let retstr = "";
            for(let key in obj){

                if(key.startsWith("_",0))
                    continue;
                else if(key == "subtype")
                    continue;
                else{
                    let keytype = typeof(obj[key]);
                    switch(keytype){
                        case "string":{
                            let vals = obj[key].split(",");

                            $.each(vals,function(index,val){
                                retstr += " ".repeat(prefix) + `${key} : "${val}"\n`;
                            });
                            break;
                        }
                        case "number":
                        case "bigint":
                        case "boolean":retstr += " ".repeat(prefix) +`${key} : ${obj[key]}\n`;break;
                        case "symbol":retstr += " ".repeat(prefix) +`${key} : ${Symbol.keyFor(obj[key])}\n`;break;
                        case "object":{
                            if(Array.isArray(obj[key])){
                                if(obj[key].length > 0){
                                    let arraystr = "";
                                    for(let arraykey in obj[key]){
                                        arraystr += " ".repeat(prefix) + key + " : ";
                                        if(typeof(obj[key][arraykey]) == "string")
                                            arraystr += '"' +obj[key][arraykey] + '"\n';
                                        else
                                            arraystr += obj[key][arraykey] + "\n";
                                    }
                                    retstr += arraystr;
                                }
                            }
                            else{
                                retstr += " ".repeat(prefix) + key + " " + obj2str(obj[key],prefix + 2) + "\n";
                            }
                            break;
                        }
                        default:break;
                    }

                }
            }
            return `{\n${retstr}` + " ".repeat(prefix - 2) + "}";

        }

        //console.log(this);
        let obj = this.toProtoObj(showall);

        let result = "";
        result += "layer{\n" + " ".repeat(2) +  obj._type.toLowerCase();
        result += obj2str(obj,4);
        result += "\n}";
        return result;
    }

    /**
     * 验证节点数据是否完整
     */
    validateRequired(){
        let result = {};
        result.code = 200;
        result.msg = "";
        // console.log(this);
        for(let key in this){
            if(nodeParams[this.subtype].hasOwnProperty(key)){
                if(typeof(this[key]) == "undefined" || this[key] == "") {
                    result.code = 401;
                    result.field = key;
                    result.text = this.gettext();
                    result.msg = `${result.text}中字段${key}不完整`;
                    return result;
                }
            }
        }
        return result;
    }

    /**
     * 设置来源节点
     * @param {*} value
     */
    setInputs(value){
        this.inputs = value;
    }

    /**
     * 设置输出节点
     * @param {*} value
     */
    setOutputs(value){
        this.outputs = value;
    }

    /**
     * 获取输入节点
     * @param {节点} seqnodes
     */
    getInputinfo(seqnodes){
        let ret = [];
        let that = this;

        $.each(seqnodes,function(index,val){
            if(that.inputs.indexOf(val.info.gettext()) >= 0){
                ret.push(val.info);
            }

        });

        return ret;
    }

    /**
     * 字符串转List
     * @param {字符串} str
     * @param {转换类型} type [int float]
     */
    static str2list(str,type='int'){
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

    /**
     * 工厂类
     * 根据子类型创建子类对象
     * @param {子类型} subtype
     * @param {对象命名} name
     * @param {二级类型} lev2type
     */
    static subfactory(subtype,name="",lev2type="",id=""){
        switch(subtype){
            case 'Conv':return new Convolution(lev2type,name,id);
            case 'Padding':return new Padding(lev2type,name,id);
            case 'Pool':return new Pooling(lev2type,name,id);
            case 'Dropout':return new Dropout(lev2type,name,id);
            case 'Norm':return new Normalization(lev2type,name,id);
            case 'Act':return new Activation(lev2type,name,id);
            case 'Data':return new Data(lev2type,name,id);
            case 'Linear':return new Linear(lev2type,name,id);
            case 'Loss':return new Loss(lev2type,name,id);
            case 'BaseFunc':return new BaseFunc(lev2type,name,id);
            case 'Vulkan':return new Vulkan(lev2type,name,id);
            case 'Input':return new Input(lev2type,name,id);
            case 'Output':return new Output(lev2type,name,id);
            default:return new LayerNode(name,id);
        }
    }

}

/**
 * 输入层
 */
class Input extends LayerNode{
    constructor(subtype="",name="",id, in_features="32,64,64"){
        super(name,id);
        this._type = 'Input';
        this.subtype = 'Input';
        this.in_features = in_features;
    }
    /**
     * 计算Shape
     */
    computeShape(obj){

        let ret = this.validateRequired();
        if(ret.code != 200)
            return ret;
        try{
          let infos = this.in_features.split(",");

          if(infos.length != 3)
            return {code:-8,msg:`${this.gettext()}参数错误,in_features应为3维向量`};

          let c = infos[0]
          let w = infos[1]
          let h = infos[2]
          if (w == "undefined") {
              w = 64
              h = 64
          }
          // if(input_channels != infos[0])
          //   return {code:-9,msg:`${this.gettext()}参数错误,channel应为${input_channels}`};
          //
          // if(w != infos[1])
          //   return {code:-9,msg:`${this.gettext()}参数错误,channel应为${w}`};
          //
          // if(h != infos[2])
          //   return {code:-9,msg:`${this.gettext()}参数错误,channel应为${h}`};

          this.out_shapes = {w:w,h:h,channel:c};

          return {code:200,w:w,h:h,channel:c};
        }
        catch(err){
            console.log(err);
            return {code:-1,msg:`${this.gettext()}参数错误`};
        }
    }


}

/**
 * 输出层
*/
class Output extends LayerNode{
    constructor(subtype="",name="",id, out_features){
        super(name,id);
        this._type = 'Output';
        this.subtype = 'Output';
        this.out_features = out_features;

    }
    /**
     * 计算Shape
     */
    computeShape(obj){

        let ret = this.validateRequired();
        if(ret.code != 200)
            return ret;
        try{
            if(this.inputs.length != 1)
                return {code:-1,msg:`${this.gettext()}连线错误`};
            let inputs = this.getInputinfo(obj);


            let w = inputs[0].out_shapes.w;
            let h = inputs[0].out_shapes.h;
            let input_channels = inputs[0].out_shapes.channel;

            if(this.out_features != h)
                return {code:-7,msg:`${this.gettext()}参数错误,out_features${h}`};

            let wout = w;
            let channelout = input_channels;
            let hout = this.out_features;
            this.out_shapes = {w:wout,h:hout,channel:this.out_channels};
            return {code:200,w:wout,h:hout,channel:channelout};
        }
        catch(err){
            return {code:-1,msg:`${this.gettext()}参数错误`};
        }
    }
}

/**
 * 卷积层
 */
class Convolution extends LayerNode{
    constructor(subtype="",name="",id="",in_channels,out_channels,
    kernel_size, stride='1', padding='0',output_padding='0', dilation='1', groups='1', bias='True'){
        super(name,id);
        this._type = 'Conv';
        this.subtype = super.gensubtype(subtype);
        this.in_channels = in_channels;
        this.out_channels = out_channels;
        this.kernel_size = kernel_size;
        this.output_padding = output_padding;
        this.stride = stride;
        this.padding = padding;
        this.dilation = dilation;
        this.groups = groups;
        this.bias = bias;
    }


    typecheck(){

        if(Number.isNaN(this.in_channels) || !Number.isSafeInteger(parseInt(this.in_channels)) || parseInt(this.in_channels) <= 0)
            return {code:-1,msg:`${this.gettext()}参数错误，in_channels应为大于0的整数 `};
        if(Number.isNaN(this.in_channels) || !Number.isSafeInteger(parseInt(this.out_channels)) || parseInt(this.out_channels) <= 0)
            return {code:-1,msg:`${this.gettext()}参数错误，out_channels应为大于0的整数 `};
        if(Number.isNaN(this.in_channels) || !Number.isSafeInteger(parseInt(this.kernel_size)) || parseInt(this.kernel_size) <= 0)
            return {code:-1,msg:`${this.gettext()}参数错误，kernel_size应为大于0的整数 `};
        if(Number.isNaN(this.in_channels) || !Number.isSafeInteger(parseInt(this.stride)) || parseInt(this.stride) <= 0)
            return {code:-1,msg:`${this.gettext()}参数错误，stride应为大于0的整数 `};
        if(Number.isNaN(this.in_channels) || !Number.isSafeInteger(parseInt(this.padding)) || parseInt(this.padding) < 0)
            return {code:-1,msg:`${this.gettext()}参数错误，padding应为大于等于0的整数 `};
        if(Number.isNaN(this.in_channels) || !Number.isSafeInteger(parseInt(this.dilation)) || parseInt(this.dilation) <= 0)
            return {code:-1,msg:`${this.gettext()}参数错误，dilation应为大于0的整数 `};
        return {code:200};

    }

    /**
     * 计算Shape
     */
    computeShape(obj){
        if(this.inputs.length != 1)
            return {code:-1,msg:`${this.gettext()}连线错误`};
        let inputs = this.getInputinfo(obj);


        let w = inputs[0].out_shapes.w;
        let h = inputs[0].out_shapes.h;
        let input_channels = inputs[0].out_shapes.channel;
        let ret = this.validateRequired();
        if(ret.code != 200)
            return ret;

        ret = this.typecheck();
        if(ret.code != 200)
            return ret;
        try{
            if(this.in_channels != input_channels)
                return {code:-1,msg:`${this.gettext()}参数错误,in_channels应为${input_channels}`};
            let k = 0,wout = 0,hout = 0;
            if(this.subtype.startsWith("ConvTrans")){
                wout = Math.floor(eval(`(${w} - 1) * ${this.stride} - 2 * ${this.padding} + ${this.kernel_size} + ${this.output_padding}`));
                hout = Math.floor(eval(`(${w} - 1) * ${this.stride} - 2 * ${this.padding} + ${this.kernel_size} + ${this.output_padding}`));
            } else if(this.subtype.startsWith("Conv")){
                k = eval(`${this.kernel_size} + (${this.kernel_size} - 1) * (${this.dilation} - 1)`);
                if(w + 2 * this.padding < k || h + 2 * this.padding < k)
                    return {code:-1,msg:`${this.gettext()}参数错误`};
                if(this.padding >= k / 2.0)
                    return {code:-1,msg:`${this.gettext()}参数错误,Padding Size 需要小于 Kernel Size的一半`};

                wout = Math.floor(eval(`(${w} + 2 * ${this.padding} - ${k})/${this.stride}`)) + 1;
                hout = Math.floor(eval(`(${h} + 2 * ${this.padding} - ${k})/${this.stride}`)) + 1;
            }

            this.out_shapes = {w:wout,h:hout,channel:this.out_channels};
            return {code:200,w:wout,h:hout,channel:this.out_channels};
        }
        catch(err){
            return {code:-1,msg:`${this.gettext()}参数错误`};
        }
    }

}

class Padding extends LayerNode{
    constructor(subtype="",name="",id="",padding='0',value='0'){
        super(name,id);
        this._type = 'Padding';
        this.subtype = super.gensubtype(subtype);
        this.padding = padding;
        this.value = value;
    }

    /**
     * 计算Shape
     */
    computeShape(obj){
        if(this.inputs.length != 1)
            return {code:-1,msg:`${this.gettext()}连线错误`};
        let inputs = this.getInputinfo(obj);


        let w = inputs[0].out_shapes.w;
        let h = inputs[0].out_shapes.h;
        let input_channels = inputs[0].out_shapes.channel;
        let ret = this.validateRequired();

        if(ret.code != 200)
            return ret;
        try{
            let wout = parseInt(w) + 2 * parseInt(this.padding);
            let hout = parseInt(h) + 2 * parseInt(this.padding);

            this.out_shapes = {w:wout,h:hout,channel:input_channels};
            return {code:200,w:wout,h:hout,channel:input_channels};
        }
        catch(err){
            console.log(err);
            return {code:-1,msg:`${this.gettext()}参数错误`};
        }
    }

}

/**
 * 池化层
 */
class Pooling extends LayerNode{
    constructor(subtype="",name="",id="",kernel_size,output_size,stride,norm_type = '1',padding='0',dilation='1',return_indices='False',
    ceil_mode='False',count_include_pad='True'){
        super(name,id);
        this._type = 'Pool';
        this.subtype = super.gensubtype(subtype);
        this.kernel_size = kernel_size;
        this.stride = stride;
        this.padding = padding;
        this.dilation = dilation;
        this.return_indices = return_indices;
        this.ceil_mode = ceil_mode;
        this.count_include_pad = count_include_pad;
        this.norm_type = norm_type;
        this.output_size = output_size;
    }

    typecheck(){
        if(!this.subtype.startsWith('Adaptive')){
            if(Number.isNaN(this.kernel_size) || !Number.isSafeInteger(parseInt(this.kernel_size)) || parseInt(this.kernel_size) <= 0)
                return {code:-1,msg:`${this.gettext()}参数错误，kernel_size应为大于0的整数 `};
            if(Number.isNaN(this.stride) || !Number.isSafeInteger(parseInt(this.stride)) || parseInt(this.stride) <= 0)
                return {code:-1,msg:`${this.gettext()}参数错误，stride应为大于0的整数 `};
            if(Number.isNaN(this.padding) || !Number.isSafeInteger(parseInt(this.padding)) || parseInt(this.padding) < 0)
                return {code:-1,msg:`${this.gettext()}参数错误，padding应为大于等于0的整数 `};
            if(Number.isNaN(this.dilation) || !Number.isSafeInteger(parseInt(this.dilation)) || parseInt(this.dilation) <= 0)
                return {code:-1,msg:`${this.gettext()}参数错误，dilation应为大于0的整数 `};
        }
        return {code:200};

    }
    /**
     * 计算Shape
     */
    computeShape(obj){
        if(this.inputs.length != 1)
            return {code:-1,msg:`${this.gettext()}连线错误`};
        let inputs = this.getInputinfo(obj);


        let w = inputs[0].out_shapes.w;
        let h = inputs[0].out_shapes.h;
        let input_channels = inputs[0].out_shapes.channel;

        let ret = this.validateRequired();
        if(ret.code != 200)
            return ret;

        ret = this.typecheck();
        if(ret.code != 200)
            return ret;
        try{
            let wout = 0;
            let hout = 0;

            if(this.subtype.startsWith('Adaptive')){
                let ret = LayerNode.str2list(this.output_size);
                if(ret == null || ret.length <= 0 || ret.length > 3)
                    return {code:-1,msg:`${this.gettext()}参数错误`};
                if(ret.length == 1){
                    wout = ret[0];
                    hout = ret[0];
                }else if(ret.length == 2){
                    wout = ret[0];
                    hout = ret[1];
                }


            }else if(this.subtype.startsWith('MaxUnpool')){
                wout = eval(`(${w} - 1) * ${this.stride} -  2 * ${this.padding} +  ${this.kernel_size}`);
                hout = eval(`(${h} - 1) * ${this.stride} -  2 * ${this.padding} +  ${this.kernel_size}`);

            }else{
                let k = eval(`${this.kernel_size} + (${this.kernel_size} - 1) * (${this.dilation} - 1)`);
                if(w + 2 * this.padding < k || h + 2 * this.padding < k)
                    return {code:-1,msg:`${this.gettext()}参数错误`};
                if(this.padding >= k / 2.0)
                    return {code:-1,msg:`${this.gettext()}参数错误,Padding Size 需要小于 Kernel Size的一半`};

                if(this.ceil_mode == 'True'){
                    wout = Math.ceil(eval(`(${w} + 2 * ${this.padding} - ${k})/${this.stride}`)) + 1;
                    hout = Math.ceil(eval(`(${h} + 2 * ${this.padding} - ${k})/${this.stride}`)) + 1;
                }
                else{
                    //console.log(`(${w} + 2 * ${this.padding} - ${k})/${this.stride}`);

                    wout = Math.floor(eval(`(${w} + 2 * ${this.padding} - ${k})/${this.stride}`)) + 1;
                    hout = Math.floor(eval(`(${h} + 2 * ${this.padding} - ${k})/${this.stride}`)) + 1;
                }

            }

            if(wout <= 0 || hout <= 0)
                return {code:-1,msg:`${this.gettext()}参数错误`};

            this.out_shapes = {w:wout,h:hout,channel:input_channels};
            return {code:200,w:wout,h:hout,channel:input_channels};
        }
        catch(err){
            console.log(err);
            return {code:-1,msg:`${this.gettext()}参数错误`};
        }
    }

}

class Normalization extends LayerNode{
    constructor(subtype="",name="",id="",num_features='0',eps='1e-05', momentum='0.1',
        affine='True', track_running_stats='True'){
        super(name,id);
        this._type = 'Norm';
        this.subtype = super.gensubtype(subtype);
        this.num_features = num_features;
        this.eps = eps;
        this.momentum = momentum;
        this.affine = affine;
        this.track_running_stats = track_running_stats;

    }

    /**
     * 计算Shape
     */
    computeShape(obj){
        if(this.inputs.length != 1)
            return {code:-1,msg:`${this.gettext()}连线错误`};
        let inputs = this.getInputinfo(obj);


        let w = inputs[0].out_shapes.w;
        let h = inputs[0].out_shapes.h;
        let input_channels = inputs[0].out_shapes.channel;
        if(this.num_features != input_channels)
            return {code:-1,msg:`${this.gettext()}参数错误,num_features应为${input_channels}`};

        this.out_shapes = {w:w,h:h,channel:this.num_features};

        return {code:200,w:w,h:h,channel:this.num_features};
    }
}

class Activation extends LayerNode{
    constructor(subtype="",name="",id="",inplace='False',negative_slope='0.01',min_val='-1.0',max_val='1.0',lambd = '0.5',dim = '1' ){
        super(name,id);
        this._type = 'Act';
        this.subtype = super.gensubtype(subtype);
        this.inplace = inplace;
        this.negative_slope = negative_slope;
        this.min_val = min_val;
        this.max_val = max_val;
        this.lambd = lambd;
        this.dim = dim;

    }

}

class Loss extends LayerNode{
    constructor(subtype="",name="",id="",size_average='',reduce='',
        reduction='mean',weight='',ignore_index='-100'){
        super(name,id);
        this._type = 'Loss';
        this.subtype = super.gensubtype(subtype);
        this.size_average = size_average;
        this.reduce = reduce;
        this.reduction = reduction;
        this.weight = weight;
        this.ignore_index = ignore_index;
    }
}

class Dropout extends LayerNode{
    constructor(subtype="",name="",id="",inplace='False',p='0.5'){
        super(name,id);
        this._type = 'Dropout';
        this.subtype = super.gensubtype(subtype);
        this.inplace = inplace;
        this.p = p;
    }

}

class Linear extends LayerNode{
    constructor(subtype="",name="",id="",in_features,out_features,
        bias="True"){
        super(name,id);
        this._type = 'Linear';
        this.subtype = super.gensubtype(subtype);
        this.in_features = in_features;
        this.out_features = out_features;
        this.bias = bias;
    }
    /**
     * 计算Shape
     */
    computeShape(obj){
        if(this.inputs.length != 1)
            return {code:-1,msg:`${this.gettext()}连线错误`};
        let inputs = this.getInputinfo(obj);


        let w = null;
        let h = inputs[0].out_shapes.h;
        let input_channels = null;

        let ret = this.validateRequired();
        if(ret.code != 200)
            return ret;
        try{
          if(this.in_features != h)
            return {code:-7,msg:`${this.gettext()}参数错误,in_feature应为${h}`};
          let wout = w;
          let channelout = input_channels;
          let hout = this.out_features;
          this.out_shapes = {w:wout,h:hout,channel:channelout};
          return {code:200,w:wout,h:hout,channel:channelout};
        }
        catch(err){
            return {code:-1,msg:`${this.gettext()}参数错误`};
        }
    }

}

class BaseFunc extends LayerNode{
    constructor(subtype="",name="",id="",shape,dim="-1",start_dim="0",end_dim="-1"){
        super(name,id);
        this._type = 'BaseFunc';
        this.layer_builder = 'TorchFuncLayer';
        this.subtype = super.gensubtype(subtype);
        this.shape = shape;
        this.dim = dim;
        this.start_dim = start_dim;
        this.end_dim = end_dim;
    }

    /**
     * 计算Shape
     */
    computeShape(obj){
        if((this.inputs.length != 2 && this.subtype == 'Add') ||
         (this.inputs.length < 2 && this.subtype == 'Cat'))
            return {code:-1,msg:`${this.gettext()}连线错误`};
        let inputs = this.getInputinfo(obj);


        let w0 = inputs[0].out_shapes.w;
        let h0 = inputs[0].out_shapes.h;
        let input_channels0 = inputs[0].out_shapes.channel;

        let w1 = inputs[1].out_shapes.w;
        let h1 = inputs[1].out_shapes.h;
        let input_channels1 = inputs[1].out_shapes.channel;

        let ret = this.validateRequired();

        if(ret.code != 200)
            return ret;
        try{

            if(this.subtype == 'Add'){
                if(w0 != w1 || h0 != h1 || input_channels0 != input_channels1){
                    return {code:-1,msg:`Shape不一致，无法Add`};
                }

            }else if(this.subtype == 'Cat'){
                let array = [];
                for(let i = 0; i < inputs.length; ++i){
                    array.push([inputs[i].out_shapes.channel,inputs[i].out_shapes.w,inputs[i].out_shapes.h]);
                }

                console.log(inputs.length)

                let dim = -1;
                if(this.dim == -1)
                    // QRS: modify (B, C, W, H)
                    // dim = array[0].length - 1;
                    dim = array[0].length;
                else
                    dim = parseInt(this.dim);

                if (dim != -1) {
                    dim = dim - 1;
                }

                for(let i = 1; i < array.length; ++i){
                    for(let j = 0; j < array[i].length; ++j){
                        if(j != dim){
                            if(array[0][j] != array[i][j])
                                return {code:-1,msg:`Shape不一致，无法Cat`};
                        }
                        else{
                            array[0][j] = parseInt(array[0][j]) + parseInt(array[i][j]);

                        }

                    }


                }
                w0 = array[0][1];
                h0 = array[0][2];
                input_channels0 = array[0][0];

            }
            this.out_shapes = {w:w0,h:h0,channel:input_channels0};
            return {code:200,w:w0,h:h0,channel:input_channels0};
        }
        catch(err){
            console.log(err);
            return {code:-1,msg:`${this.gettext()}参数1错误`};
        }
    }

}

class Vulkan extends LayerNode{
    constructor(subtype="",name="",id="",target_shape,dim,start_dim="1",end_dim="-1"){
        super(name,id);
        this._type = 'Vulkan';
        this.subtype = super.gensubtype(subtype);
        this.target_shape = target_shape;
        this.dim = dim;
        this.start_dim = start_dim;
        this.end_dim = end_dim;
    }

    /**
     * 计算Shape
     */
    computeShape(obj){
        if(this.inputs.length != 1)
            return {code:-1,msg:`${this.gettext()}连线错误`};
        let inputs = this.getInputinfo(obj);


        let w = inputs[0].out_shapes.w;
        let h = inputs[0].out_shapes.h;
        let input_channels = inputs[0].out_shapes.channel;

        let ret = this.validateRequired();
        if(ret.code != 200)
            return ret;
        try{
          let wout = 0;
          let hout = 0;
          let channelout = 0;
          if(this.subtype == 'Flatten'){
            channelout = null;
            wout = null;
            hout = w * h * input_channels;
          }else if(this.subtype == 'Reshape'){
                let ret = LayerNode.str2list(this.target_shape);
                if(ret == null || ret.length == 0 || ret.length > 4)
                    return {code:-1,msg:`${this.gettext()}参数错误`};
                let totalDim = 1;
                for(let i = 0; i < ret.length; ++i){
                    totalDim *= ret[i];
                }
                if(totalDim != w * h * input_channels)
                    return {code:-1,msg:`${this.gettext()}参数错误`};

                channelout = null;
                wout = null;
                hout = ret[ret.length - 1];
                if(ret.length > 1)
                    wout = ret[ret.length -2];
                if(ret.length > 2)
                    channelout = ret[ret.length -3];

          }
          this.out_shapes = {w:wout,h:hout,channel:channelout};
          return {code:200,w:wout,h:hout,channel:channelout};
        }
        catch(err){
            console.log(err);
            return {code:-1,msg:`${this.gettext()}参数错误`};
        }
    }

}




