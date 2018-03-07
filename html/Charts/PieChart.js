google.charts.load("current", {packages:["corechart"]});
google.charts.setOnLoadCallback(drawChart);
function drawChart() {
	
    var data = google.visualization.arrayToDataTable([
      ['Coins', 'This Session'],
      ['€2.00', 13], ['€1.00', 3], ['€0.50', 14],
      ['€0.20', 23], ['€0.10', 6], ['Misc', 30]
    ]);

    var options = {
        title: 'Coins Per Current Session',
        legend: 'none',
        pieSliceText: 'label',
        backgroundColor: { fill: '#515359'},
        slices: {  4: {offset: 0.2},
            2: {offset: 0.3},
            0: {offset: 0.1}
        },
    };

    var chart = new google.visualization.PieChart(document.getElementById('piechart'));
    chart.draw(data, options);
}
/*$(document).ready(function(input){
	$.get('index.html', function(){
    	var x = $(input).find("#2Count")
    	alert(x)
    });
    alert("Work")
})*/