
function now(){return (new Date())/1000;}

function make_closure(func, arg)
{
  return function() {return func(arg)}
}

function toggle_vis(node)
{
  console.log('toggle_vis ' + node.style.display + ' ' + node.id);
  node.style.display = (node.style.display == 'inline' ? 'none' : 'inline');
}  

