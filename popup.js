function summarize(input) {
 chrome.browserAction.onClicked.addListener(function(input) {
        chrome.tabs.executeScript(input, {file: "content.js"});
    });
}

window.addEventListener('load', function load(event){
var createButton = document.getElementById('clickme');
createButton.addEventListener('click', function() { summarize(document.getElementById('input_textbox').value); });
})

  // you can add listeners for other objects ( like other buttons ) here 