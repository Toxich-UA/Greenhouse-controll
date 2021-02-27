$(function () {
    $(".alert").hide()
});


$("#add_greenhouse").click(function (e) {
    if ($("#ip").val().trim() == "") {
        $("#ip").toggleClass("border border-danger");
    } else {
        $.ajax({
            type: "POST",
            url: "/db",
            data: {
                "ip": $("#ip").val().trim(),
                "ghname": $("#ghname").val().trim(),
                "comment": $("#comment").val().trim()
            }
        }).done(function (data) {
            if (data == "200") {
                $(".alert-success").show();
                $("#ip").val("");
                $("#ghname").val("");
                $("#comment").val("");
                setTimeout(function () {
                    $('.alert-success').hide();
                    location.reload();
                }, 1000);
            } else {
                $(".alert-danger").show();
                setTimeout(function () {
                    $('.alert-danger').hide();
                }, 1000);
            }
        })
    }
    e.preventDefault();
});

$(".btnRemove").click(function (e) {
    $.ajax({
        type: "GET",
        url: "/db",
        data: {
            "ip": $("#ghip" + this.id).text().trim()
        }
    }).done(function (data) {
        if (data == "200") {
            alert("Удалено")
            location.reload();
        }
    })
    e.preventDefault();
});