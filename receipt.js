function close_check(shouldPrint)
{
  response = http_request("POST", "close_tab.py", 
    "table="+g_currentTable+
    "&serverpin="+g_pin
  );

  if (response == null){
    console.log('null response from close_tab');
    leave_receipt_screen();
    return;
  }  

  if (response.success){
    if (shouldPrint) {
      if (g_config.printer.type == "epson") {
        epos_print(response.receipt_text, g_config.printer);
      } else if (g_config.printer.type == "webprint"){
        web_print(response.receipt_text, g_config.printer);
      } else if (g_config.printer.type == "NONE") {
        console.log("unknow printer type: " + g_config.printer.type);
      }
    }

    for (gci in response.gift_certs){
      if (g_config.printer.type == "epson") {
        epos_print_image(response.gift_certs[gci], g_config.printer);
      } else if (g_config.printer.type == "webprint"){
        web_print_image(response.gift_certs[gci], g_config.printer);
      } else {
        console.log("unknow printer type: " + g_config.printer.type);
      }
    }

    synchronize_now();
  }
  else{
    alert(response.message);
  }  
  go_to_screen('main_screen');
}

g_tab_to_move = null;
function move_tab()
{
  g_tab_to_move = g_currentTable;
  go_to_screen('main_screen');
}

function toggle_paid()
{
  var new_paid = !table_is_paid(g_currentTable);

  $.ajax({ url: "close_tab.py/set_paid", type: "POST", dataType: "json", cache: false, async: false,
    data: {table:g_currentTable, val: new_paid, serverpin: g_pin},
    error: ajax_error}
  );

  synchronize_now();
  receipt_screen_init();
}

function get_date_string(dat)
{
  var y= dat.getFullYear();
  var m = dat.getMonth()+1;
  if(m<10) m="0"+m;
  var dt = dat.getDate();
  if(dt<10) dt = "0"+dt;
  return y+"-"+m+"-"+dt;
}


function get_time_string(dat)
{
  var h= dat.getHours();
  var m = dat.getMinutes();
  if(h<10) h="0"+h;
  if(m<10) m = "0"+m;
  return h+":"+m;
}


function set_pickup()
{
  pt_popup = document.getElementById("date_time_popup");

  var date_time_popup_caption = document.getElementById("date_time_popup_caption");

  var pickup_time = table_pickup_time(g_currentTable);


  if (pickup_time != null){
    //populate input controls with whatever time was previously set for pickup
    var populate_date = new Date(pickup_time*1000);
    date_time_popup_caption.innerHTML = "table: "+ g_currentTable + " pickup time :"+populate_date;
  }else{
    date_time_popup_caption.innerHTML = "table: "+ g_currentTable + " pickup time : None";
    //populate with reasonable default: now +
    //DEFAULT_PICKUP_MINUTES, which should be like, 30-ish, I
    //would think
    var populate_date = new Date();
    populate_date.setMinutes(populate_date.getMinutes()+DEFAULT_PICKUP_MINUTES); 
  }  

  //populate the pickup date/time input controls with the
  //chosen default
  document.getElementById("pdate").value = get_date_string(populate_date);
  document.getElementById("ptime").value = get_time_string(populate_date);

  pt_popup.style.visibility="visible";
  pt_popup.focus();
}

function set_pickup_done()
{
  var pdate = document.getElementById("pdate").value;
  var ptime = document.getElementById("ptime").value;

  if (pdate == null || pdate =='')
  {
    alert('set valid date');
    document.getElementById("pdate").focus();
    return;
  } 

  if (ptime == null || ptime =='')
  {
    alert('set valid time');
    document.getElementById("ptime").focus();
    return;
  } 

  $.ajax({ url: "close_tab.py/set_pickup", type: "POST", dataType: "json", cache: false, async: true,
    data: {table:g_currentTable, val: pdate +' '+ ptime},
    error: ajax_error}
  );

  synchronize_now();

  pt_popup.style.visibility="hidden";
  receipt_screen_init();
}

function set_pickup_cancel()
{
  pt_popup.style.visibility="hidden";
}

function receipt_screen_init()
{
  var receipt_text = http_request("POST", "texttab.py", "table="+g_currentTable);
  receipt_table.innerHTML = "<pre id='receipt_text'>" + receipt_text + "<\pre>";
  var paid = table_is_paid(g_currentTable);
  receipt_table.style.backgroundColor = paid ? 'aqua': 'white';
  document.getElementById('paid').innerHTML = table_is_paid(g_currentTable) ? 'Mark Unpaid' : 'Mark Paid';
}
