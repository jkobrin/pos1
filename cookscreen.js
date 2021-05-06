
EXPECTED_COOK_TIME = 20 * 60 //20 minutes
TIME_TO_SHOW_DELIVERED = 15; //15 seconds

function format_time(time) {
   
   var timediff = Math.round((now() - time)/60) //difference in minutes;
   if (Math.abs(timediff) < 60 /* 1 hour */) {
    result = timediff + 'm';
   }
   else if(Math.abs(timediff) < 60*4) /* 4 hours */ {
    if (timediff > 0) { var hour = Math.floor(timediff/60);}
    else if (timediff < 0) { var hour = Math.ceil(timediff/60);}
    var minute = Math.abs(timediff - hour*60);
    result = hour +'h ' + minute +'m';
   }
   else {
    result = new Date(time*1000).toLocaleTimeString('en-US', {weekday: 'short', hour: '2-digit', minute: '2-digit'});
    result += '\n' + new Date(time*1000).toLocaleDateString('en-US', {month: 'short', day: '2-digit', year: 'numeric'});
   }

   if (timediff > 0){result = '+'+result;}
   return result;
}

function get_order_items()
{
  items_list = [];
  
  for (var key in g_order_pane_items)
  {
    var item = g_order_pane_items[key];

    if (item.parent_item != null || 
        item.delivery_status == DELIVERY_STATUS_DELIVERED && now() - item.mod_time > TIME_TO_SHOW_DELIVERED
    )
    {
      continue;
    }  

    if (item.created_time == null)
    {
      item.time_display = '---';
      item.time_category = "Not sent yet";
      item.expected_ready_time = 8640000000000000; //most distant future, so it will sort last
    }
    else
    {
      item.time_display = 
        item.pickup_time > 0? 'P'+ format_time(item.pickup_time) : format_time(item.created_time)
      
      if (item.mod_time - item.created_time > 60 ){
        item.time_display +=  ' ~'+Math.floor((now() - item.mod_time)/60);
      }

      if(item.pickup_time){
        item.expected_ready_time = item.pickup_time;
      }
      else if(item.delivery_status == DELIVERY_STATUS_HELD) {
        item.expected_ready_time = now() + EXPECTED_COOK_TIME;
      }
      else {
        item.expected_ready_time = item.created_time + EXPECTED_COOK_TIME;
      }

      var hours_away = (item.expected_ready_time - now()) / 60 / 60;
      if (Math.abs(hours_away) < 24 && new Date(item.expected_ready_time*1000).getDay() == new Date().getDay() ||
        Math.abs(hours_away) < 4 )
      {
        item.time_category = "Today";
      }
      else if (hours_away > 0)
      {
        item.time_category = "Future";
      }  
      else
      {
        item.time_category = "Past";
      }  
    }

    items_list.push(item);
  }
  
  items_list.sort(function(a,b){return a.expected_ready_time - b.expected_ready_time});

  return items_list;
}  

function cookscreen_table_click(table_id)
{
  //window.sessionStorage.setItem('g_currentTable', table_id);
  //window.open("pos.htm", '_self');
  set_current_table(table_id);
  go_to_screen('main_screen');
}

function cookscreen_timeclick(item_id)
{
  var item = get_order_pane_item(item_id);
  if (item.is_cancelled || item.is_open == false) {return;}
  move_delivery_status(item.id, -1);
}

function cookscreen_click(item_id)
{
  var item = get_order_pane_item(item_id);
  if (item.is_cancelled || item.is_open == false) {return;}
  move_delivery_status(item.id, +1);
}

function move_delivery_status(item_id, direction)
{
  var items = get_item_and_child_items(item_id);
  var main_item = items[0];
  var newstatus = main_item.delivery_status + direction;
  if (newstatus > MAX_DELIVERY_STATUS) {newstatus = MAX_DELIVERY_STATUS - 1;} //go the other way instead
  else if (newstatus < MIN_DELIVERY_STATUS) {return;} //do nothing
  
  items.forEach(function(item)
  {
    new_crud_command({command: "set_status", item_id: item.id, field: 'delivery_status', value: newstatus});
  })
}

function refresh_cook_screen()
{
  var current_time_category = null;

  cook_tables_div = document.getElementById("cook_tables_div");

  //hide all time cat divs they will be made visible again if
  //and when they have items put in them
  var time_cat_divs = cook_tables_div.getElementsByClassName("cat_div");
  for (i = 0; i < time_cat_divs.length; i++) {
    time_cat_divs[i].style.display = "none";
  }

  var items = get_order_items();
  for (var idx in items)
  {
    var item = items[idx];
    var classes = "order_item";

    var cfg_item = get_config_item_from_id(item.menu_item_id);
    if (cfg_item) {
      if (cfg_item.style) {classes += ' '+cfg_item.style}
      if (cfg_item.supercategory == 'wine' || cfg_item.supercategory=='bar') {classes += ' bev_item'}
      else if (cfg_item.category == 'cafe') {classes += ' cafe_item'}
      else if (cfg_item.category == 'boards') {classes += ' board_item'}
      else if (cfg_item.category == 'desserts') {classes += ' dessert_item'}
      else if (cfg_item.category.match(/coffee/)) {classes += ' dessert_item'}
      else if (cfg_item.category == 'allergy') {classes += ' allergy_item'}
    }
    else {
      classes += ' header_item';
    }

    if (item.is_cancelled) {classes += ' cancelled_item'}
    if (item.is_open == false) {classes += ' closed_item'}
    if (item.is_comped) {classes += ' comped_item'}

    if (item.delivery_status == DELIVERY_STATUS_HELD) {classes += ' held_item'}
    else if (item.delivery_status == DELIVERY_STATUS_DELIVERED) {classes += ' delivered_item'}
    else if (item.delivery_status == DELIVERY_STATUS_READY) {classes += ' ready_item'}

    if (item.time_category != current_time_category){
      //new category
      current_time_category = item.time_category;

      var time_cat_cook_table_id = "time_cat_cook_table_"+item.time_category;
      var cook_table = document.getElementById(time_cat_cook_table_id);

      if (cook_table != null) {
        //clear old items and in prepartion for the new items
        cook_table.innerHTML = "";

        //this time category div could be in wrong order now.
        //We'll remove each and reattatch it as we go to
        //ensure propper order as given by sorted items
        //then make it visible again
        var tc_div = document.getElementById("time_cat_div_"+item.time_category);
        cook_tables_div.removeChild(tc_div);
        cook_tables_div.appendChild(tc_div);
        tc_div.style.display = 'inline';
      }
      else {
        // if a cook_table doesn't already exist for this
        // category, then make one along with it's various
        // containing divs which should not exist either   

        console.log("no cook table: " + time_cat_cook_table_id + " Creating..");
        cat_div = document.createElement('div');
        cat_div.id = "time_cat_div_"+item.time_category;
        cat_div.setAttribute("class", "cat_div");
        cook_tables_div.appendChild(cat_div);
        var cat_head_div = document.createElement('div');
        cat_head_div.setAttribute("class", "supercat_head");
        cat_head_div.textContent = item.time_category;
        cat_div.appendChild(cat_head_div);
        var cat_content_div = document.createElement('div');
        cat_content_div.id = 'cat_cd_'+item.time_category;
        cat_content_div.setAttribute("class", "supercat_content_div");
        cat_div.appendChild(cat_content_div);
        cat_head_div.onclick = make_closure(toggle_vis, cat_content_div);
        var cook_table = document.createElement('table');
        cook_table.id = time_cat_cook_table_id;
        cook_table.setAttribute("class", "cook_table");
        cook_table.setAttribute("cellpadding", 2);
        cook_table.setAttribute("cellspacing", 2);
        cat_content_div.appendChild(cook_table);
      }
    }

    //add new item to current cook_table
    var table_row = document.createElement('tr');
    table_row.setAttribute('class', classes);

    if (cfg_item && cfg_item.cssstyle) {
      table_row.setAttribute('style', cfg_item.cssstyle);
    }

    var tab_col = document.createElement('td');
    tab_col.textContent = item.table_id;
    tab_col.onclick = make_closure(cookscreen_table_click, item.table_id);
    table_row.appendChild(tab_col);

    var name_col = document.createElement('td');
    name_col.innerHTML = item.item_name + '<i>' + get_add_on_string_for(item.id) +'</i>';
    name_col.onclick = make_closure(cookscreen_click, item.id);
    if (cfg_item && cfg_item.id){
      name_col.oncontextmenu = make_closure(context_tool_tip, {'button': name_col, 'item': cfg_item});
    }  
    table_row.appendChild(name_col);

    var time_col = document.createElement('td');
    time_col.setAttribute('class', 'time_display');
    time_col.textContent = item.time_display;
    time_col.onclick = make_closure(cookscreen_timeclick, item.id);
    table_row.appendChild(time_col);

    cook_table.appendChild(table_row);
  }  
}

