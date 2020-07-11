
// our homegrown web printing service functions

function web_print(msg, printer){
  $.ajax({ url: printer.web_print_service_url, type: "POST", dataType: "json", cache: false, async: true,
    data: {'msg' : msg},
    error: web_print_ajax_error,
    success: function () {console.log('print success')}
  });
}

function web_print_image(image_url, printer){
  $.ajax({ url: printer.web_print_image_service_url, type: "POST", dataType: "json", cache: false, async: true,
    data: {'url' : image_url},
    error: web_print_ajax_error,
    success: function () {console.log('print success')}
  });
}

function web_print_ajax_error(jqXHR, textStatus, errorThrown) {
  //alert(`AJAX ERROR: ${textStatus} \n ${errorThrown} \n response in console.` );
  console.log(jqXHR.responseText);
}


// epson intelligent printer printing functions

function epos_print(msg, printer) {

    // build print data
    var builder = new epson.ePOSBuilder();
    builder.addLayout(builder.LAYOUT_RECEIPT, 580);
    builder.addTextLang('en').addTextSmooth(true);
    //builder.addTextStyle(false, false, true);
    builder.addTextFont(builder.FONT_B);
    //builder.addTextAlign(builder.ALIGN_CENTER);
    builder.addTextSize(2, 2);
    builder.addTextLineSpace(50);
    builder.addText(msg);
    //builder.addTextStyle(false, false, false);
    builder.addFeedUnit(16);
    builder.addCut();

    // create print object
    var epos = new epson.ePOSPrint(
      `http://${printer.ipaddr}/cgi-bin/epos/service.cgi?devid=${printer.devid}&timeout=${printer.timeout}`
     ); 

    // register callback functions
    epos.onreceive = epson_onreceive
    epos.onerror = epson_onerror

    epos.send(builder.toString());
}


function epos_print_image (url, printer) {

  var img = new Image();
  img.src = url;
	img.onload = function() {
    //var canvas = document.createElement('canvas');
    var canvas = document.getElementById('canvas');
    canvas.setAttribute('height', img.height);
    canvas.setAttribute('width', img.width);
    var context = canvas.getContext('2d');
		context.drawImage(img, 0, 0);
    epos_print_canvas(canvas, printer)
	}

}


function epos_print_canvas(canvas, printer) {
    
    // create print object
    var epos = new epson.CanvasPrint(
      `http://${printer.ipaddr}/cgi-bin/epos/service.cgi?devid=${printer.devid}&timeout=${printer.timeout}`
    ); 

    // register callback function
    epos.onreceive = epson_onreceive;
    epos.onerror = epson_onerror;

    // paper layout
    epos.paper = epos.PAPER_RECEIPT;
    epos.layout = { width: 580 };

    //epos.mode = epos.MODE_GRAY16;
    epos.mode = epos.MODE_MONO;
    epos.halftone = epos.HALFTONE_ERROR_DIFFUSION;
    epos.cut = true;

    epos.print(canvas);
}


function epson_onreceive(res) {
  if (!res.success) {
    alert('Print Failure\ncode: '+
      res.code+'\nstatus: '+
      res.status+'\nbattery: '+
      res.battery+'\nprintjobid: '+
      res.printjobid);
  }
}


function epson_onerror(err) {
  alert('Print Failure\nstatus: '+ err.status+ '\n'+err.responseText);
}

