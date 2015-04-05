


function http_request(method, url, params)
{
  http = new XMLHttpRequest();
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
    http.setRequestHeader("Content-length", params.length);
    http.setRequestHeader("Connection", "close");
    http.send(params);
  }

  response = http.responseText;

  if (http.status != 200)  {
  // Display error message on page
    document.write("Error getting config\n\n");
    document.write(response);
    return;
  }

  return eval('(' + response + ')');
}  


