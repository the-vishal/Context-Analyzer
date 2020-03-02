alert("Generating summary highlights. This may take up to 30 seconds depending on length of article.");

console.log("1,",text)
function unicodeToChar(text) {
	return text.replace(/\\u[\dA-F]{4}/gi, 
	      function (match) {
	           return String.fromCharCode(parseInt(match.replace(/\\u/g, ''), 16));
	      });
}

// capture all text
var textToSend = document.body.innerText;

// console.log(textToSend);
// summarize and send back
var api_url = 'http://127.0.0.1:5000/analyze';
	// let userinput = select('#userinput');
	// console.log(userinput);
var post_data = {
					"data":textToSend,
				};
var settings = {
  "async": true,
  "crossDomain": true,
  "url": "http://127.0.0.1:5000/analyze",
  "method": "POST",
  "headers": {
    "content-type": "application/json"
  },
  "data": JSON.stringify(post_data)
}

$.ajax(settings).done(function (response) { 
	$.each(response, function( index, value ) {
		value = unicodeToChar(value).replace(/\\n/g, '');
		document.body.innerHTML = document.body.innerHTML.split(value).join('<span style="background-color: #fff799;">' + value + '</span>');
	});
 })