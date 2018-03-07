google.charts.load('current', { 'packages': ['corechart'] });
google.charts.setOnLoadCallback(drawChart);

function drawChart() {
    var data = google.visualization.arrayToDataTable([
      ['CoinWeight', 'CoinHeight'],
      [8, 12],
      [4, 5.5],
      [11, 14],
      [4, 5],
      [3, 3.5],
      [6.5, 7]
    ]);

    var options = {
        title: 'Height & Weight comparison',
        hAxis: { title: 'Height', minValue: 0, maxValue: 15 },
        vAxis: { title: 'Weight', minValue: 0, maxValue: 15 },
        legend: 'none',
        backgroundColor: { fill: '#515359' }
    };

    var chart = new google.visualization.ScatterChart(document.getElementById('scatchart_div'));

    chart.draw(data, options);
}