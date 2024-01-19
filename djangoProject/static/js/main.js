$(document).ready(function () {
    $('#increased').click(function () {
        $("#choosing_cluster").val(-1);
        $("#table-body").empty();
        $("#btn_name_save").text("Изменить название выброса () ")
        $.ajax({
            url: 'select_cluster',
            type: 'GET',
            data: {"id_cluster": -1, "count": 10},
            success: (data) => {
                $("#tHead").removeClass("hidden");
                $("#btn_name_save1").removeClass("hidden");
                $("#increased-head").removeClass("hidden");
                $("#label_cluster").removeClass("hidden");
                $("#in_cluster").empty().append("выбросы");
                for (i = 0; i < data.objects.length; i++) {
                    if (data.objects[i].id_name !== null) {
                        var id = data.objects[i].id_name;
                    } else {
                        var id = data.objects[i].id;
                    }

                    var row = $(`
                                <tr class="table-row" data-id='${data.objects[i].id}'>
                                    <td >
                                        <p>${data.objects[i].type}</p>
                                    </td>
                                    <td>
                                        <p>${data.objects[i].name}</p>
                                    </td>
                                    <td>
                                        <p>${data.objects[i].address}</p>
                                    </td>
                                    <td>
                                        <p>${data.objects[i].phone_number}</p>
                                    </td>
                                    <td>
                                        <p>${id}</p>
                                    </td>
                                </tr>
                                `);
                    $("#table-body").append(row)
                }
                var rows = document.getElementsByClassName("table-row");

                for (var i = 0; i < rows.length; i++) {
                    rows[i].addEventListener('click', function () {

                        $("#btn_name_save").text(`Изменить название выброса (${this.childNodes[9].innerText}) `)

                        $("#btn_name_save").data("id_increased", this.dataset.id);
                    });
                }
            },
            error: (error) => {
                alert(error);
            }
        });
    });

    $('#choosing_cluster').change(function () {
        $("#table-body").empty();
        $("#in_cluster").empty();
        $("#btn_name_save").text("Изменить название кластера ");
        if ($('#choosing_cluster').val() !== "0") {
            $("#tHead").removeClass("hidden");
            $("#increased-head").addClass("hidden");
            $("#btn_name_save1").removeClass("hidden");
            $("#label_cluster").removeClass("hidden");
            $.ajax({
                url: 'select_cluster',
                type: 'GET',
                data: {"id_cluster": $("#choosing_cluster").val(), "count": 10},
                success: (data) => {

                    $("#in_cluster").append($("#choosing_cluster option:selected").text())
                    for (i = 0; i < data.objects.length; i++) {
                        $("#table-body").append(`
                                <tr class="table-row">
                                    <td>
                                        <p>${data.objects[i].type}</p>
                                    </td>
                                    <td>
                                        <p>${data.objects[i].name}</p>
                                    </td>
                                    <td>
                                        <p>${data.objects[i].address}</p>
                                    </td>
                                    <td>
                                        <p>${data.objects[i].phone_number}</p>
                                    </td>

                                </tr>
                                `)
                    }
                },
                error: (error) => {
                    alert(error);
                }
            });
        } else {
            $("#tHead").addClass("hidden");
            $("#btn_name_save1").addClass("hidden");
            $("#increased-head").addClass("hidden");
            $("#label_cluster").addClass("hidden");
        }


    });

    function createMessage(text) {
        $("#flash1").append(
            `
                        <div class="flash">
                            <span class="closebtn">&times;</span>
                            ${text}
                        </div>
                        `
        );
        var close = document.getElementsByClassName("flash");

        for (var i = 0; i < close.length; i++) {

            close[i].onclick = function () {
                this.style.display = "none"

            }
        }
        setTimeout(function () {
                var close1 = document.getElementsByClassName("flash");

                for (var i = 0; i < close1.length; i++) {
                    close1[i].style.display = "none"

                }
            }
            , 5000);

    }

    $('#save_name').click(function () {
        if ($('#name_cluster').val().trim() === "") {
            createMessage("Наименование не может быть пустым");
        } else {
            if ($("#btn_name_save").data("id_increased") === undefined)

                $.ajax({
                    url: 'update_name_cluster',
                    type: 'GET',
                    data: {"id_cluster": $("#choosing_cluster").val(), "name": $('#name_cluster').val()},
                    success: (data) => {
                        createMessage("Наименование класстера сохранено");
                        if ($('#choosing_cluster').val() != null) {
                            $('#choosing_cluster option:selected').text($('#name_cluster').val());
                        }
                        $('#name_cluster').val("");

                    },
                    error: (error) => {
                        alert(error);
                    }
                });
            else {

                var id_increased = $("#btn_name_save").data("id_increased")
                $.ajax({
                    url: 'update_name_increased',
                    type: 'GET',
                    data: {
                        "id_increased": id_increased,
                        "name": $('#name_cluster').val()
                    },
                    success: (data) => {
                        createMessage(`Наименование выброса (${$("#btn_name_save").data("id_increased")}) сохранено`);
                        if ($('#choosing_cluster').val() != null) {
                            $('#choosing_cluster option:selected').text($('#name_cluster').val());
                        }
                        $('#name_cluster').val("");

                    },
                    error: (error) => {
                        alert(error);
                    }
                });
            }

        }
    });

});

