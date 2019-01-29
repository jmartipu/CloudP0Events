$('form').submit(function (e){

    var formData = new FormData($("#formulario_crear_evento")[0]);
    $.ajax({
        url: $(this).attr('action'),
        type: $(this).attr('method'),
        data: formData,
        cache: false,
        contentType: false,
        processData: false,
        success: [ function () {
            // window.location = "eventos/";
        } ],

    });
    e.preventDefault();
    console.log(formData)

});

