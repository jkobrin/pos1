MAIN_REFRESH_INTERVAL = 10000; //10 seconds

g_crud_commands = [];
g_order_pane_items = null;

function new_crud_command(command)
{
  g_crud_commands.push(command);
  apply_crud_command(command);
}

function apply_crud_command(command)
{
  console.log('apply crud ' + JSON.stringify(command));
  if (command.command == "add_item")
  {
    g_order_pane_items[command.item_id] = {
      item_name: command.item_name,
      table_id: command.table_id, 
      id: command.item_id,
      delivery_status: command.delivery_status, 
      is_comped: command.is_comped, 
      price: command.price, 
      taxable: command.taxable,
      parent_item: command.parent_item,
      time_category: "Not Sent Yet", pickup_time: null, created_time: null}
  }

  if (command.command == "cancel_item")
  {
    var item = get_order_pane_item(command.item_id);
    if (item) { // item may have been removed by update
      item.is_cancelled = true;
    }  
  }  

  if (command.command == "set_status")
  {
    var item = get_order_pane_item(command.item_id);
    if (item) { // item may have been removed by update
      item[command.field] = command.value;
      item.mod_time = now();
    }
  }

  refresh_screen();
}

g_synchonize_timeout = null;
function synchronize_now()
{
  clearTimeout(g_synchonize_timeout);
  synchronize(async=false);
}

var g_in_transit_crud_commands = null;
var g_last_server_contact = 0;
var g_last_update_time = null;
function handle_fresh_items(data)
{
  console.log('instruction: ' + data.instruction)
  if (data.instruction == 'reload')
  {
    // this could lose some recently entered data but it's not
    // worth dealing with since this should be like a fraction
    // of a second's worth of data entry and will happen rarely and
    // the user will probably have a clue that their data may
    // not have been sent when they see everything suddenly reset

    location.reload();
    return;
  }

  console.log('fresh items. Update time:' + data.time);
  g_last_server_contact = now();
  g_in_transit_crud_commands = null; //release these. they have been handled
  g_last_update_time = data.time;

  if (data.config) {console.log('new config'); g_config = data.config; refresh_button_board();}

  if (data.update_type == 'replace')
  {
    console.log('replace data items');
    console.log("# of items: "+Object.keys(data.items).length);
    g_order_pane_items = data.items;

  }
  else //update
  {
    console.log('incremental update data items');
    //console.log("# of items: "+Object.keys(data.items).length);
    for (var key in data.items)
    {
      console.log(data.items[key]);
    }  

    //first remove old items that were marked cancelled
    //in previous update. They had the chance to be
    //seen as 'dead' for one update interval. They will not
    //be in this new data
    for(var key in g_order_pane_items)
    {
      if (g_order_pane_items[key].is_cancelled)
      {
        delete g_order_pane_items[key];
      }
    }

    // now update g_order_pane_items with new items
    // Object.assign(g_order_pane_items, data.items);
    for(var key in data.items)
    {
      g_order_pane_items[key] = data.items[key];
    }  

    // now remove items that are marked closed, so closing
    // disappears items immediately
    for(var key in g_order_pane_items)
    {
      if (g_order_pane_items[key].is_open == false)
      {
        delete g_order_pane_items[key];
      }
    }
  }

  for(var idx in g_crud_commands)
  {
    apply_crud_command(g_crud_commands[idx]);
  }

  refresh_screen();
  //clearTimeout(g_synchonize_timeout);
  g_synchonize_timeout = setTimeout(synchronize, MAIN_REFRESH_INTERVAL);
}

function ajax_error(jqXHR, textStatus, errorThrown) {
  if (g_in_transit_crud_commands != null) {
    //put in transit objects back at from of queue, they need to be tried again
    g_crud_commands = g_in_transit_crud_commands.concat(g_crud_commands);
    g_in_transit_crud_commands = null;
  }  

  if (errorThrown != ''){
    g_synchonize_timeout = setTimeout(synchronize, MAIN_REFRESH_INTERVAL);
    document.write("<p>"+textStatus + ":w:w:" + errorThrown + "</p>" + jqXHR.responseText);
    clearTimeout(g_synchonize_timeout);
  }
  else
  { //probably network error. Silently try again in 1 minute
    g_synchonize_timeout = setTimeout(synchronize, MAIN_REFRESH_INTERVAL);
    //message_box.innerHTML = '----- ' + min_since_last_contact  + ' min. since server contact -------';
  }  
}

function synchronize(async)
{
  if (typeof(async) === 'undefined') {async = true} //substitue for default args which is not supported on chrome browser

  var crud_commands = JSON.stringify(g_crud_commands); 
  g_in_transit_crud_commands = g_crud_commands;
  g_crud_commands = [];

  console.log('async: ' + async + ' sending: ' + crud_commands);
  $.ajax({ url: "action.py/synchronize", type: "POST", dataType: "json", cache: false, async: async,
    data: {crud_commands : crud_commands, last_update_time: JSON.stringify(g_last_update_time)},
    success: handle_fresh_items, error: ajax_error });
}

function get_order_pane_item(item_id)
{
  console.log('get_order_pane_item: '+item_id);
  for (idx in g_order_pane_items)
  {
    var item = g_order_pane_items[idx];
    if (item.id == item_id)
    {
      return item;
    }
  }
  console.log('get_order_pane_item id not found: '+item_id);
}


function get_child_items(item_id)
{
  child_items = [];
  for (var idx in g_order_pane_items)
  {
    var item = g_order_pane_items[idx];
    if (item.parent_item == item_id)
    {
      child_items.push(item);
    }
  }  
  return child_items;
}  

function get_item_and_child_items(item_id)
{
  items = [];
  for (var idx in g_order_pane_items)
  {
    var item = g_order_pane_items[idx];
    if (item.id == item_id || item.parent_item == item_id)
    {
      items.push(item);
    }
  }  
  return items;
}  

function get_add_on_string_for(item_id)
{
  add_on_string = "";
  child_items = get_child_items(item_id);
  for (var idx in child_items)
  {
    if(child_items[idx].is_cancelled ){
      //TODO: show cancelled items as cancelled
      //var style_class = child_items[idx].is_cancelled ? 'cancelled_item' : null;
    } else
    {
      add_on_string += ", " + child_items[idx].item_name;
    }
  }
  return add_on_string;
}


