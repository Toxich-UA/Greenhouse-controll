const colorScheme = [
    "#25CCF7", "#FD7272", "#54a0ff", "#00d2d3",
    "#1abc9c", "#2ecc71", "#3498db", "#9b59b6", "#34495e",
    "#16a085", "#27ae60", "#2980b9", "#8e44ad", "#2c3e50",
    "#f1c40f", "#e67e22", "#e74c3c", "#ecf0f1", "#95a5a6",
    "#f39c12", "#d35400", "#c0392b", "#bdc3c7", "#7f8c8d",
    "#55efc4", "#81ecec", "#74b9ff", "#a29bfe", "#dfe6e9",
    "#00b894", "#00cec9", "#0984e3", "#6c5ce7", "#ffeaa7",
    "#fab1a0", "#ff7675", "#fd79a8", "#fdcb6e", "#e17055",
    "#d63031", "#feca57", "#5f27cd", "#54a0ff", "#01a3a4"
]
function renderSingleLineChart(data, labels, lable, ip, color) {
    var chartHolder = $('#chartsHolder');
    var ctx =
        $('<canvas/>', { 'class': 'chart' })
    chartHolder.append(ctx)
    var multipleChart = new Chart(ctx, {
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

function renderMultipleLinesChart(data, checkboxes) {
    var chartHolder = $('#chartsHolder');
    var ctx =
        $('<canvas/>', { 'class': 'chart' })
    chartHolder.append(ctx)

    let dataset = [];
    $.each(checkboxes, function (index, key) {
        dataset.push({
            label: data.names[index],
            data: data.greenhouses[key],
            fill: false,
            borderColor: colorScheme[index]
        });
    });
    var singleChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.labels,
            datasets: dataset
        },
        options: {
            title: {
                display: true,
                text: 'Data for ' + ip
            }
        }
    });
}

function select(element) {
    if ($(element).val() == "hour") {
        $("#days_range").addClass("d-none");
        $("#day").addClass("d-none");
    } else if ($(element).val() == "day") {
        $("#days_range").addClass("d-none");
        $("#day").removeClass("d-none");
    } else if ($(element).val() == "days_range") {
        $("#day").addClass("d-none");
        $("#days_range").removeClass("d-none");
    }
}

function get_today_date() {
    var date = new Date();
    var day = date.getDate();
    var month = date.getMonth() + 1;
    var year = date.getFullYear();

    if (month < 10) month = "0" + month;
    if (day < 10) day = "0" + day;

    return year + "-" + month + "-" + day;
}

$("#show").click(
    function () {
        let params = getParams();
        let ip = params[0];
        let range = params[1];
        let date_start = "";
        let date_end = "";
        let range_value = $("#range").val();
        if (range_value == "day") {
            if (date_start == "")
                date_start = get_today_date();
            else
                date_start = $("#date").val();
        }
        if (range_value == "days_range") {
            date_start = $("#date_start").val();
            date_end = $("#date_end").val();
        }
        if ((date_start == "" || date_end == "") && range_value == "days_range") {
            alert("Дата не может быть пустой");
            return;
        }
        $.ajax({
            type: "GET",
            url: "/get_logged_statistic",
            data: {
                ip: ip,
                range: range,
                date_start: date_start,
                date_end: date_end
            }
        }).done(function (dataIn) {
            $('#chartsHolder').empty();
            var data = jQuery.parseJSON(dataIn);
            var index = 0;
            if (!jQuery.isEmptyObject(data)) {
                let checkboxes = get_checkboxes();
                if (checkboxes.length != 0) {
                    if ($("#on_one").is(":checked")) {
                        renderMultipleLinesChart(data, checkboxes);
                    } else {
                        $.each(checkboxes, function (index, key) {
                            renderSingleLineChart(data.greenhouses[key], data.labels, data.names[index], data.ip, colorScheme[index]);
                        })
                    }
                } else
                    for (const key in data.greenhouses) {
                        renderSingleLineChart(data.greenhouses[key], data.labels, data.names[index], data.ip, colorScheme[index]);
                        index++;
                    }
            } else {
                $("#myModal").modal("show");
            }
        })

    }
);

function get_checkboxes() {
    let checkboxes = [];
    $(".form-check-input.sensor").each(function (index, val) {
        if (val.checked) {
            checkboxes.push($(val).val());
        }
    });
    return checkboxes;
}

function getParams() {
    range = $("#range").val();
    ip = $("#greenhouse_ip").val();
    return [ip, range];
};
