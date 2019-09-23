//
// print queue ticket
//

function print(msg, ipaddr, devid, timeout) {

    //
    // build print data
    //

    // create print data builder object
    var builder = new epson.ePOSBuilder();

    // paper layout
    builder.addLayout(builder.LAYOUT_RECEIPT, 580);

    // initialize (ank mode, smoothing)
    builder.addTextLang('en').addTextSmooth(true);

    // append message
    //builder.addTextStyle(false, false, true);
    builder.addTextFont(builder.FONT_B);
    //builder.addTextAlign(builder.ALIGN_CENTER);
    builder.addTextSize(2, 2);
    builder.addTextLineSpace(50);
    builder.addText(msg);
    //builder.addTextStyle(false, false, false);
    builder.addFeedUnit(16);

    // append paper cutting
    builder.addCut();

    //
    // send print data
    //

    // create print object
    var url = 'http://' + ipaddr + '/cgi-bin/epos/service.cgi?devid=' + devid + '&timeout=' + timeout;
    var epos = new epson.ePOSPrint(url);

    // register callback function
    epos.onreceive = function (res) {
        // print failure
        if (!res.success) {
          alert('Print Failure\ncode: '+
            res.code+'\nstatus: '+
            res.status+'\nbattery: '+
            res.battery+'\nprintjobid: '+
            res.printjobid);
        }
    }

    // register callback function
    epos.onerror = function (err) {
        // show error message
        alert('Print Failure\nstatus: '+ err.status+ '\n'+err.responseText);
    }

    // send
    epos.send(builder.toString());
}

//function print_gift (amount) {
    // to be continued
 //   setTimeout(print_gift1, 500, amount);
//}


var g_gift_height = 1200;
var g_gift_width = 512;
var fudge1 = 50;
var fudge2 = 100;

function print_gift1 (amount) {

    console.log("print_gift1 called with amount: " + amount);
    //
    // draw print data
    //

    // get context of canvas
    var canvas = $('#canvas').get(0);
    var context = canvas.getContext('2d');

    context.rotate(Math.PI / 2); //rotate 90 degrees for landscape printing
    context.clearRect(0, -g_gift_width, g_gift_height, g_gift_width);
    context.drawImage($('#cert_background').get(0), 0, -g_gift_width, g_gift_height, g_gift_width);
    context.fillStyle = 'rgba(255, 255, 255, 0.5)';
    context.fillRect(0, 0, g_gift_height, g_gift_width);
    context.fillStyle = 'rgba(0, 0, 0, 1.0)';

    // draw water mark
    //context.drawImage($('#wmark').get(0), 0, 0);
    //context.drawImage($('#wmark').get(0), 256, 324);

    // draw serial number
    context.textAlign = 'right';
    context.textBaseline = 'top';
    context.font = 'normal normal normal 128px "Arial", sans-serif';
    context.fillText(amount, g_gift_height -fudge1 , -g_gift_width+fudge1);

    context.textAlign = 'left';
    context.textBaseline = 'bottom';
    context.font = 'normal normal normal 128px "Arial", sans-serif';
    context.fillText(amount, 0+fudge1 , 0-fudge1);


    context.textAlign = 'left';
    context.textBaseline = 'top';
    context.font = 'normal normal normal 36px "Times New Roman", serif';
    context.fillText("Plancha Money", 0+fudge2, -g_gift_width+fudge2);

    context.font = 'normal normal normal 24px  "Times New Roman", serif';
    context.textAlign = 'center';
    context.textBaseline = 'middle';
    context.fillText("Use At: ", g_gift_height * 5/6, -g_gift_width/2 + 24);
    context.fillText("931 Franklin Ave.", g_gift_height * 5/6, -g_gift_width/2 +24*2);
    context.fillText("Garden City, NY", g_gift_height * 5/6, -g_gift_width/2 +24*3);

    //put it back like it was so next time this func is called it will not rotate already rotated context further
    context.rotate(-Math.PI / 2);

    //
    // print
    //

    // create print object
    var url = 'http://' + g_config.printer.ipaddr + '/cgi-bin/epos/service.cgi?devid=' + 
                g_config.printer.devid + '&timeout=' + g_config.printer.timeout;
    var epos = new epson.CanvasPrint(url);

    // register callback function
    epos.onreceive = function (res) {
        // print failure
        if (!res.success) {
          alert('Print Failure\ncode: '+
            res.code+'\nstatus: '+
            res.status+'\nbattery: '+
            res.battery+'\nprintjobid: '+
            res.printjobid);
        }
    }

    // register callback function
    epos.onerror = function (err) {
        // show error message
        alert('Print Failure\nstatus: '+ err.status+ '\n'+err.responseText);
    }

    var layout = true;
    var grayscale = false;

    // paper layout
    if (layout) {
        epos.paper = epos.PAPER_RECEIPT;
        epos.layout = { width: 580 };
    }

    // print
    if (grayscale) {
        epos.mode = epos.MODE_GRAY16;
    }
    else {
        epos.mode = epos.MODE_MONO;
        epos.halftone = epos.HALFTONE_ERROR_DIFFUSION;
    }
    epos.cut = true;
    epos.print(canvas);

    // set next serial number
    //serial = serial % 999999 + 1;
}
