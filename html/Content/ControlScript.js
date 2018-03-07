$(document).ready(function(){
setInterval(function(){
    var twoC = $("#2Count").text();
    var twoT = twoC * 2;
    $("#Total2s").text("€"+twoT);
    /*console.log("twoC = " + twoC)
    console.log("twoT = " + twoT)*/
    
    var oneC = $("#1Count").text();
    var oneT = oneC * 1;
    $("#Total1s").text("€"+oneT);
    /*console.log("oneC = " + oneC)
    console.log("oneT = " + oneT)*/
    
    var fiftyC = $("#50Count").text();
    var fiftyT = fiftyC * .5;
    $("#Total50s").text("€"+fiftyT);
    /*console.log("fiftyC = " + fiftyC)
    console.log("fiftyT = " + fiftyT)*/
    
    var twentyC = $("#20Count").text();
    var twentyT = twentyC * .2;
    $("#Total20s").text("€"+twentyT);
    /*console.log("twentyC = " + twentyC)
    console.log("twentyT = " + twentyT)*/
    
    var tenC = $("#10Count").text();
    var tenT = tenC * .1;
    $("#Total10s").text("€"+tenT);
    /*console.log("tenC = " + tenC)
    console.log("tenT = " + tenT)*/
    
    var totalCoinCountDisplay = $("#TotalCoins")
    var totalCoinCount = (twoT + oneT + fiftyT + twentyT + tenT)
    totalCoinCountDisplay.text("€"+totalCoinCount)
    }, 1000);
    
    /*var clientWidth = Math.max(window.innerWidth, document.documentElement.clientWidth)
    //alert(clientWidth)
    
    if(clientWidth < 801)
    {
    	$("#x").append(document.createElement("a").setAttribute("href", "stats.html").text("Stats"))
    }*/
});