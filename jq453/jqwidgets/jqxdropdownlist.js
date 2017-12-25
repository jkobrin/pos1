/*
jQWidgets v4.5.3 (2017-June)
Copyright (c) 2011-2017 jQWidgets.
License: http://jqwidgets.com/license/
*/
!function(a){a.jqx.jqxWidget("jqxDropDownList","",{}),a.extend(a.jqx._jqxDropDownList.prototype,{defineInstance:function(){var b={disabled:!1,width:null,height:null,items:new Array,selectedIndex:-1,source:null,scrollBarSize:15,arrowSize:19,enableHover:!0,enableSelection:!0,autoItemsHeight:!1,visualItems:new Array,groups:new Array,equalItemsWidth:!0,itemHeight:-1,visibleItems:new Array,emptyGroupText:"Group",checkboxes:!1,openDelay:250,closeDelay:300,dropDownContainer:"default",animationType:"default",autoOpen:!1,dropDownWidth:"auto",dropDownHeight:"200px",autoDropDownHeight:!1,keyboardSelection:!0,enableBrowserBoundsDetection:!1,dropDownHorizontalAlignment:"left",dropDownVerticalAlignment:"bottom",displayMember:"",valueMember:"",groupMember:"",searchMember:"",searchMode:"startswithignorecase",incrementalSearch:!0,incrementalSearchDelay:700,renderer:null,placeHolder:"Please Choose:",promptText:"Please Choose:",emptyString:"",rtl:!1,selectionRenderer:null,listBox:null,popupZIndex:9999999999999,renderMode:"default",touchMode:"auto",_checkForHiddenParent:!0,autoBind:!0,ready:null,focusable:!0,filterable:!1,filterHeight:27,filterPlaceHolder:"Looking for",filterDelay:100,template:"default",aria:{"aria-disabled":{name:"disabled",type:"boolean"}},events:["open","close","select","unselect","change","checkChange","bindingComplete","itemAdd","itemRemove","itemUpdate"]};return this===a.jqx._jqxDropDownList.prototype?b:(a.extend(!0,this,b),b)},createInstance:function(a){this.render()},render:function(){var b=this;b.width||(b.width=200),b.height||(b.height=25);var c=b.element.nodeName.toLowerCase();if("select"==c||"ul"==c||"ol"==c){b.field=b.element,b.field.className&&(b._className=b.field.className);var d={title:b.field.title};b.field.id.length?d.id=b.field.id.replace(/[^\w]/g,"_")+"_jqxDropDownList":d.id=a.jqx.utilities.createId()+"_jqxDropDownList";var e=a("<div></div>",d);b.width||(b.width=a(b.field).width()),b.height||(b.height=a(b.field).outerHeight()),e[0].style.cssText=b.field.style.cssText,a(b.field).hide().after(e);var f=b.host.data();if(b.host=e,b.host.data(f),b.element=e[0],b.element.id=b.field.id,b.field.id=d.id,b._className&&(b.host.addClass(b._className),a(b.field).removeClass(b._className)),b.field.tabIndex){var g=b.field.tabIndex;b.field.tabIndex=-1,b.element.tabIndex=g}var h=a.jqx.parseSourceTag(b.field);b.source=h.items,-1==b.selectedIndex&&(b.selectedIndex=h.index)}else if(b.host.find("li").length>0||b.host.find("option").length>0){var h=a.jqx.parseSourceTag(that.element);b.source=h.items}b.element.innerHTML="",b.isanimating=!1,b.id=b.element.id||a.jqx.utilities.createId(),b.host.attr("role","combobox"),a.jqx.aria(b,"aria-autocomplete","both"),a.jqx.aria(b,"aria-readonly",!1);var i="<div style='background-color: transparent; -webkit-appearance: none; outline: none; width:100%; height: 100%; padding: 0px; margin: 0px; border: 0px; position: relative;'><div id='dropdownlistWrapper' style='overflow: hidden; outline: none; background-color: transparent; border: none; float: left; width:100%; height: 100%; position: relative;'><div id='dropdownlistContent' unselectable='on' style='outline: none; background-color: transparent; border: none; float: left; position: relative;'></div><div id='dropdownlistArrow' unselectable='on' style='background-color: transparent; border: none; float: right; position: relative;'><div unselectable='on'></div></div></div></div>";if(null==a.jqx._jqxListBox||void 0==a.jqx._jqxListBox)throw new Error("jqxDropDownList: Missing reference to jqxlistbox.js.");b.host.attr("tabindex")||b.host.attr("tabindex",0);b.touch=a.jqx.mobile.isTouchDevice(),b.comboStructure=i,b.element.innerHTML=i,b.dropdownlistWrapper=a(b.element.firstChild.firstChild),b.dropdownlistArrow=a(b.dropdownlistWrapper[0].firstChild.nextSibling),b.arrow=a(b.dropdownlistArrow[0].firstChild),b.dropdownlistContent=a(b.dropdownlistWrapper[0].firstChild),b.dropdownlistContent.addClass(b.toThemeProperty("jqx-dropdownlist-content jqx-disableselect")),b.rtl&&b.dropdownlistContent.addClass(b.toThemeProperty("jqx-rtl jqx-dropdownlist-content-rtl")),b.addHandler(b.dropdownlistWrapper,"selectstart",function(){return!1}),b.dropdownlistWrapper[0].id="dropdownlistWrapper"+b.element.id,b.dropdownlistArrow[0].id="dropdownlistArrow"+b.element.id,b.dropdownlistContent[0].id="dropdownlistContent"+b.element.id,b._addInput(),"Please Choose:"!=b.promptText&&(b.placeHolder=b.promptText);var j=b.toThemeProperty("jqx-widget")+" "+b.toThemeProperty("jqx-dropdownlist-state-normal")+" "+b.toThemeProperty("jqx-rc-all")+" "+b.toThemeProperty("jqx-fill-state-normal");b.element.className+=" "+j,b._firstDiv=a(b.element.firstChild);try{var k="listBox"+b.id,l=a(a.find("#"+k));l.length>0&&l.remove(),a.jqx.aria(b,"aria-owns",k),a.jqx.aria(b,"aria-haspopup",!0);var m=a("<div style='overflow: hidden; background-color: transparent; border: none; position: absolute;' id='listBox"+b.id+"'><div id='innerListBox"+b.id+"'></div></div>");m.hide(),"element"==b.dropDownContainer?m.appendTo(b.host):m.appendTo(document.body),b.container=m,b.listBoxContainer=a(a.find("#innerListBox"+b.id));var n=b.width;"auto"!=b.dropDownWidth&&(n=b.dropDownWidth),null==n&&0==(n=b.host.width())&&(n=b.dropDownWidth),null==b.dropDownHeight&&(b.dropDownHeight=200);b.container.width(parseInt(n)+25),b.container.height(parseInt(b.dropDownHeight)+25),b._ready=!1,b.addHandler(b.listBoxContainer,"bindingComplete",function(c){b.listBox||(b.listBox=a.data(b.listBoxContainer[0],"jqxListBox").instance),b.selectedIndex!=b.listBoxContainer.jqxListBox("selectedIndex")?(b.listBox=a.data(b.listBoxContainer[0],"jqxListBox").instance,b.listBoxContainer.jqxListBox({selectedIndex:b.selectedIndex}),b.renderSelection("mouse")):b.renderSelection("mouse"),b._ready||(b.ready&&b.ready(),b._ready=!0),b._raiseEvent("6")}),b.addHandler(b.listBoxContainer,"itemAdd",function(a){b._raiseEvent("7",a.args)}),b.addHandler(b.listBoxContainer,"itemRemove",function(a){b._raiseEvent("8",a.args)}),b.addHandler(b.listBoxContainer,"itemUpdate",function(a){b._raiseEvent("9",a.args)}),b.listBoxContainer.jqxListBox({filterHeight:b.filterHeight,filterPlaceHolder:b.filterPlaceHolder,filterDelay:b.filterDelay,autoItemsHeight:b.autoItemsHeight,filterable:b.filterable,allowDrop:!1,allowDrag:!1,autoBind:b.autoBind,_checkForHiddenParent:!1,focusable:b.focusable,touchMode:b.touchMode,checkboxes:b.checkboxes,rtl:b.rtl,_renderOnDemand:!0,emptyString:b.emptyString,itemHeight:b.itemHeight,width:n,searchMode:b.searchMode,incrementalSearch:b.incrementalSearch,incrementalSearchDelay:b.incrementalSearchDelay,groupMember:b.groupMember,searchMember:b.searchMember,displayMember:b.displayMember,valueMember:b.valueMember,height:b.dropDownHeight,autoHeight:b.autoDropDownHeight,scrollBarSize:b.scrollBarSize,selectedIndex:b.selectedIndex,source:b.source,theme:b.theme,rendered:function(){b.selectedIndex!=b.listBoxContainer.jqxListBox("selectedIndex")?(b.listBox=a.data(b.listBoxContainer[0],"jqxListBox").instance,b.listBoxContainer.jqxListBox({selectedIndex:b.selectedIndex}),b.renderSelection("mouse")):b.renderSelection("mouse")},renderer:b.renderer,filterChange:function(a){b.autoDropDownHeight&&b.container.height(b.listBoxContainer.height()+25)}}),"element"===b.dropDownContainer?b.listBoxContainer.css({position:"absolute",top:0,left:0}):b.listBoxContainer.css({position:"absolute",zIndex:b.popupZIndex,top:0,left:0}),b.template&&b.listBoxContainer.addClass(b.toThemeProperty("jqx-"+b.template+"-item")),b.listBox=a.data(b.listBoxContainer[0],"jqxListBox").instance,b.listBox.enableSelection=b.enableSelection,b.listBox.enableHover=b.enableHover,b.listBox.equalItemsWidth=b.equalItemsWidth,b.listBox.selectIndex(b.selectedIndex),b.listBox._arrange(),b.listBoxContainer.addClass(b.toThemeProperty("jqx-popup")),a.jqx.browser.msie&&b.listBoxContainer.addClass(b.toThemeProperty("jqx-noshadow")),b.addHandler(b.listBoxContainer,"unselect",function(a){b._raiseEvent("3",{index:a.args.index,type:a.args.type,item:a.args.item})}),b.addHandler(b.listBoxContainer,"change",function(a){a.args&&("keyboard"!=a.args.type?b._raiseEvent("4",{index:a.args.index,type:a.args.type,item:a.args.item}):"keyboard"==a.args.type&&(b.isOpened()||b._raiseEvent("4",{index:b.selectedIndex,type:"keyboard",item:b.getItem(b.selectedIndex)})))}),"none"==b.animationType?b.container.css("display","none"):b.container.hide()}catch(a){console&&console.log(a)}var b=b;if(b.propertyChangeMap.disabled=function(c,d,e,f){f?(c.host.addClass(b.toThemeProperty("jqx-dropdownlist-state-disabled")),c.host.addClass(b.toThemeProperty("jqx-fill-state-disabled")),c.dropdownlistContent.addClass(b.toThemeProperty("jqx-dropdownlist-content-disabled"))):(c.host.removeClass(b.toThemeProperty("jqx-dropdownlist-state-disabled")),c.host.removeClass(b.toThemeProperty("jqx-fill-state-disabled")),c.dropdownlistContent.removeClass(b.toThemeProperty("jqx-dropdownlist-content-disabled"))),a.jqx.aria(c,"aria-disabled",c.disabled)},b.disabled&&(b.host.addClass(b.toThemeProperty("jqx-dropdownlist-state-disabled")),b.host.addClass(b.toThemeProperty("jqx-fill-state-disabled")),b.dropdownlistContent.addClass(b.toThemeProperty("jqx-dropdownlist-content-disabled"))),"top"==b.dropDownVerticalAlignment?b.arrow.addClass(b.toThemeProperty("jqx-icon-arrow-up")):b.arrow.addClass(b.toThemeProperty("jqx-icon-arrow-down")),b.arrow.addClass(b.toThemeProperty("jqx-icon")),"simple"===b.renderMode&&(b.arrow.remove(),b.host.removeClass(b.toThemeProperty("jqx-fill-state-normal")),b.host.removeClass(b.toThemeProperty("jqx-rc-all"))),b.template&&b.host.addClass(b.toThemeProperty("jqx-"+b.template)),b._updateHandlers(),b._setSize(),b._arrange(),b.listBox&&b.renderSelection(),a.jqx.browser.msie&&a.jqx.browser.version<8&&b.host.parents(".jqx-window").length>0){var o=b.host.parents(".jqx-window").css("z-index");m.css("z-index",o+10),b.listBoxContainer.css("z-index",o+10)}},resize:function(a,b){this.width=a,this.height=b,this._setSize(),this._arrange()},val:function(a){if(!this.dropdownlistContent)return"";if(this.input&&(function(b){for(var c in b)if(b.hasOwnProperty(c))return!1;return"number"!=typeof a&&("date"!=typeof a&&("boolean"!=typeof a&&"string"!=typeof a))}(a)||0==arguments.length))return this.input.val();var b=this.getItemByValue(a);return null!=b&&this.selectItem(b),this.input?this.input.val():void 0},focus:function(){try{var a=this,b=function(){a.host&&(a.host.focus(),a._firstDiv&&a._firstDiv.focus())};b(),setTimeout(function(){b()},10)}catch(a){}},_addInput:function(){var b=this.host.attr("name");this.input=a("<input type='hidden'/>"),this.host.append(this.input),b&&this.input.attr("name",b)},getItems:function(){return this.listBox?this.listBox.items:new Array},getVisibleItems:function(){return this.listBox.getVisibleItems()},_setSize:function(){null!=this.width&&-1!=this.width.toString().indexOf("px")?this.host.width(this.width):void 0==this.width||isNaN(this.width)||this.host.width(this.width),null!=this.height&&-1!=this.height.toString().indexOf("px")?this.host.height(this.height):void 0==this.height||isNaN(this.height)||this.host.height(this.height);var b=!1;null!=this.width&&-1!=this.width.toString().indexOf("%")&&(b=!0,this.element.style.width=this.width),null!=this.height&&-1!=this.height.toString().indexOf("%")&&(b=!0,this.element.style.height=this.height);var c=this,d=function(){if(c._arrange(),"auto"==c.dropDownWidth){var a=c.host.width();c.listBoxContainer.jqxListBox({width:a}),c.container.width(parseInt(a)+25)}};if(b){var e=this.host.width();"auto"!=this.dropDownWidth&&(e=this.dropDownWidth),this.listBoxContainer.jqxListBox({width:e}),this.container.width(parseInt(e)+25)}a.jqx.utilities.resize(this.host,function(){d()},!1,this._checkForHiddenParent)},isOpened:function(){var b=this,c=a.data(document.body,"openedJQXListBox"+this.id);return null!=c&&c==b.listBoxContainer},_updateHandlers:function(){var b=this,c=!1;this.removeHandlers(),this.touch||(this.addHandler(this.host,"mouseenter",function(){!b.disabled&&b.enableHover&&"simple"!==b.renderMode&&(c=!0,b.host.addClass(b.toThemeProperty("jqx-dropdownlist-state-hover")),"top"==b.dropDownVerticalAlignment?b.arrow.addClass(b.toThemeProperty("jqx-icon-arrow-up-hover")):b.arrow.addClass(b.toThemeProperty("jqx-icon-arrow-down-hover")),b.host.addClass(b.toThemeProperty("jqx-fill-state-hover")))}),this.addHandler(this.host,"mouseleave",function(){!b.disabled&&b.enableHover&&"simple"!==b.renderMode&&(b.host.removeClass(b.toThemeProperty("jqx-dropdownlist-state-hover")),b.host.removeClass(b.toThemeProperty("jqx-fill-state-hover")),b.arrow.removeClass(b.toThemeProperty("jqx-icon-arrow-down-hover")),b.arrow.removeClass(b.toThemeProperty("jqx-icon-arrow-up-hover")),c=!1)})),this.host.parents()&&this.addHandler(this.host.parents(),"scroll.dropdownlist"+this.element.id,function(a){b.isOpened()&&b.close()});var d="mousedown";this.touch&&(d=a.jqx.mobile.getTouchEventName("touchstart")),this.addHandler(this.dropdownlistWrapper,d,function(a){if(!b.disabled){var c="block"==b.container.css("display");if(!b.isanimating){if(c)return b.hideListBox(),!1;b.showListBox(),b.focusable?b.focus():a.preventDefault&&a.preventDefault()}}}),b.autoOpen&&(this.addHandler(this.host,"mouseenter",function(){!b.isOpened()&&b.autoOpen&&(b.open(),b.host.focus())}),a(document).on("mousemove."+b.id,function(a){if(b.isOpened()&&b.autoOpen){var c=b.host.coord(),d=c.top,e=c.left,f=b.container.coord(),g=f.left,h=f.top;canClose=!0,a.pageY>=d&&a.pageY<=d+b.host.height()&&a.pageX>=e&&a.pageX<e+b.host.width()&&(canClose=!1),a.pageY>=h&&a.pageY<=h+b.container.height()&&a.pageX>=g&&a.pageX<g+b.container.width()&&(canClose=!1),canClose&&b.close()}})),this.touch?this.addHandler(a(document),a.jqx.mobile.getTouchEventName("touchstart")+"."+this.id,b.closeOpenedListBox,{me:this,listbox:this.listBox,id:this.id}):this.addHandler(a(document),"mousedown."+this.id,b.closeOpenedListBox,{me:this,listbox:this.listBox,id:this.id}),this.addHandler(this.host,"keydown",function(a){var c="block"==b.container.css("display");if("none"==b.host.css("display"))return!0;if(("13"==a.keyCode||"9"==a.keyCode)&&!b.isanimating)return c&&(b.renderSelection(),"13"==a.keyCode&&b.focusable&&b._firstDiv.focus(),b.hideListBox(),b.keyboardSelection||b._raiseEvent("2",{index:b.selectedIndex,type:"keyboard",item:b.getItem(b.selectedIndex)}),"13"==a.keyCode&&b._raiseEvent("4",{index:b.selectedIndex,type:"keyboard",item:b.getItem(b.selectedIndex)})),!c||"9"==a.keyCode;if(115==a.keyCode)return b.isanimating||(b.isOpened()?b.isOpened()&&b.hideListBox():b.showListBox()),!1;if(a.altKey&&"block"==b.host.css("display"))if(38==a.keyCode){if(b.isOpened())return b.hideListBox(),!0}else if(40==a.keyCode&&!b.isOpened())return b.showListBox(),!0;return"27"!=a.keyCode||b.ishiding?b.disabled?void 0:(b._kbnavigated=b.listBox._handleKeyDown(a),b._kbnavigated):(b.isOpened()&&(b.hideListBox(),void 0!=b.tempSelectedIndex&&b.selectIndex(b.tempSelectedIndex)),!0)}),this.addHandler(this.listBoxContainer,"checkChange",function(a){b.renderSelection(),b._updateInputSelection(),b._raiseEvent(5,{label:a.args.label,value:a.args.value,checked:a.args.checked,item:a.args.item})}),this.addHandler(this.listBoxContainer,"select",function(a){if(!b.disabled){if(!a.args)return;"keyboard"!=a.args.type||b.isOpened()||b.renderSelection(),("keyboard"!=a.args.type||b.keyboardSelection)&&(b.renderSelection(),b._raiseEvent("2",{index:a.args.index,type:a.args.type,item:a.args.item,originalEvent:a.args.originalEvent}),"mouse"==a.args.type&&(b.checkboxes||(b.hideListBox(),b._firstDiv&&b.focusable&&b._firstDiv.focus())))}}),this.listBox&&this.listBox.content&&this.addHandler(this.listBox.content,"click",function(a){if(!b.disabled){if(b.listBox.itemswrapper&&a.target===b.listBox.itemswrapper[0])return!0;b.renderSelection("mouse"),b.touch||b.ishiding||b.checkboxes||(b.hideListBox(),b._firstDiv&&b.focusable&&b._firstDiv.focus()),b.keyboardSelection||(!1===b._kbnavigated&&(b.tempSelectedIndex!=b.selectedIndex&&b._raiseEvent("4",{index:b.selectedIndex,type:"mouse",item:b.getItem(b.selectedIndex)}),b._kbnavigated=!0),void 0==b._oldSelectedInd&&(b._oldSelectedIndx=b.selectedIndex),b.selectedIndex!=b._oldSelectedIndx&&(b._raiseEvent("2",{index:b.selectedIndex,type:"keyboard",item:b.getItem(b.selectedIndex)}),b._oldSelectedIndx=b.selectedIndex))}}),this.addHandler(this.host,"focus",function(a){"simple"!==b.renderMode&&(b.host.addClass(b.toThemeProperty("jqx-dropdownlist-state-focus")),b.host.addClass(b.toThemeProperty("jqx-fill-state-focus")))}),this.addHandler(this.host,"blur",function(){"simple"!==b.renderMode&&(b.host.removeClass(b.toThemeProperty("jqx-dropdownlist-state-focus")),b.host.removeClass(b.toThemeProperty("jqx-fill-state-focus")))}),this.addHandler(this._firstDiv,"focus",function(a){"simple"!==b.renderMode&&(b.host.addClass(b.toThemeProperty("jqx-dropdownlist-state-focus")),b.host.addClass(b.toThemeProperty("jqx-fill-state-focus")))}),this.addHandler(this._firstDiv,"blur",function(){"simple"!==b.renderMode&&(b.host.removeClass(b.toThemeProperty("jqx-dropdownlist-state-focus")),b.host.removeClass(b.toThemeProperty("jqx-fill-state-focus")))})},removeHandlers:function(){var b=this,c="mousedown";this.touch&&(c=a.jqx.mobile.getTouchEventName("touchstart")),this.removeHandler(this.dropdownlistWrapper,c),this.listBox&&this.listBox.content&&this.removeHandler(this.listBox.content,"click"),this.removeHandler(this.host,"loadContent"),this.removeHandler(this.listBoxContainer,"checkChange"),this.removeHandler(this.host,"keydown"),this.removeHandler(this.host,"focus"),this.removeHandler(this.host,"blur"),this.removeHandler(this._firstDiv,"focus"),this.removeHandler(this._firstDiv,"blur"),this.removeHandler(this.host,"mouseenter"),this.removeHandler(this.host,"mouseleave"),this.removeHandler(a(document),"mousemove."+b.id)},getItem:function(a){return this.listBox.getItem(a)},getItemByValue:function(a){return this.listBox.getItemByValue(a)},selectItem:function(a){void 0!=this.listBox&&(this.listBox.selectItem(a),this.selectedIndex=this.listBox.selectedIndex,this.renderSelection("mouse"))},unselectItem:function(a){void 0!=this.listBox&&(this.listBox.unselectItem(a),this.renderSelection("mouse"))},checkItem:function(a){void 0!=this.listBox&&this.listBox.checkItem(a)},uncheckItem:function(a){void 0!=this.listBox&&this.listBox.uncheckItem(a)},indeterminateItem:function(a){void 0!=this.listBox&&this.listBox.indeterminateItem(a)},renderSelection:function(){if(null!=this.listBox){this.height&&-1!=this.height.toString().indexOf("%")&&this._arrange();var b=this.listBox.visibleItems[this.listBox.selectedIndex];if(this.filterable&&-1==this.listBox.selectedIndex)for(var c in this.listBox.selectedValues){var d=this.listBox.selectedValues[c],e=this.listBox.getItemByValue(d);e&&(b=e)}if(this.checkboxes){var f=this.getCheckedItems();b=null!=f&&f.length>0?f[0]:null}if(null==b){var g=a('<span unselectable="on" style="color: inherit; border: none; background-color: transparent;"></span>');g.appendTo(a(document.body)),g.addClass(this.toThemeProperty("jqx-widget")),g.addClass(this.toThemeProperty("jqx-listitem-state-normal")),g.addClass(this.toThemeProperty("jqx-item")),a.jqx.utilities.html(g,this.placeHolder);var h=this.dropdownlistContent.css("padding-top"),i=this.dropdownlistContent.css("padding-bottom");g.css("padding-top",h),g.css("padding-bottom",i);var j=g.outerHeight();g.remove(),g.removeClass(),a.jqx.utilities.html(this.dropdownlistContent,g);var k=this.host.height();null!=this.height&&void 0!=this.height&&-1===this.height.toString().indexOf("%")&&(k=parseInt(this.height));var l=parseInt((parseInt(k)-parseInt(j))/2);return l>0&&(this.dropdownlistContent.css("margin-top",l+"px"),this.dropdownlistContent.css("margin-bottom",l+"px")),this.selectionRenderer?(a.jqx.utilities.html(this.dropdownlistContent,this.selectionRenderer(g,-1,"","")),this.dropdownlistContent.css("margin-top","0px"),this.dropdownlistContent.css("margin-bottom","0px"),this._updateInputSelection()):this._updateInputSelection(),this.selectedIndex=this.listBox.selectedIndex,"auto"===this.width&&this._arrange(),void(this.focusable&&this.isOpened()&&this.focus())}this.selectedIndex=this.listBox.selectedIndex;var g=a(document.createElement("span"));g[0].setAttribute("unselectable","on");try{g[0].style.color="inherit"}catch(a){}g[0].style.borderWidth="0px",g[0].style.backgroundColor="transparent",g.appendTo(a(document.body)),g.addClass(this.toThemeProperty("jqx-widget jqx-listitem-state-normal jqx-item"));var m=!1;try{void 0!=b.html&&null!=b.html&&b.html.toString().length>0?a.jqx.utilities.html(g,b.html):void 0!=b.label&&null!=b.label&&b.label.toString().length>0?a.jqx.utilities.html(g,b.label):null===b.label||""===b.label?(m=!0,a.jqx.utilities.html(g,"")):void 0!=b.value&&null!=b.value&&b.value.toString().length>0?a.jqx.utilities.html(g,b.value):void 0!=b.title&&null!=b.title&&b.title.toString().length>0?a.jqx.utilities.html(g,b.title):""!=b.label&&null!=b.label||(m=!0,a.jqx.utilities.html(g,""))}catch(a){}var h=this.dropdownlistContent[0].style.paddingTop,i=this.dropdownlistContent[0].style.paddingBottom;""===h&&(h="0px"),""===i&&(i="0px"),g[0].style.paddingTop=h,g[0].style.paddingBottom=i;var j=g.outerHeight();0===j&&(j=16),""!=b.label&&null!=b.label||!m||a.jqx.utilities.html(g,"");var n=this.width&&this.width.toString().indexOf("%")<=0;if(g.remove(),g.removeClass(),this.selectionRenderer)a.jqx.utilities.html(this.dropdownlistContent,this.selectionRenderer(g,b.index,b.label,b.value)),this.focusable&&this.isOpened()&&this.focus();else if(this.checkboxes){for(var o=this.getCheckedItems(),p="",q=0;q<o.length;q++)q==o.length-1?p+=o[q].label:p+=o[q].label+",";g.text(p),n&&g.css("max-width",this.host.width()-30),g.css("overflow","hidden"),g.css("display","block"),this.rtl||n&&g.css("width",this.host.width()-30),g.css("text-overflow","ellipsis"),g.css("padding-bottom",1+parseInt(i)),this.dropdownlistContent.html(g),this.focusable&&this.isOpened()&&this.focus()}else{var r=this.host.width()-this.arrowSize-3;this.width&&"auto"!==this.width&&(n&&(this.rtl||g.css("max-width",r+"px")),g[0].style.overflow="hidden",g[0].style.display="block",g[0].style.paddingTop=1+parseInt(i)+"px",this.rtl||n&&(r<0&&(r=0),g[0].style.width=r+"px"),g[0].style.textOverflow="ellipsis"),this.dropdownlistContent[0].innerHTML=g[0].innerHTML,this.focusable&&this.isOpened()&&this.focus()}var k=this.host.height();null!=this.height&&void 0!=this.height&&-1===this.height.toString().indexOf("%")&&(k=parseInt(this.height));var l=parseInt((parseInt(k)-parseInt(j))/2);l>=0&&(this.dropdownlistContent[0].style.marginTop=l+"px",this.dropdownlistContent[0].style.marginBottom=l+"px"),this.selectionRenderer&&(this.dropdownlistContent[0].style.marginTop="0px",this.dropdownlistContent[0].style.marginBottom="0px"),this.dropdownlistContent&&this.input&&this._updateInputSelection(),this.listBox&&this.listBox._activeElement&&a.jqx.aria(this,"aria-activedescendant",this.listBox._activeElement.id),"auto"===this.width&&this._arrange()}},_updateInputSelection:function(){if(this.input){var b=new Array;if(-1==this.selectedIndex)this.input.val("");else{var c=this.getSelectedItem();null!=c?(this.input.val(c.value),b.push(c.value)):this.input.val(this.dropdownlistContent.text())}if(this.checkboxes){var d=this.getCheckedItems(),e="";if(null!=d)for(var f=0;f<d.length;f++){var g=d[f].value;void 0!=g&&(f==d.length-1?e+=g:e+=g+",",b.push(g))}this.input.val(e)}}this.field&&this.input&&("select"==this.field.nodeName.toLowerCase()?a.each(this.field,function(c,d){a(this).removeAttr("selected"),this.selected=b.indexOf(this.value)>=0,this.selected&&a(this).attr("selected",!0)}):a.each(this.items,function(c,d){a(this.originalItem.originalItem).removeAttr("data-selected"),this.selected=b.indexOf(this.value)>=0,this.selected&&a(this.originalItem.originalItem).attr("data-selected",!0)}))},setContent:function(b){a.jqx.utilities.html(this.dropdownlistContent,b),this._updateInputSelection()},dataBind:function(){this.listBoxContainer.jqxListBox({source:this.source}),this.renderSelection("mouse"),null==this.source&&this.clearSelection()},clear:function(){this.listBoxContainer.jqxListBox({source:null}),this.clearSelection()},clearSelection:function(b){this.selectedIndex=-1,this._updateInputSelection(),this.listBox.clearSelection(),this.renderSelection(),this.selectionRenderer||a.jqx.utilities.html(this.dropdownlistContent,this.placeHolder)},unselectIndex:function(a,b){isNaN(a)||(this.listBox.unselectIndex(a,b),this.renderSelection())},selectIndex:function(a,b,c,d){this.listBox.selectIndex(a,b,c,d,"api")},getSelectedIndex:function(){return this.selectedIndex},getSelectedItem:function(){return this.listBox.getVisibleItem(this.selectedIndex)},getCheckedItems:function(){return this.listBox.getCheckedItems()},checkIndex:function(a){this.listBox.checkIndex(a)},uncheckIndex:function(a){this.listBox.uncheckIndex(a)},indeterminateIndex:function(a){this.listBox.indeterminateIndex(a)},checkAll:function(){this.listBox.checkAll(),this.renderSelection("mouse")},uncheckAll:function(){this.listBox.uncheckAll(),this.renderSelection("mouse")},addItem:function(a){return this.listBox.addItem(a)},insertAt:function(a,b){return null!=a&&this.listBox.insertAt(a,b)},removeAt:function(a){var b=this.listBox.removeAt(a);return this.renderSelection("mouse"),b},removeItem:function(a){var b=this.listBox.removeItem(a);return this.renderSelection("mouse"),b},updateItem:function(a,b){var c=this.listBox.updateItem(a,b);return this.renderSelection("mouse"),c},updateAt:function(a,b){var c=this.listBox.updateAt(a,b);return this.renderSelection("mouse"),c},ensureVisible:function(a){return this.listBox.ensureVisible(a)},disableAt:function(a){return this.listBox.disableAt(a)},enableAt:function(a){return this.listBox.enableAt(a)},disableItem:function(a){return this.listBox.disableItem(a)},enableItem:function(a){return this.listBox.enableItem(a)},_findPos:function(b){for(;b&&("hidden"==b.type||1!=b.nodeType||a.expr.filters.hidden(b));)b=b.nextSibling;var c=a(b).coord(!0);return[c.left,c.top]},testOffset:function(b,c,d){var e=b.outerWidth(),f=b.outerHeight(),g=a(window).width()+a(window).scrollLeft(),h=a(window).height()+a(window).scrollTop();if(c.left+e>g&&e>this.host.width()){var i=this.host.coord().left,j=e-this.host.width();c.left=i-j+2}return c.left<0&&(c.left=parseInt(this.host.coord().left)+"px"),c.top-=Math.min(c.top,c.top+f>h&&h>f?Math.abs(f+d+22):0),c},open:function(){this.showListBox()},close:function(){this.hideListBox()},_getBodyOffset:function(){var b=0,c=0;return"0px"!=a("body").css("border-top-width")&&(b=parseInt(a("body").css("border-top-width")),isNaN(b)&&(b=0)),"0px"!=a("body").css("border-left-width")&&(c=parseInt(a("body").css("border-left-width")),isNaN(c)&&(c=0)),{left:c,top:b}},showListBox:function(){if(a.jqx.aria(this,"aria-expanded",!0),this.listBox._renderOnDemand&&this.listBoxContainer.jqxListBox({_renderOnDemand:!1}),"auto"==this.dropDownWidth&&null!=this.width&&this.width.indexOf&&(-1!=this.width.indexOf("%")||-1!=this.width.indexOf("auto"))&&this.listBox.host.width()!=this.host.width()){var b=this.host.width();this.listBoxContainer.jqxListBox({width:b}),this.container.width(parseInt(b)+25)}var c,d=this,e=this.listBoxContainer,f=this.listBox,g=(a(window).scrollTop(),a(window).scrollLeft(),parseInt(this._findPos(this.host[0])[1])+parseInt(this.host.outerHeight())-1+"px"),h=parseInt(Math.round(this.host.coord(!0).left));c=h+"px","element"===this.dropDownContainer&&(g=parseInt(this.host.outerHeight())-1+"px",c=0);var i=a.jqx.mobile.isSafariMobileBrowser()||a.jqx.mobile.isWindowsPhone();if(null!=this.listBox){this.ishiding=!1,this.keyboardSelection||(this.listBox.selectIndex(this.selectedIndex),this.listBox.ensureVisible(this.selectedIndex)),this.tempSelectedIndex=this.selectedIndex,this.autoDropDownHeight&&this.container.height(this.listBoxContainer.height()+25),null!=i&&i&&(c=a.jqx.mobile.getLeftPos(this.element),g=a.jqx.mobile.getTopPos(this.element)+parseInt(this.host.outerHeight()),"0px"!=a("body").css("border-top-width")&&(g=parseInt(g)-this._getBodyOffset().top+"px"),"0px"!=a("body").css("border-left-width")&&(c=parseInt(c)-this._getBodyOffset().left+"px")),e.stop(),"simple"!==this.renderMode&&(this.host.addClass(this.toThemeProperty("jqx-dropdownlist-state-selected")),this.host.addClass(this.toThemeProperty("jqx-fill-state-pressed")),"top"==this.dropDownVerticalAlignment?this.arrow.addClass(this.toThemeProperty("jqx-icon-arrow-up-selected")):this.arrow.addClass(this.toThemeProperty("jqx-icon-arrow-down-selected"))),this.container.css("left",c),this.container.css("top",g),f._arrange();var j=!1;if("right"==this.dropDownHorizontalAlignment||this.rtl){var k=this.container.outerWidth(),l=Math.abs(k-this.host.width());k>this.host.width()?this.container.css("left",25+parseInt(Math.round(h))-l+"px"):this.container.css("left",25+parseInt(Math.round(h))+l+"px")}if("top"==this.dropDownVerticalAlignment){var m=e.height();j=!0,e.css("top",23),e.addClass(this.toThemeProperty("jqx-popup-up"));var n=parseInt(this.host.outerHeight()),o=parseInt(g)-Math.abs(m+n+23);this.container.css("top",o)}if(this.enableBrowserBoundsDetection){var p=this.testOffset(e,{left:parseInt(this.container.css("left")),top:parseInt(g)},parseInt(this.host.outerHeight()));parseInt(this.container.css("top"))!=p.top?(j=!0,e.css("top",23),e.addClass(this.toThemeProperty("jqx-popup-up"))):e.css("top",0),this.container.css("top",p.top),parseInt(this.container.css("left"))!=p.left&&this.container.css("left",p.left)}if("none"==this.animationType)this.container.css("display","block"),a.data(document.body,"openedJQXListBoxParent",d),a.data(document.body,"openedJQXListBox"+this.id,e),e.css("margin-top",0),e.css("opacity",1),f._renderItems(),d._raiseEvent("0",f);else if(this.container.css("display","block"),d.isanimating=!0,"fade"==this.animationType)e.css("margin-top",0),e.css("opacity",0),e.animate({opacity:1},this.openDelay,function(){a.data(document.body,"openedJQXListBoxParent",d),a.data(document.body,"openedJQXListBox"+d.id,e),d.ishiding=!1,d.isanimating=!1,f._renderItems(),d._raiseEvent("0",f)});else{e.css("opacity",1);var q=e.outerHeight();j?e.css("margin-top",q):e.css("margin-top",-q),e.animate({"margin-top":0},this.openDelay,function(){a.data(document.body,"openedJQXListBoxParent",d),a.data(document.body,"openedJQXListBox"+d.id,e),d.ishiding=!1,d.isanimating=!1,f._renderItems(),d._raiseEvent("0",f)})}j?(this.host.addClass(this.toThemeProperty("jqx-rc-t-expanded")),e.addClass(this.toThemeProperty("jqx-rc-b-expanded"))):(this.host.addClass(this.toThemeProperty("jqx-rc-b-expanded")),e.addClass(this.toThemeProperty("jqx-rc-t-expanded"))),"simple"!==this.renderMode&&(e.addClass(this.toThemeProperty("jqx-fill-state-focus")),this.host.addClass(this.toThemeProperty("jqx-dropdownlist-state-focus")),this.host.addClass(this.toThemeProperty("jqx-fill-state-focus")))}},hideListBox:function(){a.jqx.aria(this,"aria-expanded",!1);var b=this.listBoxContainer,c=this.listBox,d=this.container,e=this;if(a.data(document.body,"openedJQXListBox"+this.id,null),"none"==this.animationType)this.container.css("display","none");else if(!e.ishiding){b.stop();var f=b.outerHeight();b.css("margin-top",0),e.isanimating=!0;var g=-f;parseInt(this.container.coord().top)<parseInt(this.host.coord().top)&&(g=f),"fade"==this.animationType?(b.css({opacity:1}),b.animate({opacity:0},this.closeDelay,function(){d.css("display","none"),e.isanimating=!1,e.ishiding=!1})):b.animate({"margin-top":g},this.closeDelay,function(){d.css("display","none"),e.isanimating=!1,e.ishiding=!1})}this.ishiding=!0,this.host.removeClass(this.toThemeProperty("jqx-dropdownlist-state-selected")),this.host.removeClass(this.toThemeProperty("jqx-fill-state-pressed")),this.arrow.removeClass(this.toThemeProperty("jqx-icon-arrow-down-selected")),this.arrow.removeClass(this.toThemeProperty("jqx-icon-arrow-up-selected")),
this.host.removeClass(this.toThemeProperty("jqx-rc-b-expanded")),b.removeClass(this.toThemeProperty("jqx-rc-t-expanded")),this.host.removeClass(this.toThemeProperty("jqx-rc-t-expanded")),b.removeClass(this.toThemeProperty("jqx-rc-b-expanded")),b.removeClass(this.toThemeProperty("jqx-fill-state-focus")),this.host.removeClass(this.toThemeProperty("jqx-dropdownlist-state-focus")),this.host.removeClass(this.toThemeProperty("jqx-fill-state-focus")),this._raiseEvent("1",c)},closeOpenedListBox:function(b){var c=b.data.me,d=a(b.target),e=b.data.listbox;if(null==e)return!0;if(a(b.target).ischildof(b.data.me.host))return!0;if(!c.isOpened())return!0;if(a(b.target).ischildof(c.listBoxContainer))return!0;var f=!1;return a.each(d.parents(),function(){if("undefined"!=this.className&&this.className.indexOf){if(-1!=this.className.indexOf("jqx-listbox"))return f=!0,!1;if(-1!=this.className.indexOf("jqx-dropdownlist"))return c.element.id==this.id&&(f=!0),!1}}),null!=e&&!f&&c.isOpened()&&c.hideListBox(),!0},clearFilter:function(){this.listBox.clearFilter()},loadFromSelect:function(a){this.listBox.loadFromSelect(a)},refresh:function(a){!0!==a&&(this._setSize(),this._arrange(),this.listBox&&this.renderSelection())},_arrange:function(){var a=this,b=parseInt(a.host.width()),c=parseInt(a.host.height()),d=(a.arrowSize,a.arrowSize),e=b-d-6;if(e>0&&"auto"!==a.width?a.dropdownlistContent[0].style.width=e+"px":e<=0&&(a.dropdownlistContent[0].style.width="0px"),"auto"===a.width&&(a.dropdownlistContent.css("width","auto"),b=a.dropdownlistContent.width()+d+6,a.host.width(b)),a.dropdownlistContent[0].style.height=c+"px",a.dropdownlistContent[0].style.left="0px",a.dropdownlistContent[0].style.top="0px",a.dropdownlistArrow[0].style.width=d+"px",a.width&&a.width.toString().indexOf("%")>=0){var f=100*d/b,g=100*e/b;a.dropdownlistArrow[0].style.width=f+"%",a.dropdownlistContent[0].style.width=g+"%"}a.dropdownlistArrow[0].style.height=c+"px",a.rtl&&(a.dropdownlistArrow.css("float","left"),a.dropdownlistContent.css("float","right"))},destroy:function(){a.jqx.utilities.resize(this.host,null,!0),this.removeHandler(this.listBoxContainer,"select"),this.removeHandler(this.listBoxContainer,"unselect"),this.removeHandler(this.listBoxContainer,"change"),this.removeHandler(this.dropdownlistWrapper,"selectstart"),this.removeHandler(this.dropdownlistWrapper,"mousedown"),this.removeHandler(this.host,"keydown"),this.removeHandler(this.listBoxContainer,"select"),this.removeHandler(this.listBox.content,"click"),this.removeHandler(this.listBoxContainer,"bindingComplete"),this.host.parents()&&this.removeHandler(this.host.parents(),"scroll.dropdownlist"+this.element.id),this.removeHandlers(),this.listBoxContainer.jqxListBox("destroy"),this.listBoxContainer.remove(),this.host.removeClass(),this.removeHandler(a(document),"mousedown."+this.id,this.closeOpenedListBox),this.touch&&this.removeHandler(a(document),a.jqx.mobile.getTouchEventName("touchstart")+"."+this.id),this.dropdownlistArrow.remove(),delete this.dropdownlistArrow,delete this.dropdownlistWrapper,delete this.listBoxContainer,delete this.input,delete this.arrow,delete this.dropdownlistContent,delete this.listBox,delete this._firstDiv,this.container.remove(),delete this.container;var b=a.data(this.element,"jqxDropDownList");b&&delete b.instance,this.host.removeData(),this.host.remove(),delete this.comboStructure,delete this.host,delete this.element},_raiseEvent:function(b,c){void 0==c&&(c={owner:null});var d=this.events[b];args=c,args.owner=this;var e=new a.Event(d);return e.owner=this,2!=b&&3!=b&&4!=b&&5!=b&&6!=b&&7!=b&&8!=b&&9!=b||(e.args=c),this.host.trigger(e)},propertiesChangedHandler:function(a,b,c){if(c.width&&c.height&&2==Object.keys(c).length){if(a._setSize(),"width"==b&&"auto"==a.dropDownWidth){var d=a.host.width();a.listBoxContainer.jqxListBox({width:d}),a.container.width(parseInt(d)+25)}a._arrange(),a.close()}},propertyChangedHandler:function(b,c,d,e){if(void 0!=b.isInitialized&&0!=b.isInitialized&&!(b.batchUpdate&&b.batchUpdate.width&&b.batchUpdate.height&&2==Object.keys(b.batchUpdate).length)){if("template"==c&&(b.listBoxContainer.removeClass(b.toThemeProperty("jqx-"+d+"-item")),b.listBoxContainer.addClass(b.toThemeProperty("jqx-"+b.template+"-item")),b.host.removeClass(b.toThemeProperty("jqx-"+d)),b.host.addClass(b.toThemeProperty("jqx-"+b.template))),"dropDownVerticalAlignment"==c&&(b.arrow.removeClass(b.toThemeProperty("jqx-icon-arrow-up")),b.arrow.removeClass(b.toThemeProperty("jqx-icon-arrow-down")),"top"==b.dropDownVerticalAlignment?b.arrow.addClass(b.toThemeProperty("jqx-icon-arrow-up")):b.arrow.addClass(b.toThemeProperty("jqx-icon-arrow-down")),b.listBoxContainer.css("top",0),b.listBoxContainer.removeClass(this.toThemeProperty("jqx-popup-up"))),"autoItemsHeight"==c&&b.listBoxContainer.jqxListBox({autoItemsHeight:e}),"filterable"==c&&b.listBoxContainer.jqxListBox({filterable:e}),"filterHeight"==c&&b.listBoxContainer.jqxListBox({filterHeight:e}),"filterPlaceHolder"==c&&b.listBoxContainer.jqxListBox({filterPlaceHolder:e}),"filterDelay"==c&&b.listBoxContainer.jqxListBox({filterDelay:e}),"enableSelection"==c&&b.listBoxContainer.jqxListBox({enableSelection:e}),"enableHover"==c&&b.listBoxContainer.jqxListBox({enableHover:e}),"autoOpen"==c&&b._updateHandlers(),"emptyString"==c&&(b.listBox.emptyString=b.emptyString),"itemHeight"==c&&b.listBoxContainer.jqxListBox({itemHeight:e}),"renderer"==c&&b.listBoxContainer.jqxListBox({renderer:e}),"rtl"==c&&(e?(b.dropdownlistArrow.css("float","left"),b.dropdownlistContent.css("float","right")):(b.dropdownlistArrow.css("float","right"),b.dropdownlistContent.css("float","left")),b.listBoxContainer.jqxListBox({rtl:b.rtl})),"source"==c&&(b.listBoxContainer.jqxListBox({source:b.source}),b.listBox.selectedIndex=-1,b.listBox.selectIndex(this.selectedIndex),b.renderSelection(),null==e&&b.clear()),"displayMember"!=c&&"valueMember"!=c||(b.listBoxContainer.jqxListBox({displayMember:b.displayMember,valueMember:b.valueMember}),b.renderSelection()),"placeHolder"==c&&b.renderSelection(),"theme"==c&&null!=e&&(b.listBoxContainer.jqxListBox({theme:e}),b.listBoxContainer.addClass(b.toThemeProperty("jqx-popup")),a.jqx.utilities.setTheme(d,e,b.host)),"autoDropDownHeight"==c&&(b.listBoxContainer.jqxListBox({autoHeight:b.autoDropDownHeight}),b.autoDropDownHeight?b.container.height(b.listBoxContainer.height()+25):(b.listBoxContainer.jqxListBox({height:b.dropDownHeight}),b.container.height(parseInt(b.dropDownHeight)+25)),b.listBox._arrange(),b.listBox._updatescrollbars()),"searchMode"==c&&b.listBoxContainer.jqxListBox({searchMode:b.searchMode}),"incrementalSearch"==c&&b.listBoxContainer.jqxListBox({incrementalSearch:b.incrementalSearch}),"incrementalSearchDelay"==c&&b.listBoxContainer.jqxListBox({incrementalSearchDelay:b.incrementalSearchDelay}),"dropDownHeight"==c&&(b.autoDropDownHeight||(b.listBoxContainer.jqxListBox({height:b.dropDownHeight}),b.container.height(parseInt(b.dropDownHeight)+25))),"dropDownWidth"==c||"scrollBarSize"==c){var f=b.width;"auto"!=b.dropDownWidth&&(f=b.dropDownWidth),b.listBoxContainer.jqxListBox({width:f,scrollBarSize:b.scrollBarSize}),b.container.width(parseInt(f)+25)}if(("width"==c||"height"==c)&&e!=d){if(this.refresh(),"width"==c&&"auto"==b.dropDownWidth){var f=b.host.width();b.listBoxContainer.jqxListBox({width:f}),b.container.width(parseInt(f)+25)}b.close()}"checkboxes"==c&&b.listBoxContainer.jqxListBox({checkboxes:b.checkboxes}),"selectedIndex"==c&&null!=b.listBox&&(b.listBox.selectIndex(parseInt(e)),b.renderSelection())}}})}(jqxBaseFramework);

