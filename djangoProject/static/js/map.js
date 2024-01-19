let center = [55.75573294633685, 37.61887033217221];
function init() {
    let map = new ymaps.Map('map', {
        center: center,
        zoom: 10
    });
    function createPoint(data) {
        let points = []
        for (let i = 0; i < data.length; i++) {
            let point = data[i];
            points[i] = (new ymaps.Placemark([point.latitude, point.longitude], {
                hintContent: point.name,
                balloonContentHeader: point.name,
                balloonContentBody: `${point.phone_number}<br>${point.address}`,
                balloonContentFooter: ""
            }, {
                iconColor: '#1207f5'
            }));
        }
        clusterer = new ymaps.Clusterer({minClusterSize: [20]});
        clusterer.add(points);
        map.geoObjects.add(clusterer)
    }
    $('#choosing_cluster').change(function () {
        $("#in_cluster").empty();
        if ($('#choosing_cluster').val() !== "0") {
            $("#in_cluster").append($("#choosing_cluster option:selected").text())
            $("#label_cluster").removeClass("hidden");
            $("#btn_name_save1").removeClass("hidden");
            $.ajax({
                url: 'all_points',
                type: 'GET',
                data: {"id_cluster": $("#choosing_cluster").val()},
                success: (data) => {
                    map.geoObjects.removeAll();
                    createPoint(data);
                },
                error: (error) => {
                    alert(error);
                }
            });
        } else {
            map.geoObjects.removeAll();
            $("#label_cluster").addClass("hidden");
            $("#btn_name_save1").addClass("hidden");

        }
    });

    $('#increased').click(function () {
        $("#choosing_cluster").val(-1);
        $("#in_cluster").empty().append("выбросы");
        $("#label_cluster").removeClass("hidden");

        $.ajax({
            url: 'all_points',
            type: 'GET',
            data: {"id_cluster": -1},
            success: (data) => {
                map.geoObjects.removeAll();
                createPoint(data);
            },
            error: (error) => {
                alert(error);
            }
        });
    })
    ;

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
            $.ajax({
                url: 'update_name_cluster',
                type: 'GET',
                data: {"id_cluster": $("#choosing_cluster").val(), "name": $('#name_cluster').val()},
                success: (data) => {
                    createMessage("Наименование класстера сохранено");
                    if ($('#choosing_cluster').val() != null) {
                        $('#choosing_cluster option:selected').text($('#name_cluster').val());
                    }
                    $('#in_cluster').text($('#name_cluster').val());
                    $('#name_cluster').val("");
                },
                error: (error) => {
                    alert(error);
                }
            });

        }
    });

    map.controls.remove('searchControl'); // удаляем поиск
    map.controls.remove('trafficControl'); // удаляем контроль трафика
    map.controls.remove('zoomControl'); // удаляем контрол зуммирования
    map.controls.remove('rulerControl'); // удаляем контрол правил
}

ymaps.ready(init);



