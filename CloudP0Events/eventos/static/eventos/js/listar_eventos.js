$(function () {
    $.getJSON('lista_eventos').done(function (evento) {

        texto = '<thead><tr>';
        texto = texto + '<th scope=\"col\">#</th>';
        texto = texto + '<th scope=\"col\">Nombre</th>';
        texto = texto + '<th scope=\"col\">Fecha Creación</th>';
        texto = texto + '<th scope=\"col\">Hora Creación</th>';
        texto = texto + '<th scope=\"col\">Ver</th>';
        texto = texto + '<th scope=\"col\">Eliminar</th>';
        texto = texto + '</tr></thead>';
        texto = texto + '<tbody>';
        count = 0;
        $.each(evento, function (i, item) {
            texto = texto + '<tr>';
            texto = texto + '<th scope=\"row\">' + (count+1) + '</th>';
            texto = texto + '<td>' + item.fields.nombre + '</td>';
            texto = texto + '<td>' + item.fields.fecha_creacion + '</td>';
            texto = texto + '<td>' + item.fields.hora_creacion + '</td>';
            texto = texto + '<td><a href=\"' + detalle(item.pk) + '\"> ver </a></td>';
            texto = texto + '<td><a href=\"' + eliminar(item.pk) + '\"> eliminar </a></td>';
            texto = texto + '</tr>';
            count = count + 1;

        });
        texto = texto + '</tbody>';

        $("#lista_eventos_table").prepend(texto);

    });
});

function detalle(key) {
     return './evento/'+ key+'/';
}
function eliminar(key) {
     return './evento/'+ key+'/eliminar';
}