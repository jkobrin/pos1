
function majority_toggle_child_checkboxes(node) {

  var checked_boxes = node.querySelectorAll('input[type="checkbox"]:checked');
  var unchecked_boxes = node.querySelectorAll('input[type="checkbox"]:not(:checked)');
  
  if (checked_boxes.length > unchecked_boxes.length) {
    for (let checkbox of checked_boxes) { checkbox.checked = false; }
  } else {  
    for (let checkbox of unchecked_boxes) { checkbox.checked = true; }
  }  
}
