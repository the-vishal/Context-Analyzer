if(config!=undefined){
	function unicodeToChar(text) {
		alert("Generating summary highlights. This may take up to 30 seconds depending on length of article.");
		return text.replace(/\\u[\dA-F]{4}/gi, 
		function (match) {
			return String.fromCharCode(parseInt(match.replace(/\\u/g, ''), 16));
	    });
	}
  console.log(config);
  console.log(document.body.innerText)
  let TrainData = document.innerText;
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

  	var post_data = "article="+JSON.stringify(TrainData)+"&test_data="+JSON.stringify(TargetData);
  	xhttp.open(settings.method, settings.url, settings.async);
	xhttp.setRequestHeader("Content-type", "application/json");
	xhttp.send(post_data);

	 var xhttp = new XMLHttpRequest();
 	 xhttp.onreadystatechange = function() {
    	if (this.readyState == 4 && this.status == 200) {
	      	// this.responseText
	      	$.each(response, function( index, value ) {
			value = unicodeToChar(value).replace(/\\n/g, '');
			document.body.innerHTML = document.body.innerHTML.split(value).join('<span style="background-color: #fff799;">' + value + '</span>');
			});
    	}
  	};
  	


	// $.ajax(settings).done(function (response) { 
	// $.each(response, function( index, value ) {
	// 	value = unicodeToChar(value).replace(/\\n/g, '');
	// 	document.body.innerHTML = document.body.innerHTML.split(value).join('<span style="background-color: #fff799;">' + value + '</span>');
	// 	});
	//  })
}

