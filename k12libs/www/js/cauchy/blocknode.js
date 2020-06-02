'use strict';

class BlockNode{
    constructor(name) {        
        this._key = '';
        this._type = '';
        
        this._id = "Block_" + Math.round(Math.random()*8999 + 1000).toString();         
        this._group = '';
        this._name = name;         
    }

    /**
     * 工厂类
     * 根据子类型创建子类对象
     * @param {子类型} subtype 
     * @param {对象命名} name 
     */
    static subfactory(subtype,name=""){
        switch(subtype){
            case 'resBasicblock':return new ResBasicBlock(name,blockEnum["resBasicblock"].num_blocks.default,blockEnum["resBasicblock"].planes.default,blockEnum["resBasicblock"].strides.default);
            case 'resBottleneckblock':return new ResBottleneckBlock(name,blockEnum["resBottleneckblock"].num_blocks.default,blockEnum["resBottleneckblock"].planes.default,blockEnum["resBottleneckblock"].strides.default);             
            default:return new BlockNode(name);
        }             
    }

}

class ResBasicBlock extends BlockNode{
    constructor(name="",num_blocks='',planes='',strides=''){
        super(name);        
        this._type = 'Res_Basic';
        this.num_blocks = num_blocks;
        this.planes = planes;
        this.strides = strides;
    }

}

class ResBottleneckBlock extends BlockNode{
    constructor(name="",num_blocks='',planes='',strides=''){
        super(name);
        this._type = 'Res_Bottleneck';
        this.num_blocks = num_blocks;
        this.planes = planes;
        this.strides = strides;
    }

}

class DenseBottleneckBlock extends BlockNode{
    constructor(name="",num_blocks='',planes='',strides=''){
        super(name);
        this._type = 'Dense_Bottleneck';
        this.num_blocks = num_blocks;
        this.planes = planes;
        this.strides = strides;
    }

}