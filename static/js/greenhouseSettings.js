$("#change_outputs").click(function (e) {
    e.preventDefault();
    let ip = new URLSearchParams(window.location.search).get("ip");
    sensors_map = {
        "temperature_a": $("#sensors_0").val(),
        "temperature_b": $("#sensors_1").val(),
        "temperature_c": $("#sensors_2").val(),
        "temperature_d": $("#sensors_3").val(),
        "temperature_e": $("#sensors_4").val(),
        "temperature_f": $("#sensors_5").val(),
        "humidity_a": $("#sensors_6").val(),
        "humidity_b": $("#sensors_7").val(),
        "humidity_c": $("#sensors_8").val(),
        "humidity_d": $("#sensors_9").val(),
        "humidity_e": $("#sensors_10").val(),
    };

    names_map = {
        "temperature_a": $("#name_0").val(),
        "temperature_b": $("#name_1").val(),
        "temperature_c": $("#name_2").val(),
        "temperature_d": $("#name_3").val(),
        "temperature_e": $("#name_4").val(),
        "temperature_f": $("#name_5").val(),
        "humidity_a": $("#name_6").val(),
        "humidity_b": $("#name_7").val(),
        "humidity_c": $("#name_8").val(),
        "humidity_d": $("#name_9").val(),
        "humidity_e": $("#name_10").val(),
    };

    $.ajax({
        type: "GET",
        url: "/update_greenhouse_names_and_sensors",
        data: {
            "ip": ip,
            "names": JSON.stringify(names_map),
            "sensors_map": JSON.stringify(sensors_map)
        },
        contentType: "application/json"

    }).done(function (data) {
        if (data == "200") {
            window.location.href = '../greenhouse?ip=' + ip;
        }
    });


});