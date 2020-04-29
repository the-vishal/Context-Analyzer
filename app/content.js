function summarize(train_data){
	alert("Generating summary highlights. This may take up to 30 seconds depending on length of article.");
	function unicodeToChar(text) {
		return text.replace(/\\u[\dA-F]{4}/gi, 
		      function (match) {
		           return String.fromCharCode(parseInt(match.replace(/\\u/g, ''), 16));
		      });
	}

	// capture all text
	var textToSend = document.body.innerText;
	var settings = {
	  "async": true,
	  "crossDomain": true,
	  "url": "http://127.0.0.1:5000/analyze",
	  "method": "POST",
	  "headers": {
	    "content-type": "application/json"
	  },
	  "article": JSON.stringify(train_data),
	  "test_data": JSON.stringify(target_data)
	}

	$.ajax(settings).done(function (response) { 
		$.each(response, function( index, value ) {
			value = unicodeToChar(value).replace(/\\n/g, '');
			document.body.innerHTML = document.body.innerHTML.split(value).join('<span style="background-color: #fff799;">' + value + '</span>');
		});
	 })

}


window.addEventListener('load', function load(event){
var createButton = document.getElementById('clickme');
createButton.addEventListener('click', function() { summarize(document.getElementById('input_textbox').value); });
})
