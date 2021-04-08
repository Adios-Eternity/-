

    //创建地图
    var map = new AMap.Map('container', {
        zoom: 16,
        center: [114.508025,38.849796],
        resizeEnable: true

    });



    new AMap.DistrictSearch({
        extensions: 'all',
        subdistrict: 0
    }).search('立彦头村', function (status, result) {
        // 外多边形坐标数组和内多边形坐标数组


        var polygon = new AMap.Polygon({
            pathL: pathArray,
            //线条颜色，使用16进制颜色代码赋值。默认值为#006600
            strokeColor: 'rgb(20,164,173)',
            strokeWeight: 4,
            //轮廓线透明度，取值范围[0,1]，0表示完全透明，1表示不透明。默认为0.9
            strokeOpacity: 0,
            //多边形填充颜色，使用16进制颜色代码赋值，如：#FFAA00
            fillColor: '#FFFFFF',
            //多边形填充透明度，取值范围[0,1]，0表示完全透明，1表示不透明。默认为0.9
            fillOpacity: 0.3,
            //轮廓线样式，实线:solid，虚线:dashed
            strokeStyle: 'dashed',
            /*勾勒形状轮廓的虚线和间隙的样式，此属性在strokeStyle 为dashed 时有效， 此属性在    
              ie9+浏览器有效 取值： 
              实线：[0,0,0] 
              虚线：[10,10] ，[10,10] 表示10个像素的实线和10个像素的空白（如此反复）组成的虚线
              点画线：[10,2,10]， [10,2,10] 表示10个像素的实线和2个像素的空白 + 10个像素的实 
              线和10个像素的空白 （如此反复）组成的虚线*/
            strokeDasharray: [10, 2, 10]
        });
        polygon.setPath(pathArray);
        map.add(polygon);
    })

    AMapUI.load(['ui/geo/DistrictExplorer', 'lib/$'], function (DistrictExplorer, $) {

        //创建一个实例
        var districtExplorer = window.districtExplorer = new DistrictExplorer({
            eventSupport: true, //打开事件支持
            map: map,
            bubble: true
        });

        //当前聚焦的区域
        var currentAreaNode = null;

        //鼠标hover提示内容
        var $tipMarkerContent = $('<div class="tipMarker top"></div>');

        var tipMarker = new AMap.Marker({
            content: $tipMarkerContent.get(0),
            offset: new AMap.Pixel(0, 0),
            bubble: true
        });

        //根据Hover状态设置相关样式
        function toggleHoverFeature(feature, isHover, position) {

            tipMarker.setMap(isHover ? map : null);

            if (!feature) {
                return;
            }

            var props = feature.properties;

            if (isHover) {

                //更新提示内容
                $tipMarkerContent.html(props.name);
                // $tipMarkerContent.html(props.adcode + ': ' + props.name);
                //更新位置
                tipMarker.setPosition(position || props.center);
            }

            $('#area-tree').find('h2[data-adcode="' + props.adcode + '"]').toggleClass('hover', isHover);

            //更新相关多边形的样式
            var polys = districtExplorer.findFeaturePolygonsByAdcode(props.adcode);
            for (var i = 0, len = polys.length; i < len; i++) {

                polys[i].setOptions({
                    fillOpacity: isHover ? 0.2 : 0.7
                });
            }
        }

        //监听feature的hover事件

        //监听鼠标在feature上滑动
        // districtExplorer.on('featureMousemove', function (e, feature) {
        //     //更新提示位置
        //     tipMarker.setPosition(e.originalEvent.lnglat);
        // });


        //feature被点击


        //外部区域被点击

        //绘制区域面板的节点
        function renderAreaPanelNode(ele, props, color) {

            var $box = $('<li/>').addClass('lv_' + props.level);

            var $h2 = $('<h2/>').addClass('lv_' + props.level).attr({
                'data-adcode': props.adcode,
                'data-level': props.level,
                'data-children-num': props.childrenNum || void (0),
                'data-center': props.center.join(',')
            }).html(props.name).appendTo($box);

            if (color) {
                $h2.css('borderColor', color);
            }

            //如果存在子节点
            if (props.childrenNum > 0) {

                //显示隐藏
                $('<div class="showHideBtn"></div>').appendTo($box);

                //子区域列表
                $('<ul/>').addClass('sublist lv_' + props.level).appendTo($box);

                $('<div class="clear"></div>').appendTo($box);

                if (props.level !== 'country') {
                    $box.addClass('hide-sub');
                }
            }

            $box.appendTo(ele);
        }


        //填充某个节点的子区域列表
        function renderAreaPanel(areaNode) {

            var props = areaNode.getProps();

            var $subBox = $('#area-tree').find('h2[data-adcode="' + props.adcode + '"]').siblings('ul.sublist');

            if (!$subBox.length && props.childrenNum) {
                //父节点不存在，先创建
                renderAreaPanelNode($('#area-tree'), props);
                $subBox = $('#area-tree').find('ul.sublist');
            }
            if ($subBox.attr('data-loaded') === 'rendered') {
                return;
            }

            $subBox.attr('data-loaded', 'rendered');

            var subFeatures = areaNode.getSubFeatures();

            //填充子区域
            for (var i = 0, len = subFeatures.length; i < len; i++) {
                renderAreaPanelNode($subBox, areaNode.getPropsOfFeature(subFeatures[i]), colors[i % colors.length]);
            }
        }

        //绘制某个区域的边界
        function renderAreaPolygons(areaNode) {
            //更新地图视野
            map.setBounds(areaNode.getBounds(), null, null, true);

            //清除已有的绘制内容
            districtExplorer.clearFeaturePolygons();

            //绘制子区域
            districtExplorer.renderSubFeatures(areaNode, function (feature, i) {

                var fillColor = colors[i % colors.length];
                var strokeColor = colors[colors.length - 1 - i % colors.length];

                return {
                    cursor: 'default',
                    bubble: true,
                    strokeColor: strokeColor, //线颜色
                    strokeOpacity: 1, //线透明度
                    strokeWeight: 1, //线宽
                    fillColor: fillColor, //填充色
                    fillOpacity: 0.35, //填充透明度
                };
            });

            //绘制父区域
            districtExplorer.renderParentFeature(areaNode, {
                cursor: 'default',
                bubble: true,
                strokeColor: 'black', //线颜色
                strokeOpacity: 1, //线透明度
                strokeWeight: 2, //线宽
                fillColor: areaNode.getSubFeatures().length ? null : colors[0], //填充色
                fillOpacity: 0.35, //填充透明度
            });
        }

        //切换区域后刷新显示内容

        //切换区域

        //加载区域
        function loadAreaNode(adcode, callback) {

            districtExplorer.loadAreaNode(adcode, function (error, areaNode) {

                if (error) {

                    if (callback) {
                        callback(error);
                    }

                    console.error(error);

                    return;
                }

                //renderAreaPanel(areaNode);

                if (callback) {
                    callback(null, areaNode);
                }
            });
        }

        //切换到北京 110000
        //切换到密云 110118
        //switch2AreaNode(130624);
    });


    //marker
    //简单标注 在地图上自定义标注 点击显示弹窗
    AMapUI.defineTpl("ui/overlay/SimpleInfoWindow/tpl/container.html", [], function () {
        return document.getElementById('my-infowin-tpl').innerHTML;
    });


    AMapUI.loadUI(['overlay/SimpleInfoWindow'], function (SimpleInfoWindow) {

        var marker = new AMap.Marker({
            map: map,
            zIndex: 9999999,
            position: [114.508744, 38.854449],
            icon: new AMap.Icon({
                image: '../static/img/单轨车.png',
                size: new AMap.Size(100, 100),
                imageSize: new AMap.Size(35,35)
            })
            // position: map.getCenter()
        });

        var infoWindow = new SimpleInfoWindow({
            title: '单轨车数据',
            sn_name: '编号',
            sn: '110101',
            status_name: '状态',
            status: '良好',
            location_name: '地理位置',
            location: '[114.508744, 38.854449]',
            img_number: '终端节点类型',
            count: '单轨车',
            date_name: '',
            date: '',
            //基点指向marker的头部位置
            offset: new AMap.Pixel(0, -31)
        });

        function openInfoWin() {
            infoWindow.open(map, marker.getPosition());
        }

        //marker 点击时打开
        marker.on('click', function () {
            openInfoWin();
        });
    });

    AMapUI.loadUI(['overlay/SimpleInfoWindow'], function (SimpleInfoWindow) {

        var marker = new AMap.Marker({
            map: map,
            zIndex: 9999999,
            position: [114.507253,38.853639],
            icon: new AMap.Icon({
                image: '../static/img/单轨车.png',
                size: new AMap.Size(100, 100),
                imageSize: new AMap.Size(35,35)
            })
            // position: map.getCenter()
        });

        var infoWindow = new SimpleInfoWindow({
            title: '单轨车数据',
            sn_name: '编号',
            sn: '003',
            status_name: '状态',
            status: '良好',
            location_name: '地理位置',
            location: '[114.507253,38.853639]',
            img_number: '终端节点类型',
            count: '单轨车',
            date_name: '',
            date: '',
            //基点指向marker的头部位置
            offset: new AMap.Pixel(0, -31)
        });

        function openInfoWin() {
            infoWindow.open(map, marker.getPosition());
        }

        //marker 点击时打开
        marker.on('click', function () {
            openInfoWin();
        });
    });

    AMapUI.loadUI(['overlay/SimpleInfoWindow'], function (SimpleInfoWindow) {

        var marker = new AMap.Marker({
            map: map,
            zIndex: 9999999,
            position: [114.510342,38.853697],
            icon: new AMap.Icon({
                image: '../static/img/节点.png',
                size: new AMap.Size(100, 100),
                imageSize: new AMap.Size(35,35)
            })
            // position: map.getCenter()
        });

        var infoWindow = new SimpleInfoWindow({
            title: '静态终端节点',
            sn_name: '编号',
            sn: '003',
            status_name: '状态',
            status: '良好',
            location_name: '空气温湿度',
            location: '[温度,湿度]',
            img_number: '土壤温湿度',
            count: '[土壤温度，土壤湿度]',
            date_name: '二氧化碳浓度',
            date: '[]',
            //基点指向marker的头部位置
            offset: new AMap.Pixel(0, -31)
        });

        function openInfoWin() {
            infoWindow.open(map, marker.getPosition());
        }

        //marker 点击时打开
        marker.on('click', function () {
            openInfoWin();
        });
    });

    AMapUI.loadUI(['overlay/SimpleInfoWindow'], function (SimpleInfoWindow) {

        var marker = new AMap.Marker({
            map: map,
            zIndex: 9999999,
            position: [114.508701,38.850915],
            icon: new AMap.Icon({
                image: '../static/img/节点.png',
                size: new AMap.Size(100, 100),
                imageSize: new AMap.Size(35,35)
            })
            // position: map.getCenter()
        });

        var infoWindow = new SimpleInfoWindow({
            title: '静态终端节点',
            sn_name: '编号',
            sn: '003',
            status_name: '状态',
            status: '良好',
            location_name: '空气温湿度',
            location: '[温度,湿度]',
            img_number: '土壤温湿度',
            count: '[土壤温度，土壤湿度]',
            date_name: '二氧化碳浓度',
            date: '[]',
            //基点指向marker的头部位置
            offset: new AMap.Pixel(0, -31)
        });

        function openInfoWin() {
            infoWindow.open(map, marker.getPosition());
        }

        //marker 点击时打开
        marker.on('click', function () {
            openInfoWin();
        });
    });

    AMapUI.loadUI(['overlay/SimpleInfoWindow'], function (SimpleInfoWindow) {

        var marker = new AMap.Marker({
            map: map,
            zIndex: 9999999,
            position: [114.509581,38.851818],
            icon: new AMap.Icon({
                image: '../static/img/节点.png',
                size: new AMap.Size(100, 100),
                imageSize: new AMap.Size(35,35)
            })
            // position: map.getCenter()
        });

        var infoWindow = new SimpleInfoWindow({
            title: '静态终端节点',
            sn_name: '编号',
            sn: '003',
            status_name: '状态',
            status: '良好',
            location_name: '空气温湿度',
            location: '[温度,湿度]',
            img_number: '土壤温湿度',
            count: '[土壤温度，土壤湿度]',
            date_name: '二氧化碳浓度',
            date: '[]',
            //基点指向marker的头部位置
            offset: new AMap.Pixel(0, -31)
        });

        function openInfoWin() {
            infoWindow.open(map, marker.getPosition());
        }

        //marker 点击时打开
        marker.on('click', function () {
            openInfoWin();
        });
    });

    AMapUI.loadUI(['overlay/SimpleInfoWindow'], function (SimpleInfoWindow) {

        var marker = new AMap.Marker({
            map: map,
            zIndex: 9999999,
            position: [114.512821,38.85277],
            icon: new AMap.Icon({
                image: '../static/img/节点.png',
                size: new AMap.Size(100, 100),
                imageSize: new AMap.Size(35,35)
            })
            // position: map.getCenter()
        });

        var infoWindow = new SimpleInfoWindow({
            title: '静态终端节点',
            sn_name: '编号',
            sn: '003',
            status_name: '状态',
            status: '良好',
            location_name: '空气温湿度',
            location: '[温度,湿度]',
            img_number: '土壤温湿度',
            count: '[土壤温度，土壤湿度]',
            date_name: '二氧化碳浓度',
            date: '[]',
            //基点指向marker的头部位置
            offset: new AMap.Pixel(0, -31)
        });

        function openInfoWin() {
            infoWindow.open(map, marker.getPosition());
        }

        //marker 点击时打开
        marker.on('click', function () {
            openInfoWin();
        });
    });

    AMapUI.loadUI(['overlay/SimpleInfoWindow'], function (SimpleInfoWindow) {

        var marker = new AMap.Marker({
            map: map,
            zIndex: 9999999,
            position: [114.508358, 38.852511],
            icon: new AMap.Icon({
                image: '../static/img/施药机.png',
                size: new AMap.Size(100, 100),
                imageSize: new AMap.Size(35,35)
            })
            // position: map.getCenter()
        });

        var infoWindow = new SimpleInfoWindow({
            title: '施药机数据',
            sn_name: '编号',
            sn: '004',
            status_name: '状况',
            status: '良好',
            location_name: '地理位置',
            location: '[114.508358, 38.852511]',
            img_number: '终端节点类型',
            count: '施药机',
            date_name: '',
            date: '',
            //基点指向marker的头部位置
            offset: new AMap.Pixel(0, -31)
        });

        function openInfoWin() {
            infoWindow.open(map, marker.getPosition());
        }

        //marker 点击时打开
        marker.on('click', function () {
            openInfoWin();
        });
    });


    AMapUI.loadUI(['overlay/SimpleInfoWindow'], function (SimpleInfoWindow) {

        var marker = new AMap.Marker({
            map: map,
            zIndex: 9999999,
            position: [114.511426, 38.851859],
            icon: new AMap.Icon({
                image: '../static/img/灌溉阀.png',
                size: new AMap.Size(100, 100),
                imageSize: new AMap.Size(35,35)
            })

        });

        var infoWindow = new SimpleInfoWindow({
            title: '灌溉阀',
            sn_name: '编号',
            sn: '110128',
            status_name: '状态',
            status: '良好',
            location_name: '地理位置',
            location: '[114.511426,38.851859]',
            img_number: '终端节点类型',
            count: '灌溉阀',
            date_name: 'Q',
            date: '[]',

            //基点指向marker的头部位置
            offset: new AMap.Pixel(0, -31)
        });

        function openInfoWin() {
            infoWindow.open(map, marker.getPosition());
        }

        //marker 点击时打开
        marker.on('click', function () {
            openInfoWin();
        });

    });




   