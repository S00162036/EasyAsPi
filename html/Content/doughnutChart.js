window.onload = function () {
setInterval(function(){
var chart = new CanvasJS.Chart(document.getElementById("chartContainer"), {
	theme: "dark2",
	exportFileName: "Coin Chart",
	exportEnabled: true,
	animationEnabled: false,
	title:{
		text: "Coins Counted for Current Session"
	},
	legend:{
		cursor: "pointer",
		itemclick: explodePie
	},
	data: [{
		type: "doughnut",
		innerRadius: 90,
		showInLegend: true,
		toolTipContent: "<b>{name}</b>: ${y} (#percent%)",
		indexLabel: "{name} - #percent%",
		dataPoints: [
			{ y: TwoCountG, name: "€2.0" },
			{ y: OneCountG, name: "€1.0" },
			{ y: FiftyCountG, name: "€0.5" },
			{ y: TwentyCountG, name: "€0.2" },
			{ y: TenCountG, name: "€0.1" },
			{ y: MiscCountG, name: "Misc"}
		]
	}]
});
chart.render();

function explodePie (e) {
	if(typeof (e.dataSeries.dataPoints[e.dataPointIndex].exploded) === "undefined" || !e.dataSeries.dataPoints[e.dataPointIndex].exploded) {
		e.dataSeries.dataPoints[e.dataPointIndex].exploded = true;
	} else {
		e.dataSeries.dataPoints[e.dataPointIndex].exploded = false;
	}
	e.chart.render();
}
},800);
}