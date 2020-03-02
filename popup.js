function summarize(input) {
	chrome.tabs.executeScript(null, {
	    text: 'var text ='+ JSON.stringify(input)
	},
{ file: "jquery-2.2.js" }, function() {
	    chrome.tabs.executeScript(null, { file: "content.js" });
	});
}
// var userinput = document.getElementById('userinput');
// var userinput = document.getElementById('userinput').value;
// console.log(userinput);
// // let userinput = select('#userinput');
// document.getElementById('clickme').addEventListener('click', summarize);

document.addEventListener('DOMContentLoaded', documentEvents  , false);

function myAction(input) { 
    console.log("input value is : " + input.value);
    alert("The entered data is : " + input.value);
    // do processing with data
    // you need to right click the extension icon and choose "inspect popup"
    // to view the messages appearing on the console.
}

function documentEvents() {    
  document.getElementById('clickme').addEventListener('click', 
    function() { summarize(document.getElementById('input_textbox'));
  });

  // you can add listeners for other objects ( like other buttons ) here 
}