$(document).ready(function() {

     setInterval(function(){
         $.ajax({
        type: "GET",
        url: "../LocalCoinData.csv",
        dataType: "text",
        success: function(data) {processData(data);}
     });
     }, 1000); // refresh every 1000 milliseconds
});

var TwoCountG = 0;
var OneCountG = 0;
var FiftyCountG = 0;
var TwentyCountG = 0;
var TenCountG = 0;
var MiscCountG = 0;

function processData(allText) {
var TwoCount = 0;
var OneCount = 0;
var FiftyCount = 0;
var TwentyCount = 0;
var TenCount = 0;	
var MiscCount = 0;

    var oldText = allText.replace(/"/g, "");
    var newText = oldText.replace(/'/g, '"');
    var allTextLines = newText.split(/\r\n|\n/);
    
    for (var j=0; j<(allTextLines.length)-1; j++) {
            var obj = JSON.parse(allTextLines[j]);
            //console.log("CoinValue : " + obj.CoinValue)
            
            if(obj.CoinValue == "2.0")
            {
            	TwoCount++;
            	TwoCountG = TwoCount;
            }
            else if(obj.CoinValue == "1.0")
            {
            	OneCount++;
            	OneCountG = OneCount;
            }
            else if(obj.CoinValue == "0.50")
            {
            	FiftyCount++;
            	FiftyCountG = FiftyCount;
            }
            else if(obj.CoinValue == "0.20")
            {
            	TwentyCount++;
            	TwentyCountG = TwentyCount;
            }
            else if(obj.CoinValue == "0.10")
            {
            	TenCount++;
            	TenCountG = TenCount;
            }
            else if(obj.CoinValue == "Misc")
            {
            	MiscCount++;
            	MiscCountG = MiscCount;
            }
            else {console.log("Oops!")}
        }
        
        $("#2Count").text(TwoCount)
        $("#1Count").text(OneCount)
        $("#50Count").text(FiftyCount)
        $("#20Count").text(TwentyCount)
        $("#10Count").text(TenCount)
        $("#MiscCount").text(MiscCount)
        
        //alert("TwoCount = "+TwoCount)
    
    	//console.log(allText)
}