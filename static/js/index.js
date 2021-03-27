$(document).ready(function () {

    $(".fans").each(function (index) {
        if ($(this).text() == 1) {
            $(this).text("ON")
            $(this).removeClass("text-danger").addClass("text-success");
        } else {
            $(this).text("OFF")
            $(this).removeClass("text-success").addClass("text-danger");
        }

    });
    $(".pump").each(function (index) {
        if ($(this).text() == 1) {
            $(this).text("ON")
            $(this).removeClass("text-danger").addClass("text-success");
        }else{
            $(this).text("OFF")
            $(this).removeClass("text-success").addClass("text-danger");
        }
    });

    $(".lamps").each(function (index) {
        if ($(this).text() == 1) {
            $(this).text("ON")
            $(this).removeClass("text-danger").addClass("text-success");
        }else{
            $(this).text("OFF")
            $(this).removeClass("text-success").addClass("text-danger");
        }
    });

});