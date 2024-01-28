/* globals Chart:false */




for(var i = 0; i < edata.length; i++) {
  if(edata[i].bought)
    edata[i].description = `Bought ${edata[i].count}`;
//    edata[i].normal = '#d1ead9'
  else
    edata[i].description = `Bought ${edata[i].count}`;
//     edata[i].normal = '#ead9d1'
}

(() => {
  anychart.onDocumentReady(function () {
    anychart.data.loadCsvFile(
  dataset_url,
      function (data) {
        var dataTable = anychart.data.table();
        dataTable.addData(data);
        var mapping = dataTable.mapAs({
          open: 1,
          high: 3,
          low: 4,
          close: 2,
        });
        var chart = anychart.stock();
        var plot = chart.plot(0);
        plot.yGrid(true).xGrid(true).yMinorGrid(true).xMinorGrid(true);
        var series = plot.candlestick(mapping);
        series.name(company_name);
        series.legendItem().iconType('rising-falling');
        series.fallingFill("#FF0D0D");
        series.fallingStroke("#FF0D0D");
        series.risingFill("#32bf60");
        series.risingStroke("#32bf60");
        chart.title(`${company_name}`);
        chart.container('myChart');
        chart.draw();
        var eventMarkers = plot.eventMarkers();
        plot.eventMarkers().format(function() {
          console.log(this);
          if(!this.getData('bought'))
            return 'V'
          return 'Λ'
        });
        eventMarkers.data(edata);
      });
  });
  
})()