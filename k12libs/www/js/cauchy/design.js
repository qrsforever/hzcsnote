'use strict';
var $$ = go.GraphObject.make;
var selnode = {};
var selgroup = {};
var diagram = null;
var layer_palette = null;
var net_palette = null;
var nodearr = [];

$(function(){
    let allowdelete = false;
    if(project_model == 'custom')
        allowdelete = true;

    allowdelete = true;

    diagram = $$(go.Diagram, "design_div",  // must name or refer to the DIV HTML element
        {
            "undoManager.isEnabled": allowdelete,  // enable undo & redo
            "draggingTool.dragsLink": true,
            "linkingTool.isUnconnectedLinkValid": true,
            "linkingTool.portGravity": 20,
            "allowHorizontalScroll":false,
            "allowVerticalScroll":false,
            "allowCopy":false,
            "grid.visible": true,
            "allowDelete":allowdelete,

            nodeSelectionAdornmentTemplate:
                $$(go.Adornment, "Auto",
                    { layerName: "Grid" },
                    $$(go.Shape, "Rectangle", {fill:"transparent",strokeWidth: 1 }),
                    $$(go.Placeholder)
                ),
            groupSelectionAdornmentTemplate:
                $$(go.Adornment, "Auto",
                    { layerName: "Grid" },
                    $$(go.Shape, "Rectangle", {strokeWidth: 1,fill:"transparent" }),
                    $$(go.Placeholder)
                ),
            "BackgroundSingleClicked":function(e){
                $("#property_div").fadeOut(500);
                $(".toolbar-div").css("right","0px");
            },
            "ModelChanged": function(e) {
                // console.log(diagram.model.toJson());
                if(e.propertyName == "CommittedTransaction"){
                    validateprocess(diagram.model.nodeDataArray,diagram.model.linkDataArray,current_net);
                    savemodel();

                }
            }

        });
    diagram.model=$$(go.GraphLinksModel,
        {
            linkFromPortIdProperty: "fromPort",
            linkToPortIdProperty: "toPort",
            nodeDataArray:[],
            linkDataArray:[]
        });

    //连线样式
    diagram.linkTemplate =
        $$(FixedLink,
        { relinkableFrom: true, relinkableTo: true, reshapable: true },
        {
            routing: go.Link.AvoidsNodes,
            curve: go.Link.JumpGap,
            corner: 5,
            toShortLength: 4,
        },
        new go.Binding("points").makeTwoWay(),
        $$(go.Shape, { isPanelMain: true, strokeWidth: 1,fill:'lightgray' }),
        $$(go.Shape, { toArrow: "Standard", stroke: null }),
        );

    //节点模版样式
    let palette_node_template =
        $$(go.Node, "Spot",
        {
            locationSpot: go.Spot.Center
        },
        $$(go.Panel, "Auto",
            $$(go.Shape, "RoundedRectangle",
            { fill: 'rgba(29,170,241,1)', strokeWidth: 0 ,width:100,height:30},
            new go.Binding("figure", "figure")),
            $$(go.TextBlock, { stroke: "white" }, new go.Binding("text","text"))

        ));

    //block模版样式
    let palette_group_template =
        $$(go.Group, "Spot",
        {
            locationSpot: go.Spot.Center ,
            isSubGraphExpanded: false,
            ungroupable: true
        },
        $$(go.Panel, "Auto",
            $$(go.Shape, "RoundedRectangle",
            { fill: 'rgba(94,168,221,0.9)', strokeWidth: 0 ,width:120,height:50},
            new go.Binding("figure", "figure")),
            $$(go.TextBlock, { stroke: "white" }, new go.Binding("text","text"))
        ));
    for(let key in nodeEnum){
        diagram.nodeTemplateMap.add(key,
            $$(go.Node, "Vertical",
                { locationSpot: go.Spot.Center,
                  locationObjectName: "ICON",
                  selectionAdorned: false,
                },
                new go.Binding("location", "loc", go.Point.parse).makeTwoWay(go.Point.stringify),

                $$(go.Panel, "Auto",
                    {name:'ICON'},
                    $$(go.Shape, "RoundedRectangle",
                    { fill: nodeEnum[key].color, stroke:null ,width:180,height:40},
                    new go.Binding("figure", "figure")),
                    $$(go.TextBlock, {font: "14px Roboto",stroke: "whitesmoke"}, new go.Binding("text","text")),
                    $$(go.Picture,
                        {
                            name: "Picture",
                            desiredSize: new go.Size(25, 25),
                            margin: new go.Margin(6, 150, 6, 0),
                            source:"images/cauchy/" + nodeEnum[key].img
                        }
                    ),
                    makePort("T", go.Spot.Top, false, true),
                    makePort("B", go.Spot.Bottom,  true, false),
                    makePort("L", go.Spot.Left, false, true),
                    makePort("R", go.Spot.Right,  true, false)
                ),
                $$(go.TextBlock,new go.Binding("visible", "outshape", function(f) { return f !== ""; }),{font: "16px Roboto"}, new go.Binding("text","outshape")),
                {
                    // handle mouse enter/leave events to show/hide the ports
                    mouseEnter: function(e, node){
                        showSmallPorts(node, true);
                    },
                    mouseLeave: function(e, node){
                        showSmallPorts(node, false);
                    },
                    click: function(e,node){
                        nodeClick(e,node);
                    }
                }
            ),
        );

    }
    diagram.nodeTemplateMap.add("",
        $$(go.Node, go.Panel.Auto,
            new go.Binding("location", "loc", go.Point.parse).makeTwoWay(go.Point.stringify),
            $$(go.Panel, "Auto",
                $$(go.Shape, "RoundedRectangle",
                { fill: "#ECECFF", stroke:null ,width:180,height:40},
                new go.Binding("fill","color"),
                new go.Binding("figure", "figure")),
                $$(go.TextBlock, {font: "12px Roboto",stroke: "black"}, new go.Binding("text","category")),
                makePort("T", go.Spot.Top, false, true),
                makePort("R", go.Spot.Right, false, true),
                makePort("B", go.Spot.Bottom,  true, false),
                makePort("L", go.Spot.Left,  true, false)
            ),
            {
                click: function(e,node){
                    prenodeClick(e,node);
                }
            }
        ),
    );


    diagram.groupTemplateMap.add("seqblock",
        $$(go.Group, "Auto",
            new go.Binding("location", "loc", go.Point.parse).makeTwoWay(go.Point.stringify),
            {
                selectionObjectName: "PH",
                locationObjectName: "PH",
                handlesDragDropForMembers: true,  // don't need to define handlers on
                computesBoundsAfterDrag: true,
                layout:
                $$(go.GridLayout,
                    { wrappingColumn: 1, alignment: go.GridLayout.Position,
                        cellSize: new go.Size(1, 1), spacing: new go.Size(20, 20) })
            },
            new go.Binding("background", "isHighlighted", function(h) { return h ? "rgba(255,0,0,0.2)" : "transparent"; }).ofObject(),
            $$(go.Shape, "Rectangle",
                { fill: null, stroke: "orange", strokeWidth: 2 }),
            { // what to do when a drag-over or a drag-drop occurs on a Group
                //mouseDragEnter: function(e, grp, prev) { highlightGroup(grp, true); },
                //mouseDragLeave: function(e, grp, next) { highlightGroup(grp, false); },
                mouseDrop: function(e, grp) {
                    var ok = grp.addMembers(grp.diagram.selection, true);
                    if (!ok) grp.diagram.currentTool.doCancel();
                }
            },

            $$(go.Panel, "Vertical",  // title above Placeholder
                $$(go.Panel, "Horizontal",  // button next to TextBlock
                { stretch: go.GraphObject.Horizontal, background: "transparent" },
                $$("SubGraphExpanderButton",{ alignment: go.Spot.TopRight, margin: 5 }),
                $$(go.TextBlock,
                    {
                        alignment: go.Spot.Left,
                        margin: 5,
                        font: "bold 14px sans-serif",
                        opacity: 0.75,
                        stroke: "#404040"
                    },
                    new go.Binding("text", "text").makeTwoWay())
                ),  // end Horizontal Panel
                $$(go.Placeholder,
                { padding: 15, alignment: go.Spot.TopLeft })
            ),
            {
                click: function(e,node){
                    groupClick(e,node);
                }
            }
        )
    );

    diagram.groupTemplateMap.add("custom",
        $$(go.Group, "Auto",
            new go.Binding("location", "loc", go.Point.parse).makeTwoWay(go.Point.stringify),
            {
                selectionObjectName: "PH",
                locationObjectName: "PH",
                handlesDragDropForMembers: true,  // don't need to define handlers on
                computesBoundsAfterDrag: true,
                isSubGraphExpanded: false,  // only show the Group itself, not any of its members
                ungroupable: true
                //ungroupable: true
            },
            new go.Binding("background", "isHighlighted", function(h) { return h ? "rgba(255,0,0,0.2)" : "transparent"; }).ofObject(),
            $$(go.Shape, "Rectangle",
                { fill: null, stroke: "orange", strokeWidth: 2 }),
            { // what to do when a drag-over or a drag-drop occurs on a Group
                //mouseDragEnter: function(e, grp, prev) { highlightGroup(grp, true); },
                //mouseDragLeave: function(e, grp, next) { highlightGroup(grp, false); },
                mouseDrop: function(e, grp) {
                    var ok = grp.addMembers(grp.diagram.selection, true);
                    if (!ok) grp.diagram.currentTool.doCancel();
                }
            },

            $$(go.Panel, "Vertical",  // title above Placeholder
                $$(go.Panel, "Horizontal",  // button next to TextBlock
                { stretch: go.GraphObject.Horizontal, background: "transparent" },
                $$("SubGraphExpanderButton",{ alignment: go.Spot.TopRight, margin: 5 }),
                $$(go.TextBlock,
                    {
                        alignment: go.Spot.Left,
                        margin: 5,
                        font: "bold 14px sans-serif",
                        opacity: 0.75,
                        stroke: "#404040"
                    },
                    new go.Binding("text", "text").makeTwoWay())
                ),  // end Horizontal Panel
                $$(go.Placeholder,
                { padding: 15, alignment: go.Spot.TopLeft })
            ),
            {
                click: function(e,node){
                    groupClick(e,node);
                }
            }
        )
    );




    let layermodels = [];
    //let blockmodels = [];
    let netmodels = [];
    let netlinkmodels = [];
    for(let key in nodeEnum){
        var node = {};
        node.key = key;
        node.text = key;
        node.category = key;
        layermodels.push(node);
    }

    for(let key in netEnum){
        var net = {};
        net.key = key;
        net.text = key;

        net.category = netEnum[key].layout;
        net.level = "top";
        net.isGroup = true;
        netmodels.push(net);
        for(let subkey in netEnum[key].links){
            var link = {};
            link.from = netEnum[key].links[subkey].from;
            link.to = netEnum[key].links[subkey].to;
            if(netEnum[key].links[subkey].hasOwnProperty("fromPort"))
                link.fromPort = netEnum[key].links[subkey].fromPort;
            if(netEnum[key].links[subkey].hasOwnProperty("toPort"))
                link.toPort = netEnum[key].links[subkey].toPort;
            netlinkmodels.push(link);

        }

        for(let subkey in netEnum[key].nodes){
            if(netEnum[key].nodes[subkey].category == "seqblock"){
                var net = {};
                net.key = netEnum[key].nodes[subkey].key;
                net.text = net.key;
                net.category = "seqblock";
                net.level = "low";
                net.isGroup = true;
                net.group = key;
                netmodels.push(net);
                let block_name = netEnum[key].nodes[subkey].name;

                for(let subkey in netEnum[key][block_name].nodes){
                    var node = {};
                    node.key = netEnum[key][block_name].nodes[subkey].key;
                    node.text = netEnum[key][block_name].nodes[subkey].key;
                    node.category = netEnum[key][block_name].nodes[subkey].category;
                    node.group = net.key;
                    node.subtype = netEnum[key][block_name].nodes[subkey].subtype;
                    node.params = netEnum[key][block_name].nodes[subkey].params;
                    netmodels.push(node);
                }

                for(let subkey in netEnum[key][block_name].links){
                    var link = {};
                    link.from = netEnum[key][block_name].links[subkey].from;
                    link.to = netEnum[key][block_name].links[subkey].to;
                    netlinkmodels.push(link);
                }



            }else{
                var node = {};
                node.key = netEnum[key].nodes[subkey].key;
                node.text = netEnum[key].nodes[subkey].key;
                node.category = netEnum[key].nodes[subkey].category;
                node.group = key;
                node.subtype = netEnum[key].nodes[subkey].subtype;
                node.params = netEnum[key].nodes[subkey].params;
                node.loc = netEnum[key].nodes[subkey].loc;
                if(netEnum[key].nodes[subkey].hasOwnProperty("color"))
                    node.color = netEnum[key].nodes[subkey].color;
                netmodels.push(node);
            }


        }
    }

    layer_palette = $$(go.Palette, "layer_palette",
        {
            nodeTemplate: palette_node_template,
            model: new go.GraphLinksModel(layermodels)
        });
    //console.log(netlinkmodels);
    net_palette = $$(go.Palette, "network_palette",
        {
            nodeTemplateMap: diagram.nodeTemplateMap,
            groupTemplate: palette_group_template,
            model: new go.GraphLinksModel(netmodels,netlinkmodels)

        });


    //function
    $('.model-palette').on('hidden.bs.collapse', function (){
        layer_palette.requestUpdate();
        net_palette.requestUpdate();
    });
    $('.model-palette').on('show.bs.collapse', function (){
        $('.model-palette').removeClass("in");

    });

    $('.model-palette').on('shown.bs.collapse', function (){
        layer_palette.requestUpdate();
        net_palette.requestUpdate();
    });

    diagram.addDiagramListener('ExternalObjectsDropped', function(e) {
        var node = e.subject.first();
        if(node) {
            if(node.data.isGroup == true){
                diagram.commandHandler.ungroupSelection();
                if(node.data.level == "top" && node.data.category == "seqblock"){
                    current_net = node.data.text;
                }

                let nodemap = new Map();
                for(let i = 0; i < diagram.model.nodeDataArray.length; ++i){
                    let val = diagram.model.nodeDataArray[i];
                    nodemap.set(val.key,val);
                }


                e.subject.each(function(node){
                    if(node && node.data.hasOwnProperty("from") && node.data.hasOwnProperty("to")){// links

                    }else if(node) {
                        if(node.data.isGroup == true){
                            node.data.info = BlockNode.subfactory(node.data.text,node.data.text);
                        }
                        else{
                            let subtype = null;

                            if(node.data.hasOwnProperty("subtype"))
                                subtype = node.data["subtype"];
                            node.data.info = LayerNode.subfactory(node.data.category,node.data.category,subtype);
                            if(node.data.info.hasOwnProperty("subtype")){
                                subtype = node.data.info["subtype"];
                                Object.assign(node.data.info, node.data.params);
                                if(node.data.info.subtype == 'Input'){
                                    // node.data.info.in_features = "3," + $("#dataset_val_inputsize").val()+","+$("#dataset_val_inputsize").val();
                                    node.data.info.in_features = "3, 64, 64";
                                }
                                else if(node.data.info.subtype == 'Output'){
                                    // node.data.info.out_features = $("#dataset_class_num").val();
                                    node.data.info.out_features = "10";
                                }
                                diagram.model.setDataProperty(node.data, 'text', node.data.info.gettext());

                                //diagram.model.setDataProperty(node.data, 'key', node.data.info.id);
                                diagram.model.setDataProperty(node.data, 'id', node.data.info.id);
                                diagram.model.setDataProperty(node.data, 'outshape', "");
                            }
                            //nodearr.push(node.data.key);
                        }
                    }
                });
            }
            else{


                node.data.info = LayerNode.subfactory(node.data.category,node.data.category,node.data.subtype);
                if(node.data.info.subtype == 'Input'){
                    // node.data.info.in_features = "3," + $("#dataset_val_inputsize").val()+","+$("#dataset_val_inputsize").val();
                    node.data.info.in_features = "3,64,64";
                }
                else if(node.data.info.subtype == 'Output'){
                    // node.data.info.out_features = $("#dataset_class_num").val();
                    node.data.info.out_features = "10";
                }

                diagram.model.setDataProperty(node.data, 'text', node.data.info.gettext());

                //diagram.model.setDataProperty(node.data, 'key', node.data.info.id);
                diagram.model.setDataProperty(node.data, 'id', node.data.info.id);
                diagram.model.setDataProperty(node.data, 'outshape', "");
                //nodearr.push(node.data.key);
            }
        }
    });
    /*diagram.addDiagramListener('ClipboardPasted', function(e) {
        e.subject.each(function(node){
            if(node.type.name == "Spot"){
                if(node && -1 == nodearr.indexOf(node.data.key)) {
                    if(node.data.isGroup == true){

                    }
                    else{
                        node.data.info = LayerNode.subfactory(node.data.category,node.data.category,node.data.subtype);
                        model.setDataProperty(node.data, 'text', node.data.info.gettext());
                        //model.setDataProperty(node.data, 'key', node.data.info.id);
                        model.setDataProperty(node.data, 'id', node.data.info.id);
                        nodearr.push(node.data.key);
                    }
                }
            }
        });
    });*/
});


function makePort(name, spot, output, data) {
    return $$(go.Shape, 'Circle', {
        fill: null,
        stroke: null,
        desiredSize: new go.Size(10, 10),
        alignment: spot,
        alignmentFocus: spot,
        portId: name,
        fromSpot: spot,
        toSpot: spot,
        fromLinkable: output,
        toLinkable: data,
        cursor: 'pointer'
    });

}

function showSmallPorts(node, show) {
    node.ports.each(function(port) {
        if (port.portId !== "") {
            port.fill = show ? "rgba(0,0,0,.3)" : null;
        }
    });
}

function prenodeClick(e,node){

    let infos = node.data.key.split("_");
    let prenet = infos[0];
    selnode = node;
    let html = "";
    let data = node.data;
    let info = data.info;
    let category = data.category;

    if(prenodeParams[prenet].hasOwnProperty(category)){
        let param = prenodeParams[prenet][category];

        html += '<div class="form-horizontal" key="'+category +'">';
        for(var index in param){
            html += '<div class="form-group">';
            html += '<label class="col-sm-4 control-label">' + index + '</label>';
            html += '<div class="col-sm-8">';
            if(['number','string','listnumber','float'].includes(param[index].type)){
                let value = '';
                if(info && typeof(info[index]) != 'undefined' && (index in info))
                    value = info[index];
                if(value == '' && param[index].hasOwnProperty('default')){//set default value
                    value = param[index].default;
                }
                html += '<input type="text" class="form-control prenodeproperty" value = "' +
                value + '" placeholder="' + index + '" property="' + index + '">';
            }
            else if(['list','bool'].includes(param[index].type)){
                let value = '';
                if(info && typeof(info[index]) != 'undefined' && (index in info))
                    value = info[index];
                let sel = '<select class="form-control prenodeproperty" property="' + index +'">';
                for(let i in param[index].options){
                    if(value == param[index].options[i])
                    sel += '<option value="' + param[index].options[i] + '" selected>' + param[index].options[i] + '</option>';
                    else
                    sel += '<option value="' + param[index].options[i] + '">' + param[index].options[i] + '</option>';
                }
                sel += '</select>';
                html += sel;

            }
            html += '</div>';
            html += '</div>';

        }

        html += "</div>";

        $("#property_div").html(html);
        $("#property_div").fadeIn(500);
        $(".toolbar-div").css("right","260px");

        $("input.prenodeproperty").blur(function(){
            selnode.data.info[$(this).attr("property")] = $(this).val();
            savemodel();
        });
    }


}

function nodeClick(e,node){

    selnode = node;
    let html = "";
    // console.log(node.data);
    let data = node.data.info;

    // console.log(data);
    let type = data._type;
    let subtype = data.subtype;
    let param = nodeParams[subtype];


    html += '';
    html += '<div class="form-horizontal" key="'+data.text +'">';
    html += '<div class="form-group"><label class="col-sm-4 control-label">subtype</label><div class="col-sm-8">';
    html += '<select class="form-control subtype">';

    for(index in nodeEnum[type].subtype){
        let optdata = nodeEnum[type].subtype[index];
        if(optdata == subtype)
        html += '<option value="'+ optdata +'" selected>' + optdata + '</option>';
        else
        html += '<option value="'+ optdata +'">' + optdata + '</option>';
    }
    html += '</select></div></div>';
    html += '<div class="form-group"><label class="col-sm-4 control-label">name</label><div class="col-sm-8">';

    html += '<input type="text" class="form-control nodename"  id="nodename" value = "' + subtype + "_" + node.data.id + '" disabled>';
    html += '</div></div>';

    for(var index in param){
        html += '<div class="form-group">';
        html += '<label class="col-sm-4 control-label">' + index + '</label>';
        html += '<div class="col-sm-8">';
        if(['number','string','listnumber'].includes(param[index].type)){
            let value = '';
            if(typeof(data[index]) != 'undefined' && (index in data))
                value = data[index];
            html += '<input type="text" class="form-control nodeproperty" value = "' +
            value + '" placeholder="' + index + '" property="' + index + '">';
        }
        else if(['list','bool'].includes(param[index].type)){
            let value = '';
            if(typeof(data[index]) != 'undefined' && (index in data))
                value = data[index];
            let sel = '<select class="form-control nodeproperty" property="' + index +'">';
            for(let i in param[index].options){
                if(value == param[index].options[i])
                sel += '<option value="' + param[index].options[i] + '" selected>' + param[index].options[i] + '</option>';
                else
                sel += '<option value="' + param[index].options[i] + '">' + param[index].options[i] + '</option>';
            }
            sel += '</select>';
            html += sel;

        }
        html += '</div>';
        html += '</div>';

    }

    html +='</div>';
    $("#property_div").html(html);
    $("#property_div").fadeIn(500);
    $(".toolbar-div").css("right","260px");


    $("select.nodeproperty").change(function(){
        let key = $(this).attr("property");
        if(key in selnode.data.info){
            selnode.data.info[$(this).attr("property")] = $(this).val();
        }
    });
    $("select.subtype").change(function(){
        let ret = selnode.data.info.updatesubtype($(this).val());
        if(ret){
            diagram.startTransaction('');
            diagram.model.setDataProperty(selnode.data,"text",$(this).val()+"_"+selnode.data.info._id);
            diagram.commitTransaction('');
            nodeClick(e,node);

        }
    });
    $("input.nodeproperty").blur(function(){

        if($(this).attr("property") in selnode.data.info){
            selnode.data.info[$(this).attr("property")] = $(this).val();
            validateprocess(diagram.model.nodeDataArray,diagram.model.linkDataArray,current_net);
            savemodel();
        }

    });

}

function groupClick(e,node){
    selgroup = node;
    let html = "";
    let data = node.data.info;
    // console.log(selgroup.data);
    if(selgroup.data.level != "top"){
        let type = selgroup.data.text;
        let param = blockEnum[type];
        html += '<br/><br/><div class="form-horizontal" key="' + selgroup.data.text + '">';
        for(let index in param){
            html += '<div class="form-group">';
            html += '<label class="col-sm-4 control-label">' + index + '</label>';
            html += '<div class="col-sm-8">';
            if(['number','string','listnumber'].includes(param[index].type)){
                let value = '';
                if(typeof(data[index]) != 'undefined' && (index in data))
                    value = data[index];
                html += '<input type="text" class="form-control groupproperty" value = "' +
                value + '" placeholder="' + index + '" property="' + index + '">';
            }
            html += '</div>';
            html += '</div>';
        }
        html +='</div>';
        $("#property_div").html(html);
        $("#property_div").fadeIn(500);
        $(".toolbar-div").css("right","260px");
        $("input.groupproperty").blur(function(){
          data[$(this).attr("property")] = $(this).val();
          validateprocess(diagram.model.nodeDataArray,diagram.model.linkDataArray,current_net);
          savemodel();
        });

    }


}

/**
 * 寻找孤立点
 * @param {节点} nodemap
 * @param {连线} links
 */
function findisolated(nodemap, links){
    let linkednode = new Map();

    //找到入口 rootnode
    for(let [key,val] of nodemap.entries()){
        if(val.input_degree == 0){
            linkednode.set(key,val);
            break;
        }
    }

    if(linkednode.size == 1){
        let start_num = 0;
        while(start_num < linkednode.size){
            start_num = linkednode.size;
            for(let index in links){
                if(linkednode.has(links[index].from)
                    && !linkednode.has(links[index].to)
                    && nodemap.has(links[index].to)){
                        linkednode.set(links[index].to,nodemap.get(links[index].to));
                }

                if(linkednode.has(links[index].to)
                    && !linkednode.has(links[index].from)
                    && nodemap.has(links[index].from)){
                        linkednode.set(links[index].from,nodemap.get(links[index].from));
                }
            }
        }

        if(linkednode.size == nodemap.size){
            return {code:200};
        }

    }
    else{
        return {code:-1,msg:'缺少起点'};

    }

    return {code:-2,msg:'存在孤立点'};;
}

/**
 * 寻找环
 * @param {节点} nodemap
 * @param {连接线} links
 */
function findloop(nodemap, links){
    let nodes = new Array();
    let nodecount = 0;
    for(let [key,val] of nodemap.entries()){
        if(val.input_degree == 0){
            nodes.push(key);
            ++nodecount;
        }
    }

    while(nodes.length > 0){
        let node = nodes.pop();
        for(let index in links){
            let link = links[index];
            if(link.from == node && nodemap.has(link.to)){
                let node = nodemap.get(link.to);
                node.input_degree -= 1;
                if(node.input_degree == 0){
                    nodes.push(link.to);
                    ++nodecount;
                }
            }
        }
    }
    if(nodecount == nodemap.size)
        return {code:200};
    return {code:-1,msg:'存在环'};

}

/**
 * 无环有向图连通性验证
 * @param {节点} nodes
 * @param {连线} links
 */
function linkvalidate(nodes,links){
    let nodemap = new Map();
    let remainmap = new Map();

    for(let index in nodes){
        if(!nodes[index].isGroup){
            let node = {};
            node.key = nodes[index].key;
            node.input_degree = 0;
            node.output_degree = 0;
            nodemap.set(node.key,node);
            remainmap.set(nodes[index].key,nodes[index].info);
        }
    }
    for(let index in links){

        if(!links[index].hasOwnProperty('from') || !links[index].hasOwnProperty('to') || typeof(links[index].from) == 'undefined' || typeof(links[index].to) == 'undefined' ){
            return {code:-3,msg:'连线信息不完整'};
        }
        if(nodemap.has(links[index].from)){
            let node = nodemap.get(links[index].from);
            node.output_degree += 1;
        }
        if(nodemap.has(links[index].to)){
            let node = nodemap.get(links[index].to);
            node.input_degree += 1;
        }
    }

    //验证是否存在孤立点
    let ret = findisolated(nodemap,links);
    if(ret.code != 200){
        return ret;
    }

    ret = findloop(nodemap,links)
    if(ret.code != 200)
        return ret;

    return {code:200};
}

/**
 * 验证节点信息是否完整
 * @param {节点} nodes
 */
function validateNodeproperty(nodes){
    let hasinput = false;
    let hasoutput = false;
    for(let index in nodes){
        if(!nodes[index].isGroup){
            let node = nodes[index].info;
            let ret = node.validateRequired();
            if(ret.code != 200){
                return ret;
            }
            if(node._type == 'Input')
              hasinput = true;
            if(node._type == 'Output')
              hasoutput = true;
        }
    }
    if(!hasinput){
      return {code:-3,msg:'缺少输入节点'};
    }
    if(!hasoutput)
      return {code:-4,msg:'缺少输出节点'};
    return {code:200};
}


function validate_input(w,h){
    // let trainsize = tolist($("#dataset_train_inputsize").val());
    // let valsize = tolist($("#dataset_val_inputsize").val());
    // let testsize = tolist($("#dataset_test_inputsize").val());

    // if((trainsize.length != 1 && trainsize.length != 2) || (valsize.length != 1 && valsize.length != 2)
    //     ||(testsize.length != 1 && testsize.length != 2))
    //     return false;

    // if(w != trainsize[0] || h != trainsize[trainsize.length - 1] || w != valsize[0] || h != valsize[valsize.length - 1] || w != testsize[0] || h != testsize[testsize.length - 1])
    //     return false;

    return true;
}

/**
*Shape验证
*/
function validateShape(nodes,links){
  let nodemap = new Map();
  let start_node = null;
  for(let [key, val] of nodes.entries()){
    nodemap.set(val.key,val);
    diagram.model.setDataProperty(val, 'outshape', '');
    if(val.info._type == 'Input')
      start_node = val;
  }
  if(start_node == null)
    return {code:-3,msg:'缺少输入节点'};


  let ret = sortNode(nodes,links);


  if(ret.code != 200)
    return ret;
  let seqnodes = new Array();
  for(let [key, val] of ret.seqnodes.entries()){
    seqnodes.unshift(val);
  }

  let start_infos = start_node.info.in_features.split(",");
  if(start_infos.length != 3)
    return {code:-6,msg:'Input参数错误'};
  var channel = start_infos[0];
  var w = start_infos[1];
  var h = start_infos[2];

  if(!validate_input(w,h))
    return {code:-3,msg:'数据集参数设置与Input设置不匹配'};



  start_node.info.out_shapes = {w:w,h:h,channel:channel};
  //console.log(nodemap);

  for(let index = 0; index < seqnodes.length; ++index){
    let after_compute = seqnodes[index].info.computeShape(seqnodes);

    if(after_compute.code != 200)
      return after_compute;
    else{
      channel = after_compute.channel;
      w = after_compute.w;
      h = after_compute.h;
      let shape = '(32';  // batch_size
      if(channel != null)
        shape += `,${channel}`;
      if(w != null)
        shape += `,${w}`;
      if(h != null)
        shape += `,${h}`;
      shape += ')';

      diagram.model.setDataProperty(nodemap.get(seqnodes[index].key), 'outshape', shape);
    }
  }
  return {code:200};
}

/**
 * 计算Shape
 * @param {节点} nodes
 */
function computeShape(nodes){
    for(let [key,val] of nodes.entries()){
        let ret = val.info.computeShape(227,227);
        if(ret.code != 200){
            //alert(ret.msg);
            break;
        }
    }
}

/**
 * 设计图正确性验证
 * @param {*} nodes
 * @param {*} links
 * @param {*} nettype
 */
function validate(nodes,links,nettype){


    let result = linkvalidate(nodes,links);

    if(result.code != 200)
        return result;



    result = validateShape(nodes,links);
    if(result.code != 200)
        return result;


    result = validateNodeproperty(nodes);
    if(result.code != 200)
        return result;


    return {code:200};
}

function validateprocess(nodes,links,nettype){
    if($("#hproject_type").val() == 'det' || $("#hproject_type").val() == 'seg')
        return true;

    if(project_model != 'custom')
        return true;
    if(nodes.length == 0)
        return true;

    let ret = validate(nodes,links,nettype);
    if(ret.code != 200){
      $("#alert_msg").html(ret.msg);
      $("#alert_msg").parent().fadeIn();
      setTimeout('$("#alert_msg").parent().fadeOut()',5000);
      return false;
    }
    return true;
}

/**
*拓扑排序
*/
function sortNode(nodes,links){

    let seqnodes = new Map();
    let remainnodes = new Map();
    let seqlinks = new Map();
    let groups = new Map();



    for(let index in nodes){
        if(nodes[index].isGroup){
            groups.set(nodes[index].key,nodes[index]);
            continue;
        }
        seqnodes.set(nodes[index].key,nodes[index]);
        nodes[index].info.inputs = [];
        nodes[index].info.outputs = [];
        nodes[index].info.group = nodes[index].group;
    }

    for(let index in links){
        if(!remainnodes.has(links[index].from)){
            if(seqnodes.has(links[index].from)){
                remainnodes.set(links[index].from,seqnodes.get(links[index].from));
                seqnodes.delete(links[index].from);
            }
        }
    }


    if(seqnodes.size == 0){
        return {code:-5,msg:'顺序错误'};
    }

    for(let index in links){
        seqlinks.set(index,links[index]);
    }


    while(remainnodes.size > 0 && seqlinks.size > 0 ){

        for(let [nodekey,nodeval] of seqnodes.entries()){
            for(let [linkkey,linkval] of seqlinks.entries()){
                if(linkval.to == nodekey){
                    if(remainnodes.has(linkval.from)){
                        remainnodes.get(linkval.from).info.inputs = [];
                        if(!remainnodes.get(linkval.from).info.hasOwnProperty("outputs"))
                            remainnodes.get(linkval.from).info.outputs = [];
                        remainnodes.get(linkval.from).info.outputs.push(nodeval.info.gettext());

                        nodeval.info.inputs.push(remainnodes.get(linkval.from).info.gettext());
                        seqlinks.delete(linkkey);

                        let hasFrom = false;
                        for(let [lkey,lval] of seqlinks.entries()){
                            if(lval.from == linkval.from){
                                hasFrom = true;
                                break;
                            }
                        }

                        if(!hasFrom){
                            seqnodes.set(linkval.from,remainnodes.get(linkval.from));
                            remainnodes.delete(linkval.from);
                        }



                    }
                }
            }

        }

    }



    while(seqlinks.size > 0){

        for(let [linkkey,linkval] of seqlinks.entries()){

            if(!linkval.hasOwnProperty("from") || !linkval.hasOwnProperty("to") || typeof(linkval.from) == 'undefined' || typeof(linkval.to) == 'undefined'){
                return {code:-9,msg:'存在未连接的线'};
            }
            if(seqnodes.has(linkval.from) && seqnodes.has(linkval.to)){
                seqnodes.get(linkval.from).info.outputs.push(seqnodes.get(linkval.to).info.gettext());
                seqnodes.get(linkval.to).info.inputs.push(seqnodes.get(linkval.from).info.gettext());
                seqlinks.delete(linkkey);
            }
        }


    }

    return {code:200,'seqnodes':seqnodes,'remainnodes':remainnodes,'seqlinks':seqlinks,'groups':groups};

}

/**
 * 生成proto格式字符串
 * @param {*} nodes
 * @param {*} links
 */
function toPrototxt(nodes,links,nettype,netname){
    let groups = new Map();

    for(let index in nodes){
        if(nodes[index].isGroup == true)
            groups.set(nodes[index].val,nodes[index]);

    }

    let ret = sortNode(nodes,links);
    if(ret.code != 200) {
        return ret;
    }
    let seqnodes = new Array();
    for(let [key, val] of ret.seqnodes.entries()){
        seqnodes.push(val);
    }


    //computeShape(seqnodes);

    let result = {};
    result.datastr = "";

    if(nettype == "plain_net" || nettype == "custom") {
        for (let [ index, val ] of seqnodes.entries()){
            val = val.info;

            if(val._type == 'Input' || val._type == 'Output')
                continue;
            result.datastr = '\n' + val.toProtoStr() + result.datastr;
        }
        result.datastr = `plain_net {\n name: "${netname}"\n${result.datastr}\n}`;
    }
    else{
        var before_net = '';
        var block_net = ' ';
        var after_net = '';
        let block_flag = 1;
        let first_group = "";
        let block_param = "";
        for(let [index, val] of seqnodes.entries()){
            val = val.info;

            if(val._type == 'Input' || val._type == 'Output')
                continue;

            if(val.isGroup == true){
                groups.set(val.key,val);
            }

            if(first_group == "")
                first_group = val.group;
            if(val.group != first_group){
                block_flag += 1;
                first_group = val.group;
            }

            switch(block_flag){
                case 1: after_net = "\n" + val.toProtoStr() + after_net ;break;
                case 2: block_net = "\n" +val.toProtoStr() + block_net;break;
                case 3: before_net = "\n" + val.toProtoStr() + before_net;break;
                default:break;
            }

        }


        let block_mode = "";

        for(let [index, val] of groups.entries()){

            if(val.level != "top"){
                for(let key in val.info){
                    if(key.startsWith("_")){

                        if(key == "_type")
                            block_mode = val.info[key].toUpperCase();
                        continue;
                    }

                    let values = val.info[key].split(",");
                    values.forEach(function(str){
                        block_param += `  ${key}:${str}\n`;
                    });

                }
                break;
            }
        }
        block_param += `  num_classes:${curdataset["num_classes"]}`;

        before_net = 'seq_net {\n name : "before_block"' + before_net +"}";

        block_net ='block {\n  name : "res1"\nblock_mode : '+ block_mode + block_net + "}";
        if(nettype.startsWith("resNet"))
            nettype = "resNet";
        after_net = 'seq_net {\n name : "after_block"' + after_net + "}";
        block_param = 'net_params{\n' + block_param + "}";
        result.datastr = `block_wise_net {\nname: "${netname}"\nnet_mode :${nettype.toUpperCase()}\n${before_net}\n${block_net}\n${after_net}\n${block_param}\n}`;

    }
    // console.log(result.datastr);
    return result;
}

function savemodel(){
  diagram.model.modelData.position = go.Point.stringify(diagram.position);
  var gojsData = ""
  // gojsData = diagram.model.toJson();
  // console.log(gojsData);
  return
  $.ajax({
      type: "POST",
      url: "http://116.85.5.40:10061/nettype/getnettype",
      data: {"id":$("#project_id").val(),"data":diagram.model.toJson(),"column":"model","net_type":current_net},
      dataType: "json",
      success: function(json){
        if(json.result == 200){
          //goTab('main_model');
        }else{
          alert(json.resDesc);
        }
      }
  });
}



function FixedLink(){
    go.Link.call(this);
    //console.log(this);
}

go.Diagram.inherit(FixedLink, go.Link);





