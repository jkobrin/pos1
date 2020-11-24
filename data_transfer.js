
/********** data transfer utils *************/
function format_http_params(params)
{
  var ret = [];
  for (var p in params){
    ret.push(encodeURIComponent(p) + '=' + encodeURIComponent(params[p]));
  }  
  return ret.join('&');
}

function http_request(method, url, params)
{
  var http = new XMLHttpRequest();

  if(method == "GET")
  {
    // append timestamp to url to prevent caching
    url += "?timestamp=" + new Date().getTime();

    if (params) {url += "&" + params;}
    http.open(method, url, false);
    http.send(null);
  }
  else
  {
    http.open(method, url, false);
    http.setRequestHeader("Content-Type", "application/x-www-form-urlencoded"); 
    http.send(params);
  }

 var response = http.responseText;

 if (http.status != 200)  {
    // Display error message on page
   document.write("Error getting config\n\n");
   document.write(http.status + '\n');
   document.write(http.readyState);
   document.write(response);
   return;
 }

 return eval('(' + response + ')');
}  

function async_http_request(method, url, params, callback)
{

  var http = new XMLHttpRequest();

  http.onreadystatechange = function ()
  {
    if (http.readyState != 4) {return;} //request is not complete

    var response = http.responseText;

    if (http.status != 200)  {
    // Display error message on page
      document.write("Error getting config\n\n");
      document.write(http.status + '\n');
      document.write(http.readyState);
      document.write(response);
      return;
    }

    callback( eval('(' + response + ')') );
  }

  if(method == "GET")
  {
    // append timestamp to url to prevent caching
    url += "?timestamp=" + new Date().getTime();

    if (params) {url += "&" + params;}
    http.open(method, url, true);
    http.send(null);
  }
  else
  {
    http.open(method, url, true);
    http.setRequestHeader("Content-Type", "application/x-www-form-urlencoded"); 
    http.setRequestHeader("Content-length", params.length);
    http.setRequestHeader("Connection", "close");
    http.send(params);
  }
}  


