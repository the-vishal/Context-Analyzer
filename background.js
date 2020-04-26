if(config!=undefined){
	function unicodeToChar(text) {
		alert("Generating summary highlights. This may take up to 30 seconds depending on length of article.");
		return text.replace(/\\u[\dA-F]{4}/gi, 
		function (match) {
			return String.fromCharCode(parseInt(match.replace(/\\u/g, ''), 16));
	    });
	}
  let TrainData = document.body.innerText;
  let TargetData = config;
  var settings = {
	"async": true,
	"crossDomain": true,
	"url": "http://127.0.0.1:5000/analyze",
	"method": "POST",
	"headers": {
	  "content-type": "application/json"
	},
	"article": JSON.stringify(TrainData),
	"test_data": JSON.stringify(TargetData)
	}

	 var xhttp = new XMLHttpRequest();
 	 xhttp.onreadystatechange = function() {
    	if (this.readyState == 4 && this.status == 200) {
	      	console.log(this.responseText);
	      	for (var key in this.responseText) {
				value = unicodeToChar(value).replace(/\\n/g, '');
			document.body.innerHTML = document.body.innerHTML.split(value).join('<span style="background-color: #fff799;">' + value + '</span>');
			}
    	}
  	};
  	
  	var post_data = JSON.stringify({"article":encodeURIComponent(TrainData),"test_data":encodeURIComponent(TargetData)});
  	xhttp.open(settings.method, settings.url, settings.async);
	xhttp.setRequestHeader("Content-type", "application/json");
	xhttp.send(post_data);
}

