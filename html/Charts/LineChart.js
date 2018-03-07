google.charts.load('current', {'packages':['corechart']});
google.charts.setOnLoadCallback(drawChart);

function drawChart() {
    var data = google.visualization.arrayToDataTable([
      ['Session', '€2.00', '€1.00', '€0.50', '€0.20', '€0.10'],
      ['1', 4, 3, 8, 6, 10],
      ['2', 6, 2, 8, 9, 1],
      ['3', 2, 2, 1, 3, 7],
      ['4', 9, 11, 8, 5, 2]
    ]);

    var options = {
        title: 'Volume of Coins over Sessions',
        curveType: 'function',
        backgroundColor: { fill: '#515359' },
        legend: { position: 'bottom' }
    };

    var chart = new google.visualization.LineChart(document.getElementById('curve_chart'));

    chart.draw(data, options);
}
