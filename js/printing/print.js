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

