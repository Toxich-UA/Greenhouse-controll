window.chartColors = {
    red: 'rgb(255, 99, 132)',
    orange: 'rgb(255, 159, 64)',
    yellow: 'rgb(255, 205, 86)',
    green: 'rgb(75, 192, 192)',
    blue: 'rgb(54, 162, 235)',
    purple: 'rgb(153, 102, 255)',
    grey: 'rgb(201, 203, 207)'
};
function renderChart(data, labels, lable, ip, color) {
    var chartHolder = $('#chartsHolder');
    var ctx =
        $('<canvas/>', { 'class': 'chart' })
    chartHolder.append(ctx)
    var myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: lable,
                data: data,
                fill: false,
                borderColor: color
            }]
        },
        options: {
            title: {
                display: true,
                text: 'Data for ' + ip
            }
        }
    });
}

$("#hour").click(
    function () {
        $.ajax({
            type: "GET",
            url: "/get_logged_statistic_for_hour",
            data: {
            }
        }).done(function (dataIn) {
            $('#chartsHolder').empty();
            var data = jQuery.parseJSON(dataIn);

            renderChart(data.greenhouses.data.air_temperature, data.labels, "Температура воздуха", data.ip, chartColors.red);
            renderChart(data.greenhouses.data.air_humidity, data.labels, "Влажность воздуха", data.ip, chartColors.orange);
            renderChart(data.greenhouses.data.soil_temperature, data.labels, "Температура почвы", data.ip, chartColors.yellow);
            renderChart(data.greenhouses.data.soil_humidity, data.labels, "Влажность почвы", data.ip, chartColors.green);
        })

    }
);
$("#day").click(
    function () {
        $.ajax({
            type: "GET",
            url: "/get_logged_statistic_for_day",
            data: {
            }
        }).done(function (dataIn) {
            $('#chartsHolder').empty();
            var data = jQuery.parseJSON(dataIn);

            renderChart(data.greenhouses.data.air_temperature, data.labels, "Температура воздуха", data.ip, chartColors.red);
            renderChart(data.greenhouses.data.air_humidity, data.labels, "Влажность воздуха", data.ip, chartColors.orange);
            renderChart(data.greenhouses.data.soil_temperature, data.labels, "Температура почвы", data.ip, chartColors.yellow);
            renderChart(data.greenhouses.data.soil_humidity, data.labels, "Влажность почвы", data.ip, chartColors.green);

        })

    }
);
