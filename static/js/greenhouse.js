var peripherals_fans;
var peripherals_pump;
var peripherals_lamps;
var arrow_low = "bi-arrow-down-left";
var arrow_high = "bi-arrow-up-right";
var arrow_none = "bi-dash";
var text_red = "text-success";
var text_green = "text-danger";

window.onload = function () {
    update_peripherals_status();
};

function update_peripherals_status() {
    let ip = $("#ipAddres").text();
    $.ajax({
        type: "GET",
        url: "/get_peripherals_status",
        data: {
            "ip": ip
        }
    }).done(function (data) {
        var status = jQuery.parseJSON(data);
        if (status.fans == 1) {
            peripherals_fans = true
        } else {
            peripherals_fans = false
        }
        if (status.pump == 1) {
            peripherals_pump = true
        } else {
            peripherals_pump = false
        }
        if (status.lamps == 1) {
            peripherals_lamps = true
        } else {
            peripherals_lamps = false
        }
        $('#fan').prop('disabled', $("#fansControl").prop('checked'));
        $('#pump').prop('disabled', $("#pumpControl").prop('checked'));
        $('#lamps').prop('disabled', $("#lampsControl").prop('checked'));
        set_fans()
        set_pump()
        set_lamps()
    })
}

function set_fans() {

    if (peripherals_fans) {
        $("#fan").removeClass("btn-success").addClass("btn-danger").text("Turn OFF");
        $("#fansStatus").removeClass("table-danger").addClass("table-success").text("ON");
    } else {
        $("#fan").removeClass("btn-danger").addClass("btn-success").text("Turn ON");
        $("#fansStatus").removeClass("table-success").addClass("table-danger").text("OFF");
    }
    peripherals_fans = !peripherals_fans;
};
function set_pump() {

    if (peripherals_pump) {
        $("#pump").removeClass("btn-success").addClass("btn-danger").text("Turn OFF");
        $("#pumpStatus").removeClass("table-danger").addClass("table-success").text("ON");
    } else {
        $("#pump").removeClass("btn-danger").addClass("btn-success").text("Turn ON");
        $("#pumpStatus").removeClass("table-success").addClass("table-danger").text("OFF");
    }
    peripherals_pump = !peripherals_pump;
};
function set_lamps() {

    if (peripherals_lamps) {
        $("#lamps").removeClass("btn-success").addClass("btn-danger").text("Turn OFF");
        $("#lampsStatus").removeClass("table-danger").addClass("table-success").text("ON");
    } else {
        $("#lamps").removeClass("btn-danger").addClass("btn-success").text("Turn ON");
        $("#lampsStatus").removeClass("table-success").addClass("table-danger").text("OFF");
    }
    peripherals_lamps = !peripherals_lamps;
};
$(function () {
    $(".timeform").hide()
});
function hideForm(elem) {
    $("#form" + elem.id).toggle();
};
$(document).ready(function () {

    $("#fan").click(function (e) {
        $.ajax({
            type: "GET",
            url: "/toggle_peripheral_status",
            data: {
                ip: $("#ipAddres").text(),
                peripheral: "fans"
            }
        }).done(function (data) {
            if (data != "Нет данных") {
                set_fans()
            }
        })
        e.preventDefault();
    });

    $("#pump").click(function (e) {
        $.ajax({
            type: "GET",
            url: "/toggle_peripheral_status",
            data: {
                ip: $("#ipAddres").text(),
                peripheral: "pump"
            }
        }).done(function (data) {
            if (data != "Нет данных") {
                set_pump()
            }
        })
        e.preventDefault();
    });

    $("#lamps").click(function (e) {
        $.ajax({
            type: "GET",
            url: "/toggle_peripheral_status",
            data: {
                ip: $("#ipAddres").text(),
                peripheral: "lamps"
            }
        }).done(function (data) {
            if (data != "Нет данных") {
                set_lamps()
            }
        })
        e.preventDefault();
    });

    $('#fansControl').change(function () {
        $('#fan').prop('disabled', $(this).prop('checked'));

        $.ajax({
            type: "GET",
            url: "/set_control_mode",
            data: {
                ip: $("#ipAddres").text(),
                peripheral: "fans",
                status: $(this).prop('checked')
            }
        }).done(function (data) {

        });
    });

    $('#pumpControl').change(function () {
        $('#pump').prop('disabled', $(this).prop('checked'));
        $.ajax({
            type: "GET",
            url: "/set_control_mode",
            data: {
                ip: $("#ipAddres").text(),
                peripheral: "pump",
                status: $(this).prop('checked')
            }
        }).done(function (data) {

        });
    });

    $('#lampsControl').change(function () {
        $('#lamps').prop('disabled', $(this).prop('checked'));
        $.ajax({
            type: "GET",
            url: "/set_control_mode",
            data: {
                ip: $("#ipAddres").text(),
                peripheral: "lamps",
                status: $(this).prop('checked')
            }
        }).done(function (data) {

        });
    });

    $("#pumpControll").change(function (e){
        e.preventDefault()
        $.ajax({
            type: "GET",
            url: "/set_control_mode",
            data: {
                ip: $("#ipAddres").text(),
                peripheral: "pump_by_humidity",
                status: $(this).prop('checked')
            }
        }).done(function (data) {
        });
    });
    function update_status(obj, data, change) {
        obj.text(data.val);
        update_change_icon(change, data)
    };
    function update_change_icon(obj, data) {
        if (data.change > 0) {
            obj.removeClass(arrow_low).removeClass(arrow_none).addClass(arrow_high);
            obj.removeClass(text_green).addClass(text_red);
        } else if (data.change < 0) {
            obj.removeClass(arrow_high).removeClass(arrow_none).addClass(arrow_low);
            obj.removeClass(text_red).addClass(text_green);
        } else {
            obj.removeClass(arrow_low).removeClass(arrow_high).addClass(arrow_none);
            obj.removeClass(text_red).removeClass(text_green);
        }
    };
    setInterval(function () {
        let ip = $("#ipAddres").text();

        $.ajax({
            type: "GET",
            url: "/status",
            data: {
                "ip": ip
            }
        }).done(function (data) {
            var status = jQuery.parseJSON(data);
            update_status($("#temp_a"), status.temperature_a, $("#temp_a_change"))
            update_status($("#temp_b"), status.temperature_b, $("#temp_b_change"))
            update_status($("#temp_c"), status.temperature_c, $("#temp_c_change"))
            update_status($("#temp_d"), status.temperature_d, $("#temp_d_change"))
            update_status($("#temp_e"), status.temperature_e, $("#temp_e_change"))
            update_status($("#temp_f"), status.temperature_DH, $("#temp_f_change"))
            update_status($("#hum_a"), status.humidity_a, $("#hum_a_change"))
            update_status($("#hum_b"), status.humidity_b, $("#hum_b_change"))
            update_status($("#hum_c"), status.humidity_c, $("#hum_c_change"))
            update_status($("#hum_d"), status.humidity_d, $("#hum_d_change"))
            update_status($("#hum_e"), status.humidity_DH, $("#hum_e_change"))

        });
        update_peripherals_status();
    }, 5 * 1000);

    $(".pumpTimeBtn").click(function (e) {
        e.preventDefault();
        let timeStart = $("#" + this.id + "Start").val();
        let timeEnd = $("#" + this.id + "End").val();
        let start_end = timeStart + "-" + timeEnd

        if (timeStart && timeEnd) {
            $.ajax({
                type: "GET",
                url: "/add_new_pump_activation_time",
                data: {
                    ip: $("#ipAddres").text(),
                    start_end: start_end,
                    day: $(this).attr('name')
                }
            }).done(function (data) {
                if(data == "200"){
                    alert("Успешно добавлено")
                    location.reload();
                };
            });
        }
    });
    $("#removePumpTime").click(function (e) {
        e.preventDefault();
        let start_end = $(this).parent().text().trim();
        let index = $(this).parent().parent().attr("name");
        console.log(start_end);
        if (start_end) {
            $.ajax({
                type: "GET",
                url: "/remove_pump_activation_time",
                data: {
                    ip: $("#ipAddres").text(),
                    start_end: start_end,   
                    day: $("#blockName"+index).text().trim()
                }
            }).done(function (data) {
                if(data == "200"){
                    alert("Успешно удалено")
                    location.reload();
                };
            });
        }
    });
    
    $("#setNewFansTempBtn").click(function (e){
        e.preventDefault()
        let tempOn = $("#fansTempOn").val();
        let tempOff = $("#fansTempOff").val();
        if(tempOn == "" || tempOff == ""){
            $("#fansTempOn").toggleClass("border border-danger");
            $("#fansTempOff").toggleClass("border border-danger");
            return;
        }
        $.ajax({
            type: "GET",
            url: "/set_new_fans_activation_temp",
            data: {
                ip: $("#ipAddres").text(),
                start: tempOn,
                end: tempOff
            }
        }).done(function (data) {
            if(data == "200"){
                alert("Успешно добавлено")
                location.reload();
            };
        });
    });

    $("#setNewPumpHumidityBtn").click(function (e){
        e.preventDefault()
        let timeOn = $("#pumpHumOn").val();
        let timeOff = $("#pumpHumOff").val();
        if(timeOn == "" || timeOff == ""){
            $("#pumpHumOn").toggleClass("border border-danger");
            $("#pumpHumOff").toggleClass("border border-danger");
            return;
        }
        $.ajax({
            type: "GET",
            url: "/set_new_pump_activation_humidity",
            data: {
                start: timeOn,
                end: timeOff,
                ip: $("#ipAddres").text()
            }
        }).done(function (data) {
            if(data == "200"){
                alert("Успешно добавлено")
                location.reload();
            };
        });
    });

    

});
