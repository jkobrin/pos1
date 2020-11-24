
//<div id ="tool_tip_box" class="click_dismiss" onclick="this.style.visibility='hidden'"> </div>

function context_tool_tip(args)
{
  var tool_tip_box = document.getElementById('tool_tip_box');
  if (!tool_tip_box) {
    tool_tip_box = document.createElement('div');
    tool_tip_box.id = 'tool_tip_box';
    tool_tip_box.setAttribute('class', 'click_dismiss')
    document.body.appendChild(tool_tip_box);
  }  

  var description = args.item.description || '-no description-';
  var picture = args.item.picture;

  tool_tip_box.innerHTML = 
    '<h1>'+args.item.name+':'+args.item.price +'</h1> <pre>'+description+'</pre>';

  tool_tip_box.innerHTML += '<div><a target="inventory" href="inventory?id='+args.item.id+'">edit</a></div>';

  if (args.item.mynotes) {
    tool_tip_box.innerHTML += 
      '<pre style="width: 60%; padding-top: .5em; float:left; font-size: smaller; text-align: left">'+args.item.mynotes+'</pre>';
  }  
  if (args.item.picture) {
    tool_tip_box.innerHTML += 
      '<div style="padding-top: .5em; float:right; width: 40%"> <img width="100%" src="'+args.item.picture+'"/></div>';
  }    

  tool_tip_box.style.visibility ="visible";
  var button_rect  =  args.button.getBoundingClientRect()
  var buttonx = (button_rect.left + button_rect.right)/2;
  var buttony  = (button_rect.top + button_rect.bottom)/2;
  var docy = document.documentElement.clientHeight/2;
  tool_tip_box.style.top = Math.max(window.scrollY + button_rect.top - tool_tip_box.clientHeight, 0);

  return false;
}
