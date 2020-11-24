
function load_config()
{
  g_config = http_request("GET", "config.py/get", null);
}

 /******* lookup *************/
function get_config_item_from_id(menu_item_id)
{
  if (menu_item_id == null) { return null;}
  for(var supercat_idx in g_config.menu.supercategories)
  {
    var supercat = g_config.menu.supercategories[supercat_idx];
    for(var cat_idx in supercat.categories)
    {
      var cat = supercat.categories[cat_idx];
      for(var cfg_item_idx in cat.items)
      {
        var cfg_item  = cat.items[cfg_item_idx];
        if (cfg_item.id == menu_item_id)
        {
          return cfg_item;
        }
      }
    }
  }
  return null;
}


function get_config_item(item_name)
{
  console.log('get_config_item ' + item_name);
  if (item_name == null || item_name == '')
  {
    return null;
  }
  for(cat_idx in g_config.menu.supercategories)
  {
    var cat = g_config.menu.supercategories[cat_idx];
    for(subcat_idx in cat.categories)
    {
      var subcat = cat.categories[subcat_idx];
      for(item_idx in subcat.items)
      {
        var citem = subcat.items[item_idx];
        if (citem.name == item_name || citem.upc == item_name)
        {
          citem.cat = cat.name;
          citem.subcat = subcat.name;
          return citem;
        }
      }
    }
  }
}

