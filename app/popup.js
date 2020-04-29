function summarize(TargetData) {
let Target = JSON.stringify(TargetData);
	chrome.tabs.executeScript({
	code: 'var config='+Target
	}, function() {
	    chrome.tabs.executeScript({file: 'background.js'})
	});
}

window.addEventListener('load', function load(event){
	var createButton = document.getElementById('AnalyzeMe');
	createButton.addEventListener('click', function() { summarize(document.getElementById('TargetData').value); });
})