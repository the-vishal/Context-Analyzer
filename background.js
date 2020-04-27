if(config!=undefined){
	function Hilitor(tag)
	{
		  // private variables
		  var targetNode = document.body;
		  var hiliteTag = tag || "MARK";
		  var skipTags = new RegExp("^(?:" + hiliteTag + "|SCRIPT|FORM|SPAN)$");
		  var colors = ["#ff6", "#a0ffff", "#9f9", "#f99", "#f6f"];
		  var wordColor = [];
		  var colorIdx = 0;
		  var matchRegExp = "";
		  var openLeft = false;
		  var openRight = false;

		  // characters to strip from start and end of the input string
		  var endRegExp = new RegExp('^[^\\w]+|[^\\w]+$', "g");

		  // characters used to break up the input string into words
		  var breakRegExp = new RegExp('[^\\w\'-]+', "g");

		  this.setEndRegExp = function(regex) {
		    endRegExp = regex;
		    return endRegExp;
		  };

		  this.setBreakRegExp = function(regex) {
		    breakRegExp = regex;
		    return breakRegExp;
		  };

		  this.setMatchType = function(type)
		  {
		    switch(type)
		    {
		      case "left":
		        this.openLeft = false;
		        this.openRight = true;
		        break;

		      case "right":
		        this.openLeft = true;
		        this.openRight = false;
		        break;

		      case "open":
		        this.openLeft = this.openRight = true;
		        break;

		      default:
		        this.openLeft = this.openRight = false;

		    }
		  };

		  this.setRegex = function(input)
		  {
		    input = input.replace(endRegExp, "");
		    input = input.replace(breakRegExp, "|");
		    input = input.replace(/^\||\|$/g, "");
		    if(input) {
		      var re = "(" + input + ")";
		      if(!this.openLeft) {
		        re = "\\b" + re;
		      }
		      if(!this.openRight) {
		        re = re + "\\b";
		      }
		      matchRegExp = new RegExp(re, "i");
		      return matchRegExp;
		    }
		    return false;
		  };

		  this.getRegex = function()
		  {
		    var retval = matchRegExp.toString();
		    retval = retval.replace(/(^\/(\\b)?|\(|\)|(\\b)?\/i$)/g, "");
		    retval = retval.replace(/\|/g, " ");
		    return retval;
		  };

		  // recursively apply word highlighting
		  this.hiliteWords = function(node)
		  {
		    if(node === undefined || !node) return;
		    if(!matchRegExp) return;
		    if(skipTags.test(node.nodeName)) return;

		    if(node.hasChildNodes()) {
		      for(var i=0; i < node.childNodes.length; i++)
		        this.hiliteWords(node.childNodes[i]);
		    }
		    if(node.nodeType == 3) { // NODE_TEXT
		      if((nv = node.nodeValue) && (regs = matchRegExp.exec(nv))) {
		        if(!wordColor[regs[0].toLowerCase()]) {
		          wordColor[regs[0].toLowerCase()] = colors[colorIdx++ % colors.length];
		        }

		        var match = document.createElement(hiliteTag);
		        match.appendChild(document.createTextNode(regs[0]));
		        match.style.backgroundColor = wordColor[regs[0].toLowerCase()];
		        match.style.color = "#000";

		        var after = node.splitText(regs.index);
		        after.nodeValue = after.nodeValue.substring(regs[0].length);
		        node.parentNode.insertBefore(match, after);
		      }
		    };
	  };

	  // remove highlighting
	  this.remove = function()
	  {
	    var arr = document.getElementsByTagName(hiliteTag);
	    while(arr.length && (el = arr[0])) {
	      var parent = el.parentNode;
	      parent.replaceChild(el.firstChild, el);
	      parent.normalize();
	    }
	  };

	  // start highlighting at target node
	  this.apply = function(input)
	  {
	    this.remove();
	    if(input === undefined || !(input = input.replace(/(^\s+|\s+$)/g, ""))) {
	      return;
	    }
	    if(this.setRegex(input)) {
	      this.hiliteWords(targetNode);
	    }
	    return matchRegExp;
	  };

	}

	// function unicodeToChar(text) {
	// 	alert("Generating summary highlights. This may take up to 30 seconds depending on length of article.");
	// 	return text.replace(/\\u[\dA-F]{4}/gi, 
	// 	function (match) {
	// 		return String.fromCharCode(parseInt(match.replace(/\\u/g, ''), 16));
	//     });
	// }
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
	      	var myHilitor = new Hilitor();
  			myHilitor.apply(this.responseText);
	  	//for (var key in this.responseText) {
			// 	value = unicodeToChar(value).replace(/\\n/g, '');
			// document.body.innerHTML = document.body.innerHTML.split(value).join('<span style="background-color: #fff799;">' + value + '</span>');
			// }
    	}
  	};
  	
  	var post_data = JSON.stringify({"article":encodeURIComponent(TrainData),"test_data":encodeURIComponent(TargetData)});
  	xhttp.open(settings.method, settings.url, settings.async);
	xhttp.setRequestHeader("Content-type", "application/json");
	xhttp.send(post_data);
}

