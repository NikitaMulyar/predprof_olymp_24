/* globals Chart:false */




for(var i = 0; i < edata.length; i++) {
  if(edata[i].bought)
    edata[i].description = `Куплено ${edata[i].count} акций по цене ${edata[i].price}`;
  else
    edata[i].description = `Продано ${edata[i].count} акций по цене ${edata[i].price}`;
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
        chart.title(`График акций компании ${company_name}`);
        chart.container('myChart');

        chart.draw();

        table_buy = anychart.data.table();
        table_buy.addData(buy_data);
        mapping2 = table_buy.mapAs();
        mapping2.addField('value', 1);
        var plot = chart.plot(0);
        plot.yGrid(true).xGrid(true).yMinorGrid(true).xMinorGrid(true);
        var series = plot.marker(mapping2);
        series.name("Продажа");
        series.fill("#2fa946");
        series.type("triangle-up");
        series.stroke("black");
        series.size(8);

        chart.draw();

        table_sell = anychart.data.table();
        table_sell.addData(sell_data);
        mapping3 = table_sell.mapAs();
        mapping3.addField('value', 1);
        var plot = chart.plot(0);
        plot.yGrid(true).xGrid(true).yMinorGrid(true).xMinorGrid(true);
        var series = plot.marker(mapping3);
        series.name("Покупка");
        series.fill("#ec4139");
        series.type("triangle-down");
        series.stroke("black");
        series.size(8);

        chart.draw();

        var indicator = chart.plot(0).priceIndicator({value: "last-visible"});

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